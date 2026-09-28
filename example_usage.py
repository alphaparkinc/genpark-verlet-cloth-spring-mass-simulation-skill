from client import VerletClothSimulation

cloth = VerletClothSimulation(cols=4, rows=4, spacing=1.0)
print("Initial Center Particle Pos:", (cloth.particles[5].x, cloth.particles[5].y))
cloth.step(dt=0.02, gravity=9.8, iterations=10)
print("After Gravity Step:", (cloth.particles[5].x, cloth.particles[5].y))
