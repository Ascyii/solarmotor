"""Alle gemessenen Koordinaten der Quelle und der Sonne haben den Ursprung in der linken unteren Ecke des Clusters in einem rechtshaendigen flachen System.
"""

import math

class MovingEntity:
    """Embedded entity in the world with a position."""

    def __init__(self, world):
        self.world = world
        self.pos = (0.0, 0.0, 0.0)  # (x, y, z) in local untilted coordinates

    def get_pos_rotated(self):
        """Return position rotated by world's tilt around y-axis."""
        return self.world.rotate_point_y(self.pos)

class Target(MovingEntity):
    def __init__(self, world, pos=(0.0, 0.0, 0.0)):
        super().__init__(world)
        self.pos = pos

class Source(MovingEntity):
    def __init__(self, world, pos=(10.0, 10.0, 10.0)):
        super().__init__(world)
        self.pos = pos

class Mirror:
    def __init__(self, world, cluster_x=0, cluster_y=0):
        self.world = world
        self.cluster_x = cluster_x
        self.cluster_y = cluster_y
        self.angle_x = 0.0
        self.angle_y = 0.0

        # Position in un-tilted coordinate system
        self.pos = (cluster_x * self.world.grid_size,
                    cluster_y * self.world.grid_size,
                    0.0)

    def get_pos_rotated(self):
        return self.world.rotate_point_y(self.pos)

    def set_angle_from_source_target(self, source: Source, target: Target):
        # Get rotated positions
        pos_mirror = self.get_pos_rotated()
        pos_source = source.get_pos_rotated()
        pos_target = target.get_pos_rotated()

        v_source = (
            pos_source[0] - pos_mirror[0],
            pos_source[1] - pos_mirror[1],
            pos_source[2] - pos_mirror[2],
        )
        v_target = (
            pos_target[0] - pos_mirror[0],
            pos_target[1] - pos_mirror[1],
            pos_target[2] - pos_mirror[2],
        )

        def normalize(v):
            length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
            if length == 0:
                return (0, 0, 0)
            return (v[0] / length, v[1] / length, v[2] / length)

        v_source_n = normalize(v_source)
        v_target_n = normalize(v_target)

        mirror_normal = (
            v_source_n[0] + v_target_n[0],
            v_source_n[1] + v_target_n[1],
            v_source_n[2] + v_target_n[2],
        )
        mirror_normal = normalize(mirror_normal)

        # Update the angles based on the normals in rotated positions
        self.angle_y = math.degrees(math.atan2(mirror_normal[0], mirror_normal[2]))
        self.angle_x = math.degrees(math.atan2(mirror_normal[1], mirror_normal[2]))

    def get_angles(self):
        return self.angle_x, self.angle_y

class World:
    def __init__(self, tilt_deg=0.0):
        self.grid_size = 10  # In cm
        self.tilt_deg = tilt_deg  # Tilt of the grid system around y-axis
        self.mirrors = []

    def add_mirror(self, mirror):
        self.mirrors.append(mirror)

    def update_mirrors_from_source_target(self, source: Source, target: Target):
        for mirror in self.mirrors:
            mirror.set_angle_from_source_target(source, target)

    def rotate_point_y(self, point):
        """Rotate a point around the y-axis by the world's tilt angle."""
        x, y, z = point
        theta = math.radians(self.tilt_deg)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)
        x_rot = x * cos_t + z * sin_t
        y_rot = y
        z_rot = -x * sin_t + z * cos_t
        return (x_rot, y_rot, z_rot)
