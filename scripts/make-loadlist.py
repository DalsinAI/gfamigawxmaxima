#!/usr/bin/env python3
# Copyright (c) 2026 AmiCradle Team. GPL-2.0-or-later, as Maxima.
"""Maxima's load order for the Amiga's image: what Maxima's own build
(defsystem's :load of "maxima", run verbose on the build host) loaded, in
that order, as loadmaxima.lisp. The Amiga loads the same files from
MAXIMA_PREFIX (binary-clisp/ for compiled files, share/maxima/V/src/ for
the few sources the build loads as they are) and saves maxima.mem there,
as Maxima's Makefile does.
    make-loadlist.py LOAD_LOG VERSION OUT"""
import re, sys
log, version, out = sys.argv[1:4]
items = []
# CLISP wraps a long line: a quoted path can go on the next ";" line
text = re.sub(r'\n;\s+(?=")', ' ', open(log, encoding="utf-8", errors="replace").read())
for line in text.split("\n"):
    m = re.search(r'Loading binary file "binary-clisp/(.+)\.fas"', line)
    if m:
        items.append(("bin", m.group(1)))
        continue
    m = re.search(r'Loading source (?:private-)?file "(?:.*/)?([^/"]+\.lisp)"', line)
    if m:
        items.append(("src", m.group(1)))
if not any(k == "bin" for k, _ in items):
    sys.exit("make-loadlist: no compiled files in " + log)
with open(out, "w") as f:
    f.write(";;; Maxima %s for AmigaCLISP: load Maxima, save MAXIMA_PREFIX/maxima.mem.\n" % version)
    f.write(";;; Made by make-loadlist.py from Maxima's own load order (%d files).\n" % len(items))
    f.write("(in-package :cl-user)\n")
    # maxima.system defines and exports cl-user:*maxima-build-time* before
    # it loads anything (build_info() and wxMathML.lisp's wxbuild_info()
    # read it); the load list leaves maxima.system out, so it goes here.
    # Without it, wxMathML.lisp stops at read time, before it prints the
    # key wxMaxima waits for, and no cell is ever evaluated.
    import os, time
    t = time.gmtime(int(os.environ.get("SOURCE_DATE_EPOCH", os.path.getmtime(log))))
    f.write("(defvar *maxima-build-time* '(%d %d %d %d %d %d %d nil 0))\n"
            % (t.tm_sec, t.tm_min, t.tm_hour, t.tm_mday, t.tm_mon, t.tm_year, t.tm_wday))
    f.write("(export '*maxima-build-time*)\n")
    f.write("(setf *read-default-float-format* 'double-float)\n")
    f.write("(defvar *amiga-maxima-prefix* (ext:getenv \"MAXIMA_PREFIX\"))\n")
    f.write("(defun amiga-maxima-file (kind name)\n"
            "  (concatenate 'string *amiga-maxima-prefix*\n"
            "               (if (eq kind :bin) \"/binary-clisp/\" \"/share/maxima/%s/src/\")\n"
            "               name (if (eq kind :bin) \".fas\" \"\")))\n" % version)
    f.write("(dolist (f '(\n")
    for k, n in items:
        f.write("  (:%s \"%s\")\n" % (k, n))
    f.write("  ))\n  (load (amiga-maxima-file (first f) (second f)) :verbose nil))\n")
    # An AmigaDOS name ("SYS:Prefs/Env-Archive", the HOME Maxima builds its
    # userdir from) has no device part for this CLISP, so Maxima's
    # maxima-parse-dirstring made it "/SYS:Prefs/...", and the first probe
    # there put up "Please insert volume /SYS" and held Maxima until someone
    # answered it. Give it the unix-style name the other paths use
    # ("/SYS/Prefs/Env-Archive/").
    f.write("(in-package :maxima)\n"
            "(let ((parse (symbol-function 'maxima-parse-dirstring)))\n"
            "  (setf (symbol-function 'maxima-parse-dirstring)\n"
            "        (lambda (str)\n"
            "          (let ((c (position #\\: str)) (s (position #\\/ str)))\n"
            "            (funcall parse (if (and c (> c 0) (or (null s) (< c s)))\n"
            "                               (concatenate 'string \"/\" (subseq str 0 c) \"/\" (subseq str (1+ c)))\n"
            "                               str))))))\n"
            "(in-package :cl-user)\n")
    # AmigaOS has no /usr volume: Maxima's message catalogues are looked for
    # only under MAXIMA_PREFIX (Maxima adds that at start)
    f.write("(setq intl::*locale-directories* nil)\n")
    f.write("(ext:saveinitmem (concatenate 'string *amiga-maxima-prefix* \"/maxima.mem\")\n"
            "                 :init-function (function cl-user::run))\n")
    f.write("(ext:exit)\n")
print("make-loadlist: %d files" % len(items))
