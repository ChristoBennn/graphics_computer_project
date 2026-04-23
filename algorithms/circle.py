def draw_circle(surface, xc, yc, r, color):

    x = 0
    y = r
    p = 1 - r

    plot_circle(surface, xc, yc, x, y, color)

    while x < y:

        x += 1

        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x-y) + 1

        plot_circle(surface, xc, yc, x, y, color)


def plot_circle(surface, xc, yc, x, y, color):

    points = [
        (xc+x, yc+y),
        (xc-x, yc+y),
        (xc+x, yc-y),
        (xc-x, yc-y),
        (xc+y, yc+x),
        (xc-y, yc+x),
        (xc+y, yc-x),
        (xc-y, yc-x)
    ]

    for p in points:
        surface.set_at(p, color)