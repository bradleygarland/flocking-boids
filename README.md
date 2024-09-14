# Flocking Boids

---

## Summary
This repository is an attempt at a simulation of an artificial life called boids, created by Craig Reynolds in 1986.
The simulation is meant to mimic the flocking behavior of birds, and their related motions within groups. The name "boid" 
corresponds to a shortened version of "bird-oid object", which refers to a bird-like object.

Take a look at the full summary of Craig Reynold's development of boids: [Wikipedia/Boids](https://en.wikipedia.org/wiki/Boids)

## Simulation Detail
The simulation follows a set of three main principles:
1. Separation
2. Alignment
3. Cohesion
---
## Separation
Separation in boids refers to the redirection of a boid away from a density of boids to make sure that there is no
overcrowding. In this simulation, a boid in the separation process takes the position vectors of every nearby boid
 object and nudges the velocity a direction opposite to the masses.

## Alignment
Alignment refers to the process where a boid object will redirect its velocity to match the average of the neighboring
 boid objects, therefore, it will take the velocity vector of every nearby boid object and take the average and make an
impulse in its own acceleration in the direction of the average.

## Cohesion
Cohesion works as an opposite to the separation process, where separation makes the boids repel and cohesion makes the
 boid objects attract in order to maintain a viscous state between a mass of objects. This makes sure that there is an
actual flocking behavior instead of the boids flying in random motions throughout the screen.

---
# Notes
Unfortunately, at the time of the last pull request, this program is written in a naive method which is far from being
in a well optimized state. There is an abundance of looping iteration statements that cause delay in the program making
the limit on particles and boids a low quantity.

# TODO

---

- Add an aspect of flocking density, flock speed normal, max boids, boid grouping
- Add user interaction with the boids, including boid attraction to mouse and the ability to place an object
- Add pathfinding for any user placed objects previous