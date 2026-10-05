# Chapter: Rotational Motion and Rigid Body Dynamics

**Template**: `MECHANICS`  
**Prerequisites**: curr-kin-02, curr-com-01, curr-nl-01, curr-wep-02  

## Learning Objectives
- Calculate moment of inertia for discrete point masses and continuous bodies using integration and the parallel/perpendicular axis theorems.
- Formulate rotational equations of motion tau = I alpha and apply work-energy principles to fixed axis rotation.
- Determine the angular momentum of particles and rigid bodies about fixed reference points and instantaneous axes of rotation.
- Apply the principle of conservation of angular momentum to isolated systems with time-varying moments of inertia.
- Analyze pure rolling kinematics and dynamics on horizontal and inclined surfaces under static friction constraints.
- Determine critical conditions for sliding versus toppling of rigid bodies on rough planes.

---

## Moment of Inertia, Radius of Gyration, and Axis Theorems

> **Pedagogical Goal**: Define moment of inertia for discrete and continuous systems, establish the radius of gyration, and derive both parallel and perpendicular axis theorems with rigorous planar/3D applicability constraints.


---

### Concept: Moment of Inertia as Rotational Analogue of Mass

**Definition**: For a rigid system of discrete particles of masses $m_i$ at perpendicular distances $r_i$ from a specified axis of rotation, the moment of inertia $I$ is defined as $I = \sum_{i} m_i r_i^2$. For a continuous body of mass density $\rho(\vec{r})$ occupying volume $V$, the moment of inertia is the volume integral $I = \int_{V} r_\perp^2 \, dm = \int_{V} r_\perp^2 \rho(\vec{r}) \, dV$, where $r_\perp$ is the perpendicular distance of the infinitesimal mass element $dm$ from the rotation axis. Its SI unit is $\text{kg}\cdot\text{m}^2$, with dimensions $[M L^2]$.

**Physical Significance**: Imagine trying to rotate a heavy dumbbell. If the masses are close to your hand along the axis of rotation, twisting it back and forth is effortless. If the masses are moved outward to the far ends of the rod, twisting it becomes substantially harder—even though the total mass has not changed. This demonstrates that in rotational dynamics, how far the mass is distributed from the axis of rotation ($r$) matters far more than just how much mass there is, scaling quadratically as $r^2$.

**Assumptions & Scope of Validity**:
- The body is perfectly rigid, such that pairwise distances between particles remain invariant under rotation.
- The rotation axis is fixed in orientation or passes through the center of mass in a principal inertial frame.
- Classical non-relativistic regime where mass is constant and Euclidean geometry applies.


---

### Concept: Moment of Inertia of Continuous Rigid Bodies via Spatial Mass Integration

**Definition**: The second moment of the mass distribution of a continuous rigid body with respect to a line axis $L$: $$I_L \equiv \iiint_V r_\perp^2 \rho(\vec{r}) \, dV$$ where $r_\perp$ is the Euclidean distance from the element $dV$ to the line $L$.

**Physical Significance**: Moment of inertia measures how difficult it is to alter a body's angular velocity. Because mass elements contribute with the square of their radial distance from the axis ($r^2$), mass positioned far from the rotation axis contributes disproportionately more to rotational inertia than mass packed near the rotation axis.

**Assumptions & Scope of Validity**:
- Rigid body with invariant spatial distance between all constituent mass points
- Homogeneous mass distribution with constant density
- Specified geometric symmetry axes passing through centroid


---

### Formula: Moment of Inertia of Discrete Point Masses

**Governing Equation**:
$$ I = \sum_{i=1}^N m_i r_i^2 $$

**Variable Inventory & SI Units**:
- $I$: Moment of inertia about the specified axis (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $m_i$: Mass of the i-th particle (Unit: `kg` | Dim: `[M]`)
- $r_i$: Perpendicular distance of the i-th particle from the axis (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Point mass particles with negligible individual extents
- Strictly perpendicular radial distances measured from the rotation axis
- Rigid spatial configuration among all particles

**Domain of Validity**:
- Universal definition for any finite system of discrete particles in classical mechanics


---

### Formula: Moments of Inertia for Standard Symmetrical Continuous Rigid Bodies

**Governing Equation**:
$$ I_{\text{ring}} = M R^2, \quad I_{\text{disc}} = \frac{1}{2} M R^2, \quad I_{\text{rod}} = \frac{1}{12} M L^2, \quad I_{\text{solid sphere}} = \frac{2}{5} M R^2, \quad I_{\text{hollow sphere}} = \frac{2}{3} M R^2 $$

**Variable Inventory & SI Units**:
- $M$: Total mass of the rigid body (Unit: `kg` | Dim: `[M]`)
- $R$: Radius of circular cross-section or sphere (Unit: `m` | Dim: `[L]`)
- $L$: Total length of uniform rod (Unit: `m` | Dim: `[L]`)
- $I$: Centroidal principal moment of inertia (Unit: `kg m^2` | Dim: `[M][L]^2`)

**Physical Assumptions**:
- Uniform homogeneous mass distribution with constant density
- Axes pass through centroid along principal symmetry directions
- Thin rod and thin spherical shell approximations where wall thicknesses are negligible

**Domain of Validity**:
- Applies strictly to symmetric uniform bodies about their designated centroidal axes


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

### Formula: Perpendicular Axis Theorem for Planar Laminas

**Governing Equation**:
$$ I_z = I_x + I_y $$

**Variable Inventory & SI Units**:
- $I_z$: Moment of inertia about normal axis perpendicular to lamina through origin O (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $I_x$: Moment of inertia about coplanar x-axis passing through O (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $I_y$: Moment of inertia about coplanar y-axis passing through O (Unit: `kg m^2` | Dim: `[M][L]^2`)

**Physical Assumptions**:
- Rigid body is strictly a two-dimensional planar lamina lying entirely in the xy-plane (z = 0)
- All three axes x, y, and z are mutually perpendicular and intersect at a single concurrent origin O

**Domain of Validity**:
- Strictly valid ONLY for two-dimensional planar laminar bodies; fails identically for three-dimensional bodies


---

### Derivation: Formula `formula-rot-moi-perpendicular`

**Target Governing Relation**:
$$ I_z = I_x + I_y $$

#### Step-by-Step Proof
**Step 1**: Establish coordinate frame and express position of mass element
$$ z = 0 \quad \forall \, dm $$
*Physical Operation*: Identify Cartesian coordinates of differential mass element dm in the lamina plane

**Step 2**: Formulate moments of inertia about the coplanar x and y axes
$$ I_x = \int y^2 \, dm, \quad I_y = \int x^2 \, dm $$
*Physical Operation*: Determine perpendicular distance to x-axis (|y|) and y-axis (|x|)

**Step 3**: Formulate moment of inertia about perpendicular z-axis through origin
$$ r_z^2 = x^2 + y^2 \implies I_z = \int (x^2 + y^2) \, dm $$
*Physical Operation*: Express perpendicular distance r_z from z-axis using Pythagorean theorem in xy plane

**Step 4**: Distribute integral by linearity and substitute coplanar definitions
$$ I_z = \int x^2 \, dm + \int y^2 \, dm = I_y + I_x $$
*Physical Operation*: Apply linearity of integration: int (x^2 + y^2) dm = int x^2 dm + int y^2 dm

**Step 5**: Conclude perpendicular axis theorem and state dimensional equivalence
$$ I_z = I_x + I_y $$
*Physical Operation*: Commutative rearrangement

**Applicability & Limiting Conditions**:
- Strictly restricted to two-dimensional planar laminas
- Fails identically for any 3D body with non-zero z-thickness because r_x^2 = y^2 + z^2 and r_y^2 = x^2 + z^2 lead to I_x + I_y = I_z + 2 int z^2 dm != I_z


---

### Formula: Radius of Gyration

**Governing Equation**:
$$ k = \sqrt{\frac{I}{M}} \iff I = M k^2 $$

**Variable Inventory & SI Units**:
- $k$: Radius of gyration about the specified axis (Unit: `m` | Dim: `[L]`)
- $I$: Moment of inertia about the specified axis (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $M$: Total mass of the rigid body (Unit: `kg` | Dim: `[M]`)

**Physical Assumptions**:
- Rigid body of total mass M
- Specified fixed axis of rotation

**Domain of Validity**:
- Universal geometric definition representing the effective distance at which whole mass could be concentrated


---

### Worked Pedagogical Example: `ex-rot-moi-disc-cavity-01`

**Problem Statement**:
> A uniform thin circular disc of total mass $M$ and radius $R$ has a circular hole of radius $R/2$ cut out of it. The circular hole is positioned such that its rim touches the center of the original disc and the rim of the original disc (meaning the center of the cut-out hole is located at $x = R/2, y = 0$). Calculate the moment of inertia of the remaining portion of the disc about a perpendicular axis passing through the original center of the disc $O$.

**Target Quantity**: `Moment of inertia I_rem of the remaining disc about perpendicular central axis through O`

#### Systematic Solution
**Step 1 (Mass-area relationship for uniform surface density)**:
$$ A_{\text{orig}} = \pi R^2, \quad A_{\text{hole}} = \pi (R/2)^2 = \frac{1}{4} \pi R^2, \quad A_{\text{rem}} = \frac{3}{4} \pi R^2 $$
M_0 = \sigma \pi R^2, \quad m_{\text{hole}} = \frac{1}{4} M_0, \quad M = M_0 - m_{\text{hole}} = \frac{3}{4} M_0
Result: `M_0 = \frac{4}{3} M, \quad m_{\text{hole}} = \frac{1}{3} M`

**Step 2 (Moment of inertia of complete disc about central axis)**:
$$ I_{\text{orig}, O} = \frac{1}{2} M_0 R^2 $$
I_{\text{orig}, O} = \frac{1}{2} \left( \frac{4}{3} M \right) R^2 = \frac{2}{3} M R^2
Result: `I_{\text{orig}, O} = \frac{2}{3} M R^2`

**Step 3 (Parallel axis theorem for the removed circular hole about O)**:
$$ I_{\text{hole}, O} = I_{\text{cm, hole}} + m_{\text{hole}} d^2 = \frac{1}{2} m_{\text{hole}} (R/2)^2 + m_{\text{hole}} (R/2)^2 = \frac{3}{8} m_{\text{hole}} R^2 $$
I_{\text{hole}, O} = \frac{3}{8} \left( \frac{1}{3} M \right) R^2 = \frac{1}{8} M R^2
Result: `I_{\text{hole}, O} = \frac{1}{8} M R^2`

**Step 4 (Superposition subtraction for cavity)**:
$$ I_{\text{rem}, O} = I_{\text{orig}, O} - I_{\text{hole}, O} $$
I_{\text{rem}, O} = \frac{2}{3} M R^2 - \frac{1}{8} M R^2 = \left( \frac{16 - 3}{24} \right) M R^2 = \frac{13}{24} M R^2
Result: `I_{\text{rem}, O} = \frac{13}{24} M R^2`

**Final Answer**: \frac{13}{24} M R^2

**Sanity & Consistency Checks**:
- Fractional check: 13/24 = 0.5417. Notice 0.50 M R^2 < 13/24 M R^2 < 0.667 M R^2, physically sound because mass is removed near the center so remaining mass is weighted farther from O than in a complete disc of mass M (which would have 0.50 M R^2).
- Dimensional check: [M][L]^2 confirmed.


---

### Inoculation Against Misconception: `misc-rot-03`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"The perpendicular axis theorem I_z = I_x + I_y applies to any rigid body, including three-dimensional solid spheres and cylinders, as long as the three axes are mutually perpendicular."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> For a true three-dimensional body with non-zero z-coordinates, the perpendicular distances to the x, y, and z axes are r_x^2 = y^2 + z^2, r_y^2 = x^2 + z^2, and r_z^2 = x^2 + y^2. Summing I_x and I_y gives int (x^2 + y^2 + 2 z^2) dm = I_z + 2 int z^2 dm != I_z. The theorem holds strictly if and only if z = 0 identically for all mass elements, which is the definition of a two-dimensional planar lamina.

**Physical Truth & Resolution**:
Use the perpendicular axis theorem only for thin flat sheets and planar laminas. For three-dimensional bodies, use the parallel axis theorem or direct volume integration.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma Vol 1, Chapter 10, Section 10.6; Halliday, Resnick & Walker, Chapter 10, Section 10.5.

**Diagnostic Symptom**: Student attempts to find the moment of inertia of a solid cylinder or sphere about its diameter using I_z = I_x + I_y.


---

## Torque, Fixed-Axis Dynamics, and Rotational Work-Energy

> **Pedagogical Goal**: Formalize vector torque and couples, establish angular kinematic relations, prove the fundamental rotational dynamic relation tau_net = I alpha, and formulate rotational kinetic energy and the work-energy theorem.


---

### Concept: Torque and Fixed-Axis Rotational Dynamics

**Definition**: The torque $\vec{\tau}_O$ of a force $\vec{F}$ acting at a position $\vec{r}$ relative to a reference point $O$ is defined as the cross product $\vec{\tau}_O = \vec{r} \times \vec{F}$. For a rigid body constrained to rotate about a fixed axis $z$, the net external torque component along the axis is directly proportional to the body's angular acceleration $\alpha$ about that axis: $\tau_{\text{net}, z} = I_z \alpha$, where $I_z$ is the moment of inertia about the axis. SI unit is $\text{N}\cdot\text{m}$, with dimensions $[M L^2 T^{-2}]$.

**Physical Significance**: When pushing a heavy door open, pushing near the hinges requires enormous force and barely produces rotation, whereas pushing at the outer edge near the handle easily swings the door open. Furthermore, pushing parallel to the door face produces no turning effect whatsoever. The rotational effectiveness of a force depends not merely on its magnitude, but on its lever arm perpendicular to the rotation axis: $\tau = r_\perp F$.

**Assumptions & Scope of Validity**:
- The body maintains rigid geometry during rotational motion.
- The rotation axis is fixed in an inertial frame, or is a principal axis through the accelerating center of mass.
- Interatomic forces satisfy Newton's third law in central (strong) form, ensuring internal torques sum to zero.


---

### Concept: Rotational Work, Kinetic Energy, and the Rotational Work-Energy Theorem

**Definition**: The kinetic energy associated with pure rotation of a rigid body about a fixed axis with angular velocity $\omega$: $$K_{\text{rot}} = \frac{1}{2} I \omega^2$$ and the net work done by torques on the body equals its change in rotational kinetic energy: $W_{\text{net}} = \Delta K_{\text{rot}}$.

**Physical Significance**: Rotational kinetic energy is the rotational analogue of translational $\frac{1}{2} m v^2$, replacing mass $m$ with moment of inertia $I$ and linear speed $v$ with angular velocity $\omega$. Just as a linear force pushing an object over distance $dx$ does work $F dx$, a twisting torque turning an object through angle $d\theta$ does rotational work $\tau d\theta$.

**Assumptions & Scope of Validity**:
- Fixed axis of rotation in an inertial frame
- Rigid body condition ensuring identical angular velocity omega for all parts
- Negligible internal dissipative shear within the rigid body


---

### Formula: Definition and Moment Arm Representation of Torque

**Governing Equation**:
$$ \vec{\tau} = \vec{r} \times \vec{F} = r F \sin\theta \, \hat{n} = r_\perp F $$

**Variable Inventory & SI Units**:
- $\tau$: Torque vector about reference point O (Unit: `N m` | Dim: `[M][L]^2[T]^-2`)
- $r$: Position vector from reference point O to point of application of force (Unit: `m` | Dim: `[L]`)
- $F$: Applied force vector (Unit: `N` | Dim: `[M][L][T]^-2`)
- $\theta$: Angle between position vector r and force vector F
- $r_\perp$: Moment arm (perpendicular distance from O to line of action of force) (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Specified fixed reference origin O in an inertial reference frame
- Line of action of force is well-defined

**Domain of Validity**:
- Universal definition of moment of a force in classical mechanics


---

### Formula: Angular Kinematic Equations Under Constant Angular Acceleration

**Governing Equation**:
$$ \omega = \omega_0 + \alpha t, \quad \theta = \omega_0 t + \frac{1}{2} \alpha t^2, \quad \omega^2 = \omega_0^2 + 2 \alpha \theta $$

**Variable Inventory & SI Units**:
- $\omega$: Final angular velocity (Unit: `rad/s` | Dim: `[T]^-1`)
- $\omega_0$: Initial angular velocity (Unit: `rad/s` | Dim: `[T]^-1`)
- $\alpha$: Constant angular acceleration (Unit: `rad/s^2` | Dim: `[T]^-2`)
- $\theta$: Net angular displacement (Unit: `rad` | Dim: `[1]`)
- $t$: Elapsed time (Unit: `s` | Dim: `[T]`)

**Physical Assumptions**:
- Fixed rotation axis with invariant spatial orientation
- Constant angular acceleration alpha over the entire time interval

**Domain of Validity**:
- Strictly invalid if angular acceleration alpha varies with time or angle


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

### Formula: Rotational Kinetic Energy of a Rigid Body

**Governing Equation**:
$$ K_{\text{rot}} = \frac{1}{2} I \omega^2 $$

**Variable Inventory & SI Units**:
- $K_{\text{rot}}$: Rotational kinetic energy (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $I$: Moment of inertia about the axis of rotation (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $\omega$: Angular velocity of the rigid body (Unit: `rad/s` | Dim: `[T]^-1`)

**Physical Assumptions**:
- Rigid body rotating about a fixed axis or about a principal axis passing through center of mass
- Uniform angular velocity omega for all constituent mass elements

**Domain of Validity**:
- Universal relation for rigid body rotation in classical mechanics


---

### Derivation: Formula `formula-rot-ke-rotation`

**Target Governing Relation**:
$$ K_{\text{rot}} = \frac{1}{2} I \omega^2 $$

#### Step-by-Step Proof
**Step 1**: Express linear velocity of an arbitrary constituent mass element
$$ v_i = r_i \omega $$
*Physical Operation*: Evaluate magnitude for circular path perpendicular to fixed axis

**Step 2**: Sum the kinetic energies of all individual mass elements
$$ K_{\text{rot}} = \sum_{i=1}^N \frac{1}{2} m_i (r_i \omega)^2 = \sum_{i=1}^N \frac{1}{2} m_i r_i^2 \omega^2 $$
*Physical Operation*: Substitute v_i = r_i omega into the kinetic energy summation

**Step 3**: Factor out common angular velocity and pass to the continuous integral
$$ K_{\text{rot}} = \frac{1}{2} \left( \sum_{i=1}^N m_i r_i^2 \right) \omega^2 \xrightarrow{\text{continuous}} \frac{1}{2} \left( \int r_\perp^2 \, dm \right) \omega^2 $$
*Physical Operation*: Factor out constant 1/2 omega^2 across all mass points

**Step 4**: Identify the integral definition of moment of inertia
$$ K_{\text{rot}} = \frac{1}{2} I \omega^2 $$
*Physical Operation*: Substitute definition of moment of inertia I into kinetic energy expression

**Applicability & Limiting Conditions**:
- Applies strictly to pure rotation about a fixed axis or about a centroidal axis in the center-of-mass frame
- For combined translation and rotation, total kinetic energy is K_total = 1/2 M v_cm^2 + 1/2 I_cm omega^2


---

### Formula: Rotational Work-Energy Theorem

**Governing Equation**:
$$ W_{\text{net}} = \int_{\theta_1}^{\theta_2} \tau_{\text{net}}(\theta) \, d\theta = \frac{1}{2} I \omega_f^2 - \frac{1}{2} I \omega_i^2 = \Delta K_{\text{rot}} $$

**Variable Inventory & SI Units**:
- $W_{\text{net}}$: Net work done by external torques (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $\tau_{\text{net}}$: Net external torque about the rotation axis (Unit: `N m` | Dim: `[M][L]^2[T]^-2`)
- $\theta$: Angular displacement coordinate (Unit: `rad` | Dim: `[1]`)
- $I$: Moment of inertia about the fixed rotation axis (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $\omega_f$: Final angular velocity
- $\omega_i$: Initial angular velocity

**Physical Assumptions**:
- Rigid body rotating about a fixed axis in an inertial reference frame
- Work evaluated between initial angle theta_1 and final angle theta_2

**Domain of Validity**:
- Valid for any net torque function whether constant or angle-dependent


---

### Worked Pedagogical Example: `ex-rot-pulley-atwood-01`

**Problem Statement**:
> Two blocks of masses $m_1 = 3.0\text{ kg}$ and $m_2 = 1.0\text{ kg}$ are connected by a light inextensible string passing over a uniform solid cylindrical pulley of mass $M = 2.0\text{ kg}$ and radius $R = 0.10\text{ m}$. The pulley rotates about a frictionless horizontal axle through its center, and the string does not slip on the pulley rim. Taking $g = 9.80\text{ m/s}^2$, find: (a) the linear acceleration $a$ of the blocks, and (b) the string tensions $T_1$ and $T_2$ on each side of the pulley.

**Target Quantity**: `Linear acceleration a and tensions T_1, T_2`

#### Systematic Solution
**Step 1 (Newton's Second Law for descending block m_1)**:
$$ m_1 g - T_1 = m_1 a $$
3.0(9.80) - T_1 = 3.0 a \implies 29.40 - T_1 = 3.0 a
Result: `T_1 = 29.40 - 3.0 a`

**Step 2 (Newton's Second Law for ascending block m_2)**:
$$ T_2 - m_2 g = m_2 a $$
T_2 - 1.0(9.80) = 1.0 a \implies T_2 - 9.80 = 1.0 a
Result: `T_2 = 9.80 + 1.0 a`

**Step 3 (Rotational dynamic relation for pulley with no-slip constraint)**:
$$ \tau_{\text{net}} = (T_1 - T_2) R = I \alpha = \left( \frac{1}{2} M R^2 \right) \left( \frac{a}{R} \right) \implies T_1 - T_2 = \frac{1}{2} M a $$
T_1 - T_2 = \frac{1}{2} (2.0) a = 1.0 a
Result: `T_1 - T_2 = 1.0 a`

**Step 4 (System summation to solve for linear acceleration)**:
$$ (m_1 - m_2) g = \left( m_1 + m_2 + \frac{1}{2} M \right) a \implies a = \frac{(m_1 - m_2) g}{m_1 + m_2 + \frac{1}{2} M} $$
a = \frac{(3.0 - 1.0)(9.80)}{3.0 + 1.0 + 1.0} = \frac{19.60}{5.0} = 3.92\text{ m/s}^2
Result: `a = 3.92 m/s^2`

**Step 5 (Back-substitution for string tensions)**:
$$ T_1 = m_1 (g - a), \quad T_2 = m_2 (g + a) $$
T_1 = 3.0(9.80 - 3.92) = 3.0(5.88) = 17.64\text{ N}, \quad T_2 = 1.0(9.80 + 3.92) = 13.72\text{ N}
Result: `T_1 = 17.64 N, T_2 = 13.72 N`

**Final Answer**: a = 3.92 m/s^2, \quad T_1 = 17.64 N, \quad T_2 = 13.72 N

**Sanity & Consistency Checks**:
- Tension difference check: T_1 - T_2 = 17.64 - 13.72 = 3.92 N. Pulley inertial term: 1/2 M a = 1/2(2.0)(3.92) = 3.92 N. Exact match!
- Massless pulley limit: M -> 0 yields a = 2(9.8)/4 = 4.90 m/s^2, higher acceleration as expected.
- Tension hierarchy: m_1 g = 29.4 N > T_1 = 17.64 N > T_2 = 13.72 N > m_2 g = 9.8 N, completely consistent with downward acceleration of m_1 and upward acceleration of m_2.


---

### Inoculation Against Misconception: `misc-rot-04`

**Misconception Category**: `HIDDEN_CONSTRAINT_OMISSION`  
**Erroneous Intuition**: *"The tension in an ideal string remains uniform throughout its length even when passing over a real pulley with non-zero mass and moment of inertia."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> A massive pulley possesses rotational inertia I = 1/2 M R^2. By Newton's second law for rotation, an angular acceleration alpha requires a non-zero net external torque: tau_net = (T_1 - T_2) R = I alpha. If the string tensions on both sides were equal (T_1 = T_2), the net torque would be zero, making it physically impossible for the pulley to accelerate with the string without slipping.

**Physical Truth & Resolution**:
Whenever a pulley has mass or moment of inertia, the tensions on either side of the pulley must differ: T_1 - T_2 = (I / R^2) a. Only in the idealized limit of a massless pulley (I -> 0) does T_1 = T_2.

**Refutation Counterexample & Supporting Evidence**:
University Physics, Chapter 10, Example 10.3; H.C. Verma Vol 1, Chapter 10, Section 10.8.

**Diagnostic Symptom**: Student sets T_1 = T_2 in Atwood machines or hanging mass problems with massive pulleys, resulting in an erroneous system acceleration.


---

## Angular Momentum of Particles and Systems About Fixed Reference Points

> **Pedagogical Goal**: Define particle angular momentum as L = r x p with explicit origin dependence, analyze motion along straight and curved trajectories, and establish transformation laws to moving center-of-mass frames.


---

### Concept: Angular Momentum of a Particle About a Reference Point

**Definition**: The angular momentum $\vec{L}_O$ of a point particle of mass $m$ and linear momentum $\vec{p} = m \vec{v}$ with respect to a specified origin $O$ is defined as $\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$, where $\vec{r}$ is the instantaneous position vector of the particle from $O$. The magnitude is given by $L_O = m v r \sin\theta = m v r_\perp = p r_\perp$, where $r_\perp$ is the perpendicular distance (impact parameter) from $O$ to the line of the velocity vector. SI unit is $\text{kg}\cdot\text{m}^2/\text{s} = \text{J}\cdot\text{s}$, with dimensions $[M L^2 T^{-1}]$.

**Physical Significance**: Imagine standing beside a straight high-speed railway track watching a bullet train glide past at constant speed. Even though the train travels in a straight line, your head must continuously turn to follow it. The rate at which your line of sight sweeps out area measures the train's rotational tendency about your location. If you stood directly on the track in front of the train, no turning of your head would be required ($r_\perp = 0$). Hence, angular momentum is fundamentally an observer-dependent geometric relationship between linear momentum and a chosen pivot.

**Assumptions & Scope of Validity**:
- The particle is treated as a classical point mass.
- The origin $O$ is defined in an inertial reference frame.
- Non-relativistic velocities ($v \ll c$).


---

### Concept: Angular Momentum of Rigid Bodies and General Planar Decomposition

**Definition**: The angular momentum of an extended body about an origin O in terms of its center of mass motion: $$\vec{L}_O = \sum \vec{r}_i \times m_i \vec{v}_i = I_{\text{cm}} \vec{\omega} + \vec{r}_{\text{cm}} \times M \vec{v}_{\text{cm}}$$

**Physical Significance**: Total angular momentum about an external point consists of two parts: how the body spins about its own waist ($ec{L}_{\text{spin}} = I_{\text{cm}} \vec{\omega}$), plus how its center of mass sweeps out angle around the external pivot ($ec{L}_{\text{orbital}} = \vec{r}_{\text{cm}} \times \vec{P}$). Just like Earth has spin angular momentum (day-night cycle) and orbital angular momentum (orbiting the Sun).

**Assumptions & Scope of Validity**:
- Planar motion where angular velocity vector is perpendicular to motion plane
- Rigid body condition
- Reference point O is fixed in an inertial reference frame


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

### Formula: Angular Momentum of Rigid Body in Planar Motion About Arbitrary Origin

**Governing Equation**:
$$ \vec{L}_O = I_{\text{cm}} \vec{\omega} + \vec{r}_{\text{cm}} \times M \vec{v}_{\text{cm}} $$

**Variable Inventory & SI Units**:
- $\vec{L}_O$: Total angular momentum vector about reference origin O (Unit: `kg m^2/s` | Dim: `[M][L]^2[T]^-1`)
- $I_{\text{cm}}$: Moment of inertia about principal axis through center of mass (Unit: `kg m^2` | Dim: `[M][L]^2`)
- $\vec{\omega}$: Angular velocity vector of the rigid body (Unit: `rad/s` | Dim: `[T]^-1`)
- $\vec{r}_{\text{cm}}$: Position vector of center of mass relative to origin O (Unit: `m` | Dim: `[L]`)
- $M$: Total mass of the rigid body (Unit: `kg` | Dim: `[M]`)
- $\vec{v}_{\text{cm}}$: Linear velocity vector of center of mass (Unit: `m/s` | Dim: `[L][T]^-1`)

**Physical Assumptions**:
- Planar motion where angular velocity vector is perpendicular to the translational plane
- Rigid body condition with constant mass M
- Origin O is an unaccelerated fixed reference point in an inertial frame

**Domain of Validity**:
- Universal decomposition of angular momentum into spin and orbital components for general plane motion


---

### Worked Pedagogical Example: `ex-rot-projectile-angmom-01`

**Problem Statement**:
> A projectile of mass $m = 0.50\text{ kg}$ is fired from the origin $O$ on flat ground with initial speed $v_0 = 20.0\text{ m/s}$ at an angle $\theta = 60.0^\circ$ above the horizontal. Taking $g = 10.0\text{ m/s}^2$ downward along the $-y$ axis, find: (a) the angular momentum vector $\vec{L}_O$ of the projectile about the launch point $O$ at the instant it reaches the peak of its trajectory, and (b) the angular momentum vector $\vec{L}_O$ just before landing back on the ground.

**Target Quantity**: `Angular momentum vector L_O at peak and at landing`

#### Systematic Solution
**Step 1 (Kinematics of projectile at apex)**:
$$ t_{\text{peak}} = \frac{v_0 \sin\theta}{g}, \quad x_{\text{peak}} = v_0 \cos\theta \, t_{\text{peak}}, \quad y_{\text{peak}} = H = \frac{v_0^2 \sin^2\theta}{2g}, \quad \vec{v}_{\text{peak}} = v_0 \cos\theta \, \hat{i} $$
t_{\text{peak}} = \frac{20.0 \sin 60^\circ}{10.0} = \sqrt{3}\text{ s} \approx 1.732\text{ s}, \quad x_{\text{peak}} = 10.0\sqrt{3}\text{ m}, \quad y_{\text{peak}} = \frac{400(3/4)}{20} = 15.0\text{ m}, \quad \vec{v} = 10.0 \, \hat{i}\text{ m/s}
Result: `r_peak = 10 sqrt(3) i + 15.0 j, v_peak = 10.0 i`

**Step 2 (Vector cross product definition at apex)**:
$$ \vec{L}_{O,\text{peak}} = \vec{r}_{\text{peak}} \times m \vec{v}_{\text{peak}} = (x_h \hat{i} + y_h \hat{j}) \times m (v_{0x} \hat{i}) = -m y_h v_{0x} \, \hat{k} $$
\vec{L}_{O,\text{peak}} = -(0.50)(15.0)(10.0) \, \hat{k} = -75.0 \, \hat{k}\text{ kg m}^2\text{/s}
Result: `L_O,peak = -75.0 k kg m^2/s`

**Step 3 (Kinematics and torque integration to landing)**:
$$ T_{\text{flight}} = 2 t_{\text{peak}} = 2\sqrt{3}\text{ s}, \quad \vec{L}_O(t) = -\frac{1}{2} m g v_0 \cos\theta \, t^2 \, \hat{k} $$
\vec{L}_{O,\text{land}} = -\frac{1}{2} (0.50)(10.0)(10.0) (2\sqrt{3})^2 \, \hat{k} = -25.0 (12) \, \hat{k} = -300.0 \, \hat{k}\text{ kg m}^2\text{/s}
Result: `L_O,land = -300.0 k kg m^2/s`

**Final Answer**: \vec{L}_{O,\text{peak}} = -75.0 \, \hat{k}\text{ kg m}^2\text{/s}, \quad \vec{L}_{O,\text{land}} = -300.0 \, \hat{k}\text{ kg m}^2\text{/s}

**Sanity & Consistency Checks**:
- Quadratic scaling: Because torque is tau = -m g v_0 cos(theta) t, angular momentum scales quadratically as t^2. Since T_flight = 2 t_peak, L_land / L_peak = (2)^2 = 4. Indeed, -300.0 / -75.0 = 4.00! Exact agreement.
- Cross product check at landing: r_land = R i, v_land = v_0x i - v_0y j. L_land = R i x m(v_0x i - v_0y j) = -m R v_0y k. Here R = v_0^2 sin(2 theta)/g = 400(sqrt(3)/2)/10 = 20 sqrt(3) m. L_land = -0.50 (20 sqrt(3))(10 sqrt(3)) k = -0.50(600) k = -300.0 k. Dual derivation confirms result bit-for-bit.


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
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> A particle falls freely near the surface of the earth. Consider a fixed point $O$ (not vertically below the particle) on the ground. Then pickup the incorrect alternative

**Options**:
- **(A)**: The magnitude of angular momentum of the particle about $O$ is increasing
- **(B)**: The magnitude of torque of the gravitational force on the particle about $O$ is decreasing
- **(C)**: The moment of inertia of the particle about $O$ is decreasing
- **(D)**: The magnitude of angular velocity of the particle about $O$ is increasing

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **B**  
**Independent Verification Record**: `rotational-motion-question-6c7cb960`

</details>


---

## Conservation of Angular Momentum and Systems with Variable Inertia

> **Pedagogical Goal**: Derive torque-angular momentum theorem tau = dL/dt, prove angular momentum conservation when external torque vanishes, and analyze isolated systems with reconfiguring internal mass distributions.


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
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> A thin horizontal circular disc is rotating about a vertical axis passing through its centre. An insect is at rest at a point near the rim of the disc. The insect now moves along a diameter of the disc to reach its other end. During the journey of the insect, the angular speed of the disc

**Options**:
- **(A)**: continuously decreases
- **(B)**: continuously increases
- **(C)**: first increases and then decreases
- **(D)**: remains unchanged

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **C**  
**Independent Verification Record**: `rotational-motion-question-84f91c20`

</details>


---

### Verified JEE Practice Problem: `rotational-motion-question-f7cbecda`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> A thin horizontal circular disc is rotating about a vertical axis passing through its centre. An insect is at rest at a point near the rim of the disc. The insect now moves along a diameter of the disc to reach its other end. During the journey of the insect, the angular speed of the disc

**Options**:
- **(A)**: continuously decreases
- **(B)**: continuously increases
- **(C)**: first increases and then decreases
- **(D)**: remains unchanged

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **C**  
**Independent Verification Record**: `rotational-motion-question-f7cbecda`

</details>


---

## Pure Rolling Kinematics, Incline Dynamics, and Toppling

> **Pedagogical Goal**: Formulate the kinematic no-slip contact constraint v_cm = R omega, analyze static friction direction and worklessness, derive rolling acceleration and critical friction down inclined planes, and establish the critical toppling vs sliding threshold.


---

### Concept: Kinematic Constraints of Pure Rolling and the Instantaneous Center of Rotation

**Definition**: The kinematic condition of zero relative tangential velocity between two contacting rigid surfaces at their point of contact: $$\vec{v}_{\text{contact, rel}} = \vec{v}_{\text{body}}(P) - \vec{v}_{\text{surface}}(P) = \vec{0}$$

**Physical Significance**: When a wheel rolls without slipping, each point on the rim touches the ground for a single instant before peeling off along a cycloid. At that precise instant of contact, it is not sliding across the ground at all—it is momentarily stationary, like the foot of a walking person planted on the pavement.

**Assumptions & Scope of Validity**:
- Rigid circular cross-section (cylinder, sphere, wheel) of radius R
- Planar supporting surface
- Zero microscopic sliding or slipping at the contact interface


---

### Concept: Dynamics of Pure Rolling on Horizontal Surfaces and Directionality of Static Friction

**Definition**: The self-adjusting static friction force at the contact point required to satisfy the non-holonomic constraint equation $a_{\text{cm}} = R \alpha$ under applied loads: $$f_s \le \mu_s N$$

**Physical Significance**: Static friction is an adaptable force—it only pushes in whichever direction is needed to prevent the contact point from slipping! If you pull a spool by a string at the very top, the pull creates so much torque that the bottom tries to kick backward, so friction pushes forward to help it accelerate.

**Assumptions & Scope of Validity**:
- Rigid body with radius of gyration k rolling on stationary flat horizontal ground
- Applied external force F is purely horizontal at height h above center of mass
- Static friction limit f_s <= mu_s M g is not exceeded


---

### Concept: Dynamics of Pure Rolling on an Inclined Plane and the Critical Friction Threshold

**Definition**: The governing equation for linear center-of-mass acceleration of a rigid body rolling without slipping down an incline of angle theta: $$a_{\text{cm}} = \frac{g \sin\theta}{1 + \frac{k^2}{R^2}}$$

**Physical Significance**: In frictionless sliding, all objects accelerate at $g \sin\theta$ regardless of shape. But in rolling, gravity must accelerate both the linear speed AND the rotational spin. Objects with mass packed near the center (solid sphere) are easy to spin, so they waste less potential energy on rotation and win the race down the ramp!

**Assumptions & Scope of Validity**:
- Uniform rigid body with circular cross-section rolling down an incline of constant angle theta
- Static friction coefficient satisfies mu_s >= mu_min
- Zero aerodynamic drag and zero rolling resistance


---

### Concept: Critical Conditions for Sliding versus Toppling of Rigid Blocks Under Lateral Forces

**Definition**: The condition of impending rotational instability of a rigid body about a supporting pivot edge when the line of action of the contact reaction reaches the boundary of the support polygon: $$\sum \tau_{\text{edge}} = 0$$

**Physical Significance**: Think of a tall, narrow bookshelf versus a wide, flat chest of drawers on a sticky rug. If you push the tall bookshelf high up, it easily tips over before sliding across the floor because the normal reaction can't shift far enough sideways to counter the overturning torque.

**Assumptions & Scope of Validity**:
- Rigid cuboidal block with uniform mass density
- Sufficient normal support distributed across planar base
- Friction governed by Coulomb static friction model


---

### Formula: Pure Rolling Kinematic Constraint and Velocity Distribution

**Governing Equation**:
$$ v_{\text{cm}} = R \omega, \quad \vec{v}_P = \vec{0}, \quad v_{\text{top}} = 2 v_{\text{cm}} = 2 R \omega $$

**Variable Inventory & SI Units**:
- $v_{\text{cm}}$: Linear speed of center of mass (Unit: `m/s`)
- $R$: Radius of rolling body (Unit: `m` | Dim: `[L]`)
- $\omega$: Angular velocity of rolling body (Unit: `rad/s` | Dim: `[T]^-1`)
- $v_P$: Instantaneous velocity of contact point P on stationary ground (Unit: `m/s`)
- $v_{\text{top}}$: Instantaneous velocity of top rim point (Unit: `m/s`)

**Physical Assumptions**:
- Rigid wheel or cylinder rolling on a stationary flat horizontal surface
- Zero relative sliding at the instantaneous contact point (pure rolling)

**Domain of Validity**:
- Holds strictly during pure rolling; if the surface itself moves with speed v_s, constraint becomes v_cm - v_s = R omega


---

### Formula: Acceleration and Critical Friction for Pure Rolling on an Inclined Plane

**Governing Equation**:
$$ a_{\text{cm}} = \frac{g \sin\theta}{1 + \frac{I_{\text{cm}}}{M R^2}} = \frac{g \sin\theta}{1 + \frac{k^2}{R^2}}, \quad \mu_{\min} = \frac{\tan\theta}{1 + \frac{M R^2}{I_{\text{cm}}}} = \frac{\tan\theta}{1 + \frac{R^2}{k^2}} $$

**Variable Inventory & SI Units**:
- $a_{\text{cm}}$: Linear acceleration of center of mass down the incline (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $g$: Acceleration due to gravity (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $\theta$: Inclination angle of plane with horizontal (Unit: `rad or deg`)
- $I_{\text{cm}}$: Moment of inertia about center of mass
- $M$: Total mass of rolling body
- $R$: Radius of rolling body (Unit: `m`)
- $k$: Radius of gyration (I_cm = M k^2) (Unit: `m`)
- $\mu_{\min}$: Minimum coefficient of static friction to prevent slipping (Unit: `dimensionless`)

**Physical Assumptions**:
- Uniform symmetrical rigid body rolling down an incline of angle theta
- Sufficient static friction mu_s >= mu_min to ensure zero slipping
- Rigid circular contact profile

**Domain of Validity**:
- Valid strictly for pure rolling without slipping; if mu_s < mu_min, body slips with a = g(sin theta - mu_k cos theta)


---

### Derivation: Formula `formula-rot-rolling-incline-accel`

**Target Governing Relation**:
$$ a_{\text{cm}} = \frac{g \sin\theta}{1 + \frac{I_{\text{cm}}}{M R^2}} = \frac{g \sin\theta}{1 + \frac{k^2}{R^2}} $$

#### Step-by-Step Proof
**Step 1**: Formulate linear equation of motion down the incline
$$ M g \sin\theta - f_s = M a_{\text{cm}} $$
*Physical Operation*: Resolve gravity component M g sin(theta) down incline and static friction f_s up incline

**Step 2**: Formulate rotational equation of motion about center of mass
$$ f_s R = I_{\text{cm}} \alpha $$
*Physical Operation*: Evaluate torques about CM: gravity and normal force pass through CM (zero torque), friction provides torque f_s R

**Step 3**: Apply the pure rolling no-slip kinematic constraint
$$ f_s R = I_{\text{cm}} \left(\frac{a_{\text{cm}}}{R}\right) \implies f_s = \frac{I_{\text{cm}}}{R^2} a_{\text{cm}} $$
*Physical Operation*: Express angular acceleration in terms of linear acceleration: alpha = a_cm / R

**Step 4**: Substitute friction expression into the translational equation of motion
$$ M g \sin\theta - \frac{I_{\text{cm}}}{R^2} a_{\text{cm}} = M a_{\text{cm}} \implies M g \sin\theta = \left( M + \frac{I_{\text{cm}}}{R^2} \right) a_{\text{cm}} $$
*Physical Operation*: Substitute f_s = (I_cm / R^2) a_cm and group acceleration terms

**Step 5**: Solve for linear acceleration and express using radius of gyration
$$ a_{\text{cm}} = \frac{g \sin\theta}{1 + \frac{I_{\text{cm}}}{M R^2}} = \frac{g \sin\theta}{1 + \frac{k^2}{R^2}} $$
*Physical Operation*: Divide by M (1 + I_cm / (M R^2)) and substitute I_cm = M k^2

**Step 6**: Determine required friction force and critical static friction coefficient
$$ f_s = \frac{M g \sin\theta}{1 + \frac{M R^2}{I_{\text{cm}}}} \le \mu_s M g \cos\theta \implies \mu_s \ge \mu_{\min} = \frac{\tan\theta}{1 + \frac{M R^2}{I_{\text{cm}}}} = \frac{\tan\theta}{1 + \frac{R^2}{k^2}} $$
*Physical Operation*: Substitute a_cm into f_s expression and impose Coulomb inequality

**Applicability & Limiting Conditions**:
- Valid strictly for pure rolling without slipping (mu_s >= mu_min)
- If mu_s < mu_min, body slips and accelerates at a = g(sin theta - mu_k cos theta) with alpha = mu_k M g cos(theta) R / I_cm


---

### Formula: Critical Threshold Conditions for Toppling versus Sliding

**Governing Equation**:
$$ F_{\text{crit}} = \frac{M g b}{2 H}, \quad \tan\theta_{\text{crit}} = \frac{b}{h} $$

**Variable Inventory & SI Units**:
- $F_{\text{crit}}$: Critical horizontal force causing toppling on flat ground (Unit: `N` | Dim: `[M][L][T]^-2`)
- $M$: Mass of the rigid block (Unit: `kg`)
- $g$: Acceleration due to gravity (Unit: `m/s^2`)
- $b$: Base width of block along direction of force (Unit: `m` | Dim: `[L]`)
- $H$: Height above ground at which lateral force is applied (Unit: `m` | Dim: `[L]`)
- $h$: Total height of block (Unit: `m` | Dim: `[L]`)
- $\theta_{\text{crit}}$: Critical incline tilt angle causing toppling before sliding (Unit: `rad or deg`)

**Physical Assumptions**:
- Uniform homogeneous rectangular/cuboidal block resting on rough ground
- Normal reaction force shifts to extreme tipping edge at toppling threshold
- Coulomb friction model with static coefficient mu_s

**Domain of Validity**:
- Toppling precedes sliding on horizontal ground if b / (2 H) < mu_s; toppling precedes sliding on incline if b / h < mu_s


---

### Worked Pedagogical Example: `ex-rot-rolling-incline-race-01`

**Problem Statement**:
> Four uniform symmetrical bodies—a thin circular ring (hoop), a solid cylinder (disc), a thin hollow spherical shell, and a solid sphere—each having the same mass $M$ and radius $R$, are released simultaneously from rest at the top of a rough inclined plane of inclination angle $\theta$ and vertical height $h$. Assuming each body rolls purely without slipping throughout the motion: (a) express the final translational speed $v$ at the bottom of the incline in terms of $g$, $h$, and the shape factor $c = k^2/R^2$, and (b) calculate the speed ratios relative to the ring and determine the order of finish in the race.

**Target Quantity**: `Speed expression v(c) and arrival order`

#### Systematic Solution
**Step 1 (Kinetic energy decomposition in pure rolling)**:
$$ K = K_{\text{trans}} + K_{\text{rot}} = \frac{1}{2} M v^2 + \frac{1}{2} I_{\text{cm}} \omega^2 = \frac{1}{2} M v^2 + \frac{1}{2} (M k^2) \left(\frac{v}{R}\right)^2 = \frac{1}{2} M v^2 \left( 1 + \frac{k^2}{R^2} \right) $$
K = \frac{1}{2} M v^2 (1 + c), \quad c = \frac{k^2}{R^2}
Result: `K = 1/2 M v^2 (1 + c)`

**Step 2 (Conservation of mechanical energy)**:
$$ M g h = \frac{1}{2} M v^2 (1 + c) \implies v = \sqrt{\frac{2 g h}{1 + c}} $$
v_{\text{solid sphere}} = \sqrt{\frac{2gh}{1 + 0.40}} = \sqrt{\frac{10}{7} gh} \approx 1.1952 \sqrt{gh}
Result: `v_solid_sphere = sqrt(10/7 gh) approx 1.195 sqrt(gh)`

**Step 3 (Evaluate speeds for remaining three bodies)**:
$$ v_{\text{disc}} = \sqrt{\frac{2gh}{1 + 0.50}} = \sqrt{\frac{4}{3} gh} \approx 1.1547 \sqrt{gh}, \quad v_{\text{hollow}} = \sqrt{\frac{2gh}{1 + 2/3}} = \sqrt{\frac{6}{5} gh} \approx 1.0954 \sqrt{gh}, \quad v_{\text{ring}} = \sqrt{\frac{2gh}{1 + 1.0}} = \sqrt{gh} = 1.000 \sqrt{gh} $$
Speed ratios relative to ring: Solid Sphere: 1.195, Solid Cylinder: 1.155, Hollow Sphere: 1.095, Ring: 1.000
Result: `Ratios computed`

**Step 4 (Incline travel time calculation)**:
$$ t = \frac{L}{\bar{v}} = \frac{2 L}{v} = \frac{2 h}{\sin\theta \sqrt{\frac{2 g h}{1 + c}}} = \frac{1}{\sin\theta} \sqrt{\frac{2 h (1 + c)}{g}} $$
Since t is proportional to sqrt(1 + c), lower c finishes earlier.
Result: `t_solid < t_disc < t_hollow < t_ring`

**Final Answer**: v = \sqrt{\frac{2gh}{1 + k^2/R^2}}; \quad \text{Order of arrival: Solid Sphere (1st) > Solid Cylinder (2nd) > Hollow Sphere (3rd) > Ring (4th)}

**Sanity & Consistency Checks**:
- Limiting frictionless sliding: If c = 0 (point mass), v = sqrt(2 g h), the maximum possible speed.
- Energy partition check: For ring (c = 1), translational and rotational energies are equal: K_trans = K_rot = 1/2 Mgh.
- Independent acceleration check: a = g sin(theta)/(1+c). Since a_solid = 5/7 g sin(theta) > a_disc = 2/3 g sin(theta) > a_hollow = 3/5 g sin(theta) > a_ring = 1/2 g sin(theta), arrival order is confirmed.


---

### Worked Pedagogical Example: `ex-rot-toppling-block-01`

**Problem Statement**:
> A uniform rectangular block of mass $M = 10.0\text{ kg}$, base width $b = 0.40\text{ m}$, and height $h = 1.00\text{ m}$ stands upright on a rough horizontal floor with static friction coefficient $\mu_s = 0.60$. A horizontal pulling force $F$ is applied at the top edge of the block ($H = 1.00\text{ m}$). Taking $g = 10.0\text{ m/s}^2$: (a) calculate the critical force $F_{\text{topple}}$ at which the block will begin to topple, (b) calculate the critical force $F_{\text{slide}}$ at which the block would begin to slide, and (c) determine whether the block slides first or topples first.

**Target Quantity**: `F_topple, F_slide, and failure mode`

#### Systematic Solution
**Step 1 (Torque balance about the front bottom tipping corner P)**:
$$ \sum \tau_P = 0 \implies F_{\text{topple}} H - M g \left( \frac{b}{2} \right) = 0 \implies F_{\text{topple}} = \frac{M g b}{2 H} $$
F_{\text{topple}} = \frac{(10.0)(10.0)(0.40)}{2 (1.00)} = \frac{40.0}{2.00} = 20.0\text{ N}
Result: `F_topple = 20.0 N`

**Step 2 (Coulomb maximum static friction for sliding)**:
$$ F_{\text{slide}} = f_{s,\max} = \mu_s N = \mu_s M g $$
F_{\text{slide}} = (0.60)(10.0)(10.0) = 60.0\text{ N}
Result: `F_slide = 60.0 N`

**Step 3 (Comparison of threshold forces)**:
$$ F_{\text{topple}} = 20.0\text{ N} < F_{\text{slide}} = 60.0\text{ N} $$
\frac{b}{2 H} = \frac{0.40}{2(1.00)} = 0.20 < \mu_s = 0.60
Result: `Block topples before sliding`

**Final Answer**: F_{\text{topple}} = 20.0\text{ N}, \quad F_{\text{slide}} = 60.0\text{ N}; \quad \text{The block topples first at } F = 20.0\text{ N}

**Sanity & Consistency Checks**:
- Geometric ratio check: b / (2 H) = 0.20 < mu_s = 0.60 rigorously confirms toppling is the operative failure mode.
- Normal force migration: For F < 20 N, normal reaction position is x = F H / (Mg) from center. At F = 20 N, x = 20(1)/(100) = 0.20 m = b/2, precisely reaching the corner.
- Dimensional check: Force is in Newtons.


---

### Inoculation Against Misconception: `misc-rot-05`

**Misconception Category**: `SIGN_MISTAKE`  
**Erroneous Intuition**: *"Friction always acts in the opposite direction of the rolling body's linear velocity to oppose forward motion."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> In pure rolling, static friction does not oppose the velocity of the center of mass; it opposes relative slipping at the contact point. If an external horizontal force is applied above the center of percussion (h > k^2/R, e.g. at the top of a wheel), the force produces more angular acceleration than linear acceleration, causing the bottom contact point to tend to slip backward. Static friction therefore acts FORWARD in the direction of motion, accelerating the center of mass linearly while providing counter-torque.

**Physical Truth & Resolution**:
Evaluate the torque and linear force separately. Determine the slip tendency at the contact point: friction acts in whichever direction prevents slipping, which can be backward, forward, or zero.

**Refutation Counterexample & Supporting Evidence**:
Halliday, Resnick & Walker, Chapter 11, Section 11.2; H.C. Verma Vol 1, Chapter 10, Section 10.16.

**Diagnostic Symptom**: Student automatically draws friction pointing backward in all rolling problems without evaluating the line of action of external forces.


---

### Inoculation Against Misconception: `misc-rot-06`

**Misconception Category**: `FRAME_CONFUSION`  
**Erroneous Intuition**: *"Because the instantaneous velocity of the contact point in pure rolling is zero, its instantaneous acceleration must also be zero."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Zero instantaneous velocity does not imply zero acceleration. The contact point of a rolling wheel traces a cycloid in space. At the cusp of the cycloid, the velocity vanishes instantaneously (v_P = 0), but the direction of velocity is changing at its maximum rate. The contact point experiences a pure centripetal acceleration a_c = v_cm^2 / R = omega^2 R directed vertically upward toward the center of the wheel.

**Physical Truth & Resolution**:
Recognize that while v_contact = 0, a_contact = omega^2 R != 0. The contact point is accelerating upward toward the center of the rolling body.

**Refutation Counterexample & Supporting Evidence**:
University Physics, Chapter 10, Section 10.3; Feynman Lectures on Physics Vol 1, Chapter 18.

**Diagnostic Symptom**: Student claims that the contact point is an inertial reference point or that Newton's laws can be written about P without considering accelerating reference frames.


---

## Chapter Summary & Formula Recap: Rotational Motion and Rigid Body Dynamics

### Core Equations & Domains of Validity
- **Moment of Inertia of Discrete Point Masses**: $$$$
  *Validity*: General
- **Moments of Inertia for Standard Symmetrical Continuous Rigid Bodies**: $$$$
  *Validity*: General
- **Parallel Axis Theorem**: $$I = I_{\text{cm}} + M d^2$$
  *Validity*: General
- **Perpendicular Axis Theorem for Planar Laminas**: $$$$
  *Validity*: General
- **Radius of Gyration**: $$$$
  *Validity*: General
- **Definition and Moment Arm Representation of Torque**: $$$$
  *Validity*: General
- **Angular Kinematic Equations Under Constant Angular Acceleration**: $$$$
  *Validity*: General
- **Torque Dynamic Relation**: $$\vec{\tau}_{\text{net, ext}} = I \vec{\alpha} = \frac{d\vec{L}}{dt}$$
  *Validity*: General
- **Rotational Kinetic Energy of a Rigid Body**: $$$$
  *Validity*: General
- **Rotational Work-Energy Theorem**: $$$$
  *Validity*: General
- **Particle Angular Momentum**: $$\vec{L}_O = \vec{r} \times \vec{p} = m (\vec{r} \times \vec{v})$$
  *Validity*: General
- **Angular Momentum of Rigid Body in Planar Motion About Arbitrary Origin**: $$$$
  *Validity*: General
- **Conservation of Angular Momentum About Fixed Axis**: $$I_i \omega_i = I_f \omega_f$$
  *Validity*: General
- **Pure Rolling Kinematic Constraint and Velocity Distribution**: $$$$
  *Validity*: General
- **Acceleration and Critical Friction for Pure Rolling on an Inclined Plane**: $$$$
  *Validity*: General
- **Critical Threshold Conditions for Toppling versus Sliding**: $$$$
  *Validity*: General
