"""Wrapper for wgl.h

Generated by tools/gengl.py.
"""

from ctypes import CFUNCTYPE, POINTER, Structure, c_char, c_char_p, c_double, c_float, c_int
from ctypes import c_short, c_ubyte, c_uint, c_ulong, c_ulonglong, c_ushort, c_long, c_longlong

from pyglet.gl.lib import link_WGL as _link_function

if not _link_function:
    raise ImportError('opengl32.dll is not available.')

CONST = 0
GLenum = c_uint
GLboolean = c_ubyte
GLbitfield = c_uint
GLbyte = c_char
GLshort = c_short
GLint = c_int
GLsizei = c_int
GLubyte = c_ubyte
GLushort = c_ushort
GLuint = c_uint
GLfloat = c_float
GLclampf = c_float
GLdouble = c_double
GLclampd = c_double
GLvoid = None
INT8 = c_char
PINT8 = c_char_p
INT16 = c_short
PINT16 = POINTER(c_short)
INT32 = c_int
PINT32 = POINTER(c_int)
UINT8 = c_ubyte
PUINT8 = POINTER(c_ubyte)
UINT16 = c_ushort
PUINT16 = POINTER(c_ushort)
UINT32 = c_uint
PUINT32 = POINTER(c_uint)
LONG32 = c_int
PLONG32 = POINTER(c_int)
ULONG32 = c_uint
PULONG32 = POINTER(c_uint)
DWORD32 = c_uint
PDWORD32 = POINTER(c_uint)
INT64 = c_longlong
PINT64 = POINTER(c_longlong)
UINT64 = c_ulonglong
PUINT64 = POINTER(c_ulonglong)
VOID = None
LPVOID = POINTER(None)
LPCSTR = c_char_p
CHAR = c_char
BYTE = c_ubyte
WORD = c_ushort
USHORT = c_ushort
UINT = c_uint
INT = c_int
INT_PTR = POINTER(c_int)
BOOL = c_long
LONG = c_long
DWORD = c_ulong
FLOAT = c_float
COLORREF = DWORD
LPCOLORREF = POINTER(DWORD)
HANDLE = POINTER(None)
HGLRC = HANDLE
HDC = HANDLE
PROC = CFUNCTYPE(INT_PTR)

wglCopyContext = _link_function('wglCopyContext', BOOL, [HGLRC, HGLRC, UINT], None)
wglCreateContext = _link_function('wglCreateContext', HGLRC, [HDC], None)
wglCreateLayerContext = _link_function('wglCreateLayerContext', HGLRC, [HDC, c_int], None)
wglDeleteContext = _link_function('wglDeleteContext', BOOL, [HGLRC], None)
wglGetCurrentContext = _link_function('wglGetCurrentContext', HGLRC, [], None)
wglGetCurrentDC = _link_function('wglGetCurrentDC', HDC, [], None)
wglGetProcAddress = _link_function('wglGetProcAddress', PROC, [LPCSTR], None)
wglMakeCurrent = _link_function('wglMakeCurrent', BOOL, [HDC, HGLRC], None)
wglShareLists = _link_function('wglShareLists', BOOL, [HGLRC, HGLRC], None)
wglUseFontBitmapsA = _link_function('wglUseFontBitmapsA', BOOL, [HDC, DWORD, DWORD, DWORD], None)
wglUseFontBitmapsW = _link_function('wglUseFontBitmapsW', BOOL, [HDC, DWORD, DWORD, DWORD], None)
SwapBuffers = _link_function('SwapBuffers', BOOL, [HDC], None)


class struct__POINTFLOAT(Structure):
    __slots__ = [
        'x',
        'y',
    ]


struct__POINTFLOAT._fields_ = [
    ('x', FLOAT),
    ('y', FLOAT),
]

POINTFLOAT = struct__POINTFLOAT
PPOINTFLOAT = POINTER(struct__POINTFLOAT)


class struct__GLYPHMETRICSFLOAT(Structure):
    __slots__ = [
        'gmfBlackBoxX',
        'gmfBlackBoxY',
        'gmfptGlyphOrigin',
        'gmfCellIncX',
        'gmfCellIncY',
    ]


struct__GLYPHMETRICSFLOAT._fields_ = [
    ('gmfBlackBoxX', FLOAT),
    ('gmfBlackBoxY', FLOAT),
    ('gmfptGlyphOrigin', POINTFLOAT),
    ('gmfCellIncX', FLOAT),
    ('gmfCellIncY', FLOAT),
]

GLYPHMETRICSFLOAT = struct__GLYPHMETRICSFLOAT
PGLYPHMETRICSFLOAT = POINTER(struct__GLYPHMETRICSFLOAT)
LPGLYPHMETRICSFLOAT = POINTER(struct__GLYPHMETRICSFLOAT)
WGL_FONT_LINES = 0
WGL_FONT_POLYGONS = 1

wglUseFontOutlinesA = _link_function('wglUseFontOutlinesA', BOOL, [HDC, DWORD, DWORD, DWORD, FLOAT, FLOAT, c_int, LPGLYPHMETRICSFLOAT], None)
wglUseFontOutlinesW = _link_function('wglUseFontOutlinesW', BOOL, [HDC, DWORD, DWORD, DWORD, FLOAT, FLOAT, c_int, LPGLYPHMETRICSFLOAT], None)


class struct_tagLAYERPLANEDESCRIPTOR(Structure):
    __slots__ = [
        'nSize',
        'nVersion',
        'dwFlags',
        'iPixelType',
        'cColorBits',
        'cRedBits',
        'cRedShift',
        'cGreenBits',
        'cGreenShift',
        'cBlueBits',
        'cBlueShift',
        'cAlphaBits',
        'cAlphaShift',
        'cAccumBits',
        'cAccumRedBits',
        'cAccumGreenBits',
        'cAccumBlueBits',
        'cAccumAlphaBits',
        'cDepthBits',
        'cStencilBits',
        'cAuxBuffers',
        'iLayerPlane',
        'bReserved',
        'crTransparent',
    ]


struct_tagLAYERPLANEDESCRIPTOR._fields_ = [
    ('nSize', WORD),
    ('nVersion', WORD),
    ('dwFlags', DWORD),
    ('iPixelType', BYTE),
    ('cColorBits', BYTE),
    ('cRedBits', BYTE),
    ('cRedShift', BYTE),
    ('cGreenBits', BYTE),
    ('cGreenShift', BYTE),
    ('cBlueBits', BYTE),
    ('cBlueShift', BYTE),
    ('cAlphaBits', BYTE),
    ('cAlphaShift', BYTE),
    ('cAccumBits', BYTE),
    ('cAccumRedBits', BYTE),
    ('cAccumGreenBits', BYTE),
    ('cAccumBlueBits', BYTE),
    ('cAccumAlphaBits', BYTE),
    ('cDepthBits', BYTE),
    ('cStencilBits', BYTE),
    ('cAuxBuffers', BYTE),
    ('iLayerPlane', BYTE),
    ('bReserved', BYTE),
    ('crTransparent', COLORREF),
]

LAYERPLANEDESCRIPTOR = struct_tagLAYERPLANEDESCRIPTOR
PLAYERPLANEDESCRIPTOR = POINTER(struct_tagLAYERPLANEDESCRIPTOR)
LPLAYERPLANEDESCRIPTOR = POINTER(struct_tagLAYERPLANEDESCRIPTOR)
LPD_DOUBLEBUFFER = 1
LPD_STEREO = 2
LPD_SUPPORT_GDI = 16
LPD_SUPPORT_OPENGL = 32
LPD_SHARE_DEPTH = 64
LPD_SHARE_STENCIL = 128
LPD_SHARE_ACCUM = 256
LPD_SWAP_EXCHANGE = 512
LPD_SWAP_COPY = 1024
LPD_TRANSPARENT = 4096
LPD_TYPE_RGBA = 0
LPD_TYPE_COLORINDEX = 1
WGL_SWAP_MAIN_PLANE = 1
WGL_SWAP_OVERLAY1 = 2
WGL_SWAP_OVERLAY2 = 4
WGL_SWAP_OVERLAY3 = 8
WGL_SWAP_OVERLAY4 = 16
WGL_SWAP_OVERLAY5 = 32
WGL_SWAP_OVERLAY6 = 64
WGL_SWAP_OVERLAY7 = 128
WGL_SWAP_OVERLAY8 = 256
WGL_SWAP_OVERLAY9 = 512
WGL_SWAP_OVERLAY10 = 1024
WGL_SWAP_OVERLAY11 = 2048
WGL_SWAP_OVERLAY12 = 4096
WGL_SWAP_OVERLAY13 = 8192
WGL_SWAP_OVERLAY14 = 16384
WGL_SWAP_OVERLAY15 = 32768
WGL_SWAP_UNDERLAY1 = 65536
WGL_SWAP_UNDERLAY2 = 131072
WGL_SWAP_UNDERLAY3 = 262144
WGL_SWAP_UNDERLAY4 = 524288
WGL_SWAP_UNDERLAY5 = 1048576
WGL_SWAP_UNDERLAY6 = 2097152
WGL_SWAP_UNDERLAY7 = 4194304
WGL_SWAP_UNDERLAY8 = 8388608
WGL_SWAP_UNDERLAY9 = 16777216
WGL_SWAP_UNDERLAY10 = 33554432
WGL_SWAP_UNDERLAY11 = 67108864
WGL_SWAP_UNDERLAY12 = 134217728
WGL_SWAP_UNDERLAY13 = 268435456
WGL_SWAP_UNDERLAY14 = 536870912
WGL_SWAP_UNDERLAY15 = 1073741824

wglDescribeLayerPlane = _link_function('wglDescribeLayerPlane', BOOL, [HDC, c_int, c_int, UINT, LPLAYERPLANEDESCRIPTOR], None)
wglSetLayerPaletteEntries = _link_function('wglSetLayerPaletteEntries', c_int, [HDC, c_int, c_int, c_int, POINTER(COLORREF)], None)
wglGetLayerPaletteEntries = _link_function('wglGetLayerPaletteEntries', c_int, [HDC, c_int, c_int, c_int, POINTER(COLORREF)], None)
wglRealizeLayerPalette = _link_function('wglRealizeLayerPalette', BOOL, [HDC, c_int, BOOL], None)
wglSwapLayerBuffers = _link_function('wglSwapLayerBuffers', BOOL, [HDC, UINT], None)


class struct__WGLSWAP(Structure):
    __slots__ = [
        'hdc',
        'uiFlags',
    ]


struct__WGLSWAP._fields_ = [
    ('hdc', HDC),
    ('uiFlags', UINT),
]

WGLSWAP = struct__WGLSWAP
PWGLSWAP = POINTER(struct__WGLSWAP)
LPWGLSWAP = POINTER(struct__WGLSWAP)
WGL_SWAPMULTIPLE_MAX = 16

wglSwapMultipleBuffers = _link_function('wglSwapMultipleBuffers', DWORD, [UINT, POINTER(WGLSWAP)], None)


class struct_tagRECT(Structure):
    __slots__ = [
        'left',
        'top',
        'right',
        'bottom',
    ]


struct_tagRECT._fields_ = [
    ('left', LONG),
    ('top', LONG),
    ('right', LONG),
    ('bottom', LONG),
]

RECT = struct_tagRECT
PRECT = POINTER(struct_tagRECT)
NPRECT = POINTER(struct_tagRECT)
LPRECT = POINTER(struct_tagRECT)

__all__ = ['CONST', 'GLenum', 'GLboolean', 'GLbitfield', 'GLbyte', 'GLshort',
           'GLint', 'GLsizei', 'GLubyte', 'GLushort', 'GLuint', 'GLfloat', 'GLclampf',
           'GLdouble', 'GLclampd', 'GLvoid', 'INT8', 'PINT8', 'INT16', 'PINT16', 'INT32',
           'PINT32', 'UINT8', 'PUINT8', 'UINT16', 'PUINT16', 'UINT32', 'PUINT32',
           'LONG32', 'PLONG32', 'ULONG32', 'PULONG32', 'DWORD32', 'PDWORD32', 'INT64',
           'PINT64', 'UINT64', 'PUINT64', 'VOID', 'LPVOID', 'LPCSTR', 'CHAR', 'BYTE',
           'WORD', 'USHORT', 'UINT', 'INT', 'INT_PTR', 'BOOL', 'LONG', 'DWORD', 'FLOAT',
           'COLORREF', 'LPCOLORREF', 'HANDLE', 'HGLRC', 'HDC', 'PROC', 'wglCopyContext',
           'wglCreateContext', 'wglCreateLayerContext', 'wglDeleteContext',
           'wglGetCurrentContext', 'wglGetCurrentDC', 'wglGetProcAddress',
           'wglMakeCurrent', 'wglShareLists', 'wglUseFontBitmapsA', 'wglUseFontBitmapsW',
           'SwapBuffers', 'POINTFLOAT', 'PPOINTFLOAT', 'GLYPHMETRICSFLOAT',
           'PGLYPHMETRICSFLOAT', 'LPGLYPHMETRICSFLOAT', 'WGL_FONT_LINES',
           'WGL_FONT_POLYGONS', 'wglUseFontOutlinesA', 'wglUseFontOutlinesW',
           'LAYERPLANEDESCRIPTOR', 'PLAYERPLANEDESCRIPTOR', 'LPLAYERPLANEDESCRIPTOR',
           'LPD_DOUBLEBUFFER', 'LPD_STEREO', 'LPD_SUPPORT_GDI', 'LPD_SUPPORT_OPENGL',
           'LPD_SHARE_DEPTH', 'LPD_SHARE_STENCIL', 'LPD_SHARE_ACCUM',
           'LPD_SWAP_EXCHANGE', 'LPD_SWAP_COPY', 'LPD_TRANSPARENT', 'LPD_TYPE_RGBA',
           'LPD_TYPE_COLORINDEX', 'WGL_SWAP_MAIN_PLANE', 'WGL_SWAP_OVERLAY1',
           'WGL_SWAP_OVERLAY2', 'WGL_SWAP_OVERLAY3', 'WGL_SWAP_OVERLAY4',
           'WGL_SWAP_OVERLAY5', 'WGL_SWAP_OVERLAY6', 'WGL_SWAP_OVERLAY7',
           'WGL_SWAP_OVERLAY8', 'WGL_SWAP_OVERLAY9', 'WGL_SWAP_OVERLAY10',
           'WGL_SWAP_OVERLAY11', 'WGL_SWAP_OVERLAY12', 'WGL_SWAP_OVERLAY13',
           'WGL_SWAP_OVERLAY14', 'WGL_SWAP_OVERLAY15', 'WGL_SWAP_UNDERLAY1',
           'WGL_SWAP_UNDERLAY2', 'WGL_SWAP_UNDERLAY3', 'WGL_SWAP_UNDERLAY4',
           'WGL_SWAP_UNDERLAY5', 'WGL_SWAP_UNDERLAY6', 'WGL_SWAP_UNDERLAY7',
           'WGL_SWAP_UNDERLAY8', 'WGL_SWAP_UNDERLAY9', 'WGL_SWAP_UNDERLAY10',
           'WGL_SWAP_UNDERLAY11', 'WGL_SWAP_UNDERLAY12', 'WGL_SWAP_UNDERLAY13',
           'WGL_SWAP_UNDERLAY14', 'WGL_SWAP_UNDERLAY15', 'wglDescribeLayerPlane',
           'wglSetLayerPaletteEntries', 'wglGetLayerPaletteEntries',
           'wglRealizeLayerPalette', 'wglSwapLayerBuffers', 'WGLSWAP', 'PWGLSWAP',
           'LPWGLSWAP', 'WGL_SWAPMULTIPLE_MAX', 'wglSwapMultipleBuffers', 'RECT',
           'PRECT', 'NPRECT', 'LPRECT']
