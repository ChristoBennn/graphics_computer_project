def translate_points(points, tx, ty):
    return [(x + tx, y + ty) for (x, y) in points]


def translate_circles(circles, tx, ty):
    return [(x + tx, y + ty, r) for (x, y, r) in circles]


def translate_rectangles(rectangles, tx, ty):
    return [(x1 + tx, y1 + ty, x2 + tx, y2 + ty) for (x1, y1, x2, y2) in rectangles]


def translate_triangles(triangles, tx, ty):
    return [
        (
            (p1[0] + tx, p1[1] + ty),
            (p2[0] + tx, p2[1] + ty),
            (p3[0] + tx, p3[1] + ty)
        )
        for (p1, p2, p3) in triangles
    ]