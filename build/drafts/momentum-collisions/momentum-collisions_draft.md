# Chapter: Center of Mass, Momentum, and Collisions

**Template**: `MECHANICS`  
**Prerequisites**: vectors-and-coordinate-systems, differential-calculus-foundations, integral-calculus-foundations, kinematics, laws-of-motion, work-energy-power  

## Learning Objectives
- Compute the center of mass for discrete multi-particle systems and continuous symmetric bodies using integral calculus.
- Apply negative mass superposition to calculate shifts in the center of mass for bodies with hollow cavities.
- Master Newton's Second Law for systems of particles M A_cm = F_net,ext and analyze motion in the center of mass reference frame.
- Formulate the Impulse-Momentum Theorem J_net = Delta p and differentiate impulsive from non-impulsive forces.
- Apply the Principle of Conservation of Linear Momentum to isolated systems, explosions, gun recoil, and unconstrained coordinate axes.
- Derive reactive thrust forces and the Tsiolkovsky rocket equation for variable-mass flight.
- Analyze 1D elastic and inelastic collisions using Newton's experimental law of restitution e = v_sep / v_app.
- Calculate mechanical energy dissipation in inelastic impacts and analyze ballistic pendulums.
- Decompose 2D oblique collisions into line of impact and common tangential components, proving the 90 degree scattering angle for identical elastic spheres.

---

## Center of Mass Calculation and System Dynamics

> **Pedagogical Goal**: Establish discrete and continuous center of mass definitions, master negative mass cavity superposition, prove Newton's second law for a system of particles, and analyze zero-external-force internal displacements.


---

### Concept: Center of Mass of Discrete Particle Systems

**Definition**: 

**Physical Significance**: 


---

### Concept: Continuous Mass Distributions and Standard Geometries

**Definition**: 

**Physical Significance**: 


---

### Concept: Motion of Center of Mass and System Newton's Law

**Definition**: 

**Physical Significance**: 


---

### Concept: Superposition, Negative Mass, and Relative Displacement

**Definition**: 

**Physical Significance**: 


---

### Formula: Discrete Center of Mass Position Vector

**Governing Equation**:
$$ \vec{R}_{\text{cm}} = \frac{\sum_{i=1}^N m_i \vec{r}_i}{\sum_{i=1}^N m_i} = \frac{1}{M} \sum_{i=1}^N m_i \vec{r}_i $$

**Variable Inventory & SI Units**:
- $\vec{R}_{\text{cm}}$: Center of mass position vector (Unit: `m` | Dim: `[L]`)
- $m_i$: Mass of individual particle i (Unit: `kg` | Dim: `[M]`)
- $\vec{r}_i$: Position vector of individual particle i (Unit: `m` | Dim: `[L]`)
- $M$: Total system mass (Unit: `kg` | Dim: `[M]`)

**Physical Assumptions**:
- Classical point particles
- Flat Euclidean space

**Domain of Validity**:
- Valid in any coordinate system


---

### Formula: Continuous Center of Mass Integral

**Governing Equation**:
$$ \vec{R}_{\text{cm}} = \frac{1}{M} \int_{\text{body}} \vec{r} \, dm $$

**Variable Inventory & SI Units**:
- $\vec{R}_{\text{cm}}$: Center of mass position vector (Unit: `m` | Dim: `[L]`)
- $M$: Total mass of continuous body (Unit: `kg` | Dim: `[M]`)
- $\vec{r}$: Position vector of differential mass element (Unit: `m` | Dim: `[L]`)
- $dm$: Differential mass element (\rho dV, \sigma dA, or \lambda dl) (Unit: `kg` | Dim: `[M]`)

**Physical Assumptions**:
- Continuous rigid mass distribution
- Well-defined density function

**Domain of Validity**:
- Riemann integrable mass density across domain


---

### Formula: Center of Mass of Solid Uniform Hemisphere

**Governing Equation**:
$$ y_{\text{cm}} = \frac{3}{8} R $$

**Variable Inventory & SI Units**:
- $y_{\text{cm}}$: Distance of center of mass from flat base along symmetry axis (Unit: `m` | Dim: `[L]`)
- $R$: Radius of uniform solid hemisphere (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Uniform volumetric mass density \rho
- Perfect hemispherical geometry

**Domain of Validity**:
- Measured from flat circular base along normal symmetry axis


---

### Derivation: Formula `formula-mom-com-hemisphere`

**Target Governing Relation**:
$$ y_{\text{cm}} = \frac{\rho \pi \frac{R^4}{4}}{\rho \frac{2}{3} \pi R^3} = \frac{\frac{1}{4}}{\frac{2}{3}} R = \frac{3}{8} R $$

#### Step-by-Step Proof
**Step 1**: Due to rotational symmetry about the y-axis, the center of mass must lie along the symmetry axis.
$$  $$
*Physical Operation*: 

**Step 2**: Slice the hemisphere into thin circular horizontal discs of thickness dy at vertical elevation y with disc radius r.
$$  $$
*Physical Operation*: 

**Step 3**: Set up the numerator first moment of mass integral from y = 0 (base) to y = R (apex).
$$  $$
*Physical Operation*: 

**Step 4**: Evaluate the elementary polynomial definite integral.
$$  $$
*Physical Operation*: 

**Step 5**: Express total mass M in terms of density rho and total volume.
$$  $$
*Physical Operation*: 

**Step 6**: Divide the first moment by total mass to arrive at the final centroid coordinate y_cm = 3R/8.
$$  $$
*Physical Operation*: 

**Dimensional Homogeneity**: Dimension of 3/8 R is [L], matching distance units.


---

### Formula: Center of Mass of Solid Uniform Right Circular Cone

**Governing Equation**:
$$ y_{\text{cm}} = \frac{1}{4} h $$

**Variable Inventory & SI Units**:
- $y_{\text{cm}}$: Distance of center of mass from flat base along central height axis (Unit: `m` | Dim: `[L]`)
- $h$: Total vertical height of cone (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Uniform volumetric density
- Right circular cone geometry

**Domain of Validity**:
- Measured from base along symmetry axis toward vertex


---

### Formula: Center of Mass of Body with Cavity (Negative Mass Superposition)

**Governing Equation**:
$$ \vec{r}_{\text{rem}} = \frac{M \vec{r}_{\text{orig}} - m_{\text{cav}} \vec{r}_{\text{cav}}}{M - m_{\text{cav}}} $$

**Variable Inventory & SI Units**:
- $\vec{r}_{\text{rem}}$: Center of mass position vector of remaining body with cavity
- $M$: Mass of original complete body without cavity (Unit: `kg` | Dim: `[M]`)
- $\vec{r}_{\text{orig}}$: Center of mass position vector of original complete body
- $m_{\text{cav}}$: Mass of removed material filling cavity (Unit: `kg` | Dim: `[M]`)
- $\vec{r}_{\text{cav}}$: Center of mass position vector of removed cavity portion

**Physical Assumptions**:
- Uniform density throughout original body and cavity region
- Well-defined cavity geometry

**Domain of Validity**:
- Applicable to planar laminas, 3D solids, and regular geometries


---

### Formula: Center of Mass Velocity and System Linear Momentum

**Governing Equation**:
$$ \vec{V}_{\text{cm}} = \frac{\sum m_i \vec{v}_i}{M} = \frac{\vec{P}}{M} $$

**Variable Inventory & SI Units**:
- $\vec{V}_{\text{cm}}$: Velocity vector of system center of mass (Unit: `m/s` | Dim: `[L][T]^-1`)
- $m_i$: Mass of individual particle i
- $\vec{v}_i$: Velocity vector of individual particle i (Unit: `m/s`)
- $M$: Total system mass (Unit: `kg` | Dim: `[M]`)
- $\vec{P}$: Total linear momentum of system (Unit: `kg m/s` | Dim: `[M][L][T]^-1`)

**Physical Assumptions**:
- Non-relativistic mechanics
- Constant mass particles

**Domain of Validity**:
- Valid in any inertial or non-inertial reference frame


---

### Formula: Newton's Second Law for Center of Mass

**Governing Equation**:
$$ M \vec{A}_{\text{cm}} = \vec{F}_{\text{net, ext}} $$

**Variable Inventory & SI Units**:
- $M$: Total mass of system (Unit: `kg` | Dim: `[M]`)
- $\vec{A}_{\text{cm}}$: Acceleration vector of center of mass (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $\vec{F}_{\text{net, ext}}$: Vector sum of all external forces acting on system (Unit: `N`)

**Physical Assumptions**:
- Inertial reference frame
- Internal forces obey Newton's Third Law in strong form

**Domain of Validity**:
- Valid for closed systems of arbitrary internal complexity


---

### Worked Pedagogical Example: `ex-mom-disc-cavity-01`

**Problem Statement**:
> A uniform circular disc of radius $R$ and total initial mass $M$ has a circular hole of radius $R/2$ cut out from it. The hole is positioned such that its circumference touches the outer rim of the disc and also passes through the center of the original disc. Find the center of mass of the remaining portion relative to the center of the uncut disc.

**Target Quantity**: `x_rem`

#### Systematic Solution
**Step 1 ()**:
$$ m_{\text{cav}} = \sigma \pi \left(\frac{R}{2}\right)^2 = \frac{1}{4} \sigma \pi R^2 = \frac{M}{4} $$

Result: ``

**Step 2 ()**:
$$ (x_{\text{orig}}, y_{\text{orig}}) = (0, 0), \quad (x_{\text{cav}}, y_{\text{cav}}) = \left(\frac{R}{2}, 0\right) $$

Result: ``

**Step 3 ()**:
$$ x_{\text{rem}} = \frac{M x_{\text{orig}} - m_{\text{cav}} x_{\text{cav}}}{M - m_{\text{cav}}} = \frac{M(0) - \left(\frac{M}{4}\right)\left(\frac{R}{2}\right)}{M - \frac{M}{4}} = \frac{-\frac{M R}{8}}{\frac{3 M}{4}} = -\frac{R}{6} $$

Result: ``

**Step 4 ()**:
$$ y_{\text{rem}} = 0 $$

Result: ``

**Final Answer**: (x_{\text{rem}}, y_{\text{rem}}) = \left(-\frac{R}{6}, 0\right)

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Adding the cavity mass in the denominator instead of subtracting
> - Assuming the remaining mass is 3M/4 but taking hole centroid at R rather than R/2

**Sanity & Consistency Checks**:
- Removing mass from the right side (+x) must shift the remaining center of mass to the left (-x).
- |-R/6| = 0.167 R < R/2, which lies well within the remaining solid material.


---

### Worked Pedagogical Example: `ex-mom-man-plank-01`

**Problem Statement**:
> A man of mass $m = 60\text{ kg}$ stands at one end of a uniform wooden plank of mass $M = 140\text{ kg}$ and length $L = 4.0\text{ m}$ resting on a frictionless horizontal frozen lake. The man walks from one end of the plank to the other end. Find the displacement of the plank relative to the frozen lake.

**Target Quantity**: `Delta_X_plank`

#### Systematic Solution
**Step 1 ()**:
$$ \Delta x_p = -\Delta X $$

Result: ``

**Step 2 ()**:
$$ \Delta x_m = L + \Delta x_p = L - \Delta X $$

Result: ``

**Step 3 ()**:
$$ m (L - \Delta X) + M (-\Delta X) = 0 \implies m L - (m + M) \Delta X = 0 $$

Result: ``

**Step 4 ()**:
$$ \Delta X = \frac{m L}{m + M} = \frac{(60)(4.0)}{60 + 140} = \frac{240}{200} = 1.20\text{ m} $$

Result: ``

**Final Answer**: \Delta X_{\text{plank}} = 1.20\text{ m} \quad (\text{in direction opposite to man's walk})

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Assuming the man travels distance L relative to the ground
> - Forgetting that the plank also moves, so man ground displacement is L - Delta X = 2.8 m

**Sanity & Consistency Checks**:
- Displacement ratio: |Delta x_p / Delta x_m| = 1.2 / 2.8 = 3/7 = 60/140 = m/M, exactly satisfying inverse mass ratio.
- If M -> infinity, plank displacement approaches zero as expected.


---

### Inoculation Against Misconception: `misc-mom-01`

**Misconception Category**: `WRONG_CONSERVATION_LAW`  
**Erroneous Intuition**: *"Internal explosions, collisions, or internal muscular forces can accelerate the system center of mass."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students observe fragments flying out violently in an explosion and intuitively assume the center of mass must have been propelled in some direction.

**Physical Truth & Resolution**:
Newton's Third Law guarantees that all internal forces occur in equal and opposite collinear action-reaction pairs whose vector sum vanishes identically: sum(F_int) = 0. Therefore, the center of mass acceleration is governed solely by external forces: M A_cm = F_net,ext. An artillery shell in parabolic flight that bursts into pieces in mid-air continues to have its center of mass follow the exact same parabolic trajectory until fragments experience external forces such as ground impact.

**Refutation Counterexample & Supporting Evidence**:
An exploding bomb on a frictionless floor at rest will have fragments scatter in all directions, but sum(m_i v_i) = 0 and the center of mass remains perfectly motionless at the origin.

**Diagnostic Symptom**: M \vec{A}_{\text{cm}} = \vec{F}_{\text{net, ext}} \implies \vec{A}_{\text{cm}} = \vec{0} \quad \text{whenever } \vec{F}_{\text{net, ext}} = \vec{0}, \text{ regardless of internal explosive forces.}


---

### Verified JEE Practice Problem: `center-of-mass-question-e38050cc`

**Type**: `SINGLE_CORRECT_MCQ`  
**Provenance Source**: `Audited Source / Question Bank`  

> A circular plate of uniform thickness and mass $M$ has radius $R$. A circular hole of radius $R/2$ is cut out from it, touching the outer circumference of the plate. Taking the origin at the center of the original uncut plate, and the center of the cut hole at $(R/2, 0)$, the coordinates of the center of mass of the remaining portion are:

**Options**:
- **(A)**: $\left(-\frac{R}{6}, 0\right)$
- **(B)**: $\left(-\frac{R}{4}, 0\right)$
- **(C)**: $\left(-\frac{R}{8}, 0\right)$
- **(D)**: $\left(-\frac{R}{3}, 0\right)$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `cvr-q-mom-01`

</details>


---

## Linear Momentum and the Impulse-Momentum Theorem

> **Pedagogical Goal**: Define system linear momentum as total mass times center of mass velocity, establish the vector impulse integral, and formulate the Impulse-Momentum Theorem distinguishing impulsive from non-impulsive interactions.


---

### Concept: System Linear Momentum and Reference Frames

**Definition**: 

**Physical Significance**: 


---

### Concept: Impulse Vector and Impulse-Momentum Theorem

**Definition**: 

**Physical Significance**: 


---

### Concept: Impulsive vs Non-Impulsive Forces

**Definition**: 

**Physical Significance**: 


---

### Formula: System Linear Momentum Vector

**Governing Equation**:
$$ \vec{P} = \sum_{i=1}^N m_i \vec{v}_i = M \vec{V}_{\text{cm}} $$

**Variable Inventory & SI Units**:
- $\vec{P}$: Total system linear momentum vector (Unit: `kg m/s` | Dim: `[M][L][T]^-1`)
- $M$: Total system mass (Unit: `kg` | Dim: `[M]`)
- $\vec{V}_{\text{cm}}$: Velocity of system center of mass (Unit: `m/s` | Dim: `[L][T]^-1`)

**Physical Assumptions**:
- Classical mechanics
- Summation over all system components

**Domain of Validity**:
- Universal definition of linear momentum for particle systems


---

### Formula: Impulse Vector Definite Integral

**Governing Equation**:
$$ \vec{J} = \int_{t_1}^{t_2} \vec{F}(t) \, dt $$

**Variable Inventory & SI Units**:
- $\vec{J}$: Impulse vector (Unit: `N s` | Dim: `[M][L][T]^-1`)
- $\vec{F}(t)$: Time-dependent force vector
- $t_1, t_2$: Initial and final times of force interaction

**Physical Assumptions**:
- Riemann integrable force function over finite time interval

**Domain of Validity**:
- Valid for all forces (constant, piecewise, or continuous impulse)


---

### Formula: Impulse-Momentum Theorem

**Governing Equation**:
$$ \vec{J}_{\text{net}} = \Delta\vec{p} = \vec{p}_f - \vec{p}_i = m \vec{v}_f - m \vec{v}_i $$

**Variable Inventory & SI Units**:
- $\vec{J}_{\text{net}}$: Net impulse vector delivered to particle (Unit: `N s`)
- $\Delta\vec{p}$: Change in linear momentum vector (Unit: `kg m/s` | Dim: `[M][L][T]^-1`)
- $m$: Mass of particle (Unit: `kg`)
- $\vec{v}_i, \vec{v}_f$: Initial and final velocity vectors

**Physical Assumptions**:
- Inertial reference frame
- Constant particle mass during impulse

**Domain of Validity**:
- Universal theorem relating force time-integral to velocity changes


---

### Worked Pedagogical Example: `ex-mom-ball-wall-impulse-01`

**Problem Statement**:
> A rubber ball of mass $m = 0.25\text{ kg}$ moving at speed $u = 20.0\text{ m/s}$ strikes a rigid vertical wall at an angle of incidence $\theta = 30.0^\circ$ to the normal. It rebounds elastically with the same speed and angle. The contact duration is $\Delta t = 0.010\text{ s}$. Find the average force exerted by the wall on the ball.

**Target Quantity**: `F_avg`

#### Systematic Solution
**Step 1 ()**:
$$ \vec{u} = -u \cos\theta \hat{i} + u \sin\theta \hat{j} = -(20.0 \cos 30^\circ) \hat{i} + (20.0 \sin 30^\circ) \hat{j} = -10\sqrt{3} \hat{i} + 10 \hat{j}\text{ m/s} $$

Result: ``

**Step 2 ()**:
$$ \vec{v} = +u \cos\theta \hat{i} + u \sin\theta \hat{j} = +10\sqrt{3} \hat{i} + 10 \hat{j}\text{ m/s} $$

Result: ``

**Step 3 ()**:
$$ \Delta\vec{p} = m(\vec{v} - \vec{u}) = m(2 u \cos\theta \hat{i}) = (0.25)(2 \times 20.0 \times \cos 30^\circ) \hat{i} = (0.25)(40.0 \times 0.866) \hat{i} = 8.66 \hat{i}\text{ N s} $$

Result: ``

**Step 4 ()**:
$$ \vec{F}_{\text{avg}} = \frac{\Delta\vec{p}}{\Delta t} = \frac{8.66 \hat{i}}{0.010} = 866 \hat{i}\text{ N} $$

Result: ``

**Final Answer**: F_{\text{avg}} = 866\text{ N} \quad (\text{normal to the wall})

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Using speed difference u - v = 0 instead of vector change 2 u cos(theta)
> - Using sin(theta) instead of cos(theta) when angle is defined with respect to the normal

**Sanity & Consistency Checks**:
- Tangential force is identically zero since wall is smooth and tangential velocity is unchanged.
- Impulse magnitude 8.66 N s produces sensible force 866 N over 10 ms impact.


---

### Inoculation Against Misconception: `misc-mom-03`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"Impulse is a scalar quantity equal to the magnitude of force multiplied by elapsed time."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students treat impulse J = F Delta t as a simple scalar product of numbers, ignoring directional sign reversals during rebounds.

**Physical Truth & Resolution**:
Impulse is a VECTOR integral: vec(J) = int vec(F) dt = Delta vec(p). In a 1D rebound where a ball of mass m strikes a wall with velocity +u and rebounds at -u, the momentum change is NOT zero, but m(-u) - m(+u) = -2mu. The impulse magnitude is 2mu, twice as large as that for a ball that sticks to the wall.

**Refutation Counterexample & Supporting Evidence**:
A ball of mass 1 kg hitting a wall at 10 m/s and bouncing back at 10 m/s experiences impulse Delta p = (-10) - (+10) = -20 kg m/s. Treating impulse as scalar speed difference yields 10 - 10 = 0, which is catastrophically false.

**Diagnostic Symptom**: \vec{J} = \Delta\vec{p} = m \vec{v}_f - m \vec{v}_i \neq m |v_f| - m |v_i|.


---

## Conservation of Linear Momentum and Variable Mass Systems

> **Pedagogical Goal**: Formulate the universal Principle of Conservation of Linear Momentum along isolated coordinate axes, analyze explosive recoil dynamics, and derive variable-mass reactive thrust and Tsiolkovsky rocket flight.


---

### Concept: Conservation of Linear Momentum in Isolated Systems

**Definition**: 

**Physical Significance**: 


---

### Concept: Explosion, Gun Recoil, and Internal Explosive Energy

**Definition**: 

**Physical Significance**: 


---

### Concept: Mechanics of Systems with Varying Mass

**Definition**: 

**Physical Significance**: 


---

### Formula: Principle of Conservation of Linear Momentum

**Governing Equation**:
$$ \vec{P}_{\text{initial}} = \vec{P}_{\text{final}} \quad \text{when} \quad \vec{F}_{\text{net, ext}} = \vec{0} $$

**Variable Inventory & SI Units**:
- $\vec{P}_{\text{initial}}$: Total initial linear momentum vector
- $\vec{P}_{\text{final}}$: Total final linear momentum vector
- $\vec{F}_{\text{net, ext}}$: Net external force acting on system

**Physical Assumptions**:
- Isolated system (zero net external force)
- Holds along any coordinate axis where external force component vanishes

**Domain of Validity**:
- Universal physical conservation law in classical mechanics


---

### Formula: Recoil Velocity of Gun in 1D Firing

**Governing Equation**:
$$ \vec{V}_{\text{gun}} = -\frac{m}{M} \vec{v}_{\text{bullet}} $$

**Variable Inventory & SI Units**:
- $\vec{V}_{\text{gun}}$: Recoil velocity vector of gun
- $M$: Mass of gun (Unit: `kg` | Dim: `[M]`)
- $m$: Mass of bullet (Unit: `kg` | Dim: `[M]`)
- $\vec{v}_{\text{bullet}}$: Muzzle velocity vector of bullet relative to ground

**Physical Assumptions**:
- Gun and bullet initially at rest
- Zero horizontal external forces during explosion

**Domain of Validity**:
- Bullet velocity measured in ground inertial frame


---

### Formula: Reactive Thrust Force on Variable Mass System

**Governing Equation**:
$$ \vec{F}_{\text{thrust}} = \vec{v}_{\text{rel}} \frac{dm}{dt} $$

**Variable Inventory & SI Units**:
- $\vec{F}_{\text{thrust}}$: Reactive thrust force vector exerted on body
- $\vec{v}_{\text{rel}}$: Velocity of ejected mass relative to body (Unit: `m/s`)
- $\frac{dm}{dt}$: Time rate of change of body mass (negative for ejection) (Unit: `kg/s` | Dim: `[M][T]^-1`)

**Physical Assumptions**:
- Continuous mass ejection/adcretion
- Exhaust gases do not interact back on body

**Domain of Validity**:
- General reactive propulsion equation for rockets, jets, and conveyors


---

### Formula: Tsiolkovsky Rocket Equation under Gravity

**Governing Equation**:
$$ v(t) = v_0 + u_{\text{ex}} \ln\left(\frac{m_0}{m(t)}\right) - g t $$

**Variable Inventory & SI Units**:
- $v(t)$: Rocket instantaneous vertical velocity at time t
- $v_0$: Initial launch velocity
- $u_{\text{ex}}$: Constant relative exhaust speed of expelled gas (Unit: `m/s` | Dim: `[L][T]^-1`)
- $m_0$: Initial gross mass of rocket with fuel
- $m(t)$: Instantaneous mass of rocket at time t
- $g$: Uniform acceleration due to gravity (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $t$: Burn time duration (Unit: `s` | Dim: `[T]`)

**Physical Assumptions**:
- Constant exhaust speed u_ex relative to rocket
- Constant downward gravitational field g
- Negligible aerodynamic drag

**Domain of Validity**:
- Valid during powered burn phase t <= t_burnout


---

### Worked Pedagogical Example: `ex-mom-rocket-vertical-climb-01`

**Problem Statement**:
> A sounding rocket of initial gross mass $m_0 = 1000\text{ kg}$ is launched vertically upward from rest. Fuel is consumed at a constant rate of $\mu = 20.0\text{ kg/s}$ with a constant relative exhaust speed of $u_{\text{ex}} = 1500\text{ m/s}$. The total fuel mass is $800\text{ kg}$. Taking $g = 9.80\text{ m/s}^2$ and neglecting air drag, find the rocket velocity at fuel burnout.

**Target Quantity**: `v_burnout`

#### Systematic Solution
**Step 1 ()**:
$$ t_b = \frac{m_{\text{fuel}}}{\mu} = \frac{800}{20.0} = 40.0\text{ s}, \quad m_b = m_0 - m_{\text{fuel}} = 1000 - 800 = 200\text{ kg} $$

Result: ``

**Step 2 ()**:
$$ \frac{m_0}{m_b} = \frac{1000}{200} = 5.0, \quad \ln(5.0) \approx 1.6094 $$

Result: ``

**Step 3 ()**:
$$ \Delta v_{\text{thrust}} = (1500)(1.6094) = 2414.1\text{ m/s} $$

Result: ``

**Step 4 ()**:
$$ \Delta v_{\text{grav}} = (9.80)(40.0) = 392.0\text{ m/s} $$

Result: ``

**Step 5 ()**:
$$ v_b = 0 + 2414.1 - 392.0 = 2022.1\text{ m/s} \approx 2022\text{ m/s} $$

Result: ``

**Final Answer**: v_{\text{burnout}} \approx 2022\text{ m/s} = 2.02\text{ km/s}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Omitting the gravity term g * t_b
> - Calculating acceleration at t=0 and multiplying by t_b (acceleration increases dramatically as mass decreases!)

**Sanity & Consistency Checks**:
- Initial acceleration a_0 = (u_ex mu / m_0) - g = (1500 * 20 / 1000) - 9.8 = 30 - 9.8 = 20.2 m/s^2 > 0 (rocket lifts off cleanly).
- Final acceleration a_b = (30000 / 200) - 9.8 = 150 - 9.8 = 140.2 m/s^2.


---

### Inoculation Against Misconception: `misc-mom-02`

**Misconception Category**: `WRONG_CONSERVATION_LAW`  
**Erroneous Intuition**: *"Linear momentum is conserved only if mechanical kinetic energy is also conserved."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students conflate the conservation of momentum with the conservation of mechanical energy, assuming that any loss of kinetic energy invalidates momentum conservation.

**Physical Truth & Resolution**:
Conservation of linear momentum depends SOLELY on the condition that net external force is zero (F_net,ext = 0). It does not depend on whether the collision is elastic or inelastic! In completely inelastic collisions, explosions, or sticky impacts, kinetic energy is drastically altered, but linear momentum is 100% conserved.

**Refutation Counterexample & Supporting Evidence**:
A bullet embedding into a wooden block at rest loses over 99% of its kinetic energy to thermal dissipation and wood deformation, yet total horizontal linear momentum before and after impact is exactly identical.

**Diagnostic Symptom**: \Delta\vec{P} = \int \vec{F}_{\text{ext}} \, dt = \vec{0} \quad \text{holds even when } \Delta K \neq 0.


---

### Inoculation Against Misconception: `misc-mom-05`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"Applying F = m a directly to variable mass systems by treating (dm/dt) * v as an ordinary external force."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Differentiating p = m v as dp/dt = m (dv/dt) + v (dm/dt) and setting it equal to external force F_ext.

**Physical Truth & Resolution**:
The expression dp/dt = m dv/dt + v dm/dt is NOT Galilean invariant when mass crosses the system boundary! The velocity of the expelled or admitted mass must be measured RELATIVE to the moving body: F_ext + v_rel (dm/dt) = m dv/dt. Using ground velocity instead of relative exhaust velocity violates Galilean relativity.

**Refutation Counterexample & Supporting Evidence**:
In an inertial frame moving at constant velocity V, the ground velocity of rocket and exhaust changes by V, but the physical acceleration of the rocket must be identical in all inertial frames.

**Diagnostic Symptom**: m(t) \frac{d\vec{v}}{dt} = \vec{F}_{\text{ext}} + \vec{v}_{\text{rel}} \frac{dm}{dt} \quad \text{is Galilean invariant, whereas } \vec{F}_{\text{ext}} = m \frac{d\vec{v}}{dt} + \vec{v} \frac{dm}{dt} \text{ is not.}


---

## Collisions in One and Two Dimensions

> **Pedagogical Goal**: Classify elastic and inelastic impact dynamics, define Newton's restitution coefficient along the line of impact, derive head-on velocity expressions and kinetic energy dissipation, analyze ballistic pendulums, and decompose 2D oblique collisions.


---

### Concept: Classification of Collisions (Elastic, Inelastic, Perfectly Inelastic)

**Definition**: 

**Physical Significance**: 


---

### Concept: Newton's Coefficient of Restitution

**Definition**: 

**Physical Significance**: 


---

### Concept: One-Dimensional Head-On Elastic Collisions

**Definition**: 

**Physical Significance**: 


---

### Concept: Mechanical Energy Dissipation in Inelastic Collisions

**Definition**: 

**Physical Significance**: 


---

### Concept: Completely Inelastic Collisions and Ballistic Pendulum

**Definition**: 

**Physical Significance**: 


---

### Concept: Two-Dimensional Oblique Collisions and Line of Impact

**Definition**: 

**Physical Significance**: 


---

### Formula: Post-Collision Velocity v1 in 1D Head-on Elastic Collision

**Governing Equation**:
$$ v_1 = \left(\frac{m_1 - m_2}{m_1 + m_2}\right) u_1 + \left(\frac{2 m_2}{m_1 + m_2}\right) u_2 $$

**Variable Inventory & SI Units**:
- $v_1$: Final velocity of mass 1 after elastic collision (Unit: `m/s` | Dim: `[L][T]^-1`)
- $u_1, u_2$: Initial velocities of masses 1 and 2 before collision
- $m_1, m_2$: Masses of colliding spheres

**Physical Assumptions**:
- Head-on 1D motion
- Perfect elasticity (e = 1)
- Zero external impulsive forces

**Domain of Validity**:
- Valid for any mass ratio m1/m2 and initial velocities u1, u2


---

### Formula: Post-Collision Velocity v2 in 1D Head-on Elastic Collision

**Governing Equation**:
$$ v_2 = \left(\frac{2 m_1}{m_1 + m_2}\right) u_1 + \left(\frac{m_2 - m_1}{m_1 + m_2}\right) u_2 $$

**Variable Inventory & SI Units**:
- $v_2$: Final velocity of mass 2 after elastic collision (Unit: `m/s` | Dim: `[L][T]^-1`)
- $u_1, u_2$: Initial velocities of masses 1 and 2 before collision
- $m_1, m_2$: Masses of colliding spheres

**Physical Assumptions**:
- Head-on 1D motion
- Perfect elasticity (e = 1)
- Zero external impulsive forces

**Domain of Validity**:
- Valid for all classical point spheres colliding head-on elastically


---

### Formula: Newton's Coefficient of Restitution Definition

**Governing Equation**:
$$ e = \frac{v_2 - v_1}{u_1 - u_2} = \frac{v_{\text{sep}}}{v_{\text{app}}} $$

**Variable Inventory & SI Units**:
- $e$: Dimensionless coefficient of restitution (Unit: `dimensionless` | Dim: `[1]`)
- $v_1, v_2$: Final velocities along line of impact
- $u_1, u_2$: Initial velocities along line of impact

**Physical Assumptions**:
- Velocities measured strictly along the common normal (line of impact)

**Domain of Validity**:
- 0 <= e <= 1 for passive materials


---

### Formula: Kinetic Energy Loss in 1D Inelastic Collision

**Governing Equation**:
$$ \Delta K = \frac{1}{2} \left(\frac{m_1 m_2}{m_1 + m_2}\right) (1 - e^2) (u_1 - u_2)^2 $$

**Variable Inventory & SI Units**:
- $\Delta K$: Loss in mechanical kinetic energy during collision (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $m_1, m_2$: Masses of colliding bodies
- $e$: Coefficient of restitution (Unit: `dimensionless` | Dim: `[1]`)
- $u_1, u_2$: Initial velocities along line of collision

**Physical Assumptions**:
- 1D collision or head-on impact along common normal
- Zero external work

**Domain of Validity**:
- Valid for all 0 <= e <= 1


---

### Derivation: Formula `formula-mom-inelastic-energy-loss`

**Target Governing Relation**:
$$ \Delta K = K_i - K_f = \frac{1}{2} \mu (u_1 - u_2)^2 - \frac{1}{2} \mu e^2 (u_1 - u_2)^2 = \frac{1}{2} \left(\frac{m_1 m_2}{m_1 + m_2}\right) (1 - e^2) (u_1 - u_2)^2 $$

#### Step-by-Step Proof
**Step 1**: Express total kinetic energy as sum of center of mass kinetic energy and relative kinetic energy (two-body reduced mass theorem).
$$  $$
*Physical Operation*: 

**Step 2**: Initial kinetic energy before collision.
$$  $$
*Physical Operation*: 

**Step 3**: Final kinetic energy after collision. Because momentum is conserved, V_cm is unchanged.
$$  $$
*Physical Operation*: 

**Step 4**: Substitute Newton's coefficient of restitution for relative separation speed.
$$  $$
*Physical Operation*: 

**Step 5**: Express final kinetic energy in terms of initial relative velocity and e.
$$  $$
*Physical Operation*: 

**Step 6**: Subtract final kinetic energy from initial to find the dissipated energy Delta K.
$$  $$
*Physical Operation*: 

**Dimensional Homogeneity**: Dimensions of mu u^2 are [M][L]^2[T]^-2 (Energy, Joules).


---

### Formula: Oblique Collision Rebound Angle and Velocity Relations

**Governing Equation**:
$$ \tan\beta = e \tan\alpha, \quad v_t = u_t, \quad v_n = e u_n $$

**Variable Inventory & SI Units**:
- $\beta$: Angle of rebound with common normal (Unit: `rad` | Dim: `[1]`)
- $\alpha$: Angle of incidence with common normal (Unit: `rad` | Dim: `[1]`)
- $e$: Coefficient of restitution (Unit: `dimensionless` | Dim: `[1]`)
- $v_t, u_t$: Tangential velocities before and after impact
- $v_n, u_n$: Normal velocities before and after impact

**Physical Assumptions**:
- Smooth colliding surfaces (zero tangential friction)
- Line of impact along common normal

**Domain of Validity**:
- Valid for oblique impact against stationary smooth barrier or sphere


---

### Worked Pedagogical Example: `ex-mom-elastic-target-masses-01`

**Problem Statement**:
> In a nuclear reactor moderator, a fast neutron of mass $m_1 = 1.0\text{ u}$ moving with speed $u$ undergoes a head-on elastic collision with a stationary moderator nucleus of mass $m_2$ at rest ($u_2 = 0$). Calculate the fractional kinetic energy retained by the neutron when the moderator nucleus is: (a) a hydrogen nucleus ($m_2 = 1.0\text{ u}$), and (b) a carbon nucleus ($m_2 = 12.0\text{ u}$).

**Target Quantity**: `K_f / K_i`

#### Systematic Solution
**Step 1 ()**:
$$ v_1 = \left(\frac{m_1 - m_2}{m_1 + m_2}\right) u $$

Result: ``

**Step 2 ()**:
$$ \frac{K_f}{K_i} = \frac{\frac{1}{2} m_1 v_1^2}{\frac{1}{2} m_1 u^2} = \left(\frac{v_1}{u}\right)^2 = \left(\frac{m_1 - m_2}{m_1 + m_2}\right)^2 $$

Result: ``

**Step 3 ()**:
$$ \frac{K_f}{K_i} = \left(\frac{1.0 - 1.0}{1.0 + 1.0}\right)^2 = 0.0 \quad (0\% \text{ retained, } 100\% \text{ transferred}) $$

Result: ``

**Step 4 ()**:
$$ \frac{K_f}{K_i} = \left(\frac{1.0 - 12.0}{1.0 + 12.0}\right)^2 = \left(-\frac{11.0}{13.0}\right)^2 = \frac{121}{169} \approx 0.716 \quad (71.6\% \text{ retained, } 28.4\% \text{ transferred}) $$

Result: ``

**Final Answer**: (a) Hydrogen: 0.0 (100\% transferred); (b) Carbon: 121/169 approx 71.6\% retained

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Forgetting to square the velocity ratio to obtain kinetic energy ratio
> - Assuming heavy nuclei absorb more energy (heavier targets cause elastic rebounds with minimal energy transfer!)

**Sanity & Consistency Checks**:
- Energy transfer fraction is 4 m1 m2 / (m1 + m2)^2; for m1=m2=1, 4(1)(1)/(2)^2 = 1.0. For carbon: 4(1)(12)/(13)^2 = 48/169 = 0.284.
- Sum of retained + transferred = 121/169 + 48/169 = 169/169 = 1.0 identically.


---

### Worked Pedagogical Example: `ex-mom-ballistic-pendulum-01`

**Problem Statement**:
> A rifle bullet of mass $m = 10.0\text{ g} = 0.010\text{ kg}$ is fired horizontally with speed $u$ into a large wooden block of mass $M = 3.99\text{ kg}$ suspended by light vertical cords as a ballistic pendulum. The bullet comes to rest inside the block in an extremely short time. The block and embedded bullet then swing upward, reaching a maximum vertical height $h = 5.0\text{ cm} = 0.050\text{ m}$. Find the initial speed $u$ of the bullet. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `u`

#### Systematic Solution
**Step 1 ()**:
$$ m u = (M + m) V \implies V = \frac{m u}{M + m} $$

Result: ``

**Step 2 ()**:
$$ \frac{1}{2}(M + m) V^2 = (M + m) g h \implies V = \sqrt{2 g h} $$

Result: ``

**Step 3 ()**:
$$ V = \sqrt{2 \times 9.8 \times 0.050} = \sqrt{0.98} = 0.9899\text{ m/s} $$

Result: ``

**Step 4 ()**:
$$ u = \left(\frac{M + m}{m}\right) V = \left(\frac{3.99 + 0.010}{0.010}\right)(0.9899) = \left(\frac{4.00}{0.010}\right)(0.9899) = 400 \times 0.9899 \approx 396\text{ m/s} $$

Result: ``

**Final Answer**: u \approx 396\text{ m/s}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Attempting to conserve kinetic energy from the bullet to the swing apex (enormous energy is dissipated as heat during embedding!)
> - Omitting the bullet mass m in the composite pendulum mass M + m

**Sanity & Consistency Checks**:
- Initial kinetic energy of bullet = 1/2 (0.010) (396)^2 = 784 J.
- Kinetic energy of block+bullet = 1/2 (4.00) (0.99)^2 = 1.96 J (over 99.7% of initial energy dissipated into wood deformation and heat).


---

### Worked Pedagogical Example: `ex-mom-oblique-two-disc-01`

**Problem Statement**:
> Two identical smooth billiard balls A and B of mass $m$ and radius $R$ lie on a smooth horizontal table. Ball B is initially at rest. Ball A moves with initial velocity $\vec{u}_1 = u_0 \hat{i}$ with impact parameter $b = R$ (the distance between their initial parallel velocity line and the center of B). The collision is perfectly elastic ($e = 1$). Find the velocity vectors of both balls after the collision.

**Target Quantity**: `vec_v_A, vec_v_B`

#### Systematic Solution
**Step 1 ()**:
$$ \sin\theta = \frac{b}{2R} = \frac{R}{2R} = \frac{1}{2} \implies \theta = 30.0^\circ, \quad \cos\theta = \frac{\sqrt{3}}{2} $$

Result: ``

**Step 2 ()**:
$$ u_{1n} = u_0 \cos 30^\circ = \frac{\sqrt{3}}{2} u_0, \quad u_{1t} = u_0 \sin 30^\circ = \frac{1}{2} u_0 $$

Result: ``

**Step 3 ()**:
$$ v_{1t} = u_{1t} = \frac{1}{2} u_0, \quad v_{2t} = 0 $$

Result: ``

**Step 4 ()**:
$$ v_{1n} = u_{2n} = 0, \quad v_{2n} = u_{1n} = \frac{\sqrt{3}}{2} u_0 $$

Result: ``

**Step 5 ()**:
$$ v_A = \sqrt{v_{1n}^2 + v_{1t}^2} = \frac{1}{2} u_0, \quad v_B = \sqrt{v_{2n}^2 + v_{2t}^2} = \frac{\sqrt{3}}{2} u_0 $$

Result: ``

**Final Answer**: v_A = \frac{1}{2} u_0 \quad (\text{along tangent}), \quad v_B = \frac{\sqrt{3}}{2} u_0 \quad (\text{along line of centers})

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Forgetting that center-to-center distance at impact is 2R, not R
> - Assuming normal velocities don't exchange for equal masses

**Sanity & Consistency Checks**:
- Total final kinetic energy = 1/2 m (u0/2)^2 + 1/2 m (sqrt(3)/2 u0)^2 = 1/2 m u0^2 (1/4 + 3/4) = 1/2 m u0^2 = K_i (exact energy conservation).
- Scattering angle: vec(v)_A is along tangent and vec(v)_B is along normal, which are perpendicular (scattering angle exactly 90 degrees!).


---

### Inoculation Against Misconception: `misc-mom-04`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"The coefficient of restitution applies to velocity magnitudes in any arbitrary coordinate direction."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students take total speed after collision divided by total speed before collision in 2D problems.

**Physical Truth & Resolution**:
Newton's experimental law of restitution e = v_sep / v_app is defined STRICTLY along the line of impact (the common normal perpendicular to the contact surface at the point of collision). Velocities tangential to the contact interface are completely unaffected by restitution and remain invariant if the surfaces are frictionless.

**Refutation Counterexample & Supporting Evidence**:
A ball striking a smooth floor at 45 degrees with e = 0.5 only has its vertical normal velocity reduced by factor 0.5. Its horizontal tangential velocity is completely unchanged.

**Diagnostic Symptom**: e = \frac{v_{2n} - v_{1n}}{u_{1n} - u_{2n}} \quad \text{applies strictly along } \hat{n}, \text{ while } v_{1t} = u_{1t} \text{ along } \hat{t}.


---

### Inoculation Against Misconception: `misc-mom-06`

**Misconception Category**: `SIGN_MISTAKE`  
**Erroneous Intuition**: *"In oblique collision with a smooth flat wall, the tangential velocity component is reduced or reverses direction."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students treat the whole velocity vector as rebounding rather than decomposing into normal and tangential components.

**Physical Truth & Resolution**:
For a smooth surface, the contact force acts strictly normal to the surface (N hat(j)). There is zero friction force parallel to the surface (F_tangential = 0). Therefore, the impulse along the tangent is zero: J_t = 0. The tangential momentum and tangential velocity component are strictly conserved: v_t = u_t.

**Refutation Counterexample & Supporting Evidence**:
A billiard ball hitting a smooth cushion at angle alpha rebounds at angle beta where tan(beta) = tan(alpha)/e. The horizontal velocity along the rail is identical before and after impact.

**Diagnostic Symptom**: J_t = \int F_t \, dt = 0 \implies v_t = u_t.


---

### Verified JEE Practice Problem: `center-of-mass-question-ba1b4107`

**Type**: `SINGLE_CORRECT_MCQ`  
**Provenance Source**: `Audited Source / Question Bank`  

> A smooth sphere of mass $m_1$ moving with initial speed $u$ collides head-on with a stationary smooth sphere of mass $m_2$. If the coefficient of restitution between the spheres is $e$, the fraction of the initial kinetic energy lost during the collision, $\frac{\Delta K}{K_i}$, is:

**Options**:
- **(A)**: $\frac{m_2}{m_1 + m_2}(1 - e^2)$
- **(B)**: $\frac{m_1}{m_1 + m_2}(1 - e^2)$
- **(C)**: $\frac{m_1 m_2}{(m_1 + m_2)^2}(1 - e)$
- **(D)**: $\frac{m_2}{m_1 + m_2}(1 - e)$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `cvr-q-mom-02`

</details>


---

## Chapter Summary & Formula Recap: Center of Mass, Momentum, and Collisions

### Core Equations & Domains of Validity
- **formula-mom-com-discrete**: $$$$
  *Validity*: General
- **formula-mom-com-continuous**: $$$$
  *Validity*: General
- **formula-mom-com-hemisphere**: $$$$
  *Validity*: General
- **formula-mom-com-cone**: $$$$
  *Validity*: General
- **formula-mom-com-cavity**: $$$$
  *Validity*: General
- **formula-mom-com-velocity**: $$$$
  *Validity*: General
- **formula-mom-com-acceleration**: $$$$
  *Validity*: General
- **formula-mom-momentum-vector**: $$$$
  *Validity*: General
- **formula-mom-impulse-integral**: $$$$
  *Validity*: General
- **formula-mom-impulse-momentum-thm**: $$$$
  *Validity*: General
- **formula-mom-conservation**: $$$$
  *Validity*: General
- **formula-mom-recoil-velocity**: $$$$
  *Validity*: General
- **formula-mom-rocket-thrust**: $$$$
  *Validity*: General
- **formula-mom-rocket-tsiolkovsky**: $$$$
  *Validity*: General
- **formula-mom-elastic-1d-v1**: $$$$
  *Validity*: General
- **formula-mom-elastic-1d-v2**: $$$$
  *Validity*: General
- **formula-mom-restitution-def**: $$$$
  *Validity*: General
- **formula-mom-inelastic-energy-loss**: $$$$
  *Validity*: General
- **formula-mom-oblique-angle-rebound**: $$$$
  *Validity*: General
