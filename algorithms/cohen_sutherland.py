# ============================================================
# Cohen-Sutherland Line Clipping Algorithm
# ============================================================
# Region codes (outcodes)
INSIDE = 0  # 0000
LEFT   = 1  # 0001
RIGHT  = 2  # 0010
TOP    = 4  # 0100 (y kecil = atas di layar)
BOTTOM = 8  # 1000 (y besar = bawah di layar)


def _compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """Hitung region code untuk titik (x, y) terhadap window clipping."""
    code = INSIDE

    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= TOP
    elif y > ymax:
        code |= BOTTOM

    return code


def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Clip garis dari (x1,y1) ke (x2,y2) terhadap window clipping rectangle.

    Parameter:
        x1, y1      : titik awal garis
        x2, y2      : titik akhir garis
        xmin, ymin  : sudut kiri atas window
        xmax, ymax  : sudut kanan bawah window

    Return:
        (x1, y1, x2, y2) jika garis (sebagian) terlihat, atau None jika sepenuhnya di luar.
    """
    outcode1 = _compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    outcode2 = _compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    while True:
        # Kasus 1: Kedua titik di dalam window → terima
        if not (outcode1 | outcode2):
            return int(x1), int(y1), int(x2), int(y2)

        # Kasus 2: Kedua titik di luar region yang sama → tolak (buang)
        elif outcode1 & outcode2:
            return None

        # Kasus 3: Salah satu titik di luar → cari titik potong dengan batas window
        else:
            x, y = 0.0, 0.0

            # Pilih titik yang berada di luar window
            outcode_out = outcode1 if outcode1 else outcode2

            # Hitung titik potong berdasarkan region
            if outcode_out & BOTTOM:
                # Potong dengan batas bawah (y = ymax)
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif outcode_out & TOP:
                # Potong dengan batas atas (y = ymin)
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif outcode_out & RIGHT:
                # Potong dengan batas kanan (x = xmax)
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif outcode_out & LEFT:
                # Potong dengan batas kiri (x = xmin)
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Perbarui titik yang di luar dengan titik potong hasil clipping
            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = _compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                outcode2 = _compute_outcode(x2, y2, xmin, ymin, xmax, ymax)


def clip_line_segments(segments, xmin, ymin, xmax, ymax):
    """
    Clip sekumpulan segmen garis [(x1,y1,x2,y2), ...] terhadap window.
    Mengembalikan list segmen yang sudah di-clip (yang di luar dibuang).
    """
    result = []
    for seg in segments:
        clipped = cohen_sutherland_clip(*seg, xmin, ymin, xmax, ymax)
        if clipped:
            result.append(clipped)
    return result
