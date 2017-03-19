from cffi import FFI
import os

ffi = FFI()
ffi.cdef("""
/* from stdio.h */
FILE* fopen(const char* path, const char* mode);
int fclose(FILE* fp);
FILE* stderr;  /* GNU C library */
FILE* __stderrp;  /* Mac OS X */
""")

try:
    stdio = ffi.dlopen(None)
    devnull = stdio.fopen(os.devnull.encode(), b'w')
except OSError:
    pass
try:
    stdio.stderr = devnull
except KeyError:
    try:
        stdio.__stderrp = devnull
    except KeyError:
        stdio.fclose(devnull)