# Chapter: Kinematics: Rest, Motion, and Trajectories

**Template**: `MECHANICS`  
**Prerequisites**: units-and-dimensions, vectors-and-coordinate-systems, differential-calculus-foundations, integral-calculus-foundations  

## Learning Objectives
- Differentiate between distance and displacement, speed and velocity.
- Formulate and solve problems involving constant and variable acceleration using calculus.
- Analyze motion under gravity as a specific case of uniform acceleration.
- Interpret and construct position-time, velocity-time, and acceleration-time graphs.
- Decompose 2D projectile motion into independent 1D motions.
- Analyze projectile motion on inclined planes.
- Apply relative velocity concepts to solve rain-umbrella and river-swimmer problems.
- Determine conditions for collision and shortest distance of approach between moving bodies.

---

## Position, Displacement, Speed, Velocity, and Graph Slope/Area

> **Pedagogical Goal**: Establish the fundamental distinction between path-dependent scalar quantities and path-independent vector quantities in 1D.


---

### Concept: Position, Distance, and Displacement

**Definition**: Let a particle occupy position vector $\vec{r}_1 = \vec{r}(t_1)$ at initial time $t_1$ and $\vec{r}_2 = \vec{r}(t_2)$ at later time $t_2$. The displacement vector is defined as $\Delta\vec{r} = \vec{r}_2 - \vec{r}_1$. The distance traversed is the arc length integral $s = \int_{t_1}^{t_2} |\vec{v}(t)|\,dt$. While distance $s$ is a scalar path-dependent quantity ($s \ge |\Delta\vec{r}|$), displacement $\Delta\vec{r}$ depends solely on initial and final coordinates.

**Physical Significance**: Imagine walking along a winding mountain trail from a camp to an observation point. The odometer on your boots records the total ground trodden—this is distance, a non-negative scalar that never decreases. In contrast, the direct arrow connecting the camp to where you stand is your displacement vector. If you walk 5 km out and 5 km back, your distance is 10 km, but your net displacement is zero.

**Assumptions & Scope of Validity**:
- Point mass particle assumption (internal degrees of freedom and spatial extent are ignored).
- Continuous and piecewise differentiable trajectory in Euclidean three-space.


---

### Concept: Average and Instantaneous Speed and Velocity

**Definition**: The average velocity over a finite time interval $\Delta t = t_2 - t_1$ is $\vec{v}_{\text{avg}} = \frac{\Delta\vec{r}}{\Delta t} = \frac{\vec{r}(t_2) - \vec{r}(t_1)}{t_2 - t_1}$. The instantaneous velocity $\vec{v}(t)$ is the derivative of position with respect to time: $\vec{v}(t) = \lim_{\Delta t \to 0} \frac{\Delta\vec{r}}{\Delta t} = \frac{d\vec{r}}{dt}$. Instantaneous speed $v(t) = |\vec{v}(t)| = \frac{ds}{dt}$ is the magnitude of instantaneous velocity, whereas average speed is total distance divided by total time: $v_{\text{avg}} = \frac{s_{\text{total}}}{t_{\text{total}}}$.

**Physical Significance**: When driving a car, your trip may take 2 hours to cover a 100 km curved highway, giving an average speed of 50 km/h. At any split second during the drive, glancing at the speedometer displays your instantaneous speed (e.g. 70 km/h), while the direction the front of your car points gives the direction of your instantaneous velocity vector.

**Assumptions & Scope of Validity**:
- Position function $\vec{r}(t)$ is continuous and differentiable over the time domain.
- Time flows uniformly and monotonically ($dt > 0$).


---

### Inoculation Against Misconception: `misc-kin-01`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"If a particle has zero velocity at any instant, it is not accelerating."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Velocity is the instantaneous value of position derivative v = dx/dt, whereas acceleration is its rate of change a = dv/dt. A function can easily pass through zero while having a steep slope.

**Physical Truth & Resolution**:
Acceleration is the time derivative of velocity, not velocity itself. When an object reverses direction, its velocity must cross through zero, but its acceleration is non-zero because the velocity is changing continuously.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma Vol 1, Chapter 3: 'At the highest point the velocity is zero, but the acceleration is non-zero (g downward).'

**Diagnostic Symptom**: Student concludes that net force or acceleration is zero at turning points or tops of swings.


---

## Acceleration, Derivation of Constant Acceleration Equations, Calculus Integration, Free Fall

> **Pedagogical Goal**: Extend kinematic analysis to accelerated systems using calculus, culminating in standard equations for uniform acceleration and motion under gravity.


---

### Concept: Acceleration and Deceleration

**Definition**: Instantaneous acceleration is defined as $\vec{a}(t) = \lim_{\Delta t \to 0} \frac{\Delta\vec{v}}{\Delta t} = \frac{d\vec{v}}{dt} = \frac{d^2\vec{r}}{dt^2}$. In one dimension, acceleration can be expressed either as an explicit function of time $a = \frac{dv}{dt}$, or via the chain rule as a function of position $a = \frac{dv}{dt} = \frac{dv}{dx}\frac{dx}{dt} = v\frac{dv}{dx}$. Deceleration refers strictly to the condition where speed decreases, which occurs if and only if $\vec{v} \cdot \vec{a} < 0$.

**Physical Significance**: Acceleration is not simply 'going fast'—it is changing your velocity vector. If you hit the gas pedal, you accelerate forward. If you slam on the brakes, you accelerate backward (decelerating). If you turn a sharp corner at constant speedometer speed, your direction changes, meaning you are accelerating toward the inside of the turn.

**Assumptions & Scope of Validity**:
- Velocity function $\vec{v}(t)$ is differentiable.
- Inertial reference frame or accounting for pseudo-forces.


---

### Concept: Free Fall and Vertical Motion Under Gravity

**Definition**: In the absence of air resistance near the Earth's surface, all bodies experience a constant downward gravitational acceleration of magnitude $g \approx 9.8\text{ m/s}^2$ (or $10\text{ m/s}^2$ for typical JEE calculations), independent of mass, shape, or composition. Taking vertically upward as positive $+y$, the acceleration is $a_y = -g$. For launch speed $u$, the maximum height attained is $H_{\text{max}} = \frac{u^2}{2g}$, the time to apex is $t_{\text{ascent}} = \frac{u}{g}$, and total flight time is $T = \frac{2u}{g}$.

**Physical Significance**: When an apple is thrown straight upward, the Earth's gravity pulls downward with constant vigor every second of its flight. On the way up, gravity slows it down by 9.8 m/s every second until it momentarily pauses at the apex. On the way down, gravity speeds it up by 9.8 m/s every second. By pure symmetry, the time to rise to the apex equals the time to fall back to the launch height, and it strikes your hand with the exact speed it was launched.

**Assumptions & Scope of Validity**:
- Uniform gravitational field (valid for vertical displacements $h \ll R_{\text{Earth}}$).
- Air resistance and buoyancy of air are neglected.
- Earth's rotation (Coriolis acceleration) is neglected.


---

### Formula: First Kinematic Equation (Velocity-Time Relation)

**Governing Equation**:
$$ v = u + a t $$

**Variable Inventory & SI Units**:
- $v$: Final velocity at time t (Unit: `m/s` | Dim: `[L][T]^-1`)
- $u$: Initial velocity at time t = 0 (Unit: `m/s` | Dim: `[L][T]^-1`)
- $a$: Constant uniform acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $t$: Elapsed time duration (Unit: `s` | Dim: `[T]`)

**Physical Assumptions**:
- Acceleration a is strictly constant in both magnitude and direction
- 1D rectilinear motion

**Domain of Validity**:
- Applies only when acceleration does not vary with time, velocity, or position


---

### Derivation: Formula `formula-kin-const-accel-v`

**Target Governing Relation**:
$$ v = u + a t $$

#### Step-by-Step Proof
**Step 1**: Express acceleration as first derivative of velocity
$$ a = \frac{dv}{dt} \implies dv = a \, dt $$
*Physical Operation*: Definition of instantaneous rate of change of velocity.

**Step 2**: Integrate both sides with initial condition v(0) = u and final condition v(t) = v
$$ \int_{u}^{v} dv = \int_{0}^{t} a \, dt $$
*Physical Operation*: Definite integration over corresponding physical limits.

**Step 3**: Factor constant acceleration out of the integral and evaluate
$$ [v]_{u}^{v} = a [t]_{0}^{t} \implies v - u = a t \implies v = u + a t $$
*Physical Operation*: Fundamental theorem of calculus for constant integrand a.

**Applicability & Limiting Conditions**:
- Strictly valid only when a is independent of time t


---

### Formula: Second Kinematic Equation (Position-Time Relation)

**Governing Equation**:
$$ s = u t + \frac{1}{2} a t^2 $$

**Variable Inventory & SI Units**:
- $s$: Displacement over time interval t (Unit: `m` | Dim: `[L]`)
- $u$: Initial velocity at t = 0 (Unit: `m/s` | Dim: `[L][T]^-1`)
- $a$: Constant uniform acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $t$: Elapsed time (Unit: `s` | Dim: `[T]`)

**Physical Assumptions**:
- Acceleration a is strictly constant
- Motion along a single line

**Domain of Validity**:
- Displacement s represents net position shift x(t) - x(0), not total distance


---

### Derivation: Formula `formula-kin-const-accel-s`

**Target Governing Relation**:
$$ s = u t + \frac{1}{2} a t^2 $$

#### Step-by-Step Proof
**Step 1**: Express velocity as time rate of change of position
$$ v = \frac{dx}{dt} \implies dx = v(t) \, dt $$
*Physical Operation*: Calculus definition of instantaneous velocity.

**Step 2**: Substitute the first kinematic relation v(t) = u + at into the differential
$$ dx = (u + a t) \, dt $$
*Physical Operation*: Velocity variation under uniform acceleration.

**Step 3**: Integrate both sides from t = 0 (x = 0) to time t (position x = s)
$$ \int_{0}^{s} dx = \int_{0}^{t} (u + a t) \, dt $$
*Physical Operation*: Definite integration over elapsed time.

**Step 4**: Evaluate the polynomial integrals
$$ s = \left[ u t + \frac{1}{2} a t^2 \right]_{0}^{t} = u t + \frac{1}{2} a t^2 $$
*Physical Operation*: Power rule of integration.

**Applicability & Limiting Conditions**:
- Valid for constant acceleration and initial position at origin


---

### Formula: Third Kinematic Equation (Velocity-Displacement Relation)

**Governing Equation**:
$$ v^2 = u^2 + 2 a s $$

**Variable Inventory & SI Units**:
- $v$: Final velocity (Unit: `m/s` | Dim: `[L][T]^-1`)
- $u$: Initial velocity (Unit: `m/s` | Dim: `[L][T]^-1`)
- $a$: Constant acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $s$: Net displacement (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Constant acceleration a
- Time t is eliminated

**Domain of Validity**:
- Valid for 1D uniform acceleration; represents work-energy theorem per unit mass


---

### Derivation: Formula `formula-kin-const-accel-v2`

**Target Governing Relation**:
$$ v^2 = u^2 + 2 a s $$

#### Step-by-Step Proof
**Step 1**: Apply chain rule to express acceleration without explicit time dependence
$$ a = \frac{dv}{dt} = \frac{dv}{dx} \frac{dx}{dt} = v \frac{dv}{dx} $$
*Physical Operation*: Chain rule of calculus where v = dx/dt.

**Step 2**: Separate variables v and x
$$ v \, dv = a \, dx $$
*Physical Operation*: Separation of variables for first-order differential form.

**Step 3**: Integrate from initial state (x = 0, v = u) to final state (x = s, v = v)
$$ \int_{u}^{v} v \, dv = \int_{0}^{s} a \, dx $$
*Physical Operation*: Definite integration over spatial trajectory.

**Step 4**: Evaluate both integrals
$$ \left[ \frac{v^2}{2} \right]_{u}^{v} = a [x]_{0}^{s} \implies \frac{v^2 - u^2}{2} = a s \implies v^2 = u^2 + 2 a s $$
*Physical Operation*: Integration of linear function v and constant a.

**Applicability & Limiting Conditions**:
- Valid for 1D rectilinear motion under constant acceleration


---

### Formula: Displacement in the n-th Second

**Governing Equation**:
$$ s_n = u + \frac{a}{2} (2 n - 1) $$

**Variable Inventory & SI Units**:
- $s_n$: Displacement during the interval from t = (n-1) s to t = n s (Unit: `m` | Dim: `[L]`)
- $u$: Initial velocity at t = 0 (Unit: `m/s` | Dim: `[L][T]^-1`)
- $a$: Constant acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $n$: Integer second index (1, 2, 3, ...) (Unit: `dimensionless integer (representing 1 s unit)` | Dim: `[1]`)

**Physical Assumptions**:
- Time interval is exactly 1 second: Delta t = 1 s
- Constant acceleration a

**Domain of Validity**:
- Applicable only when n represents consecutive 1-second intervals from t = 0


---

### Derivation: Formula `formula-kin-nth-second`

**Target Governing Relation**:
$$ s_n = u + \frac{a}{2} (2 n - 1) $$

#### Step-by-Step Proof
**Step 1**: Define displacement in the n-th second as difference between total displacement at t = n and t = n-1
$$ s_n = s(n) - s(n - 1) $$
*Physical Operation*: Physical definition of displacement over the interval [n-1, n].

**Step 2**: Substitute second kinematic equation for t = n and t = n - 1
$$ s(n) = u n + \frac{1}{2} a n^2, \quad s(n - 1) = u (n - 1) + \frac{1}{2} a (n - 1)^2 $$
*Physical Operation*: Evaluation of position function at specific integer endpoints.

**Step 3**: Subtract the two displacement expressions and expand algebraically
$$ s_n = \left( u n + \frac{1}{2} a n^2 \right) - \left( u n - u + \frac{1}{2} a (n^2 - 2 n + 1) \right) $$
*Physical Operation*: Binomial expansion (n - 1)^2 = n^2 - 2n + 1.

**Step 4**: Simplify the algebraic terms
$$ s_n = u + \frac{1}{2} a \left( n^2 - n^2 + 2 n - 1 \right) = u + \frac{a}{2} (2 n - 1) $$
*Physical Operation*: Canceling quadratic n^2 terms.

**Applicability & Limiting Conditions**:
- Assumes duration of interval is strictly Delta t = 1 s


---

### Formula: Differential and Calculus Formulations of Acceleration

**Governing Equation**:
$$ a = \frac{dv}{dt} = v \frac{dv}{dx} = \frac{d^2 x}{dt^2} $$

**Variable Inventory & SI Units**:
- $a$: Instantaneous acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)
- $v$: Instantaneous velocity (Unit: `m/s` | Dim: `[L][T]^-1`)
- $x$: Position coordinate (Unit: `m` | Dim: `[L]`)
- $t$: Time (Unit: `s` | Dim: `[T]`)

**Physical Assumptions**:
- Differentiable position function x(t) and velocity function v(x)

**Domain of Validity**:
- Universal kinematic definition valid for arbitrary variable acceleration a(t), a(x), a(v)


---

### Worked Pedagogical Example: `ex-kin-calc-motion-01`

**Problem Statement**:
> A particle moves along the x-axis with acceleration a(t) = (3.0 t - 4.0) m/s^2, where t is in seconds. At time t = 0, the particle is at x(0) = 5.0 m and has velocity v(0) = 2.0 m/s. (a) Determine the velocity as a function of time v(t). (b) Determine the position as a function of time x(t). (c) Find the position of the particle when its velocity reaches a local minimum.

**Target Quantity**: `Velocity function v(t), position function x(t), and position at local minimum velocity`

#### Systematic Solution
**Step 1 ()**:
$$ v(t) = v(0) + \int_{0}^{t} (3.0 t' - 4.0) \, dt' = 2.0 + \left[ \frac{3.0}{2} t'^2 - 4.0 t' \right]_{0}^{t} = 1.5 t^2 - 4.0 t + 2.0 $$
Integral of 3 t is 1.5 t^2; integral of -4 is -4 t; adding initial v(0) = 2.0 gives v(t) = 1.5 t^2 - 4.0 t + 2.0 m/s.
Result: `v(t) = 1.5 t^2 - 4.0 t + 2.0 m/s`

**Step 2 ()**:
$$ x(t) = x(0) + \int_{0}^{t} (1.5 t'^2 - 4.0 t' + 2.0) \, dt' = 5.0 + \left[ 0.5 t'^3 - 2.0 t'^2 + 2.0 t' \right]_{0}^{t} = 0.5 t^3 - 2.0 t^2 + 2.0 t + 5.0 $$
Integral of 1.5 t^2 is 0.5 t^3; integral of -4 t is -2 t^2; integral of 2 is 2 t; adding initial x(0) = 5.0 gives x(t).
Result: `x(t) = 0.5 t^3 - 2.0 t^2 + 2.0 t + 5.0 m`

**Step 3 ()**:
$$ a(t) = 3.0 t - 4.0 = 0 \implies t_{\text{min}} = \frac{4.0}{3.0} = \frac{4}{3}\text{ s} $$
t = 4/3 s approx 1.333 s.
Result: `t = 4/3 s`

**Step 4 ()**:
$$ x(4/3) = 0.5 \left(\frac{4}{3}\right)^3 - 2.0 \left(\frac{4}{3}\right)^2 + 2.0 \left(\frac{4}{3}\right) + 5.0 = \frac{1}{2}\frac{64}{27} - 2 \frac{16}{9} + \frac{8}{3} + 5 = \frac{32}{27} - \frac{96}{27} + \frac{72}{27} + \frac{135}{27} = \frac{143}{27} \approx 5.30\text{ m} $$
32 - 96 + 72 + 135 = 143/27 approx 5.296 m.
Result: `x = 143/27 m approx 5.30 m`

**Final Answer**: v(t) = (1.5 t^2 - 4.0 t + 2.0) m/s; x(t) = (0.5 t^3 - 2.0 t^2 + 2.0 t + 5.0) m; position at minimum velocity is 143/27 m (approx 5.30 m).

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Do not use standard kinematic equations v = u + at because acceleration is time-dependent!

**Sanity & Consistency Checks**:
- At t = 0: v(0) = 2.0 m/s and x(0) = 5.0 m, which strictly match given initial conditions.
- Dimensional check: [1.5 t^2] = [T^-2][T^2] = [1] with pre-factor unit m/s^3 => [L][T]^-1, dimensionally homogeneous.


---

### Worked Pedagogical Example: `ex-kin-gravity-balloon-01`

**Problem Statement**:
> A hot-air balloon is ascending vertically with a constant speed of 12.0 m/s. When the balloon is at a height of 65.0 m above the ground, a passenger drops a sandbag. Taking downward gravity g = 10.0 m/s^2, determine: (a) the maximum height reached by the sandbag above the ground, and (b) the total time elapsed from the instant the sandbag is released until it strikes the ground.

**Target Quantity**: `Maximum height H_max above ground and time of flight t_ground`

#### Systematic Solution
**Step 1 ()**:
$$ y_0 = +65.0\text{ m}, \quad u = +12.0\text{ m/s}, \quad a = -g = -10.0\text{ m/s}^2 $$
u = +12.0 m/s, y_0 = 65.0 m.
Result: `Initial state established`

**Step 2 ()**:
$$ 0 = (12.0)^2 - 2(10.0)(H_{\text{max}} - 65.0) \implies H_{\text{max}} - 65.0 = \frac{144}{20} = 7.20\text{ m} $$
Apex height above ground H_max = 65.0 + 7.2 = 72.2 m.
Result: `H_max = 72.2 m`

**Step 3 ()**:
$$ y(t) = y_0 + u t - \frac{1}{2} g t^2 = 0 \implies 65.0 + 12.0 t - 5.0 t^2 = 0 \implies 5 t^2 - 12 t - 65 = 0 $$
Dividing quadratic: 5 t^2 - 12 t - 65 = 0.
Result: `5 t^2 - 12 t - 65 = 0`

**Step 4 ()**:
$$ t = \frac{-(-12) \pm \sqrt{(-12)^2 - 4(5)(-65)}}{2(5)} = \frac{12 \pm \sqrt{144 + 1300}}{10} = \frac{12 \pm \sqrt{1444}}{10} = \frac{12 \pm 38}{10} $$
t = (12 + 38)/10 = 50/10 = 5.0 s (negative root t = -2.6 s discarded as unphysical).
Result: `t = 5.0 s`

**Final Answer**: (a) Maximum height above ground is 72.2 m. (b) Total time to strike the ground is 5.0 s.

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Do not assume initial velocity is zero! The bag was moving upward with the balloon at 12 m/s when released.

**Sanity & Consistency Checks**:
- Time to apex: t_apex = u/g = 12/10 = 1.2 s.
- Free fall from apex of 72.2 m: t_fall = sqrt(2 * 72.2 / 10) = sqrt(14.44) = 3.8 s.
- Total flight time: t_total = t_apex + t_fall = 1.2 + 3.8 = 5.0 s, exactly matching the quadratic solution!


---

### Inoculation Against Misconception: `misc-kin-02`

**Misconception Category**: `SIGN_MISTAKE`  
**Erroneous Intuition**: *"Whenever a < 0, the object must be slowing down."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> The sign of acceleration merely indicates its vector direction along the chosen coordinate axis. It has no intrinsic connection to whether speed is increasing or decreasing without comparing it to the sign of velocity.

**Physical Truth & Resolution**:
Deceleration means decreasing speed, which occurs when velocity and acceleration vectors point in opposite directions (v . a < 0). A negative acceleration with negative velocity causes the body to speed up in the negative direction.

**Refutation Counterexample & Supporting Evidence**:
Halliday & Resnick, Chapter 2: 'Deceleration does not mean acceleration is negative. It means speed is decreasing.'

**Diagnostic Symptom**: Student assumes a car moving along -x with a = -2 m/s^2 is slowing down.


---

### Inoculation Against Misconception: `misc-kin-03`

**Misconception Category**: `VECTOR_SCALAR_CONFUSION`  
**Erroneous Intuition**: *"Average speed is just the absolute value of average velocity."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Average velocity depends on net displacement Delta r = r_f - r_i, whereas average speed depends on total path length s_total = int |v| dt. Since path length exceeds displacement whenever direction changes, average speed exceeds average velocity magnitude.

**Physical Truth & Resolution**:
Instantaneous speed is indeed the magnitude of instantaneous velocity, but average speed is total distance divided by time, which is strictly greater than the magnitude of average velocity whenever the trajectory bends or reverses.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma Vol 1, Chapter 3: 'Average speed is greater than or equal to the magnitude of average velocity.'

**Diagnostic Symptom**: Student computes average speed by calculating (x_f - x_i)/Delta t and taking the absolute value.


---

### Verified JEE Practice Problem: `kinematics-question-7b4e1d65`

**Type**: `NUMERICAL`  
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> A car, starting from rest, accelerates at the rate $f$ through a distance $S$, then continues at constant speed for time $t$ and then decelerates at the rate $\frac{f}{2}$ to come to rest. If the total distance traversed is $15S$, then $S = \frac{ft^2}{x}$. Find the value of $x$.

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **72**  
**Independent Verification Record**: `kinematics-question-7b4e1d65`

</details>


---

## 2D Orthogonal Motion, Ballistic Trajectories, Tower Projection, and Inclined Plane Projection

> **Pedagogical Goal**: Apply the principle of independent orthogonal motions to complex 2D ballistic trajectories, generalizing from flat ground to inclined constraints.


---

### Concept: Two-Dimensional Projectile Motion and Independence of Orthogonal Motions

**Definition**: A projectile is an object launched into a vertical plane subjected solely to uniform downward gravitational acceleration $\vec{g} = -g\hat{j}$. Choosing Cartesian axes where $x$ is horizontal and $y$ is vertical upward, the equations of motion decouple completely: $a_x = 0$ and $a_y = -g$. For launch speed $u$ at elevation angle $\theta$ above the horizontal, initial components are $u_x = u\cos\theta$ and $u_y = u\sin\theta$.

**Physical Significance**: Imagine rolling a marble across a level table while simultaneously dropping another marble from the same table edge. Both strike the floor at the exact same instant! The horizontal motion has zero influence on the vertical downward fall. This independence allows us to treat a flying baseball as two completely separate problems: coasting forward at constant speed, and rising and falling in free fall.

**Assumptions & Scope of Validity**:
- Flat Earth approximation with constant gravitational acceleration $\vec{g}$.
- Negligible aerodynamic drag, lift (Magnus effect), and wind.
- Launch and impact occur on the same horizontal plane for standard range and flight time formulas.


---

### Concept: Projectile Motion on an Inclined Plane

**Definition**: Let a plane be inclined at angle $\alpha$ to the horizontal. A particle is projected from the base of the plane with speed $u$ at angle $\theta$ with the horizontal (so the launch angle relative to the incline is $\beta = \theta - \alpha$). Choosing the $x'$-axis along the incline upward and $y'$-axis perpendicular upward, the acceleration components are $a_{x'} = -g\sin\alpha$ and $a_{y'} = -g\cos\alpha$. Flight time is determined by $y'(T) = 0 \implies T = \frac{2 u\sin(\theta - \alpha)}{g\cos\alpha}$.

**Physical Significance**: When firing a projectile up a hill of slope angle $\alpha$, gravity no longer pulls straight down relative to the ground you are walking on. By tilting our heads and aligning our coordinate axes so that the $x'$-axis lies along the surface of the hill and the $y'$-axis is perpendicular to it, the problem looks just like a normal projectile problem, except that gravity now has components in both the $x'$ and $y'$ directions.

**Assumptions & Scope of Validity**:
- Incline is planar with constant inclination angle $\alpha$.
- Uniform downward gravity $\vec{g}$.
- No bounce or impact dynamics modeled (terminates on contact).


---

### Formula: Time of Flight for Ground-to-Ground Projectile

**Governing Equation**:
$$ T = \frac{2 u \sin\theta}{g} $$

**Variable Inventory & SI Units**:
- $T$: Total flight time duration until landing (Unit: `s` | Dim: `[T]`)
- $u$: Launch speed (Unit: `m/s` | Dim: `[L][T]^-1`)
- $\theta$: Launch elevation angle with horizontal (Unit: `rad or deg` | Dim: `[1]`)
- $g$: Gravitational acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Launch and landing points at same elevation (y = 0)
- Uniform downward gravity g

**Domain of Validity**:
- Fails if projectile lands on elevated ground or cliff


---

### Formula: Maximum Height of Projectile

**Governing Equation**:
$$ H = \frac{u^2 \sin^2\theta}{2 g} $$

**Variable Inventory & SI Units**:
- $H$: Maximum vertical apex height above launch plane (Unit: `m` | Dim: `[L]`)
- $u$: Launch speed (Unit: `m/s` | Dim: `[L][T]^-1`)
- $\theta$: Launch angle (Unit: `rad or deg` | Dim: `[1]`)
- $g$: Gravitational acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Uniform gravity g
- Apex defined by v_y = 0

**Domain of Validity**:
- Measured relative to launch elevation level


---

### Formula: Horizontal Range of Projectile

**Governing Equation**:
$$ R = \frac{u^2 \sin 2\theta}{g} = \frac{2 u_x u_y}{g} $$

**Variable Inventory & SI Units**:
- $R$: Horizontal distance traveled during flight time (Unit: `m` | Dim: `[L]`)
- $u$: Launch speed (Unit: `m/s` | Dim: `[L][T]^-1`)
- $\theta$: Launch angle with horizontal (Unit: `rad or deg` | Dim: `[1]`)
- $u_x$: Horizontal velocity component u cos(theta)
- $u_y$: Vertical velocity component u sin(theta)
- $g$: Gravitational acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Symmetric ground-to-ground landing
- Uniform downward gravity g

**Domain of Validity**:
- Complementary launch angles theta and (90 deg - theta) yield identical range R


---

### Formula: Trajectory Equation of Projectile Motion

**Governing Equation**:
$$ y = x \tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta} = x \tan\theta \left(1 - \frac{x}{R}\right) $$

**Variable Inventory & SI Units**:
- $y$: Vertical displacement coordinate (Unit: `m` | Dim: `[L]`)
- $x$: Horizontal displacement coordinate (Unit: `m` | Dim: `[L]`)
- $\theta$: Initial launch angle with horizontal (Unit: `rad or deg` | Dim: `[1]`)
- $u$: Initial launch speed (Unit: `m/s` | Dim: `[L][T]^-1`)
- $R$: Horizontal range (Unit: `m` | Dim: `[L]`)
- $g$: Gravitational acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Cartesian coordinates with origin at launch point
- Uniform downward gravity -g j

**Domain of Validity**:
- Universal relation describing spatial locus y(x) independent of time t


---

### Derivation: Formula `formula-kin-projectile-trajectory`

**Target Governing Relation**:
$$ y = x \tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta} = x \tan\theta \left(1 - \frac{x}{R}\right) $$

#### Step-by-Step Proof
**Step 1**: Express time t as a function of horizontal position x from uniform horizontal motion
$$ x = (u \cos\theta) t \implies t = \frac{x}{u \cos\theta} $$
*Physical Operation*: Constant horizontal velocity component u_x = u cos(theta).

**Step 2**: Substitute t into the vertical displacement equation
$$ y = (u \sin\theta) \left( \frac{x}{u \cos\theta} \right) - \frac{1}{2} g \left( \frac{x}{u \cos\theta} \right)^2 $$
*Physical Operation*: Elimination of parameter t to find spatial locus y(x).

**Step 3**: Simplify trigonometric terms using tan(theta) = sin(theta)/cos(theta)
$$ y = x \tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta} $$
*Physical Operation*: Standard form of projectile trajectory parabola.

**Step 4**: Factor out x tan(theta) to express in terms of horizontal range R = u^2 sin(2 theta)/g
$$ y = x \tan\theta \left( 1 - \frac{g x}{2 u^2 \cos^2\theta \tan\theta} \right) = x \tan\theta \left( 1 - \frac{g x}{2 u^2 \sin\theta \cos\theta} \right) = x \tan\theta \left( 1 - \frac{x}{R} \right) $$
*Physical Operation*: Using double-angle identity sin(2 theta) = 2 sin(theta) cos(theta).

**Applicability & Limiting Conditions**:
- Valid for projectile launched from origin (0, 0)


---

### Formula: Range Up an Inclined Plane

**Governing Equation**:
$$ R_{\text{up}} = \frac{2 u^2 \sin(\theta - \alpha) \cos\theta}{g \cos^2\alpha} $$

**Variable Inventory & SI Units**:
- $R_{\text{up}}$: Range measured along the incline plane surface (Unit: `m` | Dim: `[L]`)
- $u$: Launch speed (Unit: `m/s` | Dim: `[L][T]^-1`)
- $\theta$: Launch angle relative to horizontal (Unit: `rad or deg`)
- $\alpha$: Inclination angle of plane with horizontal (Unit: `rad or deg`)
- $g$: Gravitational acceleration (Unit: `m/s^2` | Dim: `[L][T]^-2`)

**Physical Assumptions**:
- Planar incline
- Launch angle theta > alpha
- Uniform gravity g

**Domain of Validity**:
- Maximum range up incline occurs at launch angle theta = pi/4 + alpha/2


---

### Derivation: Formula `formula-kin-incline-range`

**Target Governing Relation**:
$$ R_{\text{up}} = \frac{2 u^2 \sin(\theta - \alpha) \cos\theta}{g \cos^2\alpha} $$

#### Step-by-Step Proof
**Step 1**: Align x'-axis along incline and y'-axis normal to incline; resolve initial velocity and gravity
$$ u_{x'} = u \cos(\theta - \alpha), \quad u_{y'} = u \sin(\theta - \alpha); \quad a_{x'} = -g\sin\alpha, \quad a_{y'} = -g\cos\alpha $$
*Physical Operation*: Coordinate rotation by angle alpha.

**Step 2**: Determine time of flight T by setting perpendicular displacement to zero y'(T) = 0
$$ y'(T) = u_{y'} T - \frac{1}{2} g\cos\alpha T^2 = 0 \implies T = \frac{2 u \sin(\theta - \alpha)}{g\cos\alpha} $$
*Physical Operation*: Projectile lands on incline when perpendicular coordinate returns to zero.

**Step 3**: Compute range R_up by evaluating x'(T)
$$ R_{\text{up}} = u_{x'} T - \frac{1}{2} g\sin\alpha T^2 = T \left( u\cos(\theta - \alpha) - \frac{1}{2} g\sin\alpha \frac{2 u\sin(\theta - \alpha)}{g\cos\alpha} \right) $$
*Physical Operation*: Kinematic position along x' under constant acceleration a_x' = -g sin(alpha).

**Step 4**: Combine over common denominator cos(alpha) and apply angle addition identity
$$ R_{\text{up}} = T \frac{u}{\cos\alpha} \left( \cos(\theta - \alpha)\cos\alpha - \sin(\theta - \alpha)\sin\alpha \right) = T \frac{u}{\cos\alpha} \cos((\theta - \alpha) + \alpha) = T \frac{u \cos\theta}{\cos\alpha} $$
*Physical Operation*: Trigonometric identity cos(A + B) = cos A cos B - sin A sin B.

**Step 5**: Substitute flight time T into the simplified range expression
$$ R_{\text{up}} = \left( \frac{2 u \sin(\theta - \alpha)}{g\cos\alpha} \right) \frac{u \cos\theta}{\cos\alpha} = \frac{2 u^2 \sin(\theta - \alpha) \cos\theta}{g \cos^2\alpha} $$
*Physical Operation*: Direct substitution of T.

**Applicability & Limiting Conditions**:
- Valid for projectile launch up an incline of slope angle alpha with theta > alpha


---

### Worked Pedagogical Example: `ex-kin-projectile-max-height`

**Problem Statement**:
> A projectile is launched from ground level with speed u = 40.0 m/s at an angle theta = 30.0 degrees above the horizontal. Taking downward gravity g = 10.0 m/s^2, calculate: (a) the time of flight T, (b) the maximum height H, (c) the horizontal range R, and (d) the velocity of the projectile at the apex.

**Target Quantity**: `Time of flight T, maximum height H, horizontal range R, apex velocity vector v_apex`

#### Systematic Solution
**Step 1 ()**:
$$ u_x = u\cos\theta = 40.0 \cos 30^\circ = 40.0 \left(\frac{\sqrt{3}}{2}\right) = 20\sqrt{3} \approx 34.64\text{ m/s}, \quad u_y = u\sin\theta = 40.0 \sin 30^\circ = 20.0\text{ m/s} $$
u_x = 20 sqrt(3) m/s, u_y = 20.0 m/s.
Result: `u_x = 34.64 m/s, u_y = 20.0 m/s`

**Step 2 ()**:
$$ T = \frac{2 u_y}{g} = \frac{2 (20.0)}{10.0} = 4.0\text{ s} $$
T = 40.0 / 10.0 = 4.0 s.
Result: `T = 4.0 s`

**Step 3 ()**:
$$ H = \frac{u_y^2}{2 g} = \frac{(20.0)^2}{2 (10.0)} = \frac{400}{20} = 20.0\text{ m} $$
H = 400 / 20 = 20.0 m.
Result: `H = 20.0 m`

**Step 4 ()**:
$$ R = u_x T = (20\sqrt{3}) (4.0) = 80\sqrt{3} \approx 138.56\text{ m} $$
R = 80 * 1.73205 = 138.56 m.
Result: `R = 80 sqrt(3) m approx 138.56 m`

**Step 5 ()**:
$$ \vec{v}_{\text{apex}} = u_x \hat{i} + 0 \hat{j} = 20\sqrt{3}\hat{i}\text{ m/s} \approx 34.64\hat{i}\text{ m/s} $$
Speed at apex is 20 sqrt(3) m/s directed horizontally.
Result: `v_apex = 20 sqrt(3) i m/s`

**Final Answer**: (a) Time of flight T = 4.0 s; (b) Maximum height H = 20.0 m; (c) Horizontal range R = 80*sqrt(3) m (approx 138.56 m); (d) Velocity at apex = 20*sqrt(3) i m/s (approx 34.64 m/s horizontal).

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Do not assume velocity at apex is zero! Only the vertical component v_y is zero; horizontal speed u_x persists.

**Sanity & Consistency Checks**:
- Using range formula R = u^2 sin(2 theta)/g = (1600 * sin 60 deg)/10 = 160 * (sqrt(3)/2) = 80 sqrt(3) m, perfect agreement.
- Apex speed is non-zero (34.64 m/s) and strictly equal to horizontal component.


---

### Worked Pedagogical Example: `ex-kin-incline-proj-01`

**Problem Statement**:
> A projectile is launched from the base of an inclined plane having an angle of inclination alpha = 30.0 degrees with the horizontal. The launch speed is u = 20.0 m/s at an angle theta = 60.0 degrees with the horizontal (i.e. at 30.0 degrees above the incline). Taking downward gravity g = 10.0 m/s^2, find: (a) the time of flight T until impact on the incline, (b) the range R_up along the incline, and (c) the angle at which the projectile strikes the incline.

**Target Quantity**: `Time of flight T, range along incline R_up, impact angle with incline`

#### Systematic Solution
**Step 1 ()**:
$$ u_{x'} = u\cos(\theta - \alpha) = 20\cos 30^\circ = 10\sqrt{3}\text{ m/s}, \quad u_{y'} = u\sin(\theta - \alpha) = 20\sin 30^\circ = 10.0\text{ m/s}; \quad a_{x'} = -10\sin 30^\circ = -5.0\text{ m/s}^2, \quad a_{y'} = -10\cos 30^\circ = -5\sqrt{3}\text{ m/s}^2 $$
u_x' = 17.32 m/s, u_y' = 10.0 m/s, a_x' = -5.0 m/s^2, a_y' = -8.66 m/s^2.
Result: `Components established`

**Step 2 ()**:
$$ u_{y'} T - \frac{1}{2} g\cos\alpha T^2 = 0 \implies T = \frac{2 u_{y'}}{g\cos\alpha} = \frac{2 (10.0)}{5\sqrt{3}} = \frac{4}{\sqrt{3}} = \frac{4\sqrt{3}}{3} \approx 2.309\text{ s} $$
T = 4 / sqrt(3) s approx 2.309 s.
Result: `T = 4/sqrt(3) s`

**Step 3 ()**:
$$ R_{\text{up}} = u_{x'} T + \frac{1}{2} a_{x'} T^2 = (10\sqrt{3})\left(\frac{4}{\sqrt{3}}\right) + \frac{1}{2}(-5.0)\left(\frac{16}{3}\right) = 40.0 - \frac{40.0}{3} = \frac{80.0}{3} \approx 26.67\text{ m} $$
40 - 40/3 = 80/3 approx 26.67 m.
Result: `R_up = 80/3 m approx 26.67 m`

**Step 4 ()**:
$$ v_{x'}(T) = u_{x'} + a_{x'} T = 10\sqrt{3} + (-5.0)\left(\frac{4}{\sqrt{3}}\right) = 10\sqrt{3} - \frac{20}{\sqrt{3}} = \frac{30 - 20}{\sqrt{3}} = \frac{10}{\sqrt{3}}\text{ m/s} $$
v_x'(T) = 10/sqrt(3) m/s > 0 (still traveling up incline).
Result: `v_x' = 10/sqrt(3) m/s`

**Step 5 ()**:
$$ v_{y'}(T) = u_{y'} + a_{y'} T = 10.0 + (-5\sqrt{3})\left(\frac{4}{\sqrt{3}}\right) = 10.0 - 20.0 = -10.0\text{ m/s} $$
v_y'(T) = -10 m/s downward onto incline.
Result: `v_y' = -10 m/s`

**Step 6 ()**:
$$ \tan\phi = \left| \frac{v_{y'}}{v_{x'}} \right| = \frac{10.0}{10/\sqrt{3}} = \sqrt{3} \implies \phi = 60.0^\circ $$
phi = arctan(sqrt(3)) = 60.0 deg.
Result: `phi = 60.0 deg`

**Final Answer**: (a) Time of flight T = 4/sqrt(3) s (approx 2.31 s); (b) Range up incline R_up = 80/3 m (approx 26.67 m); (c) The projectile strikes the incline at an angle of 60.0 degrees to the inclined surface.

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Do not forget that gravity has an acceleration component along the incline (a_x' = -g sin alpha)!

**Sanity & Consistency Checks**:
- Check range formula: R_up = [2 u^2 sin(theta - alpha) cos(theta)] / [g cos^2(alpha)] = [2(400) sin(30) cos(60)] / [10 (3/4)] = [800 * (1/2) * (1/2)] / [7.5] = 200 / 7.5 = 80/3 m, exact match!
- Perpendicular landing check: v_x' > 0 means the projectile does not land perpendicularly; it strikes at 60 deg.


---

### Inoculation Against Misconception: `misc-kin-04`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"To maximize projectile distance, always launch at theta = 45 deg."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> The 45-degree rule applies ONLY to flat, level ground where launch elevation equals landing elevation. When launching from a cliff or onto an incline, the optimal angle shifts significantly.

**Physical Truth & Resolution**:
The 45-degree angle maximizes range strictly on horizontal terrain. When shooting from a cliff, launch at an angle shallower than 45 deg; when shooting uphill, launch steeper than 45 deg.

**Refutation Counterexample & Supporting Evidence**:
University Physics, Chapter 3: 'Optimal launch angle from a height above ground is always less than 45 degrees.'

**Diagnostic Symptom**: Student automatically substitutes theta = 45 deg into incline range or cliff range optimization problems.


---

### Verified JEE Practice Problem: `kinematics-question-b29767c8`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `src-jee-rank-booster-03-mock-256f42c6`  

> The position of a projectile launched from the origin at $t = 0$ is given by $\vec{r} = (40\hat{i} + 50\hat{j})\text{ m}$ at $t = 2\text{ s}$. If the projectile was launched at an angle $\theta$ from the horizontal, then $\theta$ is
(take $g = 10\text{ ms}^{-2}$)

**Options**:
- **(A)**: $\tan^{-1}\frac{2}{3}$
- **(B)**: $\tan^{-1}\frac{3}{2}$
- **(C)**: $\tan^{-1}\frac{7}{4}$
- **(D)**: $\tan^{-1}\frac{4}{5}$

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: **C**  
**Independent Verification Record**: `kinematics-question-b29767c8`

</details>


---

## 1D & 2D Relative Velocity, River-Swimmer, Rain-Umbrella, and Closest Approach

> **Pedagogical Goal**: Synthesize vector addition and subtraction principles within inertial reference frames to analyze multi-body interactions.


---

### Concept: Relative Velocity and Galilean Reference Frame Transformations

**Definition**: Let observers $A$ and $B$ track particle $P$. The position vector of $P$ relative to $A$ is related to its position relative to $B$ by $\vec{r}_{P/A} = \vec{r}_{P/B} + \vec{r}_{B/A}$. Differentiating with respect to time yields the vector relative velocity formula: $\vec{v}_{P/A} = \vec{v}_{P/B} + \vec{v}_{B/A}$. Consequently, the velocity of body $A$ as observed from body $B$ is defined as $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$.

**Physical Significance**: When sitting in a train traveling at 60 km/h, another train passing you on an adjacent track at 70 km/h in the same direction seems to crawl past at only 10 km/h. But if a train passes going the opposite way at 70 km/h, it rushes past your window in a blur at 130 km/h. Velocity is not an absolute label attached to an object—it depends fundamentally on who is watching.

**Assumptions & Scope of Validity**:
- Classical non-relativistic velocities ($v \ll c$, where $c$ is the speed of light).
- Universal absolute time shared across all reference frames ($t' = t$).


---

### Concept: River-Swimmer and Wind-Airplane Kinematics

**Definition**: Let a river flow with velocity $\vec{v}_R = v_R \hat{i}$ between parallel banks separated by width $d$. A boat/swimmer moves with speed $v_{B/R}$ relative to the water at angle $\theta$ to the bank normal (upstream). The ground velocity of the boat is $\vec{v}_B = \vec{v}_{B/R} + \vec{v}_R$. Time to cross is $t = \frac{d}{v_{B/R}\cos\theta}$. The horizontal drift downstream is $x = (v_R - v_{B/R}\sin\theta) t$.

**Physical Significance**: If you try to swim directly across a flowing river perpendicular to the bank, the current carries you downstream. To land directly opposite your starting point with zero drift, you must angle your strokes upstream to cancel the water current. But if your goal is purely to reach the other side in the fewest possible seconds, you should aim straight across, regardless of how far downstream the river carries you!

**Assumptions & Scope of Validity**:
- Uniform river flow velocity across the entire width $d$.
- Swimmer speed relative to water $v_{B/R}$ is constant.


---

### Formula: Relative Velocity Vector Formula

**Governing Equation**:
$$ \vec{v}_{A/B} = \vec{v}_A - \vec{v}_B $$

**Variable Inventory & SI Units**:
- $\vec{v}_{A/B}$: Velocity of body A as observed from body B
- $\vec{v}_A$: Velocity of body A with respect to ground frame
- $\vec{v}_B$: Velocity of body B with respect to ground frame

**Physical Assumptions**:
- Classical Galilean non-relativistic kinematics
- Translating reference frames

**Domain of Validity**:
- Universal relation connecting velocities in different translating reference frames


---

### Formula: River Crossing Time and Drift Formula

**Governing Equation**:
$$ t = \frac{d}{v_{B/R} \cos\theta}, \quad x = (v_R - v_{B/R}\sin\theta) t $$

**Variable Inventory & SI Units**:
- $t$: Time duration to cross river (Unit: `s` | Dim: `[T]`)
- $d$: Width of the river between parallel banks (Unit: `m` | Dim: `[L]`)
- $v_{B/R}$: Speed of boat/swimmer relative to water
- $\theta$: Steering angle measured upstream from the bank normal (Unit: `rad or deg` | Dim: `[1]`)
- $v_R$: River flow speed
- $x$: Net horizontal drift downstream along the opposite bank (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Uniform river current velocity across width d
- Constant speed relative to water v_{B/R}

**Domain of Validity**:
- Shortest crossing time occurs at theta = 0; zero drift requires v_{B/R} >= v_R and sin(theta) = v_R / v_{B/R}


---

### Worked Pedagogical Example: `ex-kin-river-swimmer-01`

**Problem Statement**:
> A river of width d = 400 m flows with a uniform current velocity v_R = 3.0 m/s. A swimmer can swim at a constant speed of v_{S/R} = 5.0 m/s in still water. (a) If the swimmer wishes to cross the river in the shortest possible time, in what direction should they steer, what is the crossing time, and how far downstream do they drift? (b) In what direction should they steer to reach the point directly opposite the starting point (zero drift), and what is the crossing time?

**Target Quantity**: `Steering angles, crossing times, and downstream drifts for (a) shortest time and (b) zero drift`

#### Systematic Solution
**Step 1 ()**:
$$ v_y = v_{S/R} \cos\theta \implies t = \frac{d}{v_{S/R} \cos\theta} $$
Time is minimized when cos(theta) = 1 => theta = 0 (steer perpendicular to bank).
Result: `theta = 0`

**Step 2 ()**:
$$ t_{\text{min}} = \frac{400\text{ m}}{5.0\text{ m/s}} = 80.0\text{ s}, \quad x_{\text{drift}} = v_R t_{\text{min}} = (3.0\text{ m/s})(80.0\text{ s}) = 240.0\text{ m} $$
t_min = 80 s, drift = 240 m downstream.
Result: `t_min = 80 s, drift = 240 m`

**Step 3 ()**:
$$ v_{x,\text{net}} = v_R - v_{S/R}\sin\theta = 0 \implies \sin\theta = \frac{v_R}{v_{S/R}} = \frac{3.0}{5.0} = 0.60 \implies \theta = \arcsin(0.60) \approx 36.87^\circ $$
Swimmer must steer 36.9 deg upstream from the normal (or 126.9 deg from downstream bank).
Result: `theta = 36.87 deg upstream`

**Step 4 ()**:
$$ v_{y,\text{net}} = \sqrt{v_{S/R}^2 - v_R^2} = \sqrt{5.0^2 - 3.0^2} = \sqrt{25 - 9} = 4.0\text{ m/s}, \quad t = \frac{d}{v_{y,\text{net}}} = \frac{400\text{ m}}{4.0\text{ m/s}} = 100.0\text{ s} $$
Crossing speed is 4.0 m/s; time is 400/4 = 100 s.
Result: `t = 100 s`

**Final Answer**: (a) Shortest time: Steer directly perpendicular to bank (0 deg); crossing time is 80.0 s; downstream drift is 240.0 m. (b) Zero drift: Steer 36.9 degrees upstream from the normal; crossing time is 100.0 s; drift is 0.0 m.

> [!WARNING] **Common Cognitive Traps & Pitfalls**:
> - Do not confuse the shortest time path with the shortest distance path! The shortest distance path takes 100 s, whereas the shortest time path takes 80 s.

**Sanity & Consistency Checks**:
- Crossing time for zero drift (100 s) is strictly longer than minimum crossing time (80 s), which is physically required.
- Since v_{S/R} = 5.0 > v_R = 3.0, zero drift is mathematically and physically possible.


---

### Inoculation Against Misconception: `misc-kin-05`

**Misconception Category**: `FRAME_CONFUSION`  
**Erroneous Intuition**: *"An apple dropped inside an accelerating train continues to accelerate forward horizontally because the train was accelerating."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> By Newton's first and second laws, acceleration is caused by net physical forces acting on the body at that instant. Once contact with the vehicle is broken, the vehicle can exert no force on the object.

**Physical Truth & Resolution**:
A released body inherits velocity, not acceleration. Once released, forces from the vehicle cease immediately, and only gravity acts on the free body.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma Vol 1, Chapter 3: 'At the time of release, the packet has the velocity of the balloon, but its acceleration is simply g downward.'

**Diagnostic Symptom**: Student writes a_x = a_train for a bomb dropped from an accelerating airplane.


---

## Chapter Summary & Formula Recap: Kinematics: Rest, Motion, and Trajectories

### Core Equations & Domains of Validity
- **Velocity-Time Relation**: $$v = u + at$$
  *Validity*: Rectilinear or projectile motion components with constant a
- **Position-Time Relation**: $$s = ut + \frac{1}{2}at^2$$
  *Validity*: Constant a
- **Velocity-Position Relation**: $$v^2 = u^2 + 2as$$
  *Validity*: Constant a
- **Displacement in nth Second**: $$s_n = u + \frac{a}{2}(2n - 1)$$
  *Validity*: Constant a
- **Acceleration as derivative of velocity w.r.t position**: $$a = v \frac{dv}{dx}$$
  *Validity*: Velocity is a function of position
- **Time of Flight (Ground to Ground)**: $$T = \frac{2u \sin\theta}{g}$$
  *Validity*: Ground-to-ground projectile
- **Maximum Height**: $$H = \frac{u^2 \sin^2\theta}{2g}$$
  *Validity*: Ground-to-ground projectile
- **Horizontal Range**: $$R = \frac{u^2 \sin 2\theta}{g}$$
  *Validity*: Ground-to-ground projectile
- **Equation of Trajectory**: $$y = x \tan\theta - \frac{gx^2}{2u^2 \cos^2\theta}$$
  *Validity*: Standard 2D plane launch
- **Range on Inclined Plane**: $$R = \frac{2u^2 \sin\alpha \cos(\alpha+\beta)}{g \cos^2\beta}$$
  *Validity*: Incline plane projection
- **Relative Velocity**: $$\vec{v}_{AB} = \vec{v}_A - \vec{v}_B$$
  *Validity*: Galilean relativity applies
- **River Crossing Time**: $$t = \frac{d}{v_{sr} \cos\theta}$$
  *Validity*: 2D relative motion
