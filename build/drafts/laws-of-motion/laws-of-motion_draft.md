# Chapter: Newton's Laws of Motion & Dynamics

**Template**: `MECHANICS`  
**Prerequisites**: units-and-measurements, vectors-and-coordinate-systems, differential-calculus-foundations, kinematics  

## Learning Objectives
- Master Newton's three laws of motion and operational distinctions between inertial and non-inertial reference frames.
- Construct rigorous free-body diagrams for isolated particles, contact surfaces, strings, and springs.
- Formulate geometric kinematic constraints for connected string-pulley assemblies and movable wedges.
- Incorporate inertial pseudo-forces into non-inertial accelerating frames.
- Analyze Coulomb-Amontons static, limiting, and kinetic friction across planar and curved interfaces.
- Solve multi-body stacked two-block systems for threshold slipping and independent sliding accelerations.
- Determine optimum road banking angles and safe speed envelopes with and without lateral friction.
- Analyze radial dynamic equilibrium in horizontal circular motion and conical pendulums.

---

## Principles of Inertia, Momentum, and the Laws of Motion

> **Pedagogical Goal**: Establish Galileo's inertia, Newton's three laws, inertial reference frames, action-reaction pairs, and free-body diagram isolation.


---

### Concept: Galileo's Principle of Inertia and Newton's First Law

**Definition**: A body remains at rest or in a state of uniform rectilinear motion unless acted upon by a non-zero net external force: $\sum \vec{F}_{\text{ext}} = 0 \iff \frac{d\vec{v}}{dt} = 0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Inertial reference frame
- Classical non-relativistic regime ($v \ll c$)


---

### Concept: Linear Momentum, Impulse, and Newton's Second Law

**Definition**: The time rate of change of linear momentum of a particle equals the net external force acting on it: $\vec{F}_{\text{net}} = \frac{d\vec{p}}{dt} = \frac{d(m\vec{v})}{dt}$. For invariant mass $m$, $\vec{F}_{\text{net}} = m \vec{a}$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Point particle or center of mass translation
- Invariant rest mass ($dm/dt = 0$)


---

### Concept: Action-Reaction Pairs and Newton's Third Law

**Definition**: Whenever body A exerts a force on body B, body B simultaneously exerts an equal and opposite force on body A: $\vec{F}_{BA} = -\vec{F}_{AB}$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Simultaneous action-at-a-distance (classical limit)
- Distinct interacting bodies A and B


---

### Concept: Free-Body Diagram Isolation and Component Projection

**Definition**: A systematic analytical procedure wherein a chosen mechanical body is isolated from its environment, and every external force acting ON the body is represented as an applied vector at its contact or center point.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Rigid body or particle idealization
- Inertial coordinate axes


---

### Concept: Normal Reaction, String Tension, and Ideal Springs

**Definition**: Normal force $N$ is the perpendicular electromagnetic repulsive contact reaction preventing interpenetration of solid surfaces. Tension $T$ is the state of pulling stress transmitted along a string, which is uniform along massless, frictionless strings.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Ideal massless inextensible string
- Massless frictionless pulley


---

### Formula: Newton's Second Law for Constant Mass

**Governing Equation**:
$$ \vec{F}_{\text{net}} = m \vec{a} = m \frac{d^2 \vec{r}}{dt^2} $$

**Variable Inventory & SI Units**:
- $\vec{F}_{\text{net}}$: Net external force vector
- $m$: Inertial mass (Unit: `kg` | Dim: `[M]`)
- $\vec{a}$: Acceleration vector (Unit: `m s^-2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Inertial frame of reference
- Constant mass system dm/dt = 0
- Non-relativistic regime

**Domain of Validity**:
- Universal for translation of point mass or center of mass in classical mechanics


---

### Derivation: Formula `formula-dyn-second-law`

**Target Governing Relation**:
$$ \vec{F}_{\text{net}} = m \vec{a}, \quad \vec{J} = \Delta \vec{p} $$

#### Step-by-Step Proof
**Step 1**: 
$$ \vec{F}_{\text{net}} = \frac{d\vec{p}}{dt} = \frac{d(m\vec{v})}{dt} $$
*Physical Operation*: 

**Step 2**: 
$$ \vec{F}_{\text{net}} = m \frac{d\vec{v}}{dt} + \vec{v} \frac{dm}{dt} = m \vec{a} + 0 = m \vec{a} $$
*Physical Operation*: 

**Step 3**: 
$$ \vec{J} = \int_{t_1}^{t_2} \vec{F}_{\text{net}} \, dt = \int_{\vec{p}_1}^{\vec{p}_2} d\vec{p} = \vec{p}_2 - \vec{p}_1 = m \vec{v}_2 - m \vec{v}_1 $$
*Physical Operation*: 


---

### Formula: Newton's Third Law (Action-Reaction)

**Governing Equation**:
$$ \vec{F}_{AB} = -\vec{F}_{BA} $$

**Variable Inventory & SI Units**:
- $\vec{F}_{AB}$: Force exerted on body A by body B
- $\vec{F}_{BA}$: Force exerted on body B by body A

**Physical Assumptions**:
- Pairwise physical interaction between two distinct bodies A and B

**Domain of Validity**:
- Collinear central mutual interaction in classical mechanics


---

### Formula: Impulse-Momentum Theorem

**Governing Equation**:
$$ \vec{J} = \int_{t_1}^{t_2} \vec{F}_{\text{net}} \, dt = \Delta \vec{p} = m \vec{v}_2 - m \vec{v}_1 $$

**Variable Inventory & SI Units**:
- $\vec{J}$: Impulse vector (Unit: `N s (kg m s^-1)` | Dim: `[M][L][T]^-1`)
- $\vec{F}_{\text{net}}$: Net force vector
- $\Delta \vec{p}$: Change in linear momentum

**Physical Assumptions**:
- Constant particle mass
- Integrable force over duration

**Domain of Validity**:
- Universal for any force time-profile


---

### Worked Pedagogical Example: `ex-dyn-fbd-equilibrium-01`

**Problem Statement**:
> A sphere of mass $M = 10\text{ kg}$ is held suspended by a light string attached to a smooth vertical wall. The string makes an angle $\theta = 30^\circ$ with the vertical. Determine the tension $T$ in the string and the normal reaction force $N$ exerted by the wall on the sphere. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `T, N`

#### Systematic Solution
**Step 1 ()**:
$$ \sum F_y = T \cos 30^\circ - Mg = 0 \implies T = \frac{10 \times 9.8}{\cos 30^\circ} = \frac{98}{\sqrt{3}/2} \approx 113.16\text{ N} $$

Result: ``

**Step 2 ()**:
$$ \sum F_x = N - T \sin 30^\circ = 0 \implies N = 113.16 \times 0.5 = 56.58\text{ N} $$

Result: ``

**Final Answer**: T \approx 113.2\text{ N}, \quad N \approx 56.6\text{ N}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Failing to recognize that smooth wall produces normal reaction strictly perpendicular to the vertical wall surface

**Sanity & Consistency Checks**:
- As theta -> 0, T -> Mg = 98 N and N -> 0, matching vertical hanging limit
- Normal force is positive confirming contact is maintained


---

### Inoculation Against Misconception: `misc-dyn-01`

**Misconception Category**: `CONFUSING_ACTION_REACTION_PAIR`  
**Erroneous Intuition**: *"Action and reaction forces cancel each other out, so bodies should never be able to accelerate."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Because Newton's Third Law states F_AB = -F_BA, the sum F_AB + F_BA = 0, so the net force in the universe is zero and nothing moves.

**Physical Truth & Resolution**:
Action and reaction forces act on strictly DIFFERENT bodies. When computing the acceleration of body A via sum F = m_A a_A, ONLY forces exerted ON body A enter the equation. The reaction force F_BA is exerted on body B and cannot cancel forces acting on body A.

**Refutation Counterexample & Supporting Evidence**:
When a horse pulls a cart, the horse exerts forward force F_cart on the cart, accelerating the cart forward. The cart exerts equal backward reaction force F_horse on the horse; the horse accelerates forward because the ground exerts a larger forward static friction force on the horse's hooves.

**Diagnostic Symptom**: \vec{F}_{A \to B} \text{ acts on } B, \quad \vec{F}_{B \to A} \text{ acts on } A. \quad \text{They never appear on the same free-body diagram!}


---

### Inoculation Against Misconception: `misc-dyn-02`

**Misconception Category**: `NORMAL_FORCE_EQUAL_TO_MG`  
**Erroneous Intuition**: *"The normal reaction force is always equal in magnitude to the object's weight (N = mg)."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Believing that normal force is inherently the reaction to gravity and must therefore always equal mg.

**Physical Truth & Resolution**:
Normal force is an adjusting electromagnetic contact constraint preventing surface penetration, not the reaction to gravity. On an incline of angle theta, N = mg cos(theta). In an accelerating elevator, N = m(g + a). If pushed downward with force F, N = mg + F. If pulled upward, N = mg - F.

**Refutation Counterexample & Supporting Evidence**:
A book of mass 1 kg resting on a table pressed downward by a hand with 20 N force experiences normal force N = 10(9.8) + 20 = 29.8 N, not 9.8 N.

**Diagnostic Symptom**: N \text{ is determined strictly by constraint equation } \sum F_{\perp} = m a_{\perp}, \text{ not an intrinsic identity } N = mg.


---

## String-Pulley Constraints, Wedges, and Non-Inertial Reference Frames

> **Pedagogical Goal**: Formulate kinematic constraints for multi-body connected systems (pulleys, movable wedges) and analyze dynamics in linearly accelerating frames using pseudo-forces.


---

### Concept: String-Pulley Kinematic Constraints and Virtual Work

**Definition**: The kinematic relation linking the displacements, velocities, and accelerations of bodies connected by inextensible strings passing over fixed or movable pulleys, expressed by length preservation $\sum l_i = \text{const}$ or virtual work $\sum \vec{T}_i \cdot \vec{a}_i = 0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Inextensible string ($dl/dt = 0$)
- Massless string and pulley


---

### Concept: Wedge Boundary Constraints and Relative Motion

**Definition**: The kinematic boundary condition requiring that two rigid bodies in continuous sliding contact must have identical velocity and acceleration components along the direction normal to the common contact interface.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Continuous rigid surface contact without separation
- Planar interface


---

### Concept: Non-Inertial Reference Frames and Inertial Pseudo-Forces

**Definition**: In a coordinate frame accelerating with linear acceleration $\vec{a}_0$ relative to an inertial frame, Newton's second law is preserved in the form $m\vec{a}' = \sum \vec{F}_{\text{real}} + \vec{F}_{\text{pseudo}}$, where $\vec{F}_{\text{pseudo}} = -m \vec{a}_0$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Translational acceleration of observer frame $\vec{a}_0$
- Zero frame rotation ($\vec{\omega} = 0$)


---

### Formula: Virtual Work Pulley Constraint Relation

**Governing Equation**:
$$ \sum_{i=1}^n \vec{T}_i \cdot \vec{a}_i = 0 $$

**Variable Inventory & SI Units**:
- $\vec{T}_i$: Tension vector acting on body i
- $\vec{a}_i$: Acceleration vector of body i

**Physical Assumptions**:
- Ideal massless inextensible string
- Massless frictionless pulleys
- Taut string segments

**Domain of Validity**:
- Valid for any connected pulley system while string tension remains positive


---

### Derivation: Formula `formula-dyn-string-constraint`

**Target Governing Relation**:
$$ \sum_{i=1}^n \vec{T}_i \cdot \vec{a}_i = 0 $$

#### Step-by-Step Proof
**Step 1**: 
$$ L = \sum_{k} x_k + \text{constant} $$
*Physical Operation*: 

**Step 2**: 
$$ \frac{dL}{dt} = \sum_{k} v_k = 0, \quad \frac{d^2L}{dt^2} = \sum_{k} a_k = 0 $$
*Physical Operation*: 

**Step 3**: 
$$ \delta W = \sum_{i=1}^n \vec{T}_i \cdot \delta \vec{r}_i = 0 \implies \sum_{i=1}^n \vec{T}_i \cdot \vec{a}_i = 0 $$
*Physical Operation*: 


---

### Formula: Wedge Normal Acceleration Constraint

**Governing Equation**:
$$ (\vec{a}_{\text{block}} - \vec{a}_{\text{wedge}}) \cdot \hat{n} = 0 $$

**Variable Inventory & SI Units**:
- $\vec{a}_{\text{block}}$: Acceleration of block
- $\vec{a}_{\text{wedge}}$: Acceleration of wedge
- $\hat{n}$: Unit normal to contact face

**Physical Assumptions**:
- Rigid body non-penetration condition
- Persistent surface contact

**Domain of Validity**:
- Valid while contact normal force N > 0


---

### Formula: Linear Inertial Pseudo-Force

**Governing Equation**:
$$ \vec{F}_{\text{pseudo}} = -m \vec{a}_0 $$

**Variable Inventory & SI Units**:
- $\vec{F}_{\text{pseudo}}$: Fictitious inertial force
- $m$: Particle mass (Unit: `kg` | Dim: `[M]`)
- $\vec{a}_0$: Linear acceleration of observer frame (Unit: `m s^-2`)

**Physical Assumptions**:
- Translational non-inertial reference frame
- Zero angular frame rotation

**Domain of Validity**:
- Must be applied to all bodies when formulating Newton's laws in accelerating frame


---

### Derivation: Formula `formula-dyn-pseudo-force`

**Target Governing Relation**:
$$ m \vec{a}' = \vec{F}_{\text{real}} - m \vec{a}_0 $$

#### Step-by-Step Proof
**Step 1**: 
$$ \vec{r} = \vec{R}_0 + \vec{r}' $$
*Physical Operation*: 

**Step 2**: 
$$ \vec{a} = \vec{a}_0 + \vec{a}' \implies \vec{a}' = \vec{a} - \vec{a}_0 $$
*Physical Operation*: 

**Step 3**: 
$$ m \vec{a}' = m \vec{a} - m \vec{a}_0 = \vec{F}_{\text{real}} - m \vec{a}_0 = \vec{F}_{\text{real}} + \vec{F}_{\text{pseudo}} $$
*Physical Operation*: 


---

### Worked Pedagogical Example: `ex-dyn-atwood-pulley-01`

**Problem Statement**:
> In a modified Atwood machine, two masses $m_1 = 2.0\text{ kg}$ and $m_2 = 3.0\text{ kg}$ are connected by a light inextensible string passing over a frictionless light pulley. Find the common acceleration $a$ of the masses and the tension $T$ in the string when released from rest. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `a, T`

#### Systematic Solution
**Step 1 ()**:
$$ m_2 g - T = m_2 a, \quad T - m_1 g = m_1 a $$

Result: ``

**Step 2 ()**:
$$ (m_2 - m_1) g = (m_1 + m_2) a \implies a = \frac{m_2 - m_1}{m_1 + m_2} g = \frac{3.0 - 2.0}{3.0 + 2.0} \times 9.8 = \frac{1}{5} \times 9.8 = 1.96\text{ m/s}^2 $$

Result: ``

**Step 3 ()**:
$$ T = m_1 (g + a) = 2.0 \times (9.8 + 1.96) = 2.0 \times 11.76 = 23.52\text{ N} $$

Result: ``

**Final Answer**: a = 1.96\text{ m/s}^2, \quad T = 23.52\text{ N}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Assuming tension T = m2 g or T = (m1 + m2)g instead of accounting for accelerated dynamics

**Sanity & Consistency Checks**:
- Tension satisfies m1 g < T < m2 g (19.6 N < 23.52 N < 29.4 N), as required for upward/downward acceleration
- When m1 = m2, a = 0 and T = mg


---

### Worked Pedagogical Example: `ex-dyn-wedge-incline-01`

**Problem Statement**:
> A wedge of mass $M = 4.0\text{ kg}$ with incline angle $\alpha = 30^\circ$ rests on a smooth horizontal floor. A block of mass $m = 1.0\text{ kg}$ is placed on the smooth incline. Find the horizontal acceleration $A$ of the wedge. (Take $g = 9.8\text{ m/s}^2$).

**Target Quantity**: `A`

#### Systematic Solution
**Step 1 ()**:
$$ N \sin\alpha = M A \implies N = \frac{M A}{\sin\alpha} $$

Result: ``

**Step 2 ()**:
$$ N - m g \cos\alpha - m A \sin\alpha = 0 \implies N = m(g \cos\alpha + A \sin\alpha) $$

Result: ``

**Step 3 ()**:
$$ \frac{M A}{\sin\alpha} = m(g \cos\alpha + A \sin\alpha) \implies A \left( \frac{M}{\sin\alpha} - m \sin\alpha \right) = m g \cos\alpha \implies A = \frac{m g \sin\alpha \cos\alpha}{M + m \sin^2\alpha} $$

Result: ``

**Step 4 ()**:
$$ A = \frac{1.0 \times 9.8 \times 0.5 \times \frac{\sqrt{3}}{2}}{4.0 + 1.0 \times (0.5)^2} = \frac{9.8 \times 0.4330}{4.0 + 0.25} = \frac{4.2435}{4.25} \approx 0.9985\text{ m/s}^2 $$

Result: ``

**Final Answer**: A = \frac{m g \sin\alpha \cos\alpha}{M + m \sin^2\alpha} \approx 1.00\text{ m/s}^2

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Neglecting pseudo-force m A on block in non-inertial wedge frame or assuming normal force is simply mg cos(alpha)

**Sanity & Consistency Checks**:
- As M -> infty (fixed wedge), A -> 0
- As alpha -> 0 or 90 deg, horizontal coupling vanishes A -> 0


---

### Inoculation Against Misconception: `misc-dyn-06`

**Misconception Category**: `PSEUDO_FORCE_IN_INERTIAL_FRAME`  
**Erroneous Intuition**: *"Pseudo-forces (like centrifugal force) exist and act on bodies when observed from an inertial ground frame."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Applying non-inertial frame fictitious corrections when solving problems from ground reference frame.

**Physical Truth & Resolution**:
Pseudo-forces are mathematical constructs that arise strictly when describing motion from non-inertial accelerating or rotating reference frames. In an inertial reference frame, pseudo-forces are zero. A car turning a corner experiences inward friction; an occupant feels pushed outward only in the car's rotating non-inertial frame.

**Refutation Counterexample & Supporting Evidence**:
From ground frame, a pendulum in an accelerating truck is deflected backward because string tension has a forward component accelerating the bob: T sin(theta) = m a_0.

**Diagnostic Symptom**: \vec{F}_{\text{pseudo}} = -m \vec{a}_0 \quad (\text{ONLY in frame accelerating with } \vec{a}_0). \quad \text{In ground frame: } \vec{F}_{\text{pseudo}} = 0.


---

## Static, Limiting, and Kinetic Friction in Multi-Body Systems

> **Pedagogical Goal**: Differentiate static self-adjusting friction from kinetic dynamic friction, analyze angle of repose, and solve threshold slipping in stacked two-block systems.


---

### Concept: Microscopic Mechanism and Nature of Dry Friction

**Definition**: Friction is the tangential contact force opposing relative tangential displacement or tendency thereof between solid surfaces, arising from microscopic intermolecular electromagnetic bonding (cold-welding) at microscopic asperities.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Dry solid-solid contact (Coulomb-Amontons model)
- Macroscopic contact


---

### Concept: Self-Adjusting Static Friction and Limiting Value

**Definition**: Static friction $f_s$ is a self-adjusting tangential reaction force that exactly balances the net applied tangential driving force $F_{\parallel}$ up to a maximum threshold called limiting friction: $0 \le f_s \le f_{s,\text{max}} = \mu_s N$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Zero relative velocity ($v_{\text{rel}} = 0$)
- Constant static coefficient $\mu_s$


---

### Concept: Kinetic Sliding Friction and Relative Velocity Opposition

**Definition**: Once relative motion begins, the contact surfaces exert kinetic friction of magnitude $f_k = \mu_k N$, whose direction strictly opposes the relative velocity vector of the contact point: $\vec{f}_k = -\mu_k N \frac{\vec{v}_{\text{rel}}}{|\vec{v}_{\text{rel}}|}$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Non-zero relative sliding velocity ($v_{\text{rel}} \ne 0$)
- $\mu_k \le \mu_s$


---

### Concept: Angle of Repose and Angle of Contact Friction

**Definition**: The angle of repose $\theta_R$ is the maximum incline angle for which a body placed on an inclined plane remains at rest without slipping: $\theta_R = \arctan(\mu_s)$. The angle of friction $\lambda$ is the angle made by the resultant contact reaction with the normal: $\tan\lambda = \mu$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Homogeneous plane inclination
- Uniform coefficient $\mu_s$


---

### Concept: Stacked Multi-Body Systems and Threshold Slipping

**Definition**: In stacked multi-body systems, friction at the mutual contact interface accelerates the passive block. There exists a threshold driving force $F_{\text{threshold}}$ below which both blocks move with common acceleration $a$, and above which relative slipping occurs.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Rigid block stacking
- Dry friction interface


---

### Formula: Coulomb Limiting Static Friction

**Governing Equation**:
$$ f_{s,\text{max}} = \mu_s N $$

**Variable Inventory & SI Units**:
- $f_{s,\text{max}}$: Maximum static friction magnitude
- $\mu_s$: Static friction coefficient (Unit: `dimensionless` | Dim: `[1]`)
- $N$: Normal contact force (Unit: `N` | Dim: `[M][L][T]^-2`)

**Physical Assumptions**:
- Dry solid-solid contact
- Surfaces at relative rest

**Domain of Validity**:
- Governs the onset of relative slipping


---

### Formula: Kinetic Friction Law

**Governing Equation**:
$$ f_k = \mu_k N $$

**Variable Inventory & SI Units**:
- $f_k$: Kinetic friction magnitude (Unit: `N` | Dim: `[M][L][T]^-2`)
- $\mu_k$: Kinetic friction coefficient (Unit: `dimensionless` | Dim: `[1]`)
- $N$: Normal contact force (Unit: `N` | Dim: `[M][L][T]^-2`)

**Physical Assumptions**:
- Active relative sliding motion between contact surfaces
- \mu_k \le \mu_s

**Domain of Validity**:
- Applies whenever relative sliding velocity is non-zero


---

### Formula: Angle of Repose Relation

**Governing Equation**:
$$ \theta_R = \arctan(\mu_s) \iff \tan\theta_R = \mu_s $$

**Variable Inventory & SI Units**:
- $\theta_R$: Critical angle of repose (Unit: `rad or deg` | Dim: `[1]`)
- $\mu_s$: Static friction coefficient (Unit: `dimensionless` | Dim: `[1]`)

**Physical Assumptions**:
- Uniform inclined plane under gravity alone
- Block at rest on verge of slipping

**Domain of Validity**:
- Applies to block on rough incline with no external cords or forces


---

### Derivation: Formula `formula-dyn-angle-repose`

**Target Governing Relation**:
$$ \tan\theta_R = \mu_s $$

#### Step-by-Step Proof
**Step 1**: 
$$ \sum F_{\perp} = N - mg \cos\theta = 0 \implies N = mg \cos\theta $$
*Physical Operation*: 

**Step 2**: 
$$ \sum F_{\parallel} = mg \sin\theta_R - f_{s,\text{max}} = 0 \implies f_{s,\text{max}} = mg \sin\theta_R $$
*Physical Operation*: 

**Step 3**: 
$$ mg \sin\theta_R = \mu_s (mg \cos\theta_R) \implies \tan\theta_R = \mu_s \iff \theta_R = \arctan(\mu_s) $$
*Physical Operation*: 


---

### Formula: Two-Block Threshold Slip Force

**Governing Equation**:
$$ F_{\text{thresh}} = \mu_s (m_1 + m_2) g $$

**Variable Inventory & SI Units**:
- $F_{\text{thresh}}$: Maximum horizontal force on bottom block for common motion
- $m_1$: Top block mass
- $m_2$: Bottom block mass
- $\mu_s$: Static friction coefficient between blocks

**Physical Assumptions**:
- Smooth floor under bottom block
- Friction only between blocks 1 and 2
- Horizontal pulling force on lower block m2

**Domain of Validity**:
- For F <= F_thresh both blocks accelerate together with a = F/(m1 + m2)


---

### Worked Pedagogical Example: `ex-dyn-two-block-threshold-01`

**Problem Statement**:
> A block $A$ of mass $m_1 = 2.0\text{ kg}$ sits on block $B$ of mass $m_2 = 4.0\text{ kg}$, which rests on a frictionless horizontal floor. The coefficient of static friction between $A$ and $B$ is $\mu_s = 0.40$ and kinetic friction is $\mu_k = 0.30$. A horizontal force $F$ is applied to block $B$. (Take $g = 9.8\text{ m/s}^2$). (a) Find the maximum force $F_{\text{thresh}}$ for which both blocks move together without slipping. (b) If $F = 35.0\text{ N}$, compute the acceleration of each block.

**Target Quantity**: `F_thresh, a_1, a_2`

#### Systematic Solution
**Step 1 ()**:
$$ f_{s,\text{max}} = \mu_s m_1 g = 0.40 \times 2.0 \times 9.8 = 7.84\text{ N} \implies a_{\text{max}} = \frac{f_{s,\text{max}}}{m_1} = \mu_s g = 0.40 \times 9.8 = 3.92\text{ m/s}^2 $$

Result: ``

**Step 2 ()**:
$$ F_{\text{thresh}} = (m_1 + m_2) a_{\text{max}} = (2.0 + 4.0) \times 3.92 = 6.0 \times 3.92 = 23.52\text{ N} $$

Result: ``

**Step 3 ()**:
$$ f_k = \mu_k m_1 g = 0.30 \times 2.0 \times 9.8 = 5.88\text{ N} $$

Result: ``

**Step 4 ()**:
$$ a_1 = \frac{f_k}{m_1} = \frac{5.88}{2.0} = 2.94\text{ m/s}^2, \quad a_2 = \frac{F - f_k}{m_2} = \frac{35.0 - 5.88}{4.0} = \frac{29.12}{4.0} = 7.28\text{ m/s}^2 $$

Result: ``

**Final Answer**: F_{\text{thresh}} = 23.52\text{ N}; \quad a_1 = 2.94\text{ m/s}^2, \quad a_2 = 7.28\text{ m/s}^2

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Assuming static friction continues to act after slipping begins instead of dropping to kinetic value f_k

**Sanity & Consistency Checks**:
- Block B accelerates faster than block A (7.28 > 2.94 m/s^2), consistent with B slipping forward from underneath A
- If F <= 23.52 N, both accelerate at F/6.0


---

### Inoculation Against Misconception: `misc-dyn-03`

**Misconception Category**: `FRICTION_ALWAYS_OPPOSES_MOTION`  
**Erroneous Intuition**: *"Friction always acts in the opposite direction of motion and slows objects down."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Confusing 'motion of a body relative to ground' with 'relative motion of the contact surfaces'.

**Physical Truth & Resolution**:
Friction opposes relative sliding between contact surfaces, NOT the motion of the body relative to ground. Friction is often the driving force that accelerates objects forward. When walking, static friction from ground pushes foot forward. In an accelerating truck, static friction between floor and a crate accelerates the crate forward.

**Refutation Counterexample & Supporting Evidence**:
When a car accelerates forward from rest, the rear tires push backward on the road, and road friction pushes forward on the tires, accelerating the car forward.

**Diagnostic Symptom**: \vec{f}_k = -\mu_k N \frac{\vec{v}_{\text{rel}}}{|\vec{v}_{\text{rel}}|}, \quad \text{opposes } \vec{v}_{\text{rel}} = \vec{v}_{\text{contact 1}} - \vec{v}_{\text{contact 2}}.


---

### Inoculation Against Misconception: `misc-dyn-04`

**Misconception Category**: `STATIC_FRICTION_IS_ALWAYS_MAXIMAL`  
**Erroneous Intuition**: *"The static friction force acting on a stationary object is always equal to mu_s N."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Using the formula f_s = mu_s N as an equality rather than an inequality bound.

**Physical Truth & Resolution**:
Static friction is a self-adjusting force: it only takes on the exact value required to maintain equilibrium, satisfying 0 <= f_s <= mu_s N. If an object of mass 10 kg (mu_s = 0.5, N = 98 N, f_s,max = 49 N) is pushed horizontally with 10 N, static friction is exactly 10 N, not 49 N.

**Refutation Counterexample & Supporting Evidence**:
A book at rest on a horizontal desk with no horizontal applied force has static friction f_s = 0, even though mu_s N is non-zero.

**Diagnostic Symptom**: f_s = F_{\text{applied}} \quad \text{for } F_{\text{applied}} \le \mu_s N. \quad f_s = \mu_s N \text{ ONLY at verge of slipping.}


---

### Verified JEE Practice Problem: `laws-of-motion-question-e37050bb`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> What is the maximum value of the force $F$ such that the block shown in the arrangement, does not move?

$m = \sqrt{3}\text{ kg}$, $F$ is applied at $60°$ to the horizontal, $\mu = \frac{1}{2\sqrt{3}}$.

**Options**:
- **(A)**: $20\text{ N}$
- **(B)**: $10\text{ N}$
- **(C)**: $12\text{ N}$
- **(D)**: $15\text{ N}$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `laws-of-motion-question-e37050bb`

</details>


---

### Verified JEE Practice Problem: `laws-of-motion-question-ba0b4106`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> An insect crawls up a hemispherical surface very slowly. The coefficient of friction between the insect and the surface is $\frac{1}{3}$. If the line joining the centre of the hemispherical surface to the insect makes an angle $\alpha$ with the vertical, the maximum possible value of $\alpha$ so that the insect does not slip is given by

**Options**:
- **(A)**: $\cot \alpha = 3$
- **(B)**: $\sec \alpha = 3$
- **(C)**: $\operatorname{cosec} \alpha = 3$
- **(D)**: $\cos \alpha = 3$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **A**  
**Independent Verification Record**: `laws-of-motion-question-ba0b4106`

</details>


---

## Dynamics of Circular Motion, Banking of Roads, and Conical Pendulum

> **Pedagogical Goal**: Analyze radial dynamics, centripetal acceleration, optimum banking angles with and without friction, and conical pendulum geometry.


---

### Concept: Centripetal Acceleration and Radial Dynamics in Curved Paths

**Definition**: A particle of mass $m$ traversing a curved trajectory of instantaneous radius of curvature $R$ with speed $v$ experiences radial acceleration $a_c = v^2/R$, requiring a net inward radial force $F_c = m v^2 / R = m \omega^2 R$.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Curved trajectory with local radius of curvature $R$
- Inertial reference frame


---

### Concept: Optimum Banking of Roads and Friction Safe Envelopes

**Definition**: Tilting a curved roadway by an angle $\theta$ allows the horizontal component of the normal reaction $N\sin\theta$ to provide the centripetal acceleration, defining an optimum speed $v_0 = \sqrt{R g \tan\theta}$ requiring zero lateral friction.

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Circular curve of radius $R$
- Planar incline angle $\theta$


---

### Concept: The Conical Pendulum and Horizontal Circle Dynamics

**Definition**: A bob of mass $m$ suspended by a light string of length $L$ revolving in a horizontal circle of radius $R = L\sin\theta$ at constant speed $v$, where string tension vertical component balances weight ($T\cos\theta = mg$) and horizontal component provides centripetal force ($T\sin\theta = m v^2/R$).

**Physical Significance**: 

**Assumptions & Scope of Validity**:
- Inextensible light string of length $L$
- Constant angular velocity $\omega$
- Uniform gravity $g$


---

### Formula: Centripetal Force Relation

**Governing Equation**:
$$ F_c = \frac{m v^2}{R} = m \omega^2 R $$

**Variable Inventory & SI Units**:
- $F_c$: Net inward radial force (Unit: `N` | Dim: `[M][L][T]^-2`)
- $m$: Mass (Unit: `kg` | Dim: `[M]`)
- $v$: Speed (Unit: `m s^-1` | Dim: `[L][T]^-1`)
- $R$: Radius of curvature (Unit: `m` | Dim: `[L]`)
- $\omega$: Angular velocity (Unit: `rad s^-1` | Dim: `[T]^-1`)

**Physical Assumptions**:
- Curved trajectory of instantaneous radius R
- Inertial frame of reference

**Domain of Validity**:
- Universal for any 2D or 3D curved trajectory


---

### Formula: Optimum Banking Angle Formula

**Governing Equation**:
$$ v_0 = \sqrt{R g \tan\theta} \iff \tan\theta = \frac{v_0^2}{R g} $$

**Variable Inventory & SI Units**:
- $v_0$: Optimum design speed (Unit: `m s^-1` | Dim: `[L][T]^-1`)
- $R$: Curve radius (Unit: `m` | Dim: `[L]`)
- $g$: Gravitational acceleration (Unit: `m s^-2` | Dim: `[L][T]^-2`)
- $\theta$: Incline banking angle (Unit: `rad or deg` | Dim: `[1]`)

**Physical Assumptions**:
- Circular curve of radius R
- Zero sideways lateral friction required

**Domain of Validity**:
- Applies at exact optimum rated design speed


---

### Derivation: Formula `formula-dyn-banking-optimum`

**Target Governing Relation**:
$$ \tan\theta = \frac{v_0^2}{R g} $$

#### Step-by-Step Proof
**Step 1**: 
$$ N_y = N \cos\theta, \quad N_x = N \sin\theta $$
*Physical Operation*: 

**Step 2**: 
$$ \sum F_y = N \cos\theta - mg = 0 \implies N = \frac{mg}{\cos\theta} $$
*Physical Operation*: 

**Step 3**: 
$$ N \sin\theta = \frac{m v_0^2}{R} \implies \left(\frac{mg}{\cos\theta}\right)\sin\theta = \frac{m v_0^2}{R} \implies \tan\theta = \frac{v_0^2}{R g} $$
*Physical Operation*: 


---

### Formula: Banked Curve Safe Speed Limits with Friction

**Governing Equation**:
$$ v_{\text{max}} = \sqrt{R g \left( \frac{\tan\theta + \mu_s}{1 - \mu_s \tan\theta} \right)}, \quad v_{\text{min}} = \sqrt{R g \left( \frac{\tan\theta - \mu_s}{1 + \mu_s \tan\theta} \right)} $$

**Variable Inventory & SI Units**:
- $v_{\text{max}}$: Maximum speed before skidding outward
- $v_{\text{min}}$: Minimum speed before slipping inward
- $\mu_s$: Static friction coefficient (Unit: `dimensionless` | Dim: `[1]`)
- $\theta$: Banking angle

**Physical Assumptions**:
- Static friction coefficient mu_s < cot(theta) for non-zero v_min
- Rigid circular road bed

**Domain of Validity**:
- Defines the safe non-skid speed envelope [v_min, v_max]


---

### Formula: Conical Pendulum Revolution Period

**Governing Equation**:
$$ T = 2\pi \sqrt{\frac{L \cos\theta}{g}} $$

**Variable Inventory & SI Units**:
- $T$: Period of revolution (Unit: `s` | Dim: `[T]`)
- $L$: String length (Unit: `m` | Dim: `[L]`)
- $\theta$: Semi-vertical angle (Unit: `rad or deg` | Dim: `[1]`)
- $g$: Gravitational acceleration (Unit: `m s^-2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Inextensible light string
- Constant speed revolution in horizontal circle
- Uniform vertical gravity

**Domain of Validity**:
- Valid for 0 < theta < pi/2


---

### Derivation: Formula `formula-dyn-conical-period`

**Target Governing Relation**:
$$ T = 2\pi \sqrt{\frac{L \cos\theta}{g}} $$

#### Step-by-Step Proof
**Step 1**: 
$$ T \cos\theta = mg, \quad T \sin\theta = m \omega^2 (L \sin\theta) $$
*Physical Operation*: 

**Step 2**: 
$$ T = m \omega^2 L \implies \left(\frac{mg}{\cos\theta}\right) = m \omega^2 L \implies \omega = \sqrt{\frac{g}{L \cos\theta}} $$
*Physical Operation*: 

**Step 3**: 
$$ T = \frac{2\pi}{\omega} = 2\pi \sqrt{\frac{L \cos\theta}{g}} $$
*Physical Operation*: 


---

### Worked Pedagogical Example: `ex-dyn-banking-curve-01`

**Problem Statement**:
> A highway curve of radius $R = 200\text{ m}$ is banked at an angle $\theta = 15^\circ$. The coefficient of static friction between the road and tires is $\mu_s = 0.25$. Taking $g = 9.8\text{ m/s}^2$, calculate: (a) the optimum rated speed $v_0$ where no lateral friction is needed, and (b) the maximum safe speed $v_{\text{max}}$ before skidding outward.

**Target Quantity**: `v_0, v_max`

#### Systematic Solution
**Step 1 ()**:
$$ v_0 = \sqrt{200 \times 9.8 \times \tan 15^\circ} = \sqrt{1960 \times 0.26795} = \sqrt{525.18} \approx 22.92\text{ m/s} \approx 82.5\text{ km/h} $$

Result: ``

**Step 2 ()**:
$$ v_{\text{max}} = \sqrt{R g \left( \frac{\tan\theta + \mu_s}{1 - \mu_s \tan\theta} \right)} = \sqrt{1960 \times \left( \frac{0.26795 + 0.25}{1 - 0.25 \times 0.26795} \right)} = \sqrt{1960 \times \frac{0.51795}{0.93301}} = \sqrt{1960 \times 0.55514} = \sqrt{1088.07} \approx 32.99\text{ m/s} \approx 118.7\text{ km/h} $$

Result: ``

**Final Answer**: v_0 \approx 22.9\text{ m/s} \; (82.5\text{ km/h}), \quad v_{\text{max}} \approx 33.0\text{ m/s} \; (118.7\text{ km/h})

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Confusing tangent argument in friction modifier formula or using degrees instead of radians in trigonometric function

**Sanity & Consistency Checks**:
- v_max (33.0 m/s) is strictly greater than rated speed v_0 (22.9 m/s)
- When mu_s = 0, v_max collapses to v_0


---

### Worked Pedagogical Example: `ex-dyn-conical-pendulum-01`

**Problem Statement**:
> A conical pendulum consists of a bob of mass $m = 0.50\text{ kg}$ suspended by a light string of length $L = 1.20\text{ m}$. The bob revolves in a horizontal circle such that the string makes a constant angle $\theta = 30^\circ$ with the vertical. Taking $g = 9.8\text{ m/s}^2$, find: (a) the tension $T$ in the string, (b) the linear speed $v$ of the bob, and (c) the period $\tau$ of revolution.

**Target Quantity**: `T, v, tau`

#### Systematic Solution
**Step 1 ()**:
$$ T \cos 30^\circ = mg \implies T = \frac{0.50 \times 9.8}{\cos 30^\circ} = \frac{4.9}{0.8660} \approx 5.658\text{ N} $$

Result: ``

**Step 2 ()**:
$$ R = L \sin 30^\circ = 1.20 \times 0.5 = 0.60\text{ m}, \quad T \sin 30^\circ = \frac{m v^2}{R} \implies v = \sqrt{\frac{R T \sin 30^\circ}{m}} = \sqrt{\frac{0.60 \times 5.658 \times 0.5}{0.50}} = \sqrt{3.395} \approx 1.843\text{ m/s} $$

Result: ``

**Step 3 ()**:
$$ \tau = 2\pi \sqrt{\frac{1.20 \times \cos 30^\circ}{9.8}} = 2\pi \sqrt{\frac{1.20 \times 0.8660}{9.8}} = 2\pi \sqrt{\frac{1.0392}{9.8}} = 2\pi \sqrt{0.10604} = 2\pi \times 0.3256 \approx 2.046\text{ s} $$

Result: ``

**Final Answer**: T \approx 5.66\text{ N}, \quad v \approx 1.84\text{ m/s}, \quad \tau \approx 2.05\text{ s}

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Using L instead of horizontal radius R = L sin(theta) in centripetal formula

**Sanity & Consistency Checks**:
- Circumference check: 2 pi R / v = 2 pi (0.60) / 1.843 = 3.7699 / 1.843 = 2.046 s, agreeing exactly with period formula


---

### Inoculation Against Misconception: `misc-dyn-05`

**Misconception Category**: `CENTRIPETAL_FORCE_AS_PHYSICAL_ENTITY`  
**Erroneous Intuition**: *"Centripetal force is a distinct physical force that must be added to a free-body diagram in circular motion."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Treating m v^2 / R as an independent active interaction like gravity or tension.

**Physical Truth & Resolution**:
Centripetal force is not an independent physical force; it is simply the mass times centripetal acceleration m a_c on the right-hand side of Newton's second law: sum F_radial = m v^2 / R. It is provided by real physical agents (tension, gravity, normal reaction, friction). Adding an extra 'centripetal force' vector double-counts the net force.

**Refutation Counterexample & Supporting Evidence**:
For a satellite in circular orbit, gravity is the ONLY physical force acting. Gravity provides the required centripetal acceleration G M m / r^2 = m v^2 / r.

**Diagnostic Symptom**: \sum \vec{F}_{\text{real, radial}} = \frac{m v^2}{R} \hat{r}_{\text{inward}}. \quad \text{Never draw } \vec{F}_c \text{ as a separate force!}


---

## Chapter Summary & Formula Recap: Newton's Laws of Motion & Dynamics

### Core Equations & Domains of Validity
- **Newton's Second Law for Constant Mass**: $$\vec{F}_{\text{net}} = m \vec{a} = m \frac{d^2 \vec{r}}{dt^2}$$
  *Validity*: Universal for translation of point mass or center of mass in classical mechanics
- **Newton's Third Law (Action-Reaction)**: $$\vec{F}_{AB} = -\vec{F}_{BA}$$
  *Validity*: Collinear central mutual interaction in classical mechanics
- **Impulse-Momentum Theorem**: $$\vec{J} = \int_{t_1}^{t_2} \vec{F}_{\text{net}} \, dt = \Delta \vec{p} = m \vec{v}_2 - m \vec{v}_1$$
  *Validity*: Universal for any force time-profile
- **Virtual Work Pulley Constraint Relation**: $$\sum_{i=1}^n \vec{T}_i \cdot \vec{a}_i = 0$$
  *Validity*: Valid for any connected pulley system while string tension remains positive
- **Wedge Normal Acceleration Constraint**: $$(\vec{a}_{\text{block}} - \vec{a}_{\text{wedge}}) \cdot \hat{n} = 0$$
  *Validity*: Valid while contact normal force N > 0
- **Linear Inertial Pseudo-Force**: $$\vec{F}_{\text{pseudo}} = -m \vec{a}_0$$
  *Validity*: Must be applied to all bodies when formulating Newton's laws in accelerating frame
- **Coulomb Limiting Static Friction**: $$f_{s,\text{max}} = \mu_s N$$
  *Validity*: Governs the onset of relative slipping
- **Kinetic Friction Law**: $$f_k = \mu_k N$$
  *Validity*: Applies whenever relative sliding velocity is non-zero
- **Angle of Repose Relation**: $$\theta_R = \arctan(\mu_s) \iff \tan\theta_R = \mu_s$$
  *Validity*: Applies to block on rough incline with no external cords or forces
- **Two-Block Threshold Slip Force**: $$F_{\text{thresh}} = \mu_s (m_1 + m_2) g$$
  *Validity*: For F <= F_thresh both blocks accelerate together with a = F/(m1 + m2)
- **Centripetal Force Relation**: $$F_c = \frac{m v^2}{R} = m \omega^2 R$$
  *Validity*: Universal for any 2D or 3D curved trajectory
- **Optimum Banking Angle Formula**: $$v_0 = \sqrt{R g \tan\theta} \iff \tan\theta = \frac{v_0^2}{R g}$$
  *Validity*: Applies at exact optimum rated design speed
- **Banked Curve Safe Speed Limits with Friction**: $$v_{\text{max}} = \sqrt{R g \left( \frac{\tan\theta + \mu_s}{1 - \mu_s \tan\theta} \right)}, \quad v_{\text{min}} = \sqrt{R g \left( \frac{\tan\theta - \mu_s}{1 + \mu_s \tan\theta} \right)}$$
  *Validity*: Defines the safe non-skid speed envelope [v_min, v_max]
- **Conical Pendulum Revolution Period**: $$T = 2\pi \sqrt{\frac{L \cos\theta}{g}}$$
  *Validity*: Valid for 0 < theta < pi/2
