# Chapter: Work, Energy & Power

**Template**: `MECHANICS`  
**Prerequisites**: units-and-measurements, vectors-and-coordinate-systems, differential-calculus-foundations, integral-calculus-foundations, kinematics, laws-of-motion  

## Learning Objectives
- Calculate work done by constant, variable, spring, and frictional forces using scalar products and line integrals.
- Master the Work-Energy Theorem in both inertial and accelerating non-inertial reference frames.
- Distinguish conservative from non-conservative forces using path-independence and closed-loop criteria.
- Determine conservative force vectors from potential energy gradient fields F = -grad(U).
- Analyze potential energy curves U(x) to locate turning points and evaluate equilibrium stability.
- Apply the conservation of total mechanical energy and formulate energy balance under dissipative non-conservative forces.
- Calculate average and instantaneous power delivered by machines and force fields.
- Derive critical looping velocities and string slackening dynamics in vertical circular motion.

---

## Work Done by Constant and Variable Forces

> **Pedagogical Goal**: Establish the foundational scalar definition of mechanical work, evaluate line integrals for position-dependent forces, derive spring work, and examine friction work across reference frames.


---

### Concept: Work Done by a Constant Force and Scalar Product

**Definition**: The work $W$ done on a particle by a constant force $\vec{F}$ undergoing displacement $\Delta\vec{r}$ is defined as the scalar (dot) product: $W = \vec{F} \cdot \Delta\vec{r} = |\vec{F}| |\Delta\vec{r}| \cos\theta = F_x \Delta x + F_y \Delta y + F_z \Delta z$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Constant force vector over displacement
- Point mass particle or translation without internal distortion


---

### Concept: Work Done by a Variable Force and Path Line Integrals

**Definition**: For a force $\vec{F}(\vec{r})$ varying with position, work done along path $C$ from $\vec{r}_i$ to $\vec{r}_f$ is the Riemann line integral: $W = \int_C \vec{F}(\vec{r}) \cdot d\vec{r} = \int_{x_i}^{x_f} F_x dx + \int_{y_i}^{y_f} F_y dy + \int_{z_i}^{z_f} F_z dz$. In 1D, work equals the signed geometric area under the $F_x(x)$ curve.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Piecewise continuous force vector field
- Well-defined piecewise smooth curve $C$


---

### Concept: Work Done by an Ideal Spring and Hooke's Law

**Definition**: An ideal massless spring exerts restoring force $F_s(x) = -k x$ proportional to elongation $x$ from natural length. The work done BY the spring when displaced from $x_i$ to $x_f$ is $W_s = \int_{x_i}^{x_f} (-kx) dx = -\frac{1}{2} k (x_f^2 - x_i^2)$. The work done BY an external agent stretching the spring quasi-statically is $W_{\text{ext}} = +\frac{1}{2} k (x_f^2 - x_i^2)$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Ideal massless spring
- Linear elastic Hooke's regime (no plastic deformation)


---

### Concept: Work Done by Friction and Interfacial Dissipation

**Definition**: Static friction does zero work in the rest frame of the contact surface, but can do positive or negative work in other reference frames. Kinetic friction dissipative work between two sliding surfaces is strictly negative: $W_{\text{diss}} = -f_k s_{\text{rel}} = -\mu_k N s_{\text{rel}}$, transforming organized macroscopic kinetic energy into internal thermal energy.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Amontons-Coulomb friction model
- Rigid contact interface


---

### Formula: Work Done by a Constant Force

**Governing Equation**:
$$ W = \vec{F} \cdot \vec{d} = F d \cos\theta = F_x d_x + F_y d_y + F_z d_z $$

**Variable Inventory & SI Units**:
- $W$: Mechanical work done (Unit: `J (N m)` | Dim: `[M][L]^2[T]^-2`)
- $\vec{F}$: Constant force vector (Unit: `N` | Dim: `[M][L][T]^-2`)
- $\vec{d}$: Displacement vector (Unit: `m` | Dim: `[L]`)
- $\theta$: Angle between force and displacement vectors (Unit: `rad` | Dim: `[1]`)

**Physical Assumptions**:
- Force is constant in magnitude and direction throughout displacement

**Domain of Validity**:
- Point particle or translation without rotation


---

### Formula: Work Done by a Variable Force

**Governing Equation**:
$$ W = \int_{\vec{r}_i}^{\vec{r}_f} \vec{F}(\vec{r}) \cdot d\vec{r} = \int_{x_i}^{x_f} F_x \, dx + \int_{y_i}^{y_f} F_y \, dy + \int_{z_i}^{z_f} F_z \, dz $$

**Variable Inventory & SI Units**:
- $W$: Work done along trajectory (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $\vec{F}(\vec{r})$: Position-dependent force field
- $d\vec{r}$: Infinitesimal displacement element vector (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Force is integrable along piecewise smooth trajectory curve

**Domain of Validity**:
- Universal for 1D, 2D, and 3D classical particle motion


---

### Formula: Work Done by an Ideal Spring

**Governing Equation**:
$$ W_s = -\frac{1}{2} k (x_f^2 - x_i^2) $$

**Variable Inventory & SI Units**:
- $W_s$: Work done BY the spring (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $k$: Spring stiffness constant (Unit: `N/m (kg s^-2)` | Dim: `[M][T]^-2`)
- $x_i$: Initial deformation from natural length
- $x_f$: Final deformation from natural length

**Physical Assumptions**:
- Massless spring obeying Hooke's law F = -kx
- Deformation measured from unstretched length

**Domain of Validity**:
- Within elastic limit of spring material


---

### Derivation: Formula `formula-wep-work-spring`

**Target Governing Relation**:
$$ W_s = -\frac{1}{2} k (x_f^2 - x_i^2) $$

#### Step-by-Step Proof
**Step 1**: 
$$ dW_s = F_s(x) \, dx = (-kx) \, dx $$
*Physical Operation*: 

**Step 2**: 
$$ W_s = \int_{x_i}^{x_f} (-kx) \, dx = -k \int_{x_i}^{x_f} x \, dx $$
*Physical Operation*: 

**Step 3**: 
$$ W_s = -k \left[ \frac{x^2}{2} \right]_{x_i}^{x_f} = -\frac{1}{2} k (x_f^2 - x_i^2) $$
*Physical Operation*: 


---

### Formula: Work Done by Kinetic Friction

**Governing Equation**:
$$ W_{f_k} = -f_k s_{\text{rel}} = -\mu_k N s_{\text{rel}} $$

**Variable Inventory & SI Units**:
- $W_{f_k}$: Dissipative interfacial work of kinetic friction
- $\mu_k$: Coefficient of kinetic friction (Unit: `dimensionless` | Dim: `[1]`)
- $N$: Normal contact reaction force (Unit: `N` | Dim: `[M][L][T]^-2`)
- $s_{\text{rel}}$: Relative sliding displacement distance between contacting surfaces

**Physical Assumptions**:
- Constant normal force along sliding distance
- Constant coefficient mu_k

**Domain of Validity**:
- Dry sliding contact obeying Amontons-Coulomb law


---

### Worked Pedagogical Example: `ex-wep-spring-compress-01`

**Problem Statement**:
> A block of mass $m = 2.0\text{ kg}$ is released with speed $v_0 = 4.0\text{ m/s}$ on a rough horizontal floor with kinetic friction coefficient $\mu_k = 0.20$. After traveling distance $d = 2.0\text{ m}$, it collides with an uncompressed horizontal spring of spring constant $k = 400\text{ N/m}$ fixed to a rigid wall. Find the maximum compression $x_{\text{max}}$ of the spring. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `x_max`

#### Systematic Solution
**Step 1 ()**:
$$ K_i = \frac{1}{2} m v_0^2 = \frac{1}{2}(2.0)(4.0)^2 = 16.0\text{ J}, \quad K_f = 0 $$

Result: ``

**Step 2 ()**:
$$ W_{\text{net}} = W_{f_k} + W_s = -\mu_k m g (d + x_{\text{max}}) - \frac{1}{2} k x_{\text{max}}^2 $$

Result: ``

**Step 3 ()**:
$$ -(0.20)(2.0)(9.8)(2.0 + x_{\text{max}}) - \frac{1}{2}(400) x_{\text{max}}^2 = -16.0 \implies 3.92(2.0 + x_{\text{max}}) + 200 x_{\text{max}}^2 = 16.0 $$

Result: ``

**Step 4 ()**:
$$ x_{\text{max}} = \frac{-3.92 + \sqrt{3.92^2 - 4(200)(-8.16)}}{2(200)} = \frac{-3.92 + \sqrt{15.3664 + 6528}}{400} = \frac{-3.92 + 80.89}{400} \approx 0.192\text{ m} = 19.2\text{ cm} $$

Result: ``

**Final Answer**: x_{\text{max}} \approx 0.192\text{ m} = 19.2\text{ cm}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Forgetting that friction continues to act during the spring compression phase x_max
> - Omitting kinetic energy at spring contact

**Sanity & Consistency Checks**:
- Total energy dissipated by friction is 3.92 * 2.192 = 8.59 J, spring stores 1/2 * 400 * (0.192)^2 = 7.37 J, sum = 15.96 J approx 16.0 J
- x_max must be strictly positive


---

### Inoculation Against Misconception: `misc-wep-01`

**Misconception Category**: `SIGN_MISTAKE`  
**Erroneous Intuition**: *"Friction always does negative work on every body it acts upon."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students assume friction always opposes motion, and therefore the angle between force and displacement is always 180 deg, making work negative.

**Physical Truth & Resolution**:
Friction opposes RELATIVE motion at the contact interface, not necessarily motion relative to the ground. Static friction can do positive, negative, or zero work depending on the reference frame. For a crate sitting on the flatbed of an accelerating truck, static friction accelerates the crate forward in the direction of ground displacement, doing POSITIVE work.

**Refutation Counterexample & Supporting Evidence**:
A box of mass m rests on a flatbed truck accelerating at a = 2 m/s^2 over d = 10 m. Static friction f_s = ma = 2m N acts forward. Work done by static friction on the box is W = f_s d = +20m J > 0, which supplies the box's kinetic energy increase.

**Diagnostic Symptom**: W_{\text{static}} = \vec{f}_s \cdot \vec{d} > 0 \quad \text{when static friction accelerates a body in the direction of displacement.}


---

### Inoculation Against Misconception: `misc-wep-02`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"The normal reaction force never does mechanical work on any object."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students overgeneralize from horizontal sliding (where normal force is perpendicular to horizontal displacement) to believe normal force work is universally zero.

**Physical Truth & Resolution**:
Normal force is strictly perpendicular to the contact interface, but the interface itself may be moving! When a person stands in an elevator accelerating upward, the normal force on their feet is parallel to the upward displacement, performing positive work W = N d > 0.

**Refutation Counterexample & Supporting Evidence**:
In an elevator accelerating upward through height h with acceleration a, the floor exerts upward normal force N = m(g + a). Displacement is upward d = h. Work done by normal force is W_N = m(g + a)h > 0.

**Diagnostic Symptom**: W_N = \vec{N} \cdot \Delta\vec{r} \neq 0 \quad \text{whenever the contact interface has a non-zero velocity component along the normal.}


---

## Kinetic Energy and the Work-Energy Theorem

> **Pedagogical Goal**: Define kinetic energy from first principles, prove the Work-Energy Theorem for general curved 3D paths, extend it to non-inertial accelerating frames, and analyze internal force work in deformable systems.


---

### Concept: Kinetic Energy of a Translating Particle

**Definition**: Kinetic energy $K$ is the scalar capacity of a particle of mass $m$ to perform work due to its motion: $K = \frac{1}{2} m v^2 = \frac{p^2}{2m}$, where $\vec{p} = m\vec{v}$ is linear momentum. $K \ge 0$ is strictly non-negative in any inertial frame.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Point mass particle or non-rotating rigid body
- Classical non-relativistic speed ($v \ll c$)


---

### Concept: Work-Energy Theorem in Inertial Frames

**Definition**: The total work $W_{\text{net}}$ done by ALL forces (conservative, non-conservative, internal, and external) acting on a particle equals the change in its kinetic energy: $W_{\text{net}} = \sum W_i = \Delta K = K_f - K_i = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Inertial frame of reference
- Newton's Second Law $\vec{F}_{\text{net}} = m \vec{a}$ holds


---

### Concept: Work-Energy Theorem in Non-Inertial Reference Frames

**Definition**: In a frame translating with acceleration $\vec{a}_0$, the work-energy theorem remains valid provided the work of pseudo-forces $W_{\text{pseudo}} = \int (-m \vec{a}_0) \cdot d\vec{r}_{\text{rel}}$ is included: $W_{\text{real}} + W_{\text{pseudo}} = \Delta K_{\text{rel}} = \frac{1}{2} m v_{f,\text{rel}}^2 - \frac{1}{2} m v_{i,\text{rel}}^2$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Purely translating reference frame with known acceleration $\vec{a}_0(t)$
- Non-relativistic relative velocity


---

### Concept: Work Done by Internal Forces in Multi-Body Systems

**Definition**: For a multi-particle system, internal forces satisfy Newton's Third Law $\vec{F}_{ij} = -\vec{F}_{ji}$. However, the net internal work is $W_{\text{int}} = \int \vec{F}_{ij} \cdot d(\vec{r}_i - \vec{r}_j) = \int \vec{F}_{ij} \cdot d\vec{r}_{ij}$. For rigid bodies $d|\vec{r}_{ij}| = 0$ so $W_{\text{int}} = 0$; for deformable or sliding systems (e.g. springs, friction), $W_{\text{int}} \neq 0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Mutual central pair forces obeying Newton's Third Law


---

### Formula: Kinetic Energy of a Particle

**Governing Equation**:
$$ K = \frac{1}{2} m v^2 = \frac{p^2}{2m} $$

**Variable Inventory & SI Units**:
- $K$: Kinetic energy (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $m$: Inertial mass (Unit: `kg` | Dim: `[M]`)
- $v$: Speed magnitude in reference frame (Unit: `m/s` | Dim: `[L][T]^-1`)
- $p$: Magnitude of linear momentum (Unit: `kg m/s` | Dim: `[M][L][T]^-1`)

**Physical Assumptions**:
- Classical non-relativistic speed v << c
- Point mass or pure translation

**Domain of Validity**:
- Universal scalar definition in classical mechanics


---

### Formula: Work-Energy Theorem in Inertial Frame

**Governing Equation**:
$$ W_{\text{net}} = \Delta K = K_f - K_i = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2 $$

**Variable Inventory & SI Units**:
- $W_{\text{net}}$: Total net work done by all forces
- $\Delta K$: Change in kinetic energy
- $m$: Mass of particle (Unit: `kg`)
- $v_i$: Initial speed
- $v_f$: Final speed

**Physical Assumptions**:
- Inertial frame of reference
- Newton's Second Law holds

**Domain of Validity**:
- Valid for all forces including conservative, non-conservative, variable, internal, and external


---

### Derivation: Formula `formula-wep-work-energy-theorem`

**Target Governing Relation**:
$$ W_{\text{net}} = \Delta K = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2 $$

#### Step-by-Step Proof
**Step 1**: 
$$ W_{\text{net}} = \int_{\vec{r}_i}^{\vec{r}_f} \vec{F}_{\text{net}} \cdot d\vec{r} = \int_{t_i}^{t_f} m \frac{d\vec{v}}{dt} \cdot \frac{d\vec{r}}{dt} \, dt $$
*Physical Operation*: 

**Step 2**: 
$$ W_{\text{net}} = \int_{t_i}^{t_f} m \frac{d\vec{v}}{dt} \cdot \vec{v} \, dt = m \int_{\vec{v}_i}^{\vec{v}_f} \vec{v} \cdot d\vec{v} $$
*Physical Operation*: 

**Step 3**: 
$$ W_{\text{net}} = m \int_{v_i}^{v_f} v \, dv = m \left[ \frac{v^2}{2} \right]_{v_i}^{v_f} = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2 = \Delta K $$
*Physical Operation*: 


---

### Formula: Work-Energy Theorem in Non-Inertial Reference Frame

**Governing Equation**:
$$ W_{\text{real}} + W_{\text{pseudo}} = \Delta K_{\text{rel}} $$

**Variable Inventory & SI Units**:
- $W_{\text{real}}$: Work done by all physical forces along relative displacement
- $W_{\text{pseudo}}$: Work done by fictitious inertial pseudo-force int (-m a_0) . dr_rel
- $\Delta K_{\text{rel}}$: Change in kinetic energy evaluated in the accelerating frame

**Physical Assumptions**:
- Translating frame of reference with linear acceleration a_0

**Domain of Validity**:
- Displacement evaluated relative to the accelerating frame


---

### Derivation: Formula `formula-wep-wet-non-inertial`

**Target Governing Relation**:
$$ W_{\text{real}} + W_{\text{pseudo}} = \Delta K_{\text{rel}} $$

#### Step-by-Step Proof
**Step 1**: 
$$ m \vec{a}_{\text{rel}} = \vec{F}_{\text{real}} - m \vec{a}_0 $$
*Physical Operation*: 

**Step 2**: 
$$ m \vec{a}_{\text{rel}} \cdot d\vec{r}_{\text{rel}} = \vec{F}_{\text{real}} \cdot d\vec{r}_{\text{rel}} + (-m \vec{a}_0) \cdot d\vec{r}_{\text{rel}} $$
*Physical Operation*: 

**Step 3**: 
$$ \int m \frac{d\vec{v}_{\text{rel}}}{dt} \cdot \vec{v}_{\text{rel}} \, dt = \int \vec{F}_{\text{real}} \cdot d\vec{r}_{\text{rel}} + \int \vec{F}_{\text{pseudo}} \cdot d\vec{r}_{\text{rel}} \implies \Delta K_{\text{rel}} = W_{\text{real}} + W_{\text{pseudo}} $$
*Physical Operation*: 


---

### Worked Pedagogical Example: `ex-wep-wet-variable-force-01`

**Problem Statement**:
> A particle of mass $m = 1.0\text{ kg}$ is initially at rest at $x = 0$. It is subjected to a 1D force $F(x) = (6.0 - 2.0x)\text{ N}$ directed along the x-axis, where $x$ is in meters. Find: (a) the position where the particle attains maximum speed, and (b) the maximum speed $v_{\text{max}}$.

**Target Quantity**: `x_opt, v_max`

#### Systematic Solution
**Step 1 ()**:
$$ F(x) = 6.0 - 2.0x = 0 \implies x_{\text{opt}} = 3.0\text{ m} $$

Result: ``

**Step 2 ()**:
$$ W_{\text{net}} = \int_0^{3.0} (6.0 - 2.0x) \, dx = \left[ 6.0x - x^2 \right]_0^{3.0} = 6.0(3.0) - (3.0)^2 = 18.0 - 9.0 = 9.0\text{ J} $$

Result: ``

**Step 3 ()**:
$$ \frac{1}{2}(1.0) v_{\text{max}}^2 = 9.0 \implies v_{\text{max}}^2 = 18.0 \implies v_{\text{max}} = \sqrt{18.0} = 3\sqrt{2} \approx 4.24\text{ m/s} $$

Result: ``

**Final Answer**: x_{\text{opt}} = 3.0\text{ m}, \quad v_{\text{max}} = 3\sqrt{2} \approx 4.24\text{ m/s}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Setting work equal to zero instead of setting force equal to zero to find maximum speed
> - Forgetting 1/2 factor in kinetic energy

**Sanity & Consistency Checks**:
- Beyond x = 3.0 m, force becomes negative, decelerating the particle, verifying x = 3.0 m is a true maximum
- Dimensional check: [6x] = [x^2] = [N m] = [J]


---

### Worked Pedagogical Example: `ex-wep-wet-non-inertial-pendulum-01`

**Problem Statement**:
> A simple pendulum of bob mass $m$ and string length $L$ hangs in an elevator accelerating upward with constant acceleration $a_0$. If the bob is deflected by angle $\theta_0$ from the vertical and released from rest relative to the elevator, find the speed $v_{\text{rel}}$ of the bob at the lowest point.

**Target Quantity**: `v_rel`

#### Systematic Solution
**Step 1 ()**:
$$ \vec{g}_{\text{eff}} = \vec{g} - \vec{a}_0 = -(g + a_0)\hat{j} \implies g_{\text{eff}} = g + a_0 $$

Result: ``

**Step 2 ()**:
$$ h_{\text{rel}} = L - L \cos\theta_0 = L(1 - \cos\theta_0) $$

Result: ``

**Step 3 ()**:
$$ W_{\text{net, rel}} = m(g + a_0) h_{\text{rel}} = m(g + a_0) L(1 - \cos\theta_0) = \frac{1}{2} m v_{\text{rel}}^2 - 0 $$

Result: ``

**Step 4 ()**:
$$ v_{\text{rel}} = \sqrt{2(g + a_0)L(1 - \cos\theta_0)} $$

Result: ``

**Final Answer**: v_{\text{rel}} = \sqrt{2(g + a_0)L(1 - \cos\theta_0)}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Subtracting a_0 instead of adding for an upward accelerating elevator
> - Attempting to calculate tension work (string tension is perpendicular to relative displacement everywhere)

**Sanity & Consistency Checks**:
- When a_0 = 0, formula reduces to standard stationary pendulum v = sqrt(2gL(1 - cos theta_0))
- If elevator is in free fall a_0 = -g, g_eff = 0 and bob does not accelerate (v_rel = 0)


---

### Inoculation Against Misconception: `misc-wep-03`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"The Work-Energy Theorem applies only to constant forces along rectilinear paths."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Students learn W = F d cos(theta) first and mistakenly assume the theorem W_net = Delta K requires constant acceleration equations.

**Physical Truth & Resolution**:
The Work-Energy Theorem is derived by integrating Newton's Second Law along an arbitrary 3D curve: int F_net . dr = int m (dv/dt) . v dt = int m v dv = Delta K. It holds rigorously for arbitrary position-dependent, velocity-dependent, or time-dependent forces along any curved path.

**Refutation Counterexample & Supporting Evidence**:
For a simple pendulum or curved roller-coaster track where force direction and magnitude continuously vary, W_net = Delta K yields exact velocities without needing constant acceleration.

**Diagnostic Symptom**: W_{\text{net}} = \int_C \vec{F}_{\text{net}} \cdot d\vec{r} = \Delta K \quad \text{holds universally for arbitrary 3D trajectories and forces.}


---

### Inoculation Against Misconception: `misc-wep-04`

**Misconception Category**: `WRONG_CONSERVATION_LAW`  
**Erroneous Intuition**: *"Internal forces in a system can never do net mechanical work because action and reaction cancel."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Confusing linear momentum conservation (where internal forces sum to zero vector sum F_int = 0) with work, which depends on individual displacements.

**Physical Truth & Resolution**:
While action and reaction forces are equal and opposite (F_ij = -F_ji), the displacements of their respective points of application may differ! When two blocks connected by a compressed spring are released, both blocks move outward: the spring does positive work on both blocks, increasing total kinetic energy.

**Refutation Counterexample & Supporting Evidence**:
A compressed spring (k = 100 N/m, x = 0.2 m) between two masses on a frictionless floor releases. Both masses accelerate away. Total internal spring work is W_int = +1/2 k x^2 = +2 J, increasing kinetic energy from 0 to 2 J.

**Diagnostic Symptom**: W_{\text{int}} = \int \vec{F}_{12} \cdot d(\vec{r}_1 - \vec{r}_2) = \int \vec{F}_{12} \cdot d\vec{r}_{12} \neq 0 \quad \text{for deformable systems.}


---

### Verified JEE Practice Problem: `work-energy-power-question-e37050bb`

**Type**: `SINGLE_CORRECT_MCQ`  
**Provenance Source**: `Audited Source / Question Bank`  

> A particle of mass $m$ is projected with speed $u$ at an angle $\theta$ with the horizontal. The net work done by gravity on the particle from the instant of projection until it reaches the highest point of its trajectory is:

**Options**:
- **(A)**: $-\frac{1}{2} m u^2 \sin^2\theta$
- **(B)**: $\frac{1}{2} m u^2 \cos^2\theta$
- **(C)**: $-\frac{1}{2} m u^2$
- **(D)**: Zero

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `cvr-q-wep-01`

</details>


---

## Conservative Forces, Potential Energy, and Equilibrium

> **Pedagogical Goal**: Differentiate conservative from dissipative forces, define potential energy via gradient relations F = -grad(U), establish conservation of total mechanical energy, and analyze equilibrium stability from potential curvature.


---

### Concept: Conservative vs Non-Conservative Forces

**Definition**: A force $\vec{F}$ is conservative if the work done on a particle moving between two points depends ONLY on the endpoints and is independent of the path taken: $\oint_C \vec{F} \cdot d\vec{r} = 0$ for every closed loop. Mathematically, $\nabla \times \vec{F} = \vec{0}$. Forces failing this (e.g. friction, drag) are non-conservative.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Single-valued, static or position-dependent force field


---

### Concept: Potential Energy Definition and Gradient Relation

**Definition**: Potential energy $U$ is defined uniquely for conservative forces via the work of that force: $\Delta U = U_f - U_i = -W_c = -\int_{\vec{r}_i}^{\vec{r}_f} \vec{F}_c \cdot d\vec{r}$. In differential form, $dU = -\vec{F}_c \cdot d\vec{r}$, which yields the force as the negative gradient of potential energy: $\vec{F}_c = -\nabla U = -\left(\frac{\partial U}{\partial x}\hat{i} + \frac{\partial U}{\partial y}\hat{j} + \frac{\partial U}{\partial z}\hat{k}\right)$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Conservative force field
- Arbitrary reference datum where $U(\vec{r}_0) = 0$ is specified


---

### Concept: Gravitational and Elastic Potential Energy

**Definition**: For uniform near-surface gravity $\vec{F}_g = -mg\hat{j}$, gravitational potential energy is $U_g(y) = mgy$ relative to $y=0$. For an ideal spring with restoring force $F_s = -kx$, elastic potential energy is $U_s(x) = \frac{1}{2}kx^2$ relative to relaxed state $x=0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Uniform gravitational field $g = \text{const}$
- Hooke's spring constant $k = \text{const}$


---

### Concept: Conservation of Mechanical Energy and Energy Balance

**Definition**: Total mechanical energy is defined as $E_{\text{mech}} = K + U$. In the presence of only conservative forces, $W_{\text{net}} = W_c = -\Delta U \implies \Delta K + \Delta U = 0 \implies E_{\text{mech}} = \text{constant}$. In the general case with non-conservative forces, $\Delta E_{\text{mech}} = W_{\text{nc}} + W_{\text{ext}}$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Isolated system or zero non-conservative work $W_{\text{nc}} = 0$


---

### Concept: Equilibrium Analysis and Stability from Potential Curves

**Definition**: A particle is in static equilibrium where net force vanishes: $F_x = -dU/dx = 0$. The nature of equilibrium is classified by the second derivative of $U(x)$:
1. Stable Equilibrium: $\frac{d^2U}{dx^2} > 0$ (local potential minimum, restoring force returns particle)
2. Unstable Equilibrium: $\frac{d^2U}{dx^2} < 0$ (local potential maximum, repelling force drives particle away)
3. Neutral Equilibrium: $\frac{d^2U}{dx^2} = 0$ (flat potential, force remains zero on displacement).
Turning points occur where total mechanical energy equals potential energy: $E = U(x) \implies K = 0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- 1D conservative system with smooth differentiable potential $U(x)$


---

### Formula: Definition of Potential Energy for Conservative Force

**Governing Equation**:
$$ \Delta U = U_f - U_i = -W_c = -\int_{\vec{r}_i}^{\vec{r}_f} \vec{F}_c \cdot d\vec{r} $$

**Variable Inventory & SI Units**:
- $\Delta U$: Change in potential energy
- $W_c$: Work done by the conservative force
- $\vec{F}_c$: Conservative force vector

**Physical Assumptions**:
- Force field F_c is strictly conservative (curl F = 0)

**Domain of Validity**:
- Independent of integration path


---

### Formula: Force as Negative Potential Energy Gradient

**Governing Equation**:
$$ \vec{F} = -\nabla U = -\left(\frac{\partial U}{\partial x}\hat{i} + \frac{\partial U}{\partial y}\hat{j} + \frac{\partial U}{\partial z}\hat{k}\right), \quad F_x = -\frac{dU}{dx} $$

**Variable Inventory & SI Units**:
- $\vec{F}$: Conservative force vector
- $U(\vec{r})$: Scalar potential energy function
- $\nabla$: Spatial gradient vector operator

**Physical Assumptions**:
- Smooth differentiable scalar potential field U(x, y, z)

**Domain of Validity**:
- Exact differential dU = -F . dr


---

### Derivation: Formula `formula-wep-pe-gradient`

**Target Governing Relation**:
$$ \vec{F} = -\nabla U, \quad F_x = -\frac{\partial U}{\partial x} $$

#### Step-by-Step Proof
**Step 1**: 
$$ dU = \frac{\partial U}{\partial x} \, dx + \frac{\partial U}{\partial y} \, dy + \frac{\partial U}{\partial z} \, dz $$
*Physical Operation*: 

**Step 2**: 
$$ -\left( F_x \, dx + F_y \, dy + F_z \, dz \right) = \frac{\partial U}{\partial x} \, dx + \frac{\partial U}{\partial y} \, dy + \frac{\partial U}{\partial z} \, dz $$
*Physical Operation*: 

**Step 3**: 
$$ F_x = -\frac{\partial U}{\partial x}, \quad F_y = -\frac{\partial U}{\partial y}, \quad F_z = -\frac{\partial U}{\partial z} \implies \vec{F} = -\nabla U $$
*Physical Operation*: 


---

### Formula: Conservation of Mechanical Energy

**Governing Equation**:
$$ E_{\text{mech}} = K + U = \text{constant} \iff K_i + U_i = K_f + U_f $$

**Variable Inventory & SI Units**:
- $E_{\text{mech}}$: Total mechanical energy
- $K$: Kinetic energy (Unit: `J`)
- $U$: Total potential energy (Unit: `J`)

**Physical Assumptions**:
- Only conservative forces do work on system (W_nc = 0)

**Domain of Validity**:
- Zero non-conservative work and zero external energy exchange


---

### Derivation: Formula `formula-wep-mech-energy-conservation`

**Target Governing Relation**:
$$ E_{\text{mech}} = K + U = \text{constant} $$

#### Step-by-Step Proof
**Step 1**: 
$$ W_{\text{net}} = W_c + W_{\text{nc}} $$
*Physical Operation*: 

**Step 2**: 
$$ W_c + W_{\text{nc}} = \Delta K $$
*Physical Operation*: 

**Step 3**: 
$$ -\Delta U + W_{\text{nc}} = \Delta K \implies \Delta K + \Delta U = W_{\text{nc}} \implies \Delta(K + U) = W_{\text{nc}} $$
*Physical Operation*: 

**Step 4**: 
$$ \Delta(K + U) = 0 \implies K_i + U_i = K_f + U_f = E_{\text{mech}} = \text{constant} $$
*Physical Operation*: 


---

### Formula: Equilibrium Condition and Curvature Stability

**Governing Equation**:
$$ \frac{dU}{dx} = 0; \quad \frac{d^2U}{dx^2} > 0 \text{ (stable)}, \quad \frac{d^2U}{dx^2} < 0 \text{ (unstable)}, \quad \frac{d^2U}{dx^2} = 0 \text{ (neutral)} $$

**Variable Inventory & SI Units**:
- $U(x)$: 1D potential energy function
- $x$: Position coordinate (Unit: `m`)

**Physical Assumptions**:
- 1D conservative system with twice-differentiable potential U(x)

**Domain of Validity**:
- Local Taylor expansion near equilibrium coordinate x_0


---

### Worked Pedagogical Example: `ex-wep-pe-curve-equilibrium-01`

**Problem Statement**:
> The potential energy of a diatomic system as a function of atomic separation $r$ is modeled by $U(r) = \frac{A}{r^2} - \frac{B}{r}$, where $A > 0$ and $B > 0$ are constants. Determine: (a) the equilibrium separation distance $r_0$, (b) the nature of the equilibrium, and (c) the minimum work required to dissociate the system from equilibrium to infinite separation.

**Target Quantity**: `r_0, stability, W_diss`

#### Systematic Solution
**Step 1 ()**:
$$ \frac{dU}{dr} = -\frac{2A}{r^3} + \frac{B}{r^2} = 0 \implies \frac{B}{r^2} = \frac{2A}{r^3} \implies r_0 = \frac{2A}{B} $$

Result: ``

**Step 2 ()**:
$$ \frac{d^2U}{dr^2} = \frac{6A}{r^4} - \frac{2B}{r^3} = \frac{1}{r_0^3}\left( \frac{6A}{2A/B} - 2B \right) = \frac{1}{r_0^3}(3B - 2B) = \frac{B}{r_0^3} > 0 $$

Result: ``

**Step 3 ()**:
$$ \frac{d^2U}{dr^2}\Big|_{r_0} > 0 \implies \text{STABLE EQUILIBRIUM} $$

Result: ``

**Step 4 ()**:
$$ U(r_0) = \frac{A}{(2A/B)^2} - \frac{B}{(2A/B)} = \frac{B^2}{4A} - \frac{B^2}{2A} = -\frac{B^2}{4A}, \quad U(\infty) = 0 \implies W_{\text{diss}} = 0 - \left(-\frac{B^2}{4A}\right) = \frac{B^2}{4A} $$

Result: ``

**Final Answer**: r_0 = \frac{2A}{B}, \quad \text{STABLE EQUILIBRIUM}, \quad W_{\text{diss}} = \frac{B^2}{4A}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Sign errors in differentiating 1/r^2 and 1/r terms
> - Confusing potential energy at minimum with binding energy

**Sanity & Consistency Checks**:
- Dimensions: [A] = [Energy][L]^2, [B] = [Energy][L] => [r_0] = [A/B] = [L], [B^2/4A] = [Energy], dimensional consistency verified
- As r -> 0, U -> +infty (strong repulsion); as r -> infty, U -> 0 (zero interaction)


---

### Inoculation Against Misconception: `misc-wep-05`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"Potential energy can be defined for any physical force, including friction."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Believing that because work can be calculated for friction, one can simply define a 'frictional potential energy' U_f.

**Physical Truth & Resolution**:
Potential energy U requires that work between two points be independent of path, satisfying oint F . dr = 0. For kinetic friction, the line integral along a closed round trip is strictly non-zero (-2 mu_k N L < 0). Friction dissipates mechanical energy irreversibly into thermal disorder; no reversible potential energy can be formulated.

**Refutation Counterexample & Supporting Evidence**:
Sliding a block around a closed square loop of perimeter 4L on a rough floor does negative work W_f = -4 mu_k N L != 0. If a potential existed, round-trip work would be identically zero.

**Diagnostic Symptom**: \oint \vec{f}_k \cdot d\vec{r} = -\mu_k N \oint ds < 0 \implies \nabla \times \vec{f}_k \neq \vec{0} \implies \text{No potential energy exists.}


---

### Verified JEE Practice Problem: `work-energy-power-question-ba0b4106`

**Type**: `SINGLE_CORRECT_MCQ`  
**Provenance Source**: `Audited Source / Question Bank`  

> The potential energy of a conservative 1D force field is given by $U(x) = 2x^4 - 4x^2\text{ J}$, where $x$ is in meters. The positions of stable equilibrium are:

**Options**:
- **(A)**: $x = \pm 1\text{ m}$
- **(B)**: $x = 0$
- **(C)**: $x = \pm 2\text{ m}$
- **(D)**: $x = \pm \frac{1}{\sqrt{2}}\text{ m}$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `cvr-q-wep-02`

</details>


---

## Power and Vertical Circular Motion

> **Pedagogical Goal**: Formulate average and instantaneous power P = F . v, synthesize mechanical energy conservation with radial dynamics in vertical circles, derive critical looping velocities, and analyze upper quadrant string slackening.


---

### Concept: Average and Instantaneous Mechanical Power

**Definition**: Power is the time rate at which work is performed: Instantaneous power is $P = \frac{dW}{dt} = \frac{\vec{F} \cdot d\vec{r}}{dt} = \vec{F} \cdot \vec{v} = F v \cos\theta$. Average power over finite duration $\Delta t$ is $P_{\text{avg}} = \frac{\Delta W}{\Delta t}$. The SI unit is the Watt ($1\text{ W} = 1\text{ J/s} = 1\text{ kg m}^2\text{s}^{-3}$); engineering unit is horsepower ($1\text{ hp} = 746\text{ W}$).

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Force and velocity measured in the same inertial reference frame


---

### Concept: Vertical Circular Motion and Critical Looping Speeds

**Definition**: A particle of mass $m$ tied to an inextensible light string of length $R$ moves in a vertical plane under gravity. At angle $\theta$ from lowest point, radial dynamics yields string tension: $T - mg\cos\theta = \frac{mv^2}{R}$. To complete a full circle, string tension must remain non-negative at the apex: $T_{\text{top}} \ge 0 \implies v_{\text{top}} \ge \sqrt{gR}$. By energy conservation, minimum launch speed at bottom is $v_{\text{bot}} = \sqrt{5gR}$, and tension difference is identically $T_{\text{bot}} - T_{\text{top}} = 6mg$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Inextensible, massless string
- Zero air resistance
- Planar vertical circle


---

### Concept: String Slackening and Projectile Departure in Upper Quadrant

**Definition**: If bottom speed satisfies $\sqrt{2gR} < v_{\text{bot}} < \sqrt{5gR}$, the particle oscillates past the horizontal level ($\theta = \pi/2$) but cannot reach the apex ($\theta = \pi$). String tension vanishes ($T = 0$) at an angle $\theta_s$ in the upper quadrant: $\cos\theta_s = -\frac{v_{\text{bot}}^2 - 2gR}{3gR}$. Beyond this point, the particle departs from circular path, executing free parabolic projectile flight under gravity.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- String remains completely flexible and slack during parabolic flight phase


---

### Concept: Vertical Circular Motion Constrained by Rigid Rod or Pipe

**Definition**: When a particle is mounted on a light rigid rod of length $R$ or constrained inside a smooth vertical circular tube, the rod can support compression ($N < 0$ or outward normal). The particle can reach the apex with zero velocity without falling: $v_{\text{top,min}} = 0$. By energy conservation, minimum launch speed at bottom is $v_{\text{bot,min}} = \sqrt{4gR} = 2\sqrt{gR}$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Rigid, massless rod
- No friction or air resistance


---

### Formula: Instantaneous Mechanical Power

**Governing Equation**:
$$ P = \frac{dW}{dt} = \vec{F} \cdot \vec{v} = F v \cos\theta = F_x v_x + F_y v_y + F_z v_z $$

**Variable Inventory & SI Units**:
- $P$: Instantaneous power (Unit: `W (J/s)` | Dim: `[M][L]^2[T]^-3`)
- $W$: Work performed
- $\vec{F}$: Applied force vector (Unit: `N` | Dim: `[M][L][T]^-2`)
- $\vec{v}$: Velocity vector of point of application (Unit: `m/s` | Dim: `[L][T]^-1`)

**Physical Assumptions**:
- Inertial reference frame for velocity vector

**Domain of Validity**:
- Point of application velocity matched with force agent


---

### Formula: Critical Looping Velocities for Vertical Circle with String

**Governing Equation**:
$$ v_{\text{bot,min}} = \sqrt{5 g R}, \quad v_{\text{top,min}} = \sqrt{g R}, \quad T_{\text{bot}} - T_{\text{top}} = 6 mg $$

**Variable Inventory & SI Units**:
- $v_{\text{bot,min}}$: Minimum speed at lowest point to complete vertical loop
- $v_{\text{top,min}}$: Minimum speed at highest point (apex) without slackening
- $R$: Radius of circular path (length of string) (Unit: `m` | Dim: `[L]`)
- $g$: Acceleration due to gravity (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $m$: Mass of particle (Unit: `kg`)

**Physical Assumptions**:
- Light inextensible string
- No air resistance
- Planar vertical circle

**Domain of Validity**:
- String tension T >= 0 everywhere on trajectory


---

### Formula: String Slackening Angle in Upper Quadrant

**Governing Equation**:
$$ \cos\theta_{\text{slack}} = -\frac{v_{\text{bot}}^2 - 2gR}{3gR}, \quad \text{for } \sqrt{2gR} < v_{\text{bot}} < \sqrt{5gR} $$

**Variable Inventory & SI Units**:
- $\theta_{\text{slack}}$: Angle measured from lowest point at which string tension vanishes
- $v_{\text{bot}}$: Launch speed at bottom
- $R$: Radius of circle (Unit: `m`)
- $g$: Gravitational acceleration (Unit: `m/s^2`)

**Physical Assumptions**:
- Tension vanishes at angle theta_slack with non-zero speed
- Light inextensible string

**Domain of Validity**:
- Valid strictly in range pi/2 < theta < pi where cos(theta) < 0


---

### Worked Pedagogical Example: `ex-wep-power-constant-engine-01`

**Problem Statement**:
> An electric locomotive of total mass $M = 2.0 \times 10^4\text{ kg}$ starts from rest and is driven by an engine delivering constant mechanical power $P_0 = 100\text{ kW}$. Assuming no frictional or aerodynamic losses, find: (a) the speed $v(t)$ as a function of time, (b) the distance $s(t)$ covered as a function of time, and (c) the speed and distance at $t = 10.0\text{ s}$.

**Target Quantity**: `v(t), s(t), v(10), s(10)`

#### Systematic Solution
**Step 1 ()**:
$$ P_0 = \frac{dK}{dt} = \frac{d}{dt}\left( \frac{1}{2} M v^2 \right) \implies \frac{1}{2} M v^2 = P_0 t \implies v(t) = \sqrt{\frac{2 P_0 t}{M}} $$

Result: ``

**Step 2 ()**:
$$ v(t) = \sqrt{\frac{2 \times 10^5}{2 \times 10^4} t} = \sqrt{10 t} = \sqrt{10} t^{1/2} $$

Result: ``

**Step 3 ()**:
$$ s(t) = \int_0^t v(t') \, dt' = \sqrt{10} \int_0^t t'^{1/2} \, dt' = \sqrt{10} \left[ \frac{2}{3} t^{3/2} \right] = \frac{2\sqrt{10}}{3} t^{3/2} $$

Result: ``

**Step 4 ()**:
$$ v(10) = \sqrt{10 \times 10} = 10.0\text{ m/s}, \quad s(10) = \frac{2\sqrt{10}}{3} (10)^{3/2} = \frac{2\sqrt{10}}{3} (10\sqrt{10}) = \frac{200}{3} \approx 66.7\text{ m} $$

Result: ``

**Final Answer**: v(t) = \sqrt{10 t}, \quad s(t) = \frac{2\sqrt{10}}{3} t^{3/2}; \quad v(10) = 10.0\text{ m/s}, \quad s(10) = \frac{200}{3}\text{ m} \approx 66.7\text{ m}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Assuming acceleration is constant (at constant power, acceleration a = P/(M v) decreases inversely with speed)
> - Using kinematic formulas v = u + at

**Sanity & Consistency Checks**:
- Kinetic energy at t = 10 s: K = 1/2 (20000) (10)^2 = 1.0 x 10^6 J. Total energy delivered: P_0 * t = 100000 * 10 = 1.0 x 10^6 J, exact match
- Dimensions: [P t / M]^(1/2) = ([M L^2 T^-3 T] / [M])^(1/2) = (L^2 T^-2)^(1/2) = L T^-1, correct velocity dimensions


---

### Worked Pedagogical Example: `ex-wep-vcm-slack-projectile-01`

**Problem Statement**:
> A small body of mass $m$ is suspended by a light string of length $R = 1.0\text{ m}$ from a fixed peg $O$. The body is given a horizontal velocity $v_0 = \sqrt{3 g R}$ at the lowest point. Find: (a) the angle $\theta_s$ from the downward vertical where the string becomes slack, and (b) the maximum height $H_{\text{max}}$ attained by the body above the lowest point during its subsequent motion. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `theta_s, H_max`

#### Systematic Solution
**Step 1 ()**:
$$ \cos\theta_s = -\frac{v_0^2 - 2gR}{3gR} = -\frac{3gR - 2gR}{3gR} = -\frac{1}{3} \implies \theta_s = \arccos(-1/3) \approx 109.47^\circ $$

Result: ``

**Step 2 ()**:
$$ v_s^2 = v_0^2 - 2gR(1 - \cos\theta_s) = 3gR - 2gR\left(1 - \left(-\frac{1}{3}\right)\right) = 3gR - 2gR\left(\frac{4}{3}\right) = \frac{1}{3} g R $$

Result: ``

**Step 3 ()**:
$$ y_s = R(1 - \cos\theta_s) = R\left(1 - \left(-\frac{1}{3}\right)\right) = \frac{4}{3} R $$

Result: ``

**Step 4 ()**:
$$ \sin\alpha = |\cos\theta_s| = \frac{1}{3} $$

Result: ``

**Step 5 ()**:
$$ h_{\text{proj}} = \frac{v_s^2 \sin^2\alpha}{2g} = \frac{(gR/3)(1/3)^2}{2g} = \frac{R/27}{2} = \frac{R}{54} $$

Result: ``

**Step 6 ()**:
$$ H_{\text{max}} = y_s + h_{\text{proj}} = \frac{4}{3} R + \frac{1}{54} R = \frac{72 + 1}{54} R = \frac{73}{54} R = \frac{73}{54}(1.0) \approx 1.352\text{ m} $$

Result: ``

**Final Answer**: \cos\theta_s = -\frac{1}{3} \implies \theta_s \approx 109.5^\circ, \quad H_{\text{max}} = \frac{73}{54} R \approx 1.35\text{ m}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Assuming particle falls vertically downward once string goes slack
> - Using total velocity v_s instead of vertical velocity component v_s sin(alpha) for projectile height

**Sanity & Consistency Checks**:
- H_max must be less than 2R (looping apex) and greater than 4/3 R (slack point): 1.333 R < 1.352 R < 2.0 R, verified
- At slack point, T = 0 and radial component of gravity mg cos(theta_s) exactly balances m v_s^2 / R


---

### Inoculation Against Misconception: `misc-wep-06`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"In vertical circular motion, tension at the top must be strictly zero for the particle to complete the circle."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Treating the limiting boundary condition T_top = 0 as an equality that must always hold, or assuming zero tension means the string has snapped.

**Physical Truth & Resolution**:
The requirement to complete the loop is an inequality: T_top >= 0. For any launch speed v_bot > sqrt(5gR), tension at the top is strictly positive: T_top = m v_top^2 / R - mg > 0. Only at the exact threshold v_bot = sqrt(5gR) does tension vanish momentarily at the apex point.

**Refutation Counterexample & Supporting Evidence**:
If a particle is launched with v_bot = sqrt(6gR), energy conservation gives v_top = sqrt(2gR). Radial tension at apex is T_top = m(2gR)/R - mg = mg > 0.

**Diagnostic Symptom**: T_{\text{top}} = \frac{m v_{\text{top}}^2}{R} - mg \ge 0 \iff v_{\text{top}} \ge \sqrt{gR} \quad (T_{\text{top}} > 0 \text{ for any } v_{\text{bot}} > \sqrt{5gR}).


---

## Chapter Summary & Formula Recap: Work, Energy & Power

### Core Equations & Domains of Validity
- **Work Done by a Constant Force**: $$W = \vec{F} \cdot \vec{d} = F d \cos\theta = F_x d_x + F_y d_y + F_z d_z$$
  *Validity*: Point particle or translation without rotation
- **Work Done by a Variable Force**: $$W = \int_{\vec{r}_i}^{\vec{r}_f} \vec{F}(\vec{r}) \cdot d\vec{r} = \int_{x_i}^{x_f} F_x \, dx + \int_{y_i}^{y_f} F_y \, dy + \int_{z_i}^{z_f} F_z \, dz$$
  *Validity*: Universal for 1D, 2D, and 3D classical particle motion
- **Work Done by an Ideal Spring**: $$W_s = -\frac{1}{2} k (x_f^2 - x_i^2)$$
  *Validity*: Within elastic limit of spring material
- **Work Done by Kinetic Friction**: $$W_{f_k} = -f_k s_{\text{rel}} = -\mu_k N s_{\text{rel}}$$
  *Validity*: Dry sliding contact obeying Amontons-Coulomb law
- **Kinetic Energy of a Particle**: $$K = \frac{1}{2} m v^2 = \frac{p^2}{2m}$$
  *Validity*: Universal scalar definition in classical mechanics
- **Work-Energy Theorem in Inertial Frame**: $$W_{\text{net}} = \Delta K = K_f - K_i = \frac{1}{2} m v_f^2 - \frac{1}{2} m v_i^2$$
  *Validity*: Valid for all forces including conservative, non-conservative, variable, internal, and external
- **Work-Energy Theorem in Non-Inertial Reference Frame**: $$W_{\text{real}} + W_{\text{pseudo}} = \Delta K_{\text{rel}}$$
  *Validity*: Displacement evaluated relative to the accelerating frame
- **Definition of Potential Energy for Conservative Force**: $$\Delta U = U_f - U_i = -W_c = -\int_{\vec{r}_i}^{\vec{r}_f} \vec{F}_c \cdot d\vec{r}$$
  *Validity*: Independent of integration path
- **Force as Negative Potential Energy Gradient**: $$\vec{F} = -\nabla U = -\left(\frac{\partial U}{\partial x}\hat{i} + \frac{\partial U}{\partial y}\hat{j} + \frac{\partial U}{\partial z}\hat{k}\right), \quad F_x = -\frac{dU}{dx}$$
  *Validity*: Exact differential dU = -F . dr
- **Conservation of Mechanical Energy**: $$E_{\text{mech}} = K + U = \text{constant} \iff K_i + U_i = K_f + U_f$$
  *Validity*: Zero non-conservative work and zero external energy exchange
- **Equilibrium Condition and Curvature Stability**: $$\frac{dU}{dx} = 0; \quad \frac{d^2U}{dx^2} > 0 \text{ (stable)}, \quad \frac{d^2U}{dx^2} < 0 \text{ (unstable)}, \quad \frac{d^2U}{dx^2} = 0 \text{ (neutral)}$$
  *Validity*: Local Taylor expansion near equilibrium coordinate x_0
- **Instantaneous Mechanical Power**: $$P = \frac{dW}{dt} = \vec{F} \cdot \vec{v} = F v \cos\theta = F_x v_x + F_y v_y + F_z v_z$$
  *Validity*: Point of application velocity matched with force agent
- **Critical Looping Velocities for Vertical Circle with String**: $$v_{\text{bot,min}} = \sqrt{5 g R}, \quad v_{\text{top,min}} = \sqrt{g R}, \quad T_{\text{bot}} - T_{\text{top}} = 6 mg$$
  *Validity*: String tension T >= 0 everywhere on trajectory
- **String Slackening Angle in Upper Quadrant**: $$\cos\theta_{\text{slack}} = -\frac{v_{\text{bot}}^2 - 2gR}{3gR}, \quad \text{for } \sqrt{2gR} < v_{\text{bot}} < \sqrt{5gR}$$
  *Validity*: Valid strictly in range pi/2 < theta < pi where cos(theta) < 0
