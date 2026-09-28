"""Verlet Integration Cloth & Spring-Mass Dynamics Engine.
100% Python Standard Library.
"""

import math

class VerletClothSimulation:
    """Verlet integration cloth simulation with distance constraints."""
    class Particle:
        def __init__(self, x, y, pinned=False):
            self.x = x
            self.y = y
            self.px = x
            self.py = y
            self.pinned = pinned

    def __init__(self, cols=4, rows=4, spacing=1.0):
        self.cols = cols
        self.rows = rows
        self.particles = []
        for r in range(rows):
            for c in range(cols):
                pinned = (r == 0 and (c == 0 or c == cols - 1))
                self.particles.append(self.Particle(c * spacing, r * spacing, pinned))

        self.constraints = []
        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                if c + 1 < cols:
                    self.constraints.append((idx, idx + 1, spacing))
                if r + 1 < rows:
                    self.constraints.append((idx, idx + cols, spacing))

    def step(self, dt=0.02, gravity=9.8, iterations=5):
        for p in self.particles:
            if not p.pinned:
                vx = p.x - p.px
                vy = p.y - p.py + gravity * dt * dt
                p.px = p.x
                p.py = p.y
                p.x += vx
                p.y += vy

        for _ in range(iterations):
            for i1, i2, rest in self.constraints:
                p1 = self.particles[i1]
                p2 = self.particles[i2]
                dx = p2.x - p1.x
                dy = p2.y - p1.y
                dist = math.hypot(dx, dy)
                if dist < 1e-12:
                    continue
                diff = (dist - rest) / dist
                if not p1.pinned and not p2.pinned:
                    p1.x += dx * 0.5 * diff
                    p1.y += dy * 0.5 * diff
                    p2.x -= dx * 0.5 * diff
                    p2.y -= dy * 0.5 * diff
                elif not p1.pinned:
                    p1.x += dx * diff
                    p1.y += dy * diff
                elif not p2.pinned:
                    p2.x -= dx * diff
                    p2.y -= dy * diff
