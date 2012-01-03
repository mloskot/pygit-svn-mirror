#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of pygit-svn-mirror tool -
# Python port of git-svn-mirror written in Ruby by Eloy Duran.
#
# Copyright (c) 2011 Mateusz Loskot <mateusz@loskot.net>
# Copyright (c) 2010 Eloy Duran <eloy.de.enige@gmail.com> (author of git-svn-mirror in Ruby)
#
# You may use these works without restrictions, as long as this paragraph is included.
# The work is provided "as is". There is NO warranty of any kind, express or implied.
#
import optparse
import os
import subprocess
import sys

class GitSVNMirror(object):
    def __init__(self):
        self.VERSION = "0.1"
        self.__from = None
        self.__to = None
        self.__workbench = None
        self.__authors_file = None
        self.__silent = None
        self.__is_sh_shell = self.is_sh_as_shell()

    @staticmethod
    def run(argv):
        mirror = GitSVNMirror()
        if len(argv) > 1:
            cmd = argv.pop(1)
            if cmd == 'init':
                return mirror.run_init(argv)
            elif cmd == 'update':
                return mirror.run_update(argv)
 
        print("Usage: %s [init|update]" % os.path.basename(argv[0]))
        return False    

    def option_parser(self):
        opts = optparse.OptionParser(version=self.VERSION)
        opts.add_option("-s", "--silent", action="store_true", dest="s", default=False, help="Silent mode.")
        opts.set_defaults(s=None);
        return opts

    def run_init(self, argv):
        opts = self.option_parser()
        opts.set_usage("Usage: %prog init [mandatory options] [options]"
                       "\n\nMandatory options are --from and --to. Use --help to find details.")
        opts.add_option("-f", "--from", action="store", type="string", dest="f", metavar="URI", help=self.__class__.from_.__doc__)
        opts.add_option("-t", "--to", action="store", type="string", dest="t", metavar="URI", help=self.__class__.to.__doc__)
        opts.add_option("-w", "--workbench", action="store", type="string", dest="w", metavar="PATH", help=self.__class__.workbench.__doc__)
        opts.add_option("-a", "--authors-file", action="store", type="string", dest="a", metavar="PATH", help=self.__class__.authors_file.__doc__)
        opts.set_defaults(f=None, t=None, w=None, a=None);
        (options, args) = opts.parse_args(args=argv)
    
        if options.f is None:
            opts.error("\n\tmissing argument: " + self.__class__.from_.__doc__)
        if options.t is None:
            opts.error("\n\tmissing argument: " + self.__class__.to.__doc__)
    
        self.__silent = options.s
        self.from_ = options.f
        self.to = options.t
        if options.w is not None:
            self.workbench = options.w
        if options.a is not None:
            self.authors_file = options.a

        if self.from_ and self.to:
            if not os.path.exists(self.workbench):
                print("[!] Given workbench path does not exist.")
                return False
            else:
                if self.authors_file and not os.path.exists(self.authors_file):
                    print("[!] Given authors file does not exist.")
                    return False
                else:
                    self.init()
                    return True
        else:
          opts.print_usage()
          return False

    def run_update(self, argv):
        opts = self.option_parser()
        opts.set_usage("Usage: %prog update [options]")
        opts.add_option("-w", "--workbench", action="store", type="string", dest="w", metavar="PATH", help=self.__class__.workbench.__doc__)
        opts.set_defaults(w=None);
        (options, args) = opts.parse_args(args=argv)

        self.__silent = options.s

        if options.w is None and len(args) > 1:
            opts.error("\n\tmissing argument: " + self.__class__.workbench.__doc__)
    
        if options.w is not None:
            self.workbench = options.w
        
        if os.path.exists(os.path.join(self.workbench, "config")):
            self.update()
            return True
        else:
            opts.error("\n\tworkbench '" + self.workbench + "' is not a bare Git repository")
            return False
      
    def init(self):
        self.log("* Configuring mirror workbench at '%s'" % self.workbench)
        self.sh(["git", "init", "--bare"])

        self.sh(["git", "svn", "init", "--stdlayout", "--prefix=svn/", self.from_])
        if self.authors_file:
            self.sh(["git", "config", "--add", "svn.authorsfile", self.authors_file])

        self.sh(["git", "remote", "add", "origin", self.to])
        self.sh(["git", "config", "--add", "remote.origin.push", "refs/remotes/svn/*:refs/heads/*"])

        self.fetch()
        self.log("* Running garbage collection")
        self.sh(["git", "gc"])

        self.log("The mirror workbench has been configured. To push to the remote Git repo,",
            "and possibly as a cron job, run the following command:",
            "",
            "  pygit-svn-mirror update -w '%s'" % self.workbench)

    def update(self):
        self.fetch()
        self.push()

    def fetch(self):
        self.log("* Fetching from SVN repo at '%s'" % self.from_)
        self.sh(["git", "svn", "fetch"])

    def push(self):
        self.log("* Pushing to Git repo at '%s'" % self.to)
        self.sh(["git", "push", "origin"])
        
    def from_():
        doc = "The location of the SVN repository that is to be mirrored."
        def fget(self):
            if self.__from is None:
                self.__from = self.config("svn-remote.svn.url")
            assert self.__from is not None and len(self.__from.strip()) > 0
            return self.__from.strip()
        def fset(self, value):
            self.__from = value.strip()
        def fdel(self):
            del self.__from
        return locals()
    from_ = property(**from_())

    def to():
        doc = "The location of the Git repository that is the mirror."
        def fget(self):
            if self.__to is None:
                self.__to = self.config("remote.origin.url")
            assert self.__to is not None and len(self.__to.strip()) > 0
            return self.__to.strip()
        def fset(self, value):
            self.__to = value.strip()
        def fdel(self):
            del self.__to
        return locals()
    to = property(**to())

    def workbench():
        doc = "The location of the workbench repository. Defaults to the current work dir."
        def fget(self):
            p = None
            if self.__workbench:
                p = self.__workbench
            else:
                p = os.getcwd()
            assert p is not None and len(p) > 0
            return p.strip()
        def fset(self, value):
            self.__workbench = os.path.abspath(value)
        def fdel(self):
            del self.__workbench
        return locals()
    workbench = property(**workbench())

    def authors_file():
        doc = "An optional authors file used to migrate SVN usernames to Git format."
        def fget(self):
            p = None
            if self.__authors_file:
                p = self.__authors_file
            else:
                p = ""
            assert p is not None
            return p.strip()
        def fset(self, value):
            self.__authors_file = os.path.abspath(value)
        def fdel(self):
            del self.__workbench
        return locals()
    authors_file = property(**authors_file())

    def log(self, *args):
        if not self.__silent:
            print("\n%s\n" % "\n".join(args))

    def config(self, key):
        value = self.sh(["git", "config", "--get", key], capture=True)
        if value and len(value) > 0:
            return value
        else:
            return None

    def sh(self, command, **kwargs):
        os.chdir(self.workbench)
        os.environ["GIT_DIR"] = os.getcwd()
        capture = kwargs.get('capture', False)
        output = None
        try:
            assert os.environ["GIT_DIR"] == self.workbench       
            if os.getcwd() == self.workbench and len(command) > 0:
                if capture is True:
                    output = subprocess.check_output(command, shell=self.__is_sh_shell)
                else:
                    if self.__silent:
                        osdevnull = open(os.devnull, 'w')
                        subprocess.check_call(command, shell=self.__is_sh_shell, stdout=osdevnull)
                        osdevnull.close()
                    else:
                        subprocess.check_call(command, shell=self.__is_sh_shell)
                    output = "" # success
        except subprocess.CalledProcessError as e:
            sys.stderr.write("Command '%s' failed with returncode %d and output '%s'"% (" ".join(command), e.returncode, e.output))
            sys.exit(1)
        else:
            assert output is not None
            return output
            
    def is_sh_as_shell(self):
        # Controls if shell=True is set for subprocess calls
        # See the can of worms of incompatibility: http://bugs.python.org/issue13195
        import platform
        plat = platform.system()
        return plat == "Windows"
