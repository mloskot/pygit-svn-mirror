@ECHO OFF
REM
REM This file is part of pygit-svn-mirror tool -
REM Python port of git-svn-mirror written in Ruby by Eloy Duran.
REM
REM Copyright (c) 2011 Mateusz Loskot <mateusz@loskot.net>
REM Copyright (c) 2010 Eloy Duran <eloy.de.enige@gmail.com> (author of git-svn-mirror in Ruby)
REM
REM You may use these works without restrictions, as long as this paragraph is included.
REM The work is provided "as is". There is NO warranty of any kind, express or implied.
REM
REM CONFIGURATION
REM * Point PYGITSVN to root location of pygit-svn-mirror clone
REM * You may also need to update Python32 location below
set PYGITSVN=D:\dev\pygit-svn-mirror\_git\pygit-svn-mirror
REM END CONFIGURATION

set PYTHONPATH=%PYGITSVN%\lib;%PYTHONPATH%
IF NOT "%~f0" == "~f0" GOTO :WinNT
@"C:\Python32\python.exe" "%PYGITSVN%\bin\git-svn-mirror.py" %1 %2 %3 %4 %5 %6 %7 %8 %9
GOTO :EOF
:WinNT
@"C:\Python32\python.exe" "%PYGITSVN%\bin\git-svn-mirror.py" %*