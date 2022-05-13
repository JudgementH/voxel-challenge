from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(voxel_edges=0, exposure=2.0)
scene.set_floor(height=0, color=(13 / 255, 48 / 255, 72 / 255))
# scene.set_floor(height=-1 / 64, color=(1, 1, 1))
scene.set_background_color((20 / 255, 50 / 255, 70 / 255))
scene.set_directional_light((0, 0, -1), 0.1, (70 / 255, 120 / 255, 120 / 255))


@ti.kernel
def initialize_voxels():
    center = vec3(0, 0, 0)
    scene.set_voxel(vec3(0, 0, 0), 2, color=vec3(1, 0, 0))
    radius = 30
    moon_blue = vec3(70 / 255, 120 / 255, 120 / 255)
    for x, y, z in ti.ndrange((-radius, radius), (-radius, radius), (-radius, radius)):
        p = ivec3(x, y, z)
        if distance(p, center) <= radius:
            scene.set_voxel(p, 2, color=moon_blue)


initialize_voxels()

scene.finish()
