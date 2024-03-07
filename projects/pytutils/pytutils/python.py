import sys
import types


class PyInfo(object):
    PY2 = sys.version_info[0] == 2
    PY3 = sys.version_info[0] == 3

    if PY3:
        string_types = str,
        text_type = str
        binary_type = bytes
        integer_types = int,
        class_types = type,

        maxsize = sys.maxsize
    else:  # PY2
        string_types = basestring,
        text_type = unicode
        binary_type = str
        integer_types = (int, long)
        class_types = (type, types.ClassType)

        if sys.platform.startswith("java"):
            # Jython always uses 32 bits.
            maxsize = int((1 << 31) - 1)
        else:
            # It's possible to have sizeof(long) != sizeof(Py_ssize_t).
            class X(object):

                def __len__(self):
                    return 1 << 31

            try:
                len(X())
            except OverflowError:
                # 32-bit
                maxsize = int((1 << 31) - 1)
            else:
                # 64-bit
                maxsize = int((1 << 63) - 1)
            del X

