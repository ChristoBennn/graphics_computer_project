import math


def rotate_point(x, y, angle, cx, cy):
    rad = math.radians(angle)

    x -= cx
    y -= cy

    xr = x * math.cos(rad) - y * math.sin(rad)
    yr = x * math.sin(rad) + y * math.cos(rad)

    xr += cx
    yr += cy

    return int(xr), int(yr)


def rotate_points(points, angle, cx, cy):
    return [rotate_point(x, y, angle, cx, cy) for (x, y) in points]


def rotate_circles(circles, angle, cx, cy):
    return [(rotate_point(x, y, angle, cx, cy)[0],
             rotate_point(x, y, angle, cx, cy)[1],
             r) for (x, y, r) in circles]


def rotate_rectangles(rectangles, angle, cx, cy):
    return [
        (
            rotate_point(x1, y1, angle, cx, cy)[0],
            rotate_point(x1, y1, angle, cx, cy)[1],
            rotate_point(x2, y2, angle, cx, cy)[0],
            rotate_point(x2, y2, angle, cx, cy)[1]
        )
        for (x1, y1, x2, y2) in rectangles
    ]


def rotate_triangles(triangles, angle, cx, cy):
    return [
        (
            rotate_point(p1[0], p1[1], angle, cx, cy),
            rotate_point(p2[0], p2[1], angle, cx, cy),
            rotate_point(p3[0], p3[1], angle, cx, cy)
        )
        for (p1, p2, p3) in triangles
    ]