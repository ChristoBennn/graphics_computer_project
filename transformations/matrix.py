def apply_matrix(points, matrix):
    new_points = []
    for x, y in points:
        x_new = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]
        y_new = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]
        new_points.append((int(x_new), int(y_new)))
    return new_points


def apply_matrix_circles(circles, matrix):
    new_circles = []
    for x, y, r in circles:
        x_new, y_new = apply_matrix([(x, y)], matrix)[0]
        new_circles.append((x_new, y_new, r))
    return new_circles


def apply_matrix_rectangles(rectangles, matrix):
    new_rects = []
    for x1, y1, x2, y2 in rectangles:
        p1 = apply_matrix([(x1, y1)], matrix)[0]
        p2 = apply_matrix([(x2, y2)], matrix)[0]
        new_rects.append((p1[0], p1[1], p2[0], p2[1]))
    return new_rects


def apply_matrix_triangles(triangles, matrix):
    new_tris = []
    for p1, p2, p3 in triangles:
        p1_new = apply_matrix([p1], matrix)[0]
        p2_new = apply_matrix([p2], matrix)[0]
        p3_new = apply_matrix([p3], matrix)[0]
        new_tris.append((p1_new, p2_new, p3_new))
    return new_tris