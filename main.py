import pygame
from config import *

from algorithms.dda import draw_line_dda
from algorithms.bresenham import draw_line_bresenham
from algorithms.circle import draw_circle
from algorithms.cohen_sutherland import cohen_sutherland_clip

from transformations.rotate import (
    rotate_points,
    rotate_circles,
    rotate_rectangles,
    rotate_triangles
)
from transformations.scale import (
    scale_points,
    scale_circles,
    scale_rectangles,
    scale_triangles
)
from transformations.matrix import (
    apply_matrix,
    apply_matrix_circles,
    apply_matrix_rectangles,
    apply_matrix_triangles
)
from utils.grid import draw_grid

# ─── INIT ────────────────────────────────────────────────────────────────────
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Graphics Playground")

font     = pygame.font.SysFont(None, 20)
font_hud = pygame.font.SysFont("monospace", 18)

# Batas window/viewport untuk Cohen-Sutherland
WIN_XMIN = WINDOW_X
WIN_YMIN = WINDOW_Y
WIN_XMAX = WINDOW_X + WINDOW_W
WIN_YMAX = WINDOW_Y + WINDOW_H

# ─── STATE ───────────────────────────────────────────────────────────────────
points     = []
circles    = []
rectangles = []
triangles  = []

algorithm        = "dda"
clipping_enabled = True   # Toggle dengan tombol Q

running = True

# ─── MAIN LOOP ───────────────────────────────────────────────────────────────
while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ── Klik mouse: tambah titik ──────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            points.append((x, y))

        if event.type == pygame.KEYDOWN:

            # Pilih algoritma garis
            if event.key == pygame.K_1:
                algorithm = "dda"

            if event.key == pygame.K_2:
                algorithm = "bresenham"

            # Toggle clipping ON/OFF
            if event.key == pygame.K_q:
                clipping_enabled = not clipping_enabled

            # Tambah bentuk
            if event.key == pygame.K_c:          # Circle
                if len(points) >= 1:
                    x, y = points[-1]
                    circles.append((x, y, 50))

            if event.key == pygame.K_r:          # Rectangle
                if len(points) >= 2:
                    x1, y1 = points[-2]
                    x2, y2 = points[-1]
                    rectangles.append((x1, y1, x2, y2))

            if event.key == pygame.K_t:          # Triangle
                if len(points) >= 3:
                    p1 = points[-3]
                    p2 = points[-2]
                    p3 = points[-1]
                    triangles.append((p1, p2, p3))

            # ── TRANSLASI (Matrix Homogen) ────────────────────────────────
            if event.key == pygame.K_LEFT:
                matrix = [[1, 0, -10], [0, 1, 0], [0, 0, 1]]
                points     = apply_matrix(points, matrix)
                circles    = apply_matrix_circles(circles, matrix)
                rectangles = apply_matrix_rectangles(rectangles, matrix)
                triangles  = apply_matrix_triangles(triangles, matrix)

            if event.key == pygame.K_RIGHT:
                matrix = [[1, 0, 10], [0, 1, 0], [0, 0, 1]]
                points     = apply_matrix(points, matrix)
                circles    = apply_matrix_circles(circles, matrix)
                rectangles = apply_matrix_rectangles(rectangles, matrix)
                triangles  = apply_matrix_triangles(triangles, matrix)

            if event.key == pygame.K_UP:
                matrix = [[1, 0, 0], [0, 1, -10], [0, 0, 1]]
                points     = apply_matrix(points, matrix)
                circles    = apply_matrix_circles(circles, matrix)
                rectangles = apply_matrix_rectangles(rectangles, matrix)
                triangles  = apply_matrix_triangles(triangles, matrix)

            if event.key == pygame.K_DOWN:
                matrix = [[1, 0, 0], [0, 1, 10], [0, 0, 1]]
                points     = apply_matrix(points, matrix)
                circles    = apply_matrix_circles(circles, matrix)
                rectangles = apply_matrix_rectangles(rectangles, matrix)
                triangles  = apply_matrix_triangles(triangles, matrix)

            # ── ROTASI ────────────────────────────────────────────────────
            cx, cy = WIDTH // 2, HEIGHT // 2

            if event.key == pygame.K_a:
                points     = rotate_points(points, -10, cx, cy)
                circles    = rotate_circles(circles, -10, cx, cy)
                rectangles = rotate_rectangles(rectangles, -10, cx, cy)
                triangles  = rotate_triangles(triangles, -10, cx, cy)

            if event.key == pygame.K_d:
                points     = rotate_points(points, 10, cx, cy)
                circles    = rotate_circles(circles, 10, cx, cy)
                rectangles = rotate_rectangles(rectangles, 10, cx, cy)
                triangles  = rotate_triangles(triangles, 10, cx, cy)

            # ── SCALING ───────────────────────────────────────────────────
            if event.key == pygame.K_w:
                points     = scale_points(points, 1.1, 1.1, cx, cy)
                circles    = scale_circles(circles, 1.1, 1.1, cx, cy)
                rectangles = scale_rectangles(rectangles, 1.1, 1.1, cx, cy)
                triangles  = scale_triangles(triangles, 1.1, 1.1, cx, cy)

            if event.key == pygame.K_s:
                points     = scale_points(points, 0.9, 0.9, cx, cy)
                circles    = scale_circles(circles, 0.9, 0.9, cx, cy)
                rectangles = scale_rectangles(rectangles, 0.9, 0.9, cx, cy)
                triangles  = scale_triangles(triangles, 0.9, 0.9, cx, cy)

    # ═══════════════════════════════════════════════════════════════════════
    #  RENDER
    # ═══════════════════════════════════════════════════════════════════════
    screen.fill(BG_COLOR)
    draw_grid(screen)

    # ── Window / Viewport border ─────────────────────────────────────────
    window_rect = pygame.Rect(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
    pygame.draw.rect(screen, WINDOW_COLOR, window_rect, 2)

    # Label viewport
    label = font_hud.render("Viewport (Clipping Window)", True, WINDOW_COLOR)
    screen.blit(label, (WINDOW_X, WINDOW_Y - 22))

    # ── Circles ──────────────────────────────────────────────────────────
    if clipping_enabled:
        screen.set_clip(window_rect)
    for c in circles:
        draw_circle(screen, c[0], c[1], c[2], CIRCLE_COLOR)
    screen.set_clip(None)

    # ── Rectangles (Cohen-Sutherland per sisi) ───────────────────────────
    for r in rectangles:
        x1, y1, x2, y2 = r
        edges = [
            (x1, y1, x2, y1),   
            (x2, y1, x2, y2),   
            (x2, y2, x1, y2),   
            (x1, y2, x1, y1),  
        ]
        for edge in edges:
            if clipping_enabled:
                clipped = cohen_sutherland_clip(
                    *edge, WIN_XMIN, WIN_YMIN, WIN_XMAX, WIN_YMAX
                )
                if clipped:
                    pygame.draw.line(screen, RECTANGLE_COLOR,
                                     clipped[:2], clipped[2:])
            else:
                pygame.draw.line(screen, RECTANGLE_COLOR,
                                 edge[:2], edge[2:])

    # ── Triangles (Cohen-Sutherland per sisi) ────────────────────────────
    for t in triangles:
        p1, p2, p3 = t
        edges = [(*p1, *p2), (*p2, *p3), (*p3, *p1)]
        for edge in edges:
            if clipping_enabled:
                clipped = cohen_sutherland_clip(
                    *edge, WIN_XMIN, WIN_YMIN, WIN_XMAX, WIN_YMAX
                )
                if clipped:
                    pygame.draw.line(screen, TRIANGLE_COLOR,
                                     clipped[:2], clipped[2:])
            else:
                pygame.draw.line(screen, TRIANGLE_COLOR,
                                 edge[:2], edge[2:])

    # ── Points ───────────────────────────────────────────────────────────
    for p in points:
        pygame.draw.circle(screen, POINT_COLOR, p, 4)
        text = font.render(f"{p}", True, POINT_COLOR)
        screen.blit(text, (p[0] + 5, p[1] - 5))

    # ── Garis (Cohen-Sutherland → DDA / Bresenham) ───────────────────────
    if len(points) >= 2:
        x1, y1 = points[-2]
        x2, y2 = points[-1]

        if clipping_enabled:
            # Terapkan Cohen-Sutherland sebelum menggambar
            clipped = cohen_sutherland_clip(
                x1, y1, x2, y2, WIN_XMIN, WIN_YMIN, WIN_XMAX, WIN_YMAX
            )
            if clipped:
                cx1, cy1, cx2, cy2 = clipped
                if algorithm == "dda":
                    draw_line_dda(screen, cx1, cy1, cx2, cy2, LINE_DDA_COLOR)
                else:
                    draw_line_bresenham(screen, cx1, cy1, cx2, cy2, LINE_BRESENHAM_COLOR)
        else:
            if algorithm == "dda":
                draw_line_dda(screen, x1, y1, x2, y2, LINE_DDA_COLOR)
            else:
                draw_line_bresenham(screen, x1, y1, x2, y2, LINE_BRESENHAM_COLOR)

    # ── HUD (informasi kontrol) ───────────────────────────────────────────
    clip_status = "ON  [Cohen-Sutherland]" if clipping_enabled else "OFF"
    clip_color  = (80, 255, 140) if clipping_enabled else (255, 100, 100)

    hud = [
        (f"Algoritma : {'DDA' if algorithm == 'dda' else 'Bresenham'}  [1=DDA / 2=Bresenham]", (200, 200, 200)),
        (f"Clipping  : {clip_status}  [Q]",                                                      clip_color),
        ("Shapes    : [C] Circle   [R] Rectangle   [T] Triangle",                                (200, 200, 200)),
        ("Transform : [A/D] Rotasi   [W/S] Scale   [Arrow] Translasi",                           (200, 200, 200)),
    ]
    for i, (line, color) in enumerate(hud):
        surf = font_hud.render(line, True, color)
        screen.blit(surf, (10, 10 + i * 22))

    pygame.display.update()

pygame.quit()