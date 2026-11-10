/* arexx.rexx: wxMaxima's ARexx port (WXMAXIMA.1). Start wxMaxima first,
 * with RexxMast running, and wait for "Maxima is ready for input". Prints
 * PASS or FAIL for each check, then QUITs it (FORCE: the test's cells are
 * not saved). rx tests/arexx.rexx
 * Copyright (c) 2026 AmiCradle Team */
OPTIONS RESULTS
bad = 0
IF ~SHOW('P', 'WXMAXIMA.1') THEN DO
    SAY 'FAIL wxMaxima is not running (no WXMAXIMA.1)'
    EXIT 20
END
ADDRESS 'WXMAXIMA.1'

'VERSION'
CALL check 'VERSION', rc = 0 & LEFT(result, 9) = 'wxMaxima '
'HELP'
CALL check 'HELP', rc = 0 & POS('EVAL', result) > 0 & POS('QUIT', result) > 0
'EVAL "2+3" WAIT'
CALL check 'EVAL 2+3 WAIT', rc = 0 & POS('5', result) > 0
r1 = result
'EVAL "integrate(x^2, x);" WAIT'
CALL check 'EVAL integrate WAIT', rc = 0 & POS('x', result) > 0 & POS('3', result) > 0
'EVAL "expand((a+b)^2)" WAIT'
CALL check 'EVAL expand WAIT', rc = 0 & POS('a', result) > 0 & POS('b', result) > 0
'BUSY'
CALL check 'BUSY after WAIT', rc = 0 & result = 0
'EVAL "1+1"'
CALL check 'EVAL without WAIT', rc = 0
DO i = 1 TO 600
    'BUSY'
    IF result = 0 THEN LEAVE
    ADDRESS COMMAND 'Wait 1'
END
CALL check 'BUSY ends', result = 0
'OPEN NoSuchDrawer/none.wxmx'
CALL check 'OPEN missing', rc = 10
'NOSUCH'
CALL check 'unknown', rc >= 10
'DEACTIVATE'
CALL check 'DEACTIVATE', rc = 0
'ACTIVATE'
CALL check 'ACTIVATE', rc = 0
'SAVE'
CALL check 'SAVE untitled, no FILE: RC 10, no requester', rc = 10
'QUIT'
CALL check 'QUIT unsaved untitled: RC 5, stays', rc = 5 & SHOW('P', 'WXMAXIMA.1')
ADDRESS COMMAND 'Delete >NIL: RAM:wxm-arexx-test.wxmx'
'SAVE FILE RAM:wxm-arexx-test.wxmx'
CALL check 'SAVE FILE', rc = 0 & EXISTS('RAM:wxm-arexx-test.wxmx')
'QUIT FORCE'
CALL check 'QUIT FORCE', rc = 0
DO i = 1 TO 60
    IF ~SHOW('P', 'WXMAXIMA.1') THEN LEAVE
    ADDRESS COMMAND 'Wait 1'
END
CALL check 'port gone after QUIT FORCE', ~SHOW('P', 'WXMAXIMA.1')
IF bad = 0 THEN SAY 'wxmaxima arexx: ALL PASS'
ELSE SAY 'wxmaxima arexx:' bad 'FAILED'
EXIT bad

check: PARSE ARG what, ok
IF ok THEN SAY 'PASS' what
ELSE DO
  SAY 'FAIL' what '(rc' rc', result "'LEFT(result, 60)'")'
  bad = bad + 1
END
RETURN
