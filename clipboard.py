import ctypes

from ctypes.wintypes import BOOL, HWND, HANDLE, HGLOBAL, UINT, LPVOID
from ctypes import c_size_t as SIZE_T

OpenClipboard = ctypes.windll.user32.OpenClipboard
OpenClipboard.argtypes = HWND,
OpenClipboard.restype = BOOL

EmptyClipboard = ctypes.windll.user32.EmptyClipboard
EmptyClipboard.restype = BOOL

GetClipboardData = ctypes.windll.user32.GetClipboardData
GetClipboardData.argtypes = UINT,
GetClipboardData.restype = HANDLE

SetClipboardData = ctypes.windll.user32.SetClipboardData
SetClipboardData.argtypes = UINT, HANDLE
SetClipboardData.restype = HANDLE

CloseClipboard = ctypes.windll.user32.CloseClipboard
CloseClipboard.restype = BOOL

CF_UNICODETEXT = 13

GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
GlobalAlloc.argtypes = UINT, SIZE_T
GlobalAlloc.restype = HGLOBAL

GlobalLock = ctypes.windll.kernel32.GlobalLock
GlobalLock.argtypes = HGLOBAL,
GlobalLock.restype = LPVOID

GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
GlobalUnlock.argtypes = HGLOBAL,

GlobalSize = ctypes.windll.kernel32.GlobalSize
GlobalSize.argtypes = HGLOBAL,
GlobalSize.restype = SIZE_T

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040

unicode_type = type(u'')

# Copies given text to clipboard
def copyToClipboard(data_str):
    # if not isinstance(data_str, unicode_type):
    #     data_str = data_str.decode('mbcs')
    data_str1 = data_str.encode('utf-16le')
    if not OpenClipboard(None):
        raise Exception("Failed to open clipboard")

    if not EmptyClipboard():
        CloseClipboard()
        raise Exception("Failed to empty clipboard")

    handle = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(data_str1) + 2)
    if not handle:
        CloseClipboard()
        raise Exception("Failed to allocate global memory")

    pcontents = GlobalLock(handle)
    if not pcontents:
        CloseClipboard()
        raise Exception("Failed to lock global memory")

    ctypes.memmove(pcontents, data_str1, len(data_str1))
    GlobalUnlock(handle)

    if not SetClipboardData(CF_UNICODETEXT, handle):
        CloseClipboard()
        raise Exception("Failed to set clipboard data")

    if not CloseClipboard():
        raise Exception("Failed to close clipboard")

