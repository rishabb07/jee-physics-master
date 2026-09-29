# Chapter: Current Electricity

**Template**: `ELECTRODYNAMICS`  
**Prerequisites**: curr-es-01, curr-wep-01  

## Learning Objectives
- Understand electric current as charge flux, define current density J = n q v_d, and derive microscopic Ohm's law J = sigma E.
- Relate macroscopic resistance R = rho L / A to conductor geometry and determine resistance changes under recasting and stretching with volume conservation.
- Analyze linear and non-linear resistor combinations in series and parallel networks.
- Apply Kirchhoff's Current Law (Junction Law) and Kirchhoff's Voltage Law (Loop Law) to multi-loop DC circuits.
- Model ideal and real measuring instruments (ammeter with zero internal resistance, voltmeter with infinite internal resistance) and evaluate branch currents and voltages.

---

## Microscopic Electric Current, Drift Velocity, and Ohm's Law

> **Pedagogical Goal**: Establish the microscopic mechanism of conduction electrons, derive I = n e A v_d, formulate current density J = sigma E, and distinguish thermal electronic motion from collective drift velocity.


---

### Concept: Microscopic Electric Conduction, Drift Velocity, and Carrier Mobility

**Definition**: Drift velocity $\vec{v}_d$ is the ensemble-averaged vector velocity acquired by free charge carriers in a conductive medium under the influence of an applied macroscopic electric field $\vec{E}$, governed by $\vec{v}_d = -\mu \vec{E} = -\frac{e\tau}{m}\vec{E}$, where $\mu$ is carrier mobility, $e$ is elementary charge, $m$ is effective carrier mass, and $\tau$ is momentum relaxation time.

**Physical Significance**: Imagine a dense crowd of thousands of people packed tightly into a long corridor, all sprinting chaotically in random directions at meters per second, constantly bumping into one another so that the crowd as a whole remains stationary. If someone gently tilts the entire corridor downhill, every person still bounces frantically back and forth at high speed, but the whole crowd collectively crawls downhill at a few millimeters per minute. The frantic bouncing is the electron thermal motion ($10^5\,\text{m/s}$), the downhill slope is the applied electric field $\vec{E}$, and the slow collective crawl is the drift velocity ($10^{-4}\,\text{m/s}$).

**Assumptions & Scope of Validity**:
- Classical Drude model of non-interacting free electron gas in an isotropic ionic lattice
- Independent electron collisions that completely randomize velocity with mean relaxation time $\tau$
- Uniform electric field $\vec{E}$ throughout the cross-section of the conductor
- Steady-state DC current with negligible inductive or capacitive transient effects


---

### Formula: Drift Velocity and Current Density

**Governing Equation**:
$$ I = n e A v_d,\quad \vec{J} = n e \vec{v}_d = \sigma \vec{E} $$

**Variable Inventory & SI Units**:
- $I$: Electric current (Unit: `A` | Dim: `[I]`)
- $n$: Free carrier number density (Unit: `m^-3` | Dim: `[L]^-3`)
- $e$: Elementary charge magnitude (Unit: `C` | Dim: `[I][T]`)
- $A$: Conductor cross-sectional area (Unit: `m^2` | Dim: `[L]^2`)
- $v_d$: Mean drift velocity (Unit: `m/s` | Dim: `[L][T]^-1`)
- $J$: Current density (Unit: `A/m^2` | Dim: `[I][L]^-2`)
- $\sigma$: Electrical conductivity (Unit: `S/m` | Dim: `[M]^-1[L]^-3[T]^3[I]^2`)
- $E$: Electric field strength (Unit: `V/m` | Dim: `[M][L][T]^-3[I]^-1`)

**Physical Assumptions**:
- Drude classical conduction model
- Homogeneous isotropic metallic conductor
- Steady-state electric field

**Domain of Validity**:
- Valid in ohmic regime where drift velocity is small compared to random Fermi/thermal velocity


---

### Derivation: Formula `formula-curr-drift-micro`

**Target Governing Relation**:
$$ $I = n e A v_d,\quad \vec{J} = \sigma \vec{E}$ $$

#### Step-by-Step Proof
**Step 1**: Determine the acceleration of a conduction electron of mass $m$ and charge $-e$ in an applied electric field $\vec{E}$.
$$ $\vec{a} = -\frac{e\vec{E}}{m}$ $$
*Physical Operation*: Apply Newton's second law $\vec{F} = m\vec{a}$ and isolate $\vec{a}$

**Step 2**: Calculate the ensemble-averaged drift velocity $\vec{v}_d$ accumulated over mean relaxation time $\tau$.
$$ $\vec{v}_d = \langle \vec{v}(t) \rangle = \vec{a}\tau = -\frac{e\tau}{m}\vec{E}$ $$
*Physical Operation*: Take the statistical ensemble average with $\langle \vec{v}_{\text{thermal}} \rangle = \vec{0}$ and average collision interval $\langle t \rangle = \tau$

**Step 3**: Relate drift speed magnitude $v_d$ to electric field magnitude $E$ using electron mobility $\mu$.
$$ $v_d = \mu E,\quad \text{where } \mu = \frac{e\tau}{m}$ $$
*Physical Operation*: Define electron mobility $\mu = \frac{e\tau}{m}$ as drift speed per unit field

**Step 4**: Calculate the total mobile charge $\Delta q$ crossing a transverse cross-sectional area $A$ in time $\Delta t$.
$$ $\Delta q = n e A v_d \Delta t$ $$
*Physical Operation*: Substitute cylinder volume $\Delta V_{\text{cyl}} = A \Delta x = A (v_d \Delta t)$ swept by drifting carriers

**Step 5**: Formulate macroscopic electric current $I$ as the time rate of charge transport.
$$ $I = n e A v_d$ $$
*Physical Operation*: Substitute $\Delta q = n e A v_d \Delta t$ and take the derivative

**Step 6**: Express current density vector $\vec{J}$ and derive microscopic Ohm's law.
$$ $\vec{J} = \left(\frac{n e^2\tau}{m}\right)\vec{E} = \sigma \vec{E}$ $$
*Physical Operation*: Substitute $\vec{v}_d = -\frac{e\tau}{m}\vec{E}$ and define conductivity $\sigma = \frac{n e^2\tau}{m}$

**Applicability & Limiting Conditions**:
- Valid for ohmic metallic conductors in the regime $v_d \ll v_{\text{thermal}}$
- Constant temperature maintaining invariant electron relaxation time $\tau$
- Uniform carrier concentration and cross-sectional area


---

## Macroscopic Resistance, Material Resistivity, and Wire Recasting

> **Pedagogical Goal**: Relate resistance to conductor geometry R = rho l / A and analyze resistance scaling under volume conservation during wire stretching and recasting, explicitly disproving 1/r^2 area-only scaling.


---

### Concept: Volume Conservation and Geometric Scaling Under Wire Recasting and Stretching

**Definition**: Wire recasting and drawing are volume-conserving geometric transformations of an incompressible conductor ($V = A l = \text{constant}$), under which electrical resistance scales quadratically with length ($R \propto l^2$) and inversely with the fourth power of radius ($R \propto r^{-4}$) or diameter ($R \propto d^{-4}$).

**Physical Significance**: Imagine rolling a lump of playdough into a cylinder. If you roll and stretch it until its diameter is cut in half, the playdough must go somewhere—it elongates to exactly 4 times its starting length. For electric current, the charges now face a double penalty: they must squeeze through a pipe that is 4 times narrower (contributing a factor of 4 to resistance) and travel through a corridor that is 4 times longer (contributing another factor of 4). Combining both effects multiplies the resistance by $4 \times 4 = 16$.

**Assumptions & Scope of Validity**:
- Strict conservation of mass and volume ($V_1 = V_2$ with zero material loss)
- Incompressible solid material with constant mass density $\rho_m$
- Uniform cylindrical geometry maintained throughout the length after deformation
- Constant material resistivity $\rho$ (isothermal conditions, identical crystalline state)


---

### Formula: Resistance Under Volume Conservation

**Governing Equation**:
$$ R = \rho \frac{l^2}{V} = \frac{\rho V}{\pi^2 r^4} \propto \frac{1}{r^4} $$

**Variable Inventory & SI Units**:
- $R$: Conductor resistance (Unit: `\Omega` | Dim: `[M][L]^2[T]^-3[I]^-2`)
- $\rho$: Material electrical resistivity (Unit: `\Omega m` | Dim: `[M][L]^3[T]^-3[I]^-2`)
- $l$: Conductor length (Unit: `m` | Dim: `[L]`)
- $V$: Conductor volume (Unit: `m^3` | Dim: `[L]^3`)
- $r$: Wire circular radius (Unit: `m` | Dim: `[L]`)

**Physical Assumptions**:
- Incompressible conductor material with volume conservation V = A l = \text{const}
- Uniform deformation along length
- Constant resistivity \rho

**Domain of Validity**:
- Wire drawn through dies, stretched, or recast without mass loss at constant temperature


---

### Derivation: Formula `formula-curr-recasting-volume`

**Target Governing Relation**:
$$ $R = \rho \frac{l^2}{V} = \rho \frac{V}{\pi^2 r^4} \propto \frac{1}{r^4}$ $$

#### Step-by-Step Proof
**Step 1**: State the macroscopic resistance formula for a uniform cylindrical conductor.
$$ $R = \rho \frac{l}{A}$ $$
*Physical Operation*: Express electrical resistance in terms of intrinsic resistivity $\rho$, conductor length $l$, and cross-sectional area $A$

**Step 2**: Formulate the volumetric conservation constraint during recasting or stretching.
$$ $A_1 l_1 = A_2 l_2 = V$ $$
*Physical Operation*: Enforce $V_1 = V_2 = V = \text{constant}$ under mass and density conservation

**Step 3**: Express electrical resistance as an explicit function of length $l$ under volume conservation.
$$ $R = \rho \frac{l}{\frac{V}{l}} = \rho \frac{l^2}{V} \implies R \propto l^2$ $$
*Physical Operation*: Substitute $A = \frac{V}{l}$ into the resistance equation

**Step 4**: Express electrical resistance as an explicit function of cross-sectional area $A$ under volume conservation.
$$ $R = \rho \frac{\frac{V}{A}}{A} = \rho \frac{V}{A^2} \implies R \propto \frac{1}{A^2}$ $$
*Physical Operation*: Substitute $l = \frac{V}{A}$ into the resistance equation

**Step 5**: Substitute circular cylindrical geometry in terms of radius $r$ and diameter $d$.
$$ $R = \frac{\rho V}{\pi^2 r^4} = \frac{16\rho V}{\pi^2 d^4} \implies R \propto \frac{1}{r^4} \propto \frac{1}{d^4}$ $$
*Physical Operation*: Substitute $A = \pi r^2$ and $A = \frac{\pi d^2}{4}$ into the volume-dependent resistance relation

**Step 6**: Formulate the scaling ratio connecting initial and final resistances upon wire deformation.
$$ $\frac{R_2}{R_1} = \left(\frac{r_1}{r_2}\right)^4 = \left(\frac{d_1}{d_2}\right)^4 = \left(\frac{l_2}{l_1}\right)^2$ $$
*Physical Operation*: Divide $R_2$ by $R_1$ to eliminate common physical constants $\rho$ and $V$

**Applicability & Limiting Conditions**:
- Volume conservation holds strictly ($V = A l = \text{constant}$)
- Resistivity $\rho$ is invariant during the geometric transformation
- Cross-sectional shape remains uniform along the length of the conductor


---

### Worked Pedagogical Example: `ex-curr-recast-wire-01`

**Problem Statement**:
> A uniform cylindrical copper wire has an initial resistance $R_1 = 10.0\,\Omega$, length $l_1$, and cross-sectional radius $r_1$. The wire is drawn through a drawing die (stretched/recast) so that its radius is reduced uniformly by a factor of 2, resulting in a final radius $r_2 = \frac{r_1}{2}$. Assuming that the density and material resistivity $\rho$ of copper remain strictly constant throughout the deformation process:
(a) Determine the new length $l_2$ of the wire in terms of $l_1$ under the constraint of volume conservation.
(b) Derive the general scaling law relating resistance $R$ to radius $r$ when the volume of the conductor is held constant.
(c) Calculate the exact numerical value of the new electrical resistance $R_2$ in ohms ($\Omega$).

**Target Quantity**: `l_2, R_2 / R_1, \text{ and } R_2`

#### Systematic Solution
**Step 1 (Resistance formula for a uniform cylindrical conductor)**:
$$ R_1 = \rho \frac{l_1}{A_1} = \rho \frac{l_1}{\pi r_1^2} = 10.0\,\Omega $$
R_1 = 10.0\,\Omega
Result: `Initial resistance R_1 = \rho l_1 / (\pi r_1^2) = 10.0 \Omega.`

**Step 2 (Volume conservation during drawing / stretching)**:
$$ V_1 = V_2 \implies A_1 l_1 = A_2 l_2 \implies \pi r_1^2 l_1 = \pi r_2^2 l_2 $$
r_2 = \frac{r_1}{2} \implies \frac{r_1}{r_2} = 2 \implies l_2 = l_1 (2)^2 = 4 l_1
Result: `Final length is four times the initial length: l_2 = 4 l_1.`

**Step 3 (Calculation of deformed cross-sectional area)**:
$$ A_2 = \pi r_2^2 = \pi \left(\frac{r_1}{2}\right)^2 = \frac{\pi r_1^2}{4} = \frac{A_1}{4} $$
r_2 = \frac{r_1}{2} \implies A_2 = \frac{A_1}{4}
Result: `Final cross-sectional area is one-fourth the initial area: A_2 = A_1 / 4.`

**Step 4 (Resistance scaling under volume conservation)**:
$$ R = \rho \frac{l}{A} = \rho \frac{l \cdot A}{A^2} = \frac{\rho V}{A^2} = \frac{\rho V}{\pi^2 r^4} \implies R \propto \frac{1}{r^4} $$
\frac{R_2}{R_1} = \left(\frac{r_1}{r_1 / 2}\right)^4 = 2^4 = 16
Result: `R_2 = 16 R_1 (resistance increases by a factor of 16).`

**Step 5 (Numerical computation of new resistance)**:
$$ R_2 = 16 R_1 = 16 \times 10.0\,\Omega = 160.0\,\Omega $$
R_1 = 10.0\,\Omega \implies R_2 = 16 \times 10.0 = 160\,\Omega
Result: `New resistance R_2 = 160 \Omega.`

**Final Answer**: l_2 = 4 l_1; \quad R_2 = 16 R_1 = 160\,\Omega

**Sanity & Consistency Checks**:
- Limiting check r_2 -> r_1: If no deformation occurs (r_2 = r_1), R_2 = (1)^4 R_1 = 10.0 \Omega.
- Physical direction: Making a conductor both 4 times longer and 4 times thinner must compound resistance, giving a much larger resistance (160 \Omega > 10 \Omega).
- Dimensional check: [R_2] = [\rho l / A] = (\Omega m) * m / m^2 = \Omega, verified.
- Mass invariance: Mass m = d * V = d * A_1 l_1 = d * (A_1/4) (4 l_1) = d * A_2 l_2, mass is strictly conserved.


---

### Inoculation Against Misconception: `misc-curr-01`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"When a wire of radius r is recast into a wire of radius r/2, its resistance doubles because resistance is inversely proportional to radius."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> Resistance depends on area A = \pi r^2, not radius r. Furthermore, under volume conservation V = A l = \text{constant}, halving the radius not only reduces area to A/4 but also stretches the wire to 4 times its length (l_new = 4 l_old). Compounding these two effects yields R \propto 1/r^4, producing a 16-fold increase, not a 2-fold increase.

**Physical Truth & Resolution**:
The resistance of a uniform conductor is defined macroscopically as $R = \rho \frac{l}{A} = \rho \frac{l}{\pi r^2}$. Even for a wire of fixed length, resistance is inversely proportional to the cross-sectional area ($R \propto 1/r^2$), so halving the radius would quadruple the resistance ($4\times$).
However, when a wire of initial length $l_1$ and radius $r_1$ is drawn through a die or recast into a thinner wire of radius $r_2 = r_1 / 2$, no material is added or removed. Assuming constant material density, the volume $V$ remains strictly conserved:
$$V = A_1 l_1 = A_2 l_2 \implies l_2 = l_1 \left(\frac{r_1}{r_2}\right)^2$$
When $r_2 = r_1 / 2$, the length quadruples: $l_2 = 4 l_1$. At the same time, the cross-sectional area is reduced to one-fourth: $A_2 = \pi (r_1/2)^2 = A_1 / 4$. Expressing resistance in terms of volume:
$$R = \rho \frac{l}{A} = \rho \frac{l \cdot A}{A^2} = \frac{\rho V}{A^2} = \frac{\rho V}{\pi^2 r^4} \implies R \propto \frac{1}{r^4}$$
Taking the ratio of the new resistance $R_2$ to the old resistance $R_1$:
$$\frac{R_2}{R_1} = \left(\frac{r_1}{r_2}\right)^4 = 2^4 = 16$$
Thus, recasting a wire to half its radius increases its electrical resistance by a factor of 16, which is eight times larger than the naive prediction of doubling.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 2, Chapter 32 (Electric Current in Conductors), Section 32.5: 'Resistance and Resistivity'; Question current-electricity-question-ce6aab7f.

**Diagnostic Symptom**: Student calculates the new resistance as 2 * R1 or 4 * R1 when a wire is stretched or drawn to a specified radius.


---

### Verified JEE Practice Problem: `current-electricity-question-ce6aab7f`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Resistor Networks, Symmetry Reductions, and Equivalent Resistance

> **Pedagogical Goal**: Master series and parallel reductions, delta-wye transformations, and nodal symmetry methods for complex resistor lattices.


---

## Kirchhoff's Laws and Multi-Loop DC Circuit Analysis

> **Pedagogical Goal**: Apply Kirchhoff's Current Law (conservation of charge) and Voltage Law (conservation of energy) systematically using branch-current and node-voltage methods.


---

## Electrical Measuring Instruments: Ideal and Real Ammeters and Voltmeters

> **Pedagogical Goal**: Model circuit instrumentation, establish the ideal ammeter (R_A -> 0) and ideal voltmeter (R_V -> infty) boundary conditions, and eliminate the misconception that branch ammeters read total battery current.


---

### Concept: Electrical Measuring Instruments: Ideal and Real Meters, Galvanometer Shunting, and Multipliers

**Definition**: An ammeter is a series-connected current-measuring instrument whose ideal operating limit is $R_A = 0$; a voltmeter is a parallel-connected voltage-measuring instrument whose ideal operating limit is $R_V = \infty$. Galvanometer range extension is governed by parallel shunting ($S = \frac{I_g G}{I - I_g}$) for currents and series multiplication ($R_s = \frac{V}{I_g} - G$) for voltages.

**Physical Significance**: Think of measuring fluid in an irrigation network. To measure the rate of water flow inside a canal (current), you insert a flow turbine inside the channel. If the turbine is heavy and obstructed, it chokes the water flow and gives a false reading; an ideal flow meter must spin with zero drag ($R_A = 0$). To measure the pressure difference between two pipes (voltage), you tap a pressure gauge between them. If the gauge leaks water, it changes the pipe pressures; an ideal pressure gauge must be completely sealed with zero leakage ($R_V = \infty$).

**Assumptions & Scope of Validity**:
- Galvanometer coil deflection is strictly linear with current (constant radial magnetic field and Hookean restoring spring)
- Purely resistive DC steady-state network with zero inductive reactance
- Zero lead resistance in external connecting wires


---

### Formula: Ideal Ammeter and Voltmeter Branch Equations

**Governing Equation**:
$$ S = \frac{I_g G}{I - I_g},\quad R_s = \frac{V}{I_g} - G $$

**Variable Inventory & SI Units**:
- $S$: Shunt resistance for ammeter (Unit: `\Omega` | Dim: `[M][L]^2[T]^-3[I]^-2`)
- $R_s$: Series multiplier resistance for voltmeter (Unit: `\Omega` | Dim: `[M][L]^2[T]^-3[I]^-2`)
- $G$: Galvanometer coil resistance (Unit: `\Omega` | Dim: `[M][L]^2[T]^-3[I]^-2`)
- $I_g$: Full-scale deflection current (Unit: `A` | Dim: `[I]`)
- $I$: Maximum current range (Unit: `A` | Dim: `[I]`)
- $V$: Maximum voltage range (Unit: `V` | Dim: `[M][L]^2[T]^-3[I]^-1`)

**Physical Assumptions**:
- Linear magnetic deflection torque proportional to current
- Temperature-independent resistance

**Domain of Validity**:
- Applies to moving coil galvanometer conversion to ammeters and voltmeters


---

### Derivation: Formula `formula-curr-measuring-meters`

**Target Governing Relation**:
$$ $S = \frac{I_g G}{I - I_g},\quad R_s = \frac{V}{I_g} - G,\quad R_A \to 0,\quad R_V \to \infty$ $$

#### Step-by-Step Proof
**Step 1**: Establish parallel circuit configuration and current division for ammeter conversion.
$$ $I_S S = I_g G \implies (I - I_g) S = I_g G$ $$
*Physical Operation*: Express shunt current as $I_S = I - I_g$ and equate potential drops across parallel branches: $V_S = V_G$

**Step 2**: Isolate the required shunt resistance $S$ to measure a maximum current $I$.
$$ $S = \frac{I_g G}{I - I_g} = \frac{G}{n_I - 1},\quad \text{where } n_I = \frac{I}{I_g}$ $$
*Physical Operation*: Divide by $(I - I_g)$ and define the current multiplication factor $n_I = \frac{I}{I_g}$

**Step 3**: Compute the equivalent resistance of the shunted galvanometer and deduce the ideal ammeter condition.
$$ $R_A = \frac{G S}{G + S} < S;\quad \lim_{S \to 0} R_A = 0 \implies V_A = I R_A = 0$ $$
*Physical Operation*: Solve for equivalent resistance $R_A = \frac{G S}{G + S}$ and take the limit as desired measurement capability $I \to \infty \implies S \to 0$

**Step 4**: Establish series circuit configuration and voltage division for voltmeter conversion.
$$ $V = I_g R_s + I_g G = I_g(R_s + G)$ $$
*Physical Operation*: Express potential drops using common series current $I_g$ at full-scale deflection

**Step 5**: Isolate the required series multiplier resistance $R_s$ to measure a maximum potential difference $V$.
$$ $R_s = \frac{V}{I_g} - G = G(n_V - 1),\quad \text{where } n_V = \frac{V}{I_g G}$ $$
*Physical Operation*: Divide by $I_g$, subtract $G$, and define the voltage multiplication factor $n_V = \frac{V}{I_g G}$

**Step 6**: Compute the total internal resistance of the converted voltmeter and deduce the ideal voltmeter condition.
$$ $R_V = R_s + G;\quad \lim_{R_s \to \infty} R_V = \infty \implies I_V = \lim_{R_V \to \infty} \frac{V}{R_V} = 0$ $$
*Physical Operation*: Take the limit as target full-scale voltage $V \to \infty \implies R_s \to \infty$

**Applicability & Limiting Conditions**:
- Valid for linear DC moving-coil galvanometers
- Purely resistive circuit operating conditions


---

### Inoculation Against Misconception: `misc-curr-02`

**Misconception Category**: `HIDDEN_CONSTRAINT_OMISSION`  
**Erroneous Intuition**: *"An ideal ammeter placed in any branch of a multi-branch parallel circuit measures the total current supplied by the battery because its internal resistance is zero."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> An ammeter measures only the flux of electric charge that physically passes through its own terminals: I_meter = I_branch. In a multi-loop circuit, Kirchhoff's Current Law enforces current division at each junction (\sum I_in = \sum I_out). Unless placed in the main trunk directly in series with the battery before any junction, an ammeter only records a branch fraction of the total battery current.

**Physical Truth & Resolution**:
An ideal ammeter is an instrument engineered to measure current without perturbing the circuit; it possesses zero internal resistance ($R_A = 0$) so that the potential difference across its terminals is zero ($V_A = I R_A = 0$). While this ensures that inserting the ammeter in series with a branch does not alter the equivalent resistance of that branch or the total circuit currents, the instrument remains localized to that specific branch. According to Kirchhoff's Current Law (conservation of charge), the total current $I_{\text{total}}$ delivered by the power source divides at any parallel junction according to the branch admittances:
$$I_{\text{total}} = \sum_{k=1}^N I_k$$
An ammeter placed in branch $j$ measures strictly the branch current $I_j = \frac{V_j}{R_j}$. It does NOT measure $I_{\text{total}}$, unless that branch happens to be the undivided main trunk connected directly in series with the source. Furthermore, placing an ideal ammeter in series with a branch resistor $R_j$ does not short out parallel branches, because the branch resistor $R_j$ still limits the branch current to $V / R_j$.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 2, Chapter 32 (Electric Current in Conductors), Section 32.11: 'Ammeter and Voltmeter'; Questions current-electricity-question-3a1b8c4d and current-electricity-question-d2492f7f.

**Diagnostic Symptom**: Student takes the reading of a branch ammeter as the total current in circuit problems, or fails to apply current divider rules when an ammeter is in the branch.


---

### Verified JEE Practice Problem: `current-electricity-question-3a1b8c4d`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

### Verified JEE Practice Problem: `current-electricity-question-d2492f7f`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Chapter Summary & Formula Recap: Current Electricity

### Core Equations & Domains of Validity
- **Drift Velocity and Current Density**: $$I = n e A v_d,\quad \vec{J} = n e \vec{v}_d = \sigma \vec{E}$$
  *Validity*: Valid under constant thermal conditions and classical Drude relaxation time approximation
- **Resistance Under Volume Conservation (Recasting / Stretching)**: $$R = \rho \frac{l}{A} = \rho \frac{l}{\pi r^2} = \rho \frac{V_{\text{vol}}}{\pi^2 r^4} \propto \frac{1}{r^4}$$
  *Validity*: Plastic deformation or melting/recasting with zero mass loss (V = A * l = constant)
- **Ideal Ammeter and Voltmeter Branch Equations**: $$R_A \to 0 \implies V_A = 0,\quad R_V \to \infty \implies I_V = 0$$
  *Validity*: Valid whenever measuring devices are specified as ideal
