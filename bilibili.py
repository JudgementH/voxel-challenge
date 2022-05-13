from scene import Scene
import taichi as ti
from taichi.math import *

DAY = False
scene = Scene(voxel_edges=0, exposure=2 if DAY else 30)
scene.set_floor(height=-35 / 64, color=(1, 0.6, 0.8))

if DAY:
    scene.set_background_color((1, 0.5, 0.7))
    scene.set_directional_light((1, 2, 1), 0.2, (1, 1, 0.8))

BODY = vec3(0.6, 0.6, 0.6) if DAY else vec3(0.1, 0.1, 0.1)
LINE = vec3(0, 0, 0) if DAY else vec3(0, 0.4, 0.7)
DEBUG = vec3(1, 0, 0)


@ti.func
def ellipse(pos, thickness, a, b, c):
    for x, y, z in ti.ndrange((-a, a), (-b, b), (0, thickness)):
        p = vec3(x, y, z)
        if (x / a) ** 2 + (y / b) ** 2 <= 1:
            scene.set_voxel(pos + p, 1, c)


@ti.func
def cube(pos, l, h, w, c, mat=1, axis=vec3(0, 0, 1), angle=0):
    for x, y, z in ti.ndrange((-l // 2, l // 2), (-h // 2, h // 2), (0, w)):
        p = vec3(x, y, z)
        scene.set_voxel(pos + rotate3d(p, axis=axis, ang=radians(angle)), mat, c)


@ti.func
def rcube(pos, l, h, w, c, r, mat=1):
    for x, y, z in ti.ndrange((0, l), (0, h), (0, w)):
        p = vec3(x, y, z)
        if 0 <= y <= r and r - ti.sqrt(r ** 2 - (y - r) ** 2) <= x <= l - r + ti.sqrt(r ** 2 - (y - r) ** 2):
            scene.set_voxel(pos + p, mat, c)
        elif h - r <= y <= h and r - ti.sqrt(r ** 2 - (y - h + r) ** 2) <= x <= l - r + ti.sqrt(
                r ** 2 - (y - h + r) ** 2):
            scene.set_voxel(pos + p, mat, c)
        elif r < y < h - r:
            scene.set_voxel(pos + p, mat, c)


@ti.func
def draw_w(pos, thickness, h, d, t, c, mat=1):
    b = -2 * (h + ti.sqrt(h ** 2 - t * h)) / d
    a = b ** 2 / (4 * h)
    for x, y, z in ti.ndrange((-d + 1, d), (t - h - 1, t), (0, thickness)):
        p, x0, temp = vec3(x, y, z), abs(x), ti.sqrt(b ** 2 - 4 * a * (t - y))
        if a * x ** 2 + b * x0 + t - 2 <= y <= a * x ** 2 + b * x0 + t + 2:
            scene.set_voxel(pos + p, mat, c)


@ti.kernel
def initialize_voxels():
    ellipse(vec3(-20, -30, -20), 40, 3, 5, LINE)
    ellipse(vec3(20, -30, -20), 40, 3, 5, LINE)
    rcube(vec3(-45, -30, -20), 90, 60, 40, BODY, 10, 1)
    cube(vec3(0, 0, 20), 70, 50, 2, LINE, 1 if DAY else 2)
    cube(vec3(0, 0, 20), 66, 46, 2, LINE, 0)
    cube(vec3(13, 8, 20), 16, 4, 2, LINE, 1 if DAY else 2, angle=-20)  # right eye
    cube(vec3(-13, 9, 20), 16, 4, 2, LINE, 1 if DAY else 2, angle=20)  # left eye
    draw_w(vec3(0, -10, 20), 2, 7, 10, 3, LINE, 1 if DAY else 2)  # mouth
    cube(vec3(-10, 30, 0), 4, 40, 4, LINE, 1 if DAY else 2, angle=70)
    cube(vec3(10, 30, 0), 4, 40, 4, LINE, 1 if DAY else 2, angle=-50)


initialize_voxels()

scene.finish()
