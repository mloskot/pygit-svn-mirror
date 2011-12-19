pygit-svn-mirror
----------------

A command-line tool that automates the task of creating a Git mirror for a SVN
repo, and keeping it up-to-date.

This is direct Python port of [git-svn-mirror][orig] written in Ruby by Eloy Duran.
The guide below is a direct copy of README.md authored by Eloy Duran.

pygit-svn-mirror 1.0 is based on [git-svn-mirror][orig] SHA:alloy/git-svn-mirror/42f52463

Why
---

Figuring this stuff out is a pain in the bum, in my opinion, and its probably
not even done yet. So please do contribute! Also, if I would keep doing this by
hand, I would forget how to do it, a few weeks down the line.

Install
-------

Requirements:

1. Python 3+

Simply, clone [pygit-svn-mirror][my] and add the `lib` directory to `PYTHONPATH`.
Next run `git-svn.mirror.py` script from command line.
Use `git-svn.mirror.py --help` and the guide below to learn how to use it.

NOTE: Below, I use `pygit-svn-mirror` command. This is placeholder for Shell
script proxy which I'm going to add at some point.

On Windows, you can copy `bin\pygit-svn-mirror.bat` script to location included
in your PATH or you can add the `bin\` directory to PATH.
Next, edit the script and update `PYGITSVN` variable with location to your
local clone [pygit-svn-mirror][my] repository.
This way, you can run the tool through `pygit-svn-mirror.bat` script.

Configure the ‘workbench’
-------------------------

To mirror a SVN repo, first the local ‘workbench’ repo has to be configured.
This ‘workbench’ is the GIT repo where the SVN revisions will be stored and
from where these revisions will be pushed to the remote mirror GIT repo.

Start by creating the directory:

	$ mkdir -p /path/to/workbench

Then initialize the ‘workbench’:

	$ cd /path/to/workbench
	$ pygit-svn-mirror init --from=http://svn-host/repo_root --to=git@git-host:user/mirror.git

This will create a ‘bare’ GIT repo, configure the SVN and GIT remotes, fetch
the revisions from the SVN remote, and compact the ‘workbench’ by running the
GIT garbage collector.

It can often be handy to supply an authors file, with the <tt>--authors-file</tt>
option, which is used to migrate user names to GIT names and email addresses.
The entries in this file should look like:

	svn-user-name = User Name <user@example.com>

Update mirror
-------------

To push the latest changes from the SVN repo to the GIT repo, run the following
command from the ‘workbench’ repo:

	$ pygit-svn-mirror update

Or by specifying the path(s) to one or more ‘workbench’ repos:

	$ pygit-svn-mirror update /path/to/workbench1 /path/to/workbench2

You will probably normally not want to perform this step by hand. You can solve
this by adding this command as a cron job, in which case you can silence the
tool with the <tt>--silent</tt> option.

‘init’ help banner
----------------

	Usage: pygit-svn-mirror init [mandatory options] [options]
	
	  Mandatory options are --from and --to.
	
	    --from URI                   The location of the SVN repository that is to be mirrored.
	    --to URI                     The location of the GIT repository that is the mirror.
	    --workbench PATH             The location of the workbench repository. Defaults to the current work dir.
	    --authors-file PATH          An optional authors file used to migrate SVN usernames to GIT's format.
	-s, --silent                     Silent mode.

‘update’ help banner
--------------------

	Usage: pygit-svn-mirror update [options] [workbench1] ...
	
	  Defaults to the current work dir if none is given.
	
	-s, --silent                     Silent mode.

Contributing
------------

Once you've made your great commits:

1. [Fork][fk] pygit-svn-mirror
2. Create a topic branch - `git checkout -b my_branch`
3. Push to your branch - `git push origin my_branch`
4. Create an [Issue][is] with a link to your branch
5. That’s it!

Credits
-------

Thanks to Eloy Duran for the original [git-svn-mirror][orig] written in Ruby

License In Three Lines (LITL)
-----------------------------

	© 2011 Mateusz Loskot <mateusz@loskot.net>
    © 2010 Eloy Duran <eloy.de.enige@gmail.com> (author of git-svn-mirror in Ruby)
	You may use these works without restrictions, as long as this paragraph is included.
	The work is provided “as is”. There is NO warranty of any kind, express or implied.

[fk]: http://help.github.com/forking/
[is]: http://github.com/mloskot/pygit-svn-mirror/issues
[my]: http://github.com/mloskot/pygit-svn-mirror/
[orig]: http://github.com/alloy/git-svn-mirror/