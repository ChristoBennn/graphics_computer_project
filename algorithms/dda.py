def draw_line_dda(surface, x1, y1, x2, y2, color):

    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for i in range(int(steps)):
        surface.set_at((round(x), round(y)), color)
        x += x_inc
        y += y_inc