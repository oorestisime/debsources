# Copyright (C) 2013-2014  The Debsources developers <info@sources.debian.net>.
# See the AUTHORS file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=AUTHORS;hb=HEAD
#
# This file is part of Debsources. Debsources is free software: you can
# redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.  For more information
# see the COPYING file at the top-level directory of this distribution and at
# https://anonscm.debian.org/gitweb/?p=qa/debsources.git;a=blob;f=COPYING;hb=HEAD

from __future__ import absolute_import

import datetime


# Limit on the maximum key length for Postgres columns which are subject to
# btree indexing. The actual value is 8192, but we play safe and round down.
# This allows to have complete indexes, rather than partial, which would
# require AND ing the index predicate to all queries, for the index to be
# consistently use.
MAX_KEY_LENGTH = 8000

# this list should be kept in sync with
# https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-VCS-fields
VCS_TYPES = ("arch", "bzr", "cvs", "darcs", "git", "hg", "mtn", "svn")

# this list should be kept in sync with languages supported by sloccount. A
# good start is http://www.dwheeler.com/sloccount/sloccount.html (section
# "Basic concepts"). Others have been added to the Debian package via patches.
SLOCCOUNT_LANGUAGES = (

    # sloccount 2.26 languages
    "ada", "asm", "awk", "sh", "ansic", "cpp", "cs", "csh", "cobol", "exp",
    "fortran", "f90", "haskell", "java", "lex", "lisp", "makefile", "ml",
    "modula3", "objc", "pascal", "perl", "php", "python",
    "ruby", "sed", "sql", "tcl", "yacc",

    # enhancements from Debian patches, version 2.26-5
    "erlang", "jsp", "vhdl", "xml",
)

# this list should be kept in sync with languages supported by (exuberant)
# ctags. See: http://ctags.sourceforge.net/languages.html and the output of
# `ctags --list-languages`
CTAGS_LANGUAGES = (
    'ant', 'asm', 'asp', 'awk', 'basic', 'beta', 'c', 'c++',
    'c#', 'cobol', 'dosbatch', 'eiffel', 'erlang', 'flex', 'fortran', 'go',
    'html', 'java', 'javascript', 'lisp', 'lua', 'make', 'matlab',
    'objectivec', 'ocaml', 'pascal', 'perl', 'php', 'python', 'rexx', 'ruby',
    'scheme', 'sh', 'slang', 'sml', 'sql', 'tcl', 'tex', 'vera', 'verilog',
    'vhdl', 'vim', 'yacc',
)

# TODO uniform CTAGS_* language naming (possibly without blessing any of the
# two, but using a 3rd, Debsources specific, canonical form)

METRIC_TYPES = ("size",)


# debian package areas
AREAS = ["main", "contrib", "non-free"]

# sane (?) default if the package prefix file is not available
PREFIXES_DEFAULT = ['0', '2', '3', '4', '6', '7', '9', 'a', 'b', 'c', 'd', 'e',
                    'f', 'g', 'h', 'i', 'j', 'k', 'l', 'lib3', 'liba', 'libb',
                    'libc', 'libd', 'libe', 'libf', 'libg', 'libh', 'libi',
                    'libj', 'libk', 'libl', 'libm', 'libn', 'libo', 'libp',
                    'libq', 'libr', 'libs', 'libt', 'libu', 'libv', 'libw',
                    'libx', 'liby', 'libz', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z']

DEBIAN_RELEASES = {
    'buzz':    {'version': '1.1',
                'date': datetime.date(1996,  6, 17), 'archived': True},
    'rex':     {'version': '1.2',
                'date': datetime.date(1996, 12, 12), 'archived': True},
    'bo':      {'version': '1.3',
                'date': datetime.date(1997,  6,  5), 'archived': True},
    'hamm':    {'version': '2.0',
                'date': datetime.date(1998,  7, 24), 'archived': True},
    'slink':   {'version': '2.1',
                'date': datetime.date(1999,  3,  9), 'archived': True},
    'potato':  {'version': '2.2',
                'date': datetime.date(2000,  8, 15), 'archived': True},
    'woody':   {'version': '3.0',
                'date': datetime.date(2002,  7, 19), 'archived': True},
    'sarge':   {'version': '3.1',
                'date': datetime.date(2005,  6,  6), 'archived': True},
    'etch':    {'version': '4.0',
                'date': datetime.date(2007,  4,  8), 'archived': True},
    'lenny':   {'version': '5.0',
                'date': datetime.date(2009,  2, 15), 'archived': True},
    'squeeze': {'version': '6.0',
                'date': datetime.date(2011,  2,  6), 'archived': True},
    'wheezy':  {'version': '7',
                'date': datetime.date(2013,  5,  4), 'archived': False},
    'jessie':  {'version': '8',
                'date': datetime.date(2015,  4,  25), 'archived': False},

}

SUITES = {
    'release': [  # known releases sorted by release date
        'buzz', 'rex', 'bo', 'hamm', 'slink', 'potato', 'woody', 'sarge',
        'etch', 'lenny', 'squeeze', 'wheezy', 'jessie', 'stretch', 'sid'
    ],
    'devel': [],  # known release variants; filled below
    'all': [],	  # all known releases + variants; filled below
}
SUITE_VARIANTS = ['%s-updates', '%s-proposed-updates', '%s-backports',
                  '%s-lts']
for s in SUITES['release']:
    SUITES['all'].append(s)
    for v in SUITE_VARIANTS:
        variant = v % s
        SUITES['all'].append(variant)
        SUITES['devel'].append(variant)
SUITES['devel'].append('experimental')
SUITES['all'].append('experimental')

DPKG_EXTRACT_UMASK = 0o022

COPYRIGHT_ORACLES = ['debian']

CLOC_LANGUAGES = [
    "ABAP", "ActionScript", "Ada", "ADSO/IDSM", "AMPLE", "Ant", "Apex Trigger",
    "Arduino Sketch", "ASP", "ASP.Net", "AspectJ", "Assembly", "AutoHotkey",
    "awk", "Bourne Again Shell", "Bourne Shell", "C", "C Shell", "C#", "C++",
    "C/C++ Header", "CCS", "Clojure", "ClojureC", "ClojureScript", "CMake",
    "COBOL", "CoffeeScript", "ColdFusion", "ColdFusion CFScript", "Coq",
    "Crystal", "CSON", "CSS", "CUDA", "Cython", "D", "DAL", "Dart", "diff",
    "DITA", "DOORS Extension Language", "DOS Batch", "DTD", "dtrace", "ECPP",
    "EEx", "Elixir", "Elm", "ERB", "Erlang", "Expect", "F#", "Focus", "Forth",
    "Fortran 77", "Fortran 90", "Fortran 95", "GDScript", "Go", "Grails",
    "Groovy", "Haml", "Handlebars", "Harbour", "Haskell", "HLSL", "HTML",
    "IDL", "InstallShield", "Java", "JavaScript", "JavaServer Faces", "JCL",
    "JSON", "JSP", "Julia", "Kermit", "Korn Shell", "Kotlin", "LESS", "lex",
    "Lisp", "LiveLink OScript", "Lua", "m4", "make", "MATLAB", "Maven",
    "Modula3", "MSBuild script", "MUMPS", "Mustache", "MXML", "NAnt script",
    "NASTRAN DMAP", "Nemerle", "Objective C", "Objective C++", "OCaml",
    "OpenCL", "Oracle Forms", "Oracle Reports", "Pascal", "Pascal/Puppet",
    "Patran Command Language", "Perl", "PHP", "PHP/Pascal", "Pig Latin",
    "PL/I", "PowerBuilder", "PowerShell", "Prolog", "Protocol Buffers",
    "PureScript", "Python", "QML", "Qt", "Qt Project", "R", "Racket", "Razor",
    "Rexx", "RobotFramework", "Ruby", "Ruby HTML", "Rust", "SAS", "SASS",
    "Scala", "sed", "SKILL", "SKILL++", "Smarty", "Softbridge Basic", "SQL",
    "SQL Data", "SQL Stored Procedure", "Standard ML", "Stylus", "Swift",
    "Tcl/Tk", "Teamcenter met", "Teamcenter mth", "Titanium Style Sheet",
    "Twig", "TypeScript", "Unity-Prefab", "Vala", "Vala Header",
    "Velocity Template Language", "Verilog-SystemVerilog", "VHDL",
    "vim script", "Visual Basic", "Visual Fox Pro", "Visualforce Component",
    "Visualforce Page", "Windows Message File", "Windows Module Definition",
    "Windows Resource File", "WiX include", "WiX source",
    "WiX string localization", "XAML", "xBase", "xBase Header", "XHTML", "XMI",
    "XML", "XQuery", "XSD", "XSLT", "yacc", "YAML", "zsh", "Brainfuck",
    "Teamcenter def", "Markdown"]
