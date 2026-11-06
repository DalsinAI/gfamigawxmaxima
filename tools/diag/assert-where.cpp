// Diagnostic only (never shipped): wraps wx's assert entry for asserts with
// a C string message and writes where it was called from, as an offset from
// this function, to T:wxassert.log, so the address can be found in the
// unstripped binary.
#include <stdio.h>
extern "C" void __real__Z10wxOnAssertPKciS0_S0_S0_(const char *, int, const char *, const char *, const char *);
extern "C" void __real__Z10wxOnAssertPKciS0_S0_(const char *, int, const char *, const char *);
extern "C" void __wrap__Z10wxOnAssertPKciS0_S0_S0_(const char *file, int line, const char *func,
                                                   const char *cond, const char *msg)
{
    void *ra = __builtin_return_address(0);
    FILE *f = fopen("T:wxassert.log", "a");
    if (f) {
        fprintf(f, "assert %s:%d %s (%s) caller %p wrap5 %p\n", file, line, func ? func : "", cond ? cond : "",
                ra, (void *)&__wrap__Z10wxOnAssertPKciS0_S0_S0_);
        fclose(f);
    }
    __real__Z10wxOnAssertPKciS0_S0_S0_(file, line, func, cond, msg);
}
extern "C" void __wrap__Z10wxOnAssertPKciS0_S0_(const char *file, int line, const char *func, const char *cond)
{
    void *ra = __builtin_return_address(0);
    FILE *f = fopen("T:wxassert.log", "a");
    if (f) {
        fprintf(f, "assert %s:%d %s (%s) caller %p wrap5 %p\n", file, line, func ? func : "", cond ? cond : "",
                ra, (void *)&__wrap__Z10wxOnAssertPKciS0_S0_S0_);
        fclose(f);
    }
    __real__Z10wxOnAssertPKciS0_S0_(file, line, func, cond);
}
