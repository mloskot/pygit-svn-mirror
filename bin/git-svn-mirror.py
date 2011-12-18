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
if __name__ == "__main__":
  from gitsvnmirror import GitSVNMirror
  import sys
  success = GitSVNMirror.run(sys.argv)
  if not success:
    exit(1)