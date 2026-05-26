# BallisticsApp
App to make ballistic calculations based on user input.

## Kinetic Energy
One of the biggest determinants of a bullets penetration and effectiveness is its kinetic energy. We can calculate this by substituting the bullets weight and expected velocity into the kinetic energy equation:
$Ke = 1/2mv^2$

## Momentum
Momentum also plays a large part in the effectiveness of a round. In this case, rounds with higher momentum are less vulnerable to resistance from the material they are traveling through. We can calculate momentum by plugging in the bullets mass and expected velocity in to the momentum equation: 
$p = mv$

## External Ballistics 
**Gravity** and **Air Resistance** have a very strong impact on the flight of a bullet. As soon as a bullet leaves the barrel, air resistance begins to make the bullet lose velocity and gravity makes the bullet lose height. This results in a parabolic trajectory and flight. In fact, gravity and air resistance play such a part in the flight of the bullet that the bullets departure line is tangent to the trajectory of the bullet only at the muzzle. Immediately, the trajectory drops below the bore axis/departure line. The angle of departure is formed by the intersection of the line of departure and the horozontal line of sight "baseline". 

### Ballistic Coeffecient
Ballistic coeffectient
: a measure of a bullet's relative ability to overcome air resistance.
Each bullet can be assigned a numeric value that expresses this efficency. The main basis of this value is a ratio comparing the performance characteristics of a particular bullet against the known trajectory characteristics of a standard projectile. Specifically, this ratio compares the drag of a bullet (loss of velo caused by air resistance in flight) to the drag of the standard projectile. The formula is: BC = Drag of standard projectile / Drag of test projectile.

