# genpark-verlet-cloth-spring-mass-simulation-skill

Agent Skill implementing **Position-Based Verlet Integration Cloth Dynamics** with structural distance constraints and pinned boundary conditions.

## Architectural Overview
```mermaid
flowchart TD
    Grid["2D Particle Grid (x, px)"] --> Ext["External Acceleration (Gravity: g * dt^2)"]
    Ext --> Verlet["Verlet Integration: x_new = 2x - px + a * dt^2"]
    Verlet --> Relax["Iterative Distance Constraint Relaxation"]
    Relax --> Anchors["Preserve Pinned Corner Positions"]
```
