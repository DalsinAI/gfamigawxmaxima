# GFAmigaWxMaxima

wxMaxima, the worksheet for the Maxima computer algebra system, for AmigaOS 3: 68040, the FPU when there is one (fpuauto), on the GFOpenWX Toolkit (wxWidgets on GFOpenLayout). Maxima runs beside it on AmigaCLISP.

Status: work in progress, not yet run on an Amiga.

## What is built

| Part | Version | From |
|---|---|---|
| wxMaxima | 26.10.0 | its release tag, fetched at build time |
| Maxima | 5.50.0 | its source release, fetched at build time |
| AmigaCLISP | 0.1 rc1 | DalsinAI/amigaclisp: the host CLISP that compiles Maxima, and the Amiga lisp that runs it |
| GFOpenWX Toolkit | team3/wxmaxima-wx-20261106 | DalsinAI/gfopenwxtoolkit |

`wxmaxima.lock` pins every one of them. Nothing third-party is kept in this repository.

## Building

```
STOVE=~/AmiCradle/stoves/os32-gcc16-open6 OUT=out ./build-amiga.sh
```

A run that reaches its time budget says RESUME; run it again until it says DONE. `out/` gets `wxMaxima`, the `maxima` launcher and `wxMaxima-<version>.tgz`, the drawer below.

## The drawer

```
wxMaxima/
  wxMaxima              the program
  Maxima/
    maxima              our launcher: sets MAXIMA_PREFIX, starts lisp with maxima.mem
    lisp                AmigaCLISP
    clisp/              CLISP's compiled system
    binary-clisp/       Maxima's compiled files (compiled on the build host: CLISP's .fas are the same everywhere)
    share/maxima/       Maxima's packages and sources
    loadmaxima.lisp     Maxima's load order
    makeimage.lisp      the first start's script
    maxima.mem          made on the Amiga at first start (a memory image belongs to the machine it is made on)
```

wxMaxima finds `Maxima/maxima` beside itself, starts it with `-s <port>` and talks to it over a local socket, as on every other system.

## ARexx

Each wxMaxima window has an ARexx port, `WXMAXIMA.1` (`WXMAXIMA.2` for a second window), from the GFOpenWX Toolkit's `wxARexxPort` on arexx.class.

| Command | Does |
| --- | --- |
| `OPEN FILE/A` | open a worksheet (`.wxmx`, `.wxm`) or a `.mac` file |
| `SAVE` | save the worksheet (asks for a name if it has none; RC 5 when not saved) |
| `EVAL EXPR/A,WAIT/S` | a new cell with EXPR, evaluated; WAIT answers once Maxima has finished |
| `EVALALL` | evaluate every cell |
| `INTERRUPT` | stop the evaluation |
| `BUSY` | RESULT: 1 while Maxima is working, else 0 |
| `QUIT`, `ACTIVATE`, `DEACTIVATE`, `VERSION`, `HELP`, `FAULT` | the toolkit's standard commands |

```
/* wxMaxima: integrate, wait, save */
OPTIONS RESULTS
ADDRESS 'WXMAXIMA.1'
'EVAL "integrate(x^2, x);" WAIT'
'SAVE'
```

## Changes to wxMaxima

`patches/`: Maxima's place in the drawer, the variables Maxima must see set in wxMaxima's own process (an Amiga CLI takes its parent's variables, it has no environment block), a longer wait for Maxima to connect, and the ARexx port (`src/AmigaRexx.cpp`).

## Licence

wxMaxima and Maxima are GPL v2 or later (Maxima: GPL v2); this port's patches, launcher and scripts are under GPL v2 or later.

Designed, tested and delivered by The AmiCradle Team.
Copyright (c) 2026 AmiCradle Team
