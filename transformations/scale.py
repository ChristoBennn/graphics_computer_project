def scale_point(x, y, sx, sy, cx, cy):

    x -= cx
    y -= cy

    x *= sx
    y *= sy

    x += cx
    y += cy

    return int(x), int(y)


def scale_points(points, sx, sy, cx, cy):
    return [scale_point(x, y, sx, sy, cx, cy) for (x, y) in points]


def scale_circles(circles, sx, sy, cx, cy):
    return [
        (scale_point(x, y, sx, sy, cx, cy)[0],
         scale_point(x, y, sx, sy, cx, cy)[1],
         int(r * sx))
        for (x, y, r) in circles
    ]


def scale_rectangles(rectangles, sx, sy, cx, cy):
    return [
        (
            scale_point(x1, y1, sx, sy, cx, cy)[0],
            scale_point(x1, y1, sx, sy, cx, cy)[1],
            scale_point(x2, y2, sx, sy, cx, cy)[0],
            scale_point(x2, y2, sx, sy, cx, cy)[1]
        )
        for (x1, y1, x2, y2) in rectangles
    ]


def scale_triangles(triangles, sx, sy, cx, cy):
    return [
        (
            scale_point(p1[0], p1[1], sx, sy, cx, cy),
            scale_point(p2[0], p2[1], sx, sy, cx, cy),
            scale_point(p3[0], p3[1], sx, sy, cx, cy)
        )
        for (p1, p2, p3) in triangles
    ]