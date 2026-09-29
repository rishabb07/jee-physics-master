# Chapter: Rotational Motion

**Template**: `MECHANICS`  
**Prerequisites**: curr-kin-02, curr-com-01, curr-nl-01  

## Learning Objectives
- Calculate moment of inertia for discrete point masses and continuous bodies using integration and the parallel/perpendicular axis theorems.
- Formulate rotational equations of motion tau = I alpha and apply work-energy principles to fixed axis rotation.
- Determine the angular momentum of particles and rigid bodies about fixed reference points and instantaneous axes of rotation.
- Apply the principle of conservation of angular momentum to isolated systems with time-varying moments of inertia.
- Analyze pure rolling kinematics and dynamics on horizontal and inclined surfaces under static friction constraints.

---

## Moment of Inertia and the Parallel Axis Theorem

> **Pedagogical Goal**: Establish rotational inertia for discrete and continuous mass distributions and apply the parallel axis theorem rigorously through the center of mass.


---

### Concept: Moment of Inertia as Rotational Analogue of Mass

**Definition**: For a rigid system of discrete particles of masses $m_i$ at perpendicular distances $r_i$ from a specified axis of rotation, the moment of inertia $I$ is defined as $I = \sum_{i} m_i r_i^2$. For a continuous body of mass density $\rho(\vec{r})$ occupying volume $V$, the moment of inertia is the volume integral $I = \int_{V} r_\perp^2 \, dm = \int_{V} r_\perp^2 \rho(\vec{r}) \, dV$, where $r_\perp$ is the perpendicular distance of the infinitesimal mass element $dm$ from the rotation axis. Its SI unit is $\text{kg}\cdot\text{m}^2$, with dimensions $[M L^2]$.

**Physical Significance**: Imagine trying to rotate a heavy dumbbell. If the masses are close to your hand along the axis of rotation, twisting it back and forth is effortless. If the masses are moved outward to the far ends of the rod, twisting it becomes substantially harder—even though the total mass has not changed. This demonstrates that in rotational dynamics, how far the mass is distributed from the axis of rotation ($r$) matters far more than just how much mass there is, scaling quadratically as $r^2$.

**Assumptions & Scope of Validity**:
- The body is perfectly rigid, such that pairwise distances between particles remain invariant under rotation.
- The rotation axis is fixed in orientation or passes through the center of mass in a principal inertial frame.
- Classical non-relativistic regime where mass is constant and Euclidean geometry applies.


---

### Formula: Parallel Axis Theorem

**Governing Equation**:
$$ I = I_{\text{cm}} + M d^2 $$

**Variable Inventory & SI Units**:
- $I$: Moment of inertia about parallel axis (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $I_{\text{cm}}$: Moment of inertia about parallel axis through center of mass (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $M$: Total mass of rigid body (Unit: `kg` | Dim: `[M]`)
- $d$: Perpendicular distance between the two parallel axes (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Rigid body assumption
- Both axes are strictly parallel
- One axis passes strictly through the center of mass

**Domain of Validity**:
- Applicable to three-dimensional rigid bodies of arbitrary geometry for any pair of parallel axes where one is a centroidal axis


---

### Derivation: Formula `formula-rot-moi-parallel`

**Target Governing Relation**:
$$ $$I = I_{\text{cm}} + M d^2$$ $$

#### Step-by-Step Proof
**Step 1**: Establish a coordinate frame with origin at the center of mass (CM) and align the $z$-axis with the CM rotation axis.
$$ $$\vec{R}_{\text{axis}} = \vec{d} = d_x \hat{i} + d_y \hat{j},\quad |\vec{d}| = d$$ $$
*Physical Operation*: Set coordinate system with origin $O$ at the center of mass, taking the rotation axis through CM as the $z$-axis. The parallel axis $z'$ is displaced by a perpendicular vector $\vec{d} = d_x \hat{i} + d_y \hat{j}$ in the $xy$-plane, where $|\vec{d}| = d = \sqrt{d_x^2 + d_y^2}$.

**Step 2**: Express the position of a mass element $dm$ relative to the center of mass and relative to the displaced parallel axis.
$$ $$\vec{r}_\perp = (x' - d_x)\hat{i} + (y' - d_y)\hat{j}$$ $$
*Physical Operation*: Let the position vector of mass element $dm$ in the CM frame be $\vec{r}' = x' \hat{i} + y' \hat{j} + z' \hat{k}$. Its position vector relative to the parallel axis $z'$ is $\vec{r} = \vec{r}' - \vec{d} = (x' - d_x)\hat{i} + (y' - d_y)\hat{j} + z' \hat{k}$.

**Step 3**: Compute the square of the perpendicular distance from the parallel axis $z'$ to the mass element $dm$.
$$ $$r_\perp^2 = (x'^2 + y'^2) + (d_x^2 + d_y^2) - 2(x' d_x + y' d_y) = r_\perp'^2 + d^2 - 2 \vec{r}'_\perp \cdot \vec{d}$$ $$
*Physical Operation*: Calculate the squared magnitude $r_\perp^2 = |\vec{r}_\perp|^2 = (x' - d_x)^2 + (y' - d_y)^2$ and expand the binomial terms.

**Step 4**: Integrate the squared perpendicular distance over the entire mass of the rigid body to obtain total moment of inertia.
$$ $$I = \int r_\perp'^2 \, dm + d^2 \int dm - 2 \vec{d} \cdot \int \vec{r}'_\perp \, dm$$ $$
*Physical Operation*: Integrate with respect to mass element $dm$ across the entire body volume $V$: $I = \int r_\perp^2 \, dm$.

**Step 5**: Evaluate the three integral terms using the definitions of $I_{\text{cm}}$, total mass $M$, and the center of mass reference frame.
$$ $$\int r_\perp'^2 \, dm = I_{\text{cm}},\quad d^2 \int dm = M d^2,\quad \int \vec{r}'_\perp \, dm = \vec{0}$$ $$
*Physical Operation*: Identify: (1) $\int r_\perp'^2 \, dm = I_{\text{cm}}$ by definition of moment of inertia about the CM axis. (2) $\int dm = M$, so $d^2 \int dm = M d^2$. (3) $\int \vec{r}'_\perp \, dm = M \vec{R}_{\text{cm}, \perp}' = \vec{0}$ because the origin was chosen precisely at the center of mass.

**Step 6**: Substitute the evaluated integrals into the expansion to establish the parallel axis theorem.
$$ $$I = I_{\text{cm}} + M d^2$$ $$
*Physical Operation*: Combine terms to arrive at the final algebraic formula.

**Applicability & Limiting Conditions**:
- Must be applied between a center-of-mass axis and a parallel axis; cannot be applied directly between two arbitrary non-CM axes without passing through CM.
- The two axes must be strictly parallel.
- The body must be rigid.


---

## Torque and Fixed-Axis Rotational Dynamics

> **Pedagogical Goal**: Formulate the dynamical relation tau_net = I alpha for rigid bodies rotating about a fixed axis or accelerating through the center of mass.


---

### Concept: Torque and Fixed-Axis Rotational Dynamics

**Definition**: The torque $\vec{\tau}_O$ of a force $\vec{F}$ acting at a position $\vec{r}$ relative to a reference point $O$ is defined as the cross product $\vec{\tau}_O = \vec{r} \times \vec{F}$. For a rigid body constrained to rotate about a fixed axis $z$, the net external torque component along the axis is directly proportional to the body's angular acceleration $\alpha$ about that axis: $\tau_{\text{net}, z} = I_z \alpha$, where $I_z$ is the moment of inertia about the axis. SI unit is $\text{N}\cdot\text{m}$, with dimensions $[M L^2 T^{-2}]$.

**Physical Significance**: When pushing a heavy door open, pushing near the hinges requires enormous force and barely produces rotation, whereas pushing at the outer edge near the handle easily swings the door open. Furthermore, pushing parallel to the door face produces no turning effect whatsoever. The rotational effectiveness of a force depends not merely on its magnitude, but on its lever arm perpendicular to the rotation axis: $\tau = r_\perp F$.

**Assumptions & Scope of Validity**:
- The body maintains rigid geometry during rotational motion.
- The rotation axis is fixed in an inertial frame, or is a principal axis through the accelerating center of mass.
- Interatomic forces satisfy Newton's third law in central (strong) form, ensuring internal torques sum to zero.


---

### Formula: Torque Dynamic Relation

**Governing Equation**:
$$ \vec{\tau}_{\text{net, ext}} = I \vec{\alpha} = \frac{d\vec{L}}{dt} $$

**Variable Inventory & SI Units**:
- $\tau$: Net external torque (Unit: `N m` | Dim: `[M][L]^2[T]^-2`)
- $I$: Moment of inertia about rotation axis (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $\alpha$: Angular acceleration (Unit: `rad/s^2` | Dim: `[T]^-2`)
- $L$: Angular momentum (Unit: `kg m^2/s` | Dim: `[M][L]^2[T]^-1`)

**Physical Assumptions**:
- Rigid body
- Fixed rotation axis or rotation about center of mass
- Axis is principal axis of inertia

**Domain of Validity**:
- Holds in inertial frame or in accelerating frame if pseudo-force torques about CM are accounted for


---

### Derivation: Formula `formula-rot-torque-dyn`

**Target Governing Relation**:
$$ $$\tau_{\text{net, ext}} = I \alpha$$ $$

#### Step-by-Step Proof
**Step 1**: Discretize the rigid body into $N$ particles of mass $m_i$ rotating in planes perpendicular to the fixed axis $z$ at radial distances $r_i$.
$$ $$a_{i, t} = r_i \alpha$$ $$
*Physical Operation*: Decompose the acceleration of each particle $i$ into tangential and radial components: $\vec{a}_i = a_{i, t} \hat{\theta}_i + a_{i, r} \hat{r}_i$, where $a_{i, t} = r_i \alpha$ and $a_{i, r} = -r_i \omega^2$.

**Step 2**: Apply Newton's second law along the tangential direction for particle $i$.
$$ $$F_{i, t} = m_i r_i \alpha$$ $$
*Physical Operation*: Multiply tangential acceleration by particle mass $m_i$ to find the net tangential force component acting on particle $i$: $F_{i, t} = m_i a_{i, t}$.

**Step 3**: Calculate the axial component of torque $\tau_{i, z}$ acting on particle $i$ about the rotation axis.
$$ $$\tau_{i, z} = m_i r_i^2 \alpha$$ $$
*Physical Operation*: Take the moment of force about the axis $z$: $\tau_{i, z} = r_i F_{i, t} = r_i (m_i r_i \alpha)$.

**Step 4**: Sum the torques over all constituent particles of the rigid body.
$$ $$\tau_{\text{net}, z} = \left(\sum_{i=1}^N m_i r_i^2\right) \alpha$$ $$
*Physical Operation*: Sum both sides from $i=1$ to $N$ and factor out the common angular acceleration $\alpha$: $\tau_{\text{net}, z} = \sum_{i=1}^N \tau_{i, z} = \sum_{i=1}^N (m_i r_i^2 \alpha) = \left(\sum_{i=1}^N m_i r_i^2\right) \alpha$.

**Step 5**: Demonstrate that internal torques between constituent particles cancel pairwise.
$$ $$\tau_{\text{int}, z} = 0 \implies \tau_{\text{net}, z} = \tau_{\text{net, ext}, z}$$ $$
*Physical Operation*: Decompose total torque into external and internal contributions: $\vec{\tau}_{\text{net}} = \vec{\tau}_{\text{ext}} + \sum_{i < j} (\vec{r}_i \times \vec{F}_{ij} + \vec{r}_j \times \vec{F}_{ji}) = \vec{\tau}_{\text{ext}} + \sum_{i < j} (\vec{r}_i - \vec{r}_j) \times \vec{F}_{ij}$. By Newton's third law in strong form, $\vec{F}_{ij}$ acts along $(\vec{r}_i - \vec{r}_j)$, so $(\vec{r}_i - \vec{r}_j) \times \vec{F}_{ij} = \vec{0}$.

**Step 6**: Substitute the definition of moment of inertia $I = \sum_{i=1}^N m_i r_i^2$ (or $\int r_\perp^2 \, dm$) to finalize the equation.
$$ $$\tau_{\text{net, ext}} = I \alpha$$ $$
*Physical Operation*: Replace $\sum_{i=1}^N m_i r_i^2$ by the moment of inertia $I$.

**Applicability & Limiting Conditions**:
- Valid for rotation about a fixed axis in an inertial frame.
- Valid about an axis passing through the center of mass even if the center of mass is accelerating.
- Invalid for an accelerating non-CM point unless pseudo-force torque is included.


---

## Angular Momentum of a Particle About Fixed Reference Points

> **Pedagogical Goal**: Define angular momentum as a cross product L = r x p and deconstruct the misconception that rectilinear uniform or accelerated motion implies zero angular momentum.


---

### Concept: Angular Momentum of a Particle About a Reference Point

**Definition**: The angular momentum $\vec{L}_O$ of a point particle of mass $m$ and linear momentum $\vec{p} = m \vec{v}$ with respect to a specified origin $O$ is defined as $\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$, where $\vec{r}$ is the instantaneous position vector of the particle from $O$. The magnitude is given by $L_O = m v r \sin\theta = m v r_\perp = p r_\perp$, where $r_\perp$ is the perpendicular distance (impact parameter) from $O$ to the line of the velocity vector. SI unit is $\text{kg}\cdot\text{m}^2/\text{s} = \text{J}\cdot\text{s}$, with dimensions $[M L^2 T^{-1}]$.

**Physical Significance**: Imagine standing beside a straight high-speed railway track watching a bullet train glide past at constant speed. Even though the train travels in a straight line, your head must continuously turn to follow it. The rate at which your line of sight sweeps out area measures the train's rotational tendency about your location. If you stood directly on the track in front of the train, no turning of your head would be required ($r_\perp = 0$). Hence, angular momentum is fundamentally an observer-dependent geometric relationship between linear momentum and a chosen pivot.

**Assumptions & Scope of Validity**:
- The particle is treated as a classical point mass.
- The origin $O$ is defined in an inertial reference frame.
- Non-relativistic velocities ($v \ll c$).


---

### Formula: Particle Angular Momentum

**Governing Equation**:
$$ \vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v}) $$

**Variable Inventory & SI Units**:
- $L_O$: Angular momentum about origin O (Unit: `kg m^2/s` | Dim: `[M][L]^2[T]^-1`)
- $r$: Position vector from origin O to particle (Unit: `m` | Dim: `[L]`)
- $p$: Linear momentum vector (Unit: `kg m/s` | Dim: `[M][L][T]^-1`)
- $m$: Particle mass (Unit: `kg` | Dim: `[M]`)
- $v$: Particle velocity vector (Unit: `m/s` | Dim: `[L][T]^-1`)

**Physical Assumptions**:
- Point mass particle
- Reference point O is explicitly specified in an inertial frame

**Domain of Validity**:
- Universal definition for point mass particle in classical mechanics


---

### Derivation: Formula `formula-rot-angmom-particle`

**Target Governing Relation**:
$$ $$\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$$ $$

#### Step-by-Step Proof
**Step 1**: Define the instantaneous position and linear momentum of a particle relative to a chosen reference origin $O$.
$$ $$\vec{p} = m \vec{v}$$ $$
*Physical Operation*: Specify the particle's mass $m$ and position vector $\vec{r}$ measured from origin $O$. Define linear momentum $\vec{p} = m \vec{v} = m \frac{d\vec{r}}{dt}$.

**Step 2**: Formulate the moment of momentum (angular momentum) $\vec{L}_O$ as the vector cross product of position and linear momentum.
$$ $$\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$$ $$
*Physical Operation*: Take the vector cross product of position vector $\vec{r}$ with linear momentum $\vec{p}$: $\vec{L}_O = \vec{r} \times \vec{p} = \vec{r} \times (m \vec{v})$.

**Step 3**: Differentiate the angular momentum vector with respect to time to verify dynamic consistency with Newton's second law.
$$ $$\frac{d\vec{L}_O}{dt} = (\vec{v} \times \vec{p}) + \left(\vec{r} \times \frac{d\vec{p}}{dt}\right)$$ $$
*Physical Operation*: Apply the product rule of vector calculus: $\frac{d\vec{L}_O}{dt} = \frac{d}{dt}(\vec{r} \times \vec{p}) = \left(\frac{d\vec{r}}{dt} \times \vec{p}\right) + \left(\vec{r} \times \frac{d\vec{p}}{dt}\right)$.

**Step 4**: Evaluate the first term $\vec{v} \times \vec{p}$ using the definition of linear momentum.
$$ $$\vec{v} \times \vec{p} = \vec{0}$$ $$
*Physical Operation*: Factor out mass $m$: $\vec{v} \times (m \vec{v}) = m (\vec{v} \times \vec{v})$. Since the cross product of any vector with itself is identically zero, this term vanishes.

**Step 5**: Substitute Newton's second law $\frac{d\vec{p}}{dt} = \vec{F}_{\text{net}}$ into the second term to prove $\frac{d\vec{L}_O}{dt} = \vec{\tau}_O$.
$$ $$\frac{d\vec{L}_O}{dt} = \vec{\tau}_O$$ $$
*Physical Operation*: Replace $\frac{d\vec{p}}{dt}$ with $\vec{F}_{\text{net}}$: $\frac{d\vec{L}_O}{dt} = \vec{r} \times \vec{F}_{\text{net}} = \vec{\tau}_O$, verifying foundational dynamical consistency.

**Step 6**: Compute the scalar magnitude of angular momentum in terms of the impact parameter $r_\perp$.
$$ $$L_O = m v r_\perp = p r_\perp$$ $$
*Physical Operation*: Calculate magnitude: $|\vec{L}_O| = m |\vec{r}||\vec{v}|\sin\theta = m v (r \sin\theta) = m v r_\perp = p r_\perp$, where $r_\perp = r \sin\theta$ is the perpendicular distance from $O$ to the line of motion.

**Applicability & Limiting Conditions**:
- Applies to any point mass particle moving along an arbitrary trajectory in 3D space.
- Reference point $O$ must be explicitly specified.
- Valid in an inertial reference frame.


---

### Inoculation Against Misconception: `misc-rot-01`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"A particle moving along a straight line at constant velocity has zero angular momentum because angular momentum only exists for bodies rotating in circles or curved paths."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Angular momentum is not an intrinsic property of a trajectory; it is defined strictly relative to a chosen reference point O as L_O = r x p. Any particle whose line of motion does not pass through O has a non-zero perpendicular distance r_perp, yielding a non-zero, conserved angular momentum even during uniform rectilinear motion.

**Physical Truth & Resolution**:
The angular momentum of a particle of mass $m$ with linear momentum $\vec{p} = m\vec{v}$ relative to a chosen origin $O$ is defined as the cross product $\vec{L}_O = \vec{r} \times \vec{p}$, where $\vec{r}$ is the position vector from $O$ to the particle. Its magnitude is given by $L_O = m v r \sin\phi = m v r_\perp$, where $r_\perp$ is the perpendicular distance (impact parameter) from the reference point $O$ to the particle's line of motion. As long as the line of motion does not intersect point $O$ ($r_\perp \neq 0$), the particle possesses non-zero angular momentum about $O$. Furthermore, if the particle moves at constant velocity (zero net external force), $\vec{\tau}_O = \vec{r} \times \vec{F} = 0$, which proves via Newton's second law for rotation that $\vec{L}_O$ is strictly conserved in both magnitude and direction throughout the linear motion.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 1, Chapter 10 (Rotational Mechanics), Section 10.15: 'Angular Momentum of a Particle'; Halliday, Resnick, Walker, Fundamentals of Physics, Section 11-6; Question rotational-motion-question-6c7cb960.

**Diagnostic Symptom**: Student sets L = 0 whenever a particle moves in a straight line, or claims angular momentum can only be computed if a physical axle or circular orbit is present.


---

### Verified JEE Practice Problem: `rotational-motion-question-6c7cb960`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Conservation of Angular Momentum and Systems with Variable Inertia

> **Pedagogical Goal**: Analyze rotational systems under zero external torque, derive angular velocity scaling for variable mass distributions, and contrast angular momentum conservation with non-conservation of mechanical kinetic energy.


---

### Concept: Conservation of Angular Momentum and Systems with Variable Inertia

**Definition**: If the net external torque acting on a system about a fixed axis or point $O$ is zero ($\vec{\tau}_{\text{ext}, O} = \vec{0}$), the total angular momentum of the system about that point remains constant in time: $\frac{d\vec{L}_{\text{total}}}{dt} = \vec{0} \implies \vec{L}_{\text{total}} = \text{constant}$. For rotation about a fixed axis $z$ where $\tau_{\text{ext}, z} = 0$, this implies $I_i \omega_i = I_f \omega_f$.

**Physical Significance**: A spinning figure skater pulls their outstretched arms and leg inward toward their body. Without pushing off the ice, their rotational speed dramatically surges. By pulling their limbs inward, the skater decreases their moment of inertia ($I$). Because no external twisting force (torque) acts on them, their angular momentum $L = I \omega$ must remain invariant, forcing the angular speed $\omega$ to increase. Interestingly, the skater does mechanical work using internal muscle contraction, which increases their rotational kinetic energy $K_{\text{rot}} = \frac{L^2}{2I}$.

**Assumptions & Scope of Validity**:
- Net external torque about the reference axis or point is strictly zero.
- For fixed-axis scalar application, the axis is an inertial axis of symmetry or fixed axis of rotation.
- Internal forces satisfy Newton's third law in strong form.


---

### Formula: Conservation of Angular Momentum About Fixed Axis

**Governing Equation**:
$$ I_i \omega_i = I_f \omega_f $$

**Variable Inventory & SI Units**:
- $I_i$: Initial moment of inertia about axis
- $\omega_i$: Initial angular velocity
- $I_f$: Final moment of inertia about axis
- $\omega_f$: Final angular velocity

**Physical Assumptions**:
- Net external torque about the designated rotation axis vanishes (\tau_{\text{ext}, z} = 0)

**Domain of Validity**:
- Valid for isolated systems or systems with zero net torque along a specific axis


---

### Derivation: Formula `formula-rot-conservation-angmom`

**Target Governing Relation**:
$$ $$I_i \omega_i = I_f \omega_f$$ $$

#### Step-by-Step Proof
**Step 1**: State the fundamental dynamical equation relating external torque to the rate of change of total angular momentum.
$$ $$\tau_{\text{net, ext}, z} = \frac{dL_z}{dt}$$ $$
*Physical Operation*: Project the vector equation onto the fixed axis of rotation (taken as the $z$-axis): $\tau_{\text{net, ext}, z} = \frac{dL_z}{dt}$.

**Step 2**: Apply the physical condition of zero net external torque along the rotation axis.
$$ $$\frac{dL_z}{dt} = 0 \implies L_z(t) = \text{constant}$$ $$
*Physical Operation*: Set $\tau_{\text{net, ext}, z} = 0$, giving $\frac{dL_z}{dt} = 0$.

**Step 3**: Integrate the rate equation between initial state ($t_i$) and final state ($t_f$).
$$ $$L_{z, i} = L_{z, f}$$ $$
*Physical Operation*: Integrate both sides from $t_i$ to $t_f$: $\int_{t_i}^{t_f} \frac{dL_z}{dt} \, dt = 0 \implies L_z(t_f) - L_z(t_i) = 0$.

**Step 4**: Substitute the constitutive relationship for fixed-axis rotation $L_z = I \omega$ at both states.
$$ $$I_i \omega_i = I_f \omega_f$$ $$
*Physical Operation*: Substitute initial state $L_{z, i} = I_i \omega_i$ and final state $L_{z, f} = I_f \omega_f$ into the conservation relation.

**Step 5**: Solve for the final angular velocity in terms of the initial state and the ratio of moments of inertia.
$$ $$\omega_f = \frac{I_i}{I_f} \omega_i$$ $$
*Physical Operation*: Divide both sides by $I_f$ (where $I_f > 0$): $\omega_f = \left(\frac{I_i}{I_f}\right) \omega_i$.

**Step 6**: Examine the non-conservation of rotational kinetic energy to verify physical work-energy consistency.
$$ $$K_f = \frac{I_i}{I_f} K_i,\quad \Delta K_{\text{rot}} = W_{\text{internal}}$$ $$
*Physical Operation*: Express kinetic energy ratio using constant $L$: $\frac{K_f}{K_i} = \frac{I_i}{I_f}$. If moment of inertia decreases ($I_f < I_i$), kinetic energy increases: $\Delta K = K_f - K_i = W_{\text{internal}} > 0$.

**Applicability & Limiting Conditions**:
- Net external torque along the axis of rotation must be zero during the entire transition.
- Does not require mechanical energy conservation.
- Applies to deformable bodies, coupled spinning discs, or systems with internal radial motion.


---

### Worked Pedagogical Example: `ex-rot-angmom-disc-01`

**Problem Statement**:
> A uniform thin circular disc of mass $M$ and radius $R$ is rotating freely in a horizontal plane about a frictionless fixed vertical axis passing through its center with initial angular velocity $\omega_0$. An insect of mass $m = \frac{M}{2}$, initially at the center of the disc ($r = 0$), starts crawling radially outward along a marked radius on the disc at a constant speed $u$ relative to the disc until it reaches the outer periphery ($r = R$).
(a) Determine the angular velocity $\omega(r)$ of the disc as a function of the radial distance $r \in [0, R]$ of the insect from the center.
(b) Find the angular velocity $\omega(R)$ when the insect reaches the outer rim $r = R$.
(c) Evaluate the ratio of the rotational kinetic energy of the system when the insect is at the rim ($r = R$) to its initial rotational kinetic energy ($r = 0$), and provide the physical explanation for any discrepancy in mechanical energy.

**Target Quantity**: `\omega(r), \omega(R), \text{ and } K_{\text{rot}}(R) / K_{\text{rot}}(0)`

#### Systematic Solution
**Step 1 (Torque analysis and conservation of angular momentum)**:
$$ \tau_{z, \text{ext}} = \frac{dL_z}{dt} = 0 \implies L_z = \text{constant} $$
\tau_{z, \text{ext}} = 0
Result: `Total angular momentum L_z about the central vertical axis is conserved throughout the motion.`

**Step 2 (System moment of inertia as a function of radial coordinate)**:
$$ I(r) = I_{\text{disc}} + m r^2 = \frac{1}{2} M R^2 + \left(\frac{M}{2}\right) r^2 = \frac{1}{2} M (R^2 + r^2) $$
I(0) = \frac{1}{2} M R^2, \quad I(R) = \frac{1}{2} M R^2 + \frac{1}{2} M R^2 = M R^2
Result: `Initial inertia I_0 = (1/2) M R^2; final inertia at rim I_f = M R^2 (inertia doubles).`

**Step 3 (Equating initial and instantaneous angular momentum)**:
$$ I(r) \omega(r) = I(0) \omega_0 \implies \frac{1}{2} M (R^2 + r^2) \omega(r) = \frac{1}{2} M R^2 \omega_0 $$
\omega(r) = \frac{R^2}{R^2 + r^2} \omega_0, \quad \omega(R) = \frac{R^2}{R^2 + R^2} \omega_0 = \frac{1}{2} \omega_0
Result: `\omega(r) = \frac{R^2}{R^2 + r^2} \omega_0; \quad \omega(R) = \frac{\omega_0}{2}`

**Step 4 (Rotational kinetic energy ratio evaluation)**:
$$ K_{\text{rot}}(r) = \frac{1}{2} I(r) [\omega(r)]^2 = \frac{L_z^2}{2 I(r)} $$
\frac{K_{\text{rot}}(R)}{K_{\text{rot}}(0)} = \frac{I_0}{I(R)} = \frac{\frac{1}{2} M R^2}{M R^2} = \frac{1}{2}
Result: `The rotational kinetic energy ratio is exactly 1/2 (50% reduction in rotational kinetic energy).`

**Step 5 (Dynamic torque and internal non-conservative work accounting)**:
$$ F_{\text{cor}} = 2 m \omega u, \quad \tau_{\text{internal}} = - r F_{\text{cor}} = - 2 m \omega u r, \quad W_{\text{insect}} = \Delta K_{\text{rot}} = -\frac{1}{8} M R^2 \omega_0^2 $$
\Delta K_{\text{rot}} = \frac{1}{8} M R^2 \omega_0^2 - \frac{1}{4} M R^2 \omega_0^2 = -\frac{1}{8} M R^2 \omega_0^2
Result: `Mechanical kinetic energy is not conserved; 50% is dissipated/absorbed through internal muscular action.`

**Final Answer**: \omega(r) = \frac{R^2}{R^2 + r^2} \omega_0; \quad \omega(R) = \frac{\omega_0}{2}; \quad \frac{K_{\text{rot}}(R)}{K_{\text{rot}}(0)} = \frac{1}{2}

**Sanity & Consistency Checks**:
- Limiting case r -> 0: \omega(0) = [R^2 / (R^2 + 0)] \omega_0 = \omega_0, recovering the initial undisturbed state.
- Limiting case m -> 0: If the insect is massless, \omega(r) = \omega_0 for all r, confirming zero perturbation from a massless crawler.
- Monotonicity: d\omega / dr = - [2 r R^2 \omega_0] / (R^2 + r^2)^2 < 0 for all r > 0, ensuring angular velocity strictly decreases as mass moves outward.
- Dimensional homogeneity: [\omega(r)] = [\omega_0] = T^{-1}, since R^2 / (R^2 + r^2) is dimensionless.


---

### Inoculation Against Misconception: `misc-rot-02`

**Misconception Category**: `WRONG_CONSERVATION_LAW`  
**Erroneous Intuition**: *"When a system conserves angular momentum under zero external torque, its rotational kinetic energy must also remain conserved."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Rotational kinetic energy is K_rot = L^2 / (2 I). When mass moves radially, moment of inertia I changes while L remains constant, so K_rot scales inversely with I. Internal muscular forces or sliding friction do work, causing mechanical kinetic energy to change dramatically despite perfect conservation of angular momentum.

**Physical Truth & Resolution**:
Conservation of angular momentum requires only that the net external torque about the axis of rotation is zero: $\tau_{\text{ext}} = 0 \implies L = I \omega = \text{constant}$. In contrast, mechanical kinetic energy conservation requires that the net work done by all non-conservative forces (both external AND internal) is zero: $W_{\text{nc, ext}} + W_{\text{nc, int}} = 0$. Rotational kinetic energy can be expressed directly in terms of angular momentum as $K_{\text{rot}} = \frac{1}{2} I \omega^2 = \frac{L^2}{2I}$. If the mass distribution of the system reconfigures internally (such as a figure skater pulling in their limbs, an insect crawling outward on a turntable, or two rotating discs clutching via friction), the moment of inertia changes from $I_1$ to $I_2$. Because $L$ is constant, $K_{\text{rot}} \propto \frac{1}{I}$. If $I$ decreases, $K_{\text{rot}}$ increases (the extra energy is supplied by positive internal muscular work done against centrifugal forces). If $I$ increases, $K_{\text{rot}}$ decreases (energy is dissipated or absorbed by internal non-conservative work). Thus, conservation of angular momentum does NOT imply conservation of kinetic energy.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 1, Section 10.18: 'Conservation of Angular Momentum'; I.E. Irodov, Problems in General Physics, Problem 1.258; Questions rotational-motion-question-84f91c20 and rotational-motion-question-f7cbecda.

**Diagnostic Symptom**: Student sets initial KE equal to final KE in problems involving changing rotational inertia (e.g., student solving for final angular velocity by writing (1/2) I1 w1^2 = (1/2) I2 w2^2).


---

### Verified JEE Practice Problem: `rotational-motion-question-84f91c20`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

### Verified JEE Practice Problem: `rotational-motion-question-f7cbecda`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Pure Rolling Kinematics and Energy Methods

> **Pedagogical Goal**: Connect translational and rotational kinematics under the non-slip constraint v_cm = R omega, analyze instantaneous center of rotation, and formulate combined kinetic energy.


---

## Chapter Summary & Formula Recap: Rotational Motion

### Core Equations & Domains of Validity
- **Parallel Axis Theorem**: $$I = I_{\text{cm}} + M d^2$$
  *Validity*: One axis must pass strictly through the center of mass
- **Fixed Axis Rotational Dynamics**: $$\tau_{\text{net, ext}} = I \alpha$$
  *Validity*: Valid about a fixed inertial axis or about the center of mass even if accelerating
- **Angular Momentum of a Particle**: $$\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$$
  *Validity*: Valid for any particle trajectory in 3D Euclidean space
- **Conservation of Angular Momentum About Fixed Axis**: $$I_i \omega_i = I_f \omega_f$$
  *Validity*: Net external torque component along the axis of rotation must be zero (tau_ext,z = 0)
