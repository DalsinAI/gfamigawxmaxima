/* Eval.rexx: wxMaxima works out an expression and prints the answer.
   rx Eval.rexx "integrate(x^2, x)"   (wxMaxima running) */
OPTIONS RESULTS
PARSE ARG expr
IF expr = '' THEN expr = 'integrate(x^2, x)'
IF ~SHOW('P', 'WXMAXIMA.1') THEN DO
    SAY 'wxMaxima is not running.'
    EXIT 5
END
ADDRESS 'WXMAXIMA.1'
'EVAL' '"'expr'"' 'WAIT'
IF rc = 0 THEN SAY expr '=' result
ELSE SAY 'Maxima could not do it (rc' rc')'
