# Chapter: Thermodynamics

**Template**: `THERMODYNAMICS`  
**Prerequisites**: curr-therm-01, curr-wep-01  

## Learning Objectives
- Understand thermodynamic state variables, equilibrium, and internal energy as an exact differential state function.
- Apply the First Law of Thermodynamics dQ = dU + dW using rigorous physics sign conventions.
- Analyze cyclic and non-cyclic gas processes (isobaric, isochoric, isothermal, adiabatic, polytropic) and calculate boundary work from PV integrals.
- Derive and apply reversible adiabatic scaling relations T V^(gamma-1) = const and P V^gamma = const for ideal gases and relativistic photon gases.
- Evaluate thermal efficiencies of heat engines, Carnot limits, and Second Law formulations.

---

## Thermodynamic State Variables, Internal Energy, and the First Law

> **Pedagogical Goal**: Define thermodynamic equilibrium, establish internal energy U as an exact state function, and formulate the First Law of Thermodynamics dQ = dU + dW using consistent physics sign conventions.


---

### Concept: The First Law of Thermodynamics: Internal Energy, Heat, and Work

**Definition**: The First Law of Thermodynamics states that energy cannot be created or destroyed, only transformed. For an infinitesimal quasi-static transition in a closed thermodynamic system: $dQ = dU + dW$, where $dQ$ is the inexact differential of heat added to the system, $dU$ is the exact differential of internal energy, and $dW = P dV$ is the inexact differential of work performed BY the system on its surroundings. In integrated form: $Q = \Delta U + W$. In SI units, all quantities have dimensions of energy $[M L^2 T^{-2}]$ and are measured in Joules ($\text{J}$).

**Physical Significance**: Think of a system's internal energy as the balance in a bank account. You can increase your balance by depositing money (adding heat $dQ$) or decrease it by spending money on bills (doing work on the surroundings $dW$). While deposits ($dQ$) and expenses ($dW$) describe transactions along a path, the net balance in the account ($U$) depends strictly on your current financial state. Regardless of whether money arrived via salary or interest, the balance changes by exactly $\Delta U = Q - W$.

**Assumptions & Scope of Validity**:
- The system is closed, with no mass transfer across system boundaries.
- Kinetic and potential energy of the macroscopic system as a whole remain constant (internal energy change only).
- Quasi-static thermodynamic states with well-defined pressure, volume, and temperature.


---

### Formula: First Law of Thermodynamics

**Governing Equation**:
$$ dQ = dU + dW = dU + P dV $$

**Variable Inventory & SI Units**:
- $Q$: Heat transferred to system (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $U$: Internal energy of system (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $W$: Work done by system (Unit: `J` | Dim: `[M][L]^2[T]^-2`)
- $P$: Pressure (Unit: `Pa` | Dim: `[M][L]^-1[T]^-2`)
- $V$: Volume (Unit: `m^3` | Dim: `[L]^3`)

**Physical Assumptions**:
- Closed stationary thermodynamic system
- Negligible bulk kinetic/potential energy changes

**Domain of Validity**:
- Quasi-static boundary work dW = P dV holds for reversible processes; universal energy conservation holds generally


---

### Derivation: Formula `formula-td-first-law`

**Target Governing Relation**:
$$ $$dQ = dU + dW$$ $$

#### Step-by-Step Proof
**Step 1**: Formulate the universal conservation of energy for the isolated composite system comprising the thermodynamic system and its surroundings.
$$ $$dE_{\text{system}} = -dE_{\text{surroundings}}$$ $$
*Physical Operation*: Express the conservation principle in differential form: $dE_{\text{system}} + dE_{\text{surroundings}} = 0$.

**Step 2**: Partition system energy into macroscopic mechanical energy and microscopic internal energy $U$.
$$ $$dE_{\text{system}} = dU$$ $$
*Physical Operation*: Set macroscopic mechanical energy variations to zero ($dK_{\text{macro}} = 0$, $d\Phi_{\text{macro}} = 0$) for a stationary system at rest in the laboratory frame: $dE_{\text{system}} = dU$.

**Step 3**: Classify boundary energy transfers into mechanical work $dW$ performed by the system and heat $dQ$ absorbed by the system.
$$ $$-dE_{\text{surroundings}} = dQ - dW$$ $$
*Physical Operation*: By definition of energy conservation at the boundary, energy gained by surroundings consists of mechanical work done on them ($+dW$) minus thermal energy transferred from them into the system ($-dQ$): $-dE_{\text{surroundings}} = dQ - dW$.

**Step 4**: Equate the internal energy change $dU$ to the net boundary energy transfer.
$$ $$dQ = dU + dW$$ $$
*Physical Operation*: Substitute $-dE_{\text{surroundings}} = dQ - dW$ into the energy balance: $dU = dQ - dW$.

**Step 5**: Express mechanical boundary work in terms of pressure and volume change for a quasi-static process.
$$ $$dW = P dV$$ $$
*Physical Operation*: For an outward displacement $dx$ of a piston of cross-sectional area $A$ against internal pressure $P$: $dW = (P A) dx = P (A dx) = P dV$.

**Step 6**: Combine expressions to write the differential First Law with state and path distinctions.
$$ $$dQ = dU + P dV$$ $$
*Physical Operation*: Substitute $dW = P dV$: $dQ = dU + P dV$. Note that $dU$ is an exact differential of state ($\oint dU = 0$), whereas $dQ$ and $dW$ are inexact path-dependent differentials.

**Applicability & Limiting Conditions**:
- Valid for all closed thermodynamic systems.
- Sign convention: $dQ > 0$ for heat absorbed by the system, $dW > 0$ for work performed by the system.
- Valid for reversible and irreversible processes (with $dW = P dV$ applying strictly in quasi-static conditions).


---

## Standard Gas Processes and Work on PV Diagrams

> **Pedagogical Goal**: Systematize isobaric, isochoric, and isothermal processes, calculating boundary work from integral P dV and analyzing closed indicator diagrams.


---

## Reversible Adiabatic Processes in Classical Ideal Gases

> **Pedagogical Goal**: Derive and apply reversible adiabatic scaling relations T V^(gamma-1) = const and P V^gamma = const, compute boundary work, and resolve sign misconceptions regarding internal energy variation.


---

### Concept: Adiabatic Processes and Polytropic Relations in Ideal Gases

**Definition**: An adiabatic process is a thermodynamic transition during which no heat enters or leaves the system across its boundaries ($dQ = 0$). For a reversible (quasi-static) adiabatic expansion or compression of an ideal gas with constant heat capacities, the process is governed by the relation $P V^\gamma = \text{constant}$, where $\gamma = C_p / C_v$ is the adiabatic index (heat capacity ratio). Equivalent forms are $T V^{\gamma - 1} = \text{constant}$ and $P^{1 - \gamma} T^\gamma = \text{constant}$.

**Physical Significance**: When you pump air into a bicycle tire with a hand pump, the base of the pump quickly becomes noticeably hot. This heating is not primarily due to friction, but due to rapid compression of the gas. The compression happens too quickly for heat to escape through the cylinder walls ($dQ \approx 0$). By the First Law, the mechanical work done pushing the piston compresses the gas and converts directly into internal thermal energy ($dU = -dW = +W_{\text{on}}$), forcing the gas temperature to rise.

**Assumptions & Scope of Validity**:
- The boundary is thermally insulating (adiabatic enclosure) or the process occurs fast enough that heat exchange is negligible.
- The working substance behaves as an ideal gas with constant specific heat capacities $C_p$ and $C_v$.
- The process is quasi-static and reversible (no dissipative shock waves or friction).


---

### Formula: Reversible Adiabatic Process for Ideal Gas

**Governing Equation**:
$$ T V^{\gamma - 1} = \text{constant},\quad P V^\gamma = \text{constant} $$

**Variable Inventory & SI Units**:
- $T$: Absolute temperature (Unit: `K` | Dim: `[\Theta]`)
- $V$: Gas volume (Unit: `m^3` | Dim: `[L]^3`)
- $P$: Gas pressure (Unit: `Pa` | Dim: `[M][L]^-1[T]^-2`)
- $\gamma$: Heat capacity ratio C_p/C_v (Unit: `dimensionless` | Dim: `[1]`)

**Physical Assumptions**:
- Ideal gas equation of state P V = n R T
- Reversible quasi-static process
- Zero heat exchange dQ = 0
- Constant heat capacity ratio \gamma

**Domain of Validity**:
- Applies only to reversible adiabatic processes; fails for irreversible processes like free expansion into vacuum


---

### Derivation: Formula `formula-td-adiabatic-ideal-gas`

**Target Governing Relation**:
$$ $$T V^{\gamma - 1} = \text{constant}$$ $$

#### Step-by-Step Proof
**Step 1**: Impose the adiabatic condition $dQ = 0$ in the First Law of Thermodynamics.
$$ $$dU = -P dV$$ $$
*Physical Operation*: Set $dQ = 0$: $0 = dU + P dV \implies dU = -P dV$.

**Step 2**: Substitute the internal energy differential for an ideal gas $dU = n C_v dT$.
$$ $$n C_v dT = -P dV$$ $$
*Physical Operation*: Replace $dU$ by $n C_v dT$: $n C_v dT = -P dV$.

**Step 3**: Eliminate pressure $P$ using the ideal gas equation of state $P = \frac{n R T}{V}$.
$$ $$n C_v dT = -\frac{n R T}{V} dV$$ $$
*Physical Operation*: Substitute $P = \frac{n R T}{V}$: $n C_v dT = -\left(\frac{n R T}{V}\right) dV$.

**Step 4**: Separate variables $T$ and $V$ by dividing both sides by $n T$.
$$ $$\frac{dT}{T} + \frac{R}{C_v} \frac{dV}{V} = 0$$ $$
*Physical Operation*: Divide by $n T$ (for $T > 0$): $C_v \frac{dT}{T} = -R \frac{dV}{V} \implies \frac{dT}{T} + \frac{R}{C_v} \frac{dV}{V} = 0$.

**Step 5**: Express the ratio $R / C_v$ in terms of the adiabatic index $\gamma$.
$$ $$\frac{dT}{T} + (\gamma - 1) \frac{dV}{V} = 0$$ $$
*Physical Operation*: Apply Mayer's relation $R = C_p - C_v$ and the definition $\gamma = C_p / C_v$: $\frac{R}{C_v} = \frac{C_p - C_v}{C_v} = \frac{C_p}{C_v} - 1 = \gamma - 1$. Substitute into the differential equation.

**Step 6**: Integrate the separated differential equation.
$$ $$\ln\left(T V^{\gamma - 1}\right) = \text{constant}$$ $$
*Physical Operation*: Integrate both sides assuming constant $\gamma$: $\int \frac{dT}{T} + (\gamma - 1) \int \frac{dV}{V} = \text{constant} \implies \ln T + (\gamma - 1) \ln V = \text{constant}$.

**Step 7**: Exponentiate both sides to obtain the temperature-volume adiabatic relation.
$$ $$T V^{\gamma - 1} = \text{constant}$$ $$
*Physical Operation*: Take the exponential of both sides: $T V^{\gamma - 1} = \exp(\text{constant}) = \text{constant}$.

**Applicability & Limiting Conditions**:
- Reversible (quasi-static) adiabatic process.
- Ideal gas with constant adiabatic index $\gamma$.
- Thermally insulated boundaries ($dQ = 0$).


---

### Worked Pedagogical Example: `ex-td-adiabatic-compression-01`

**Problem Statement**:
> A sample of $n = 2.0\text{ mol}$ of a diatomic ideal gas (with ratio of specific heats $\gamma = 1.4 = \frac{7}{5}$ and constant-volume molar heat capacity $C_V = \frac{5}{2}R$) is initially at temperature $T_0 = 300\text{ K}$ and volume $V_0$. The gas is enclosed in a thermally insulated cylinder fitted with a frictionless, non-conducting movable piston. The gas is compressed slowly and quasi-statically to a final volume $V_f = \frac{V_0}{32}$.
(a) Determine the final temperature $T_f$ of the gas in kelvin.
(b) Calculate the work done ON the gas ($W_{\text{on}}$) during this compression process in kilojoules (take universal gas constant $R = 8.314\text{ J/(mol}\cdot\text{K)}$).
(c) Verify the First Law of Thermodynamics by evaluating the change in internal energy $\Delta U$ of the gas.

**Target Quantity**: `T_f, W_{\text{on}}, \text{ and } \Delta U`

#### Systematic Solution
**Step 1 (Reversible adiabatic temperature-volume scaling relation)**:
$$ T V^{\gamma - 1} = \text{constant} \implies T_f = T_0 \left(\frac{V_0}{V_f}\right)^{\gamma - 1} $$
\gamma = 1.4 = \frac{7}{5}, \quad \gamma - 1 = \frac{2}{5} = 0.4, \quad \frac{V_0}{V_f} = 32 = 2^5
Result: `T_f = T_0 (2^5)^{2/5} = T_0 (2^2) = 4 T_0`

**Step 2 (Numerical evaluation of final temperature)**:
$$ T_f = 4 T_0 = 4 \times 300\text{ K} = 1200\text{ K} $$
T_0 = 300\text{ K}
Result: `Final temperature T_f = 1200 K (an increase of \Delta T = 900 K).`

**Step 3 (Change in internal energy from temperature rise)**:
$$ \Delta U = n C_V \Delta T = n \left(\frac{5}{2} R\right) (T_f - T_0) $$
\Delta U = (2.0\text{ mol}) \times \left(\frac{5}{2} \times 8.314\text{ J/(mol}\cdot\text{K)}\right) \times (1200\text{ K} - 300\text{ K}) = 5 \times 8.314 \times 900 = 37413\text{ J}
Result: `\Delta U = +37413 J = +37.413 kJ`

**Step 4 (Work done on the gas via the First Law of Thermodynamics)**:
$$ Q = \Delta U + W_{\text{by}} \implies 0 = \Delta U - W_{\text{on}} \implies W_{\text{on}} = \Delta U $$
W_{\text{on}} = +37.413\text{ kJ}, \quad W_{\text{by}} = -37.413\text{ kJ}
Result: `Work done on the gas W_on = +37.413 kJ (or +37.4 kJ to 3 significant figures).`

**Step 5 (Independent validation via direct adiabatic work integration)**:
$$ W_{\text{by}} = \frac{n R (T_0 - T_f)}{\gamma - 1} = \frac{2.0 \times 8.314 \times (300 - 1200)}{1.4 - 1} $$
W_{\text{by}} = \frac{-14965.2}{0.4} = -37413\text{ J}
Result: `Direct adiabatic integral yields identical result: W_on = +37.413 kJ.`

**Final Answer**: T_f = 1200\text{ K}; \quad W_{\text{on}} = +37.413\text{ kJ} \quad (\text{or } +37.4\text{ kJ}); \quad \Delta U = +37.413\text{ kJ}

**Sanity & Consistency Checks**:
- Physical compression heating: Compressing a thermally isolated gas adds external mechanical work which cannot escape as heat, guaranteeing T_f > T_0 (1200 K > 300 K).
- Dimensional consistency: [n C_V \Delta T] = mol * (J/(mol K)) * K = J, matching [W] = J.
- Limiting check V_f -> V_0: If V_f = V_0, T_f = T_0 (1)^{0.4} = 300 K, \Delta U = 0, W_on = 0.
- First Law balance: Q = \Delta U + W_by = 37.413 kJ + (-37.413 kJ) = 0 kJ, exactly satisfying Q = 0.


---

### Inoculation Against Misconception: `misc-td-01`

**Misconception Category**: `SIGN_MISTAKE`  
**Erroneous Intuition**: *"In an adiabatic expansion of an ideal gas, the work done by the gas is positive (W > 0), so the internal energy of the gas must increase and its temperature must rise."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> The First Law of Thermodynamics in physics dictates \Delta U = Q - W_by. For an adiabatic process, Q = 0, meaning \Delta U = - W_by. When the gas expands, W_by > 0, which directly forces \Delta U < 0; the internal energy decreases as it is converted into boundary work on the environment.

**Physical Truth & Resolution**:
In standard physics sign convention, the First Law of Thermodynamics is formulated as $dQ = dU + dW_{\text{by}}$, where $dW_{\text{by}} = P dV$ is the work performed BY the gas on its surroundings. Rewriting this for the change in internal energy gives $\Delta U = Q - W_{\text{by}}$. For an adiabatic process, the system is thermally isolated from its environment, so heat exchange is strictly zero: $Q = 0$. Consequently:
$$\Delta U = - W_{\text{by}}$$
During an expansion ($dV > 0$), the gas performs positive work on the surrounding piston or medium ($W_{\text{by}} = \int P dV > 0$). Since no heat energy can enter through the adiabatic boundary to fund this mechanical work, the energy must be extracted entirely from the thermal kinetic energy of the gas molecules. Therefore, $\Delta U = - W_{\text{by}} < 0$. For an ideal gas whose internal energy is given by $U = n C_V T$, a decrease in internal energy mandates a decrease in absolute temperature: $\Delta T = \Delta U / (n C_V) < 0$. Adiabatic expansion inevitably causes cooling, not heating.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 2, Chapter 26 (First Law of Thermodynamics), Section 26.5: 'Work Done by an Ideal Gas'; University Physics with Modern Physics, 13th Edition, Section 19.8; Questions thermodynamics-question-71b685c0 and thermodynamics-question-7e2f5a91.

**Diagnostic Symptom**: Student concludes that a gas heats up during adiabatic expansion, or writes \Delta U = + W in their thermodynamic energy balance.


---

### Verified JEE Practice Problem: `thermodynamics-question-71b685c0`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

### Verified JEE Practice Problem: `thermodynamics-question-7e2f5a91`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Radiation Thermodynamics and Photon Gas Adiabatic Expansion

> **Pedagogical Goal**: Extend thermodynamics beyond classical non-relativistic matter to relativistic blackbody radiation, deriving u = a T^4, radiation pressure P = u/3, and adiabatic scaling T V^(1/3) = const.


---

### Concept: Radiation Thermodynamics and the Relativistic Photon Gas

**Definition**: Blackbody radiation enclosed within a volume $V$ in thermal equilibrium at absolute temperature $T$ constitutes a photon gas characterized by an internal energy density $u(T) = a T^4$, where $a = 4\sigma/c$ is the radiation constant and $\sigma$ is the Stefan-Boltzmann constant. Due to the relativistic dispersion relation $E = pc$ and isotropic photon flux, the radiation pressure is isotropic and given by $P = \frac{1}{3} u = \frac{1}{3} a T^4$. For a reversible adiabatic expansion ($dQ = 0$), the First Law dictates $d(u V) + P dV = 0$, leading to the adiabatic scaling $T^3 V = \text{constant}$ (or $T V^{1/3} = \text{constant}$), which for a spherical cavity of radius $R$ corresponds to $T R = \text{constant}$.

**Physical Significance**: Imagine an empty spherical cavity with perfectly reflecting, movable walls in thermal equilibrium at temperature $T$. The cavity is not truly empty: it is filled with a gas of photons continuously emitted and absorbed by the walls. Unlike a classical gas of molecules, photons travel at the speed of light ($c$) and carry linear momentum $p = E/c$. Because photons have ultra-relativistic momentum, their collisions with the walls exert an outward radiation pressure $P = \frac{1}{3} u$, where $u$ is the energy density. If the cavity slowly expands adiabatically, the expanding cavity does work on the walls at the expense of radiant photon energy, causing the radiation to cool according to $T R = \text{constant}$, which is identical to the cosmological redshift of cosmic microwave background radiation during cosmic expansion.

**Assumptions & Scope of Validity**:
- The radiation is blackbody radiation in complete thermodynamic equilibrium with the cavity walls.
- The photon gas is isotropic, unpolarized on average, and obeys Planck's spectral distribution.
- The cavity expansion is quasi-static and adiabatic ($dQ = 0$).
- Photons are ultra-relativistic particles obeying $E = pc$.


---

### Formula: Adiabatic Expansion of Photon Gas

**Governing Equation**:
$$ T^3 V = \text{constant},\quad u = a T^4,\quad P = \frac{1}{3} u $$

**Variable Inventory & SI Units**:
- $T$: Equilibrium radiation temperature (Unit: `K` | Dim: `[\Theta]`)
- $V$: Cavity volume (Unit: `m^3` | Dim: `[L]^3`)
- $u$: Radiation energy density (Unit: `J/m^3` | Dim: `[M][L]^-1[T]^-2`)
- $P$: Radiation pressure (Unit: `Pa` | Dim: `[M][L]^-1[T]^-2`)
- $a$: Radiation density constant (Unit: `J/(m^3 K^4)` | Dim: `[M][L]^-1[T]^-2[\Theta]^-4`)

**Physical Assumptions**:
- Blackbody photon gas in thermal equilibrium
- Isotropic radiation field
- Relativistic ultra-relativistic energy-momentum relation E = p c

**Domain of Validity**:
- Quasi-static adiabatic expansion of photon cavity with perfectly reflecting walls


---

### Derivation: Formula `formula-td-radiation-adiabatic`

**Target Governing Relation**:
$$ $$T^3 V = \text{constant}$$ $$

#### Step-by-Step Proof
**Step 1**: Express total internal energy $U$ of blackbody radiation in cavity volume $V$ at temperature $T$.
$$ $$U = a V T^4$$ $$
*Physical Operation*: Multiply energy density $u(T) = a T^4$ by volume $V$ to find total radiant energy: $U = u V = a V T^4$, where $a = 4\sigma/c$ is the radiation constant.

**Step 2**: Calculate the total differential of internal energy $dU$ using the multivariable product rule.
$$ $$dU = a T^4 dV + 4 a V T^3 dT$$ $$
*Physical Operation*: Differentiate $U(V, T)$ with respect to independent state variables $V$ and $T$: $dU = d(a V T^4) = a T^4 dV + 4 a V T^3 dT$.

**Step 3**: Formulate the boundary mechanical work $dW$ using the relativistic radiation pressure equation of state.
$$ $$dW = \frac{1}{3} a T^4 dV$$ $$
*Physical Operation*: Substitute $u = a T^4$ into radiation pressure $P = \frac{1}{3} u = \frac{1}{3} a T^4$. The quasi-static boundary work is $dW = P dV = \frac{1}{3} a T^4 dV$.

**Step 4**: Apply the First Law of Thermodynamics for a reversible adiabatic expansion ($dQ = 0$).
$$ $$4 a V T^3 dT + \left(1 + \frac{1}{3}\right) a T^4 dV = 0$$ $$
*Physical Operation*: Substitute $dU$ and $dW$ into $0 = dU + dW$: $0 = (a T^4 dV + 4 a V T^3 dT) + \frac{1}{3} a T^4 dV$.

**Step 5**: Combine the volume differential terms.
$$ $$4 a V T^3 dT + \frac{4}{3} a T^4 dV = 0$$ $$
*Physical Operation*: Simplify $1 + \frac{1}{3} = \frac{4}{3}$: $4 a V T^3 dT + \frac{4}{3} a T^4 dV = 0$.

**Step 6**: Separate variables by dividing by $\frac{4}{3} a V T^4$.
$$ $$\frac{dT}{T} + \frac{1}{3} \frac{dV}{V} = 0$$ $$
*Physical Operation*: Divide by $\frac{4}{3} a V T^4$ (assuming $T > 0$ and $V > 0$): $3 \frac{dT}{T} + \frac{dV}{V} = 0 \implies \frac{dT}{T} + \frac{1}{3} \frac{dV}{V} = 0$.

**Step 7**: Integrate the separated differential equation to establish the photon gas scaling laws.
$$ $$T^3 V = \text{constant}$$ $$
*Physical Operation*: Integrate both sides: $\ln T + \frac{1}{3} \ln V = \text{constant} \implies \ln(T V^{1/3}) = \text{constant} \implies T V^{1/3} = \text{constant}$. Cubing both sides yields $T^3 V = \text{constant}$.

**Step 8**: Specialize to a spherical cavity of radius $R$ to derive the radial temperature scaling.
$$ $$T R = \text{constant}$$ $$
*Physical Operation*: For a sphere, $V = \frac{4}{3}\pi R^3$. Then $V^{1/3} = \left(\frac{4}{3}\pi\right)^{1/3} R$. Substituting into $T V^{1/3} = \text{constant}$ yields $T R = \text{constant}$.

**Applicability & Limiting Conditions**:
- Reversible adiabatic expansion of blackbody radiation/photon gas in 3D cavity.
- Relativistic energy-momentum relation $E = pc$ ensuring $P = u/3$.
- Thermally insulated cavity with reflecting or absorbing/emitting walls in equilibrium.


---

### Inoculation Against Misconception: `misc-td-02`

**Misconception Category**: `INVALID_FORMULA_CONDITION`  
**Erroneous Intuition**: *"The polytropic relation P V^gamma = constant and T V^(gamma - 1) = constant applies to all adiabatic processes, including irreversible free expansion into a vacuum."*  

> [!CAUTION] **Flawed Reasoning Mechanism**:
> The derivation of $P V^\gamma = \text{constant}$ integrates $dU = - P dV$, which requires well-defined equilibrium pressure throughout the gas and reversible boundary work. In free expansion against vacuum, $P_{\text{ext}} = 0$, so $W = 0$ and $\Delta U = 0$, resulting in constant temperature ($T_f = T_i$), in total contradiction to $P V^\gamma = \text{constant}$.

**Physical Truth & Resolution**:
The relation $P V^\gamma = \text{constant}$ is derived by combining the differential First Law $dQ = dU + P dV$ with $dQ = 0$, $dU = n C_V dT$, and the ideal gas equation $P = n R T / V$. This derivation strictly assumes that:
1. The process is reversible (quasi-static), ensuring the system passes through a continuum of thermodynamic equilibrium states with spatially uniform pressure $P$.
2. The mechanical work done by the system is given by the reversible boundary integral $W = \int P dV$.
In an irreversible free expansion (Joule expansion) of an ideal gas into an insulated evacuated vessel, the gas expands against zero opposing external pressure ($P_{\text{ext}} = 0$). Therefore, the work done on the surroundings is zero: $W = 0$. Because the container walls are thermally insulated, heat exchange is also zero: $Q = 0$. By the First Law of Thermodynamics:
$$\Delta U = Q - W = 0 - 0 = 0$$
For an ideal gas, internal energy depends only on temperature ($U = U(T)$), which means $\Delta T = 0$, or $T_f = T_i$. The temperature does not drop at all! If one naively applied the reversible formula $T V^{\gamma - 1} = \text{constant}$, one would falsely predict a drastic temperature drop $T_f = T_i (V_i / V_f)^{\gamma - 1} < T_i$. Free expansion generates entropy ($\Delta S = n R \ln(V_f / V_i) > 0$), and applying $P V^\gamma = \text{constant}$ is completely physically invalid.

**Refutation Counterexample & Supporting Evidence**:
H.C. Verma, Concepts of Physics Vol 2, Chapter 27 (Specific Heats of Gases), Section 27.8: 'Free Expansion'; Fundamentals of Physics by Halliday, Resnick, Walker, Section 19-8; Question thermodynamics-question-3fe51020.

**Diagnostic Symptom**: Student applies T V^(gamma - 1) = const or P V^gamma = const to free expansion or sudden burst of a container into a vacuum.


---

### Verified JEE Practice Problem: `thermodynamics-question-3fe51020`

**Type**: `SINGLE_CORRECT`  
**Provenance Source**: `Canonical KB`  

> 

<details>
<summary>Click to view independently verified solution key</summary>

**Verified Answer**: ****  
**Independent Verification Record**: `None`

</details>


---

## Heat Engines, the Carnot Cycle, and Second Law Formulations

> **Pedagogical Goal**: Analyze thermal cycles, calculate theoretical engine efficiency eta = 1 - T_C / T_H, and examine Kelvin-Planck and Clausius statements of the Second Law.


---

## Chapter Summary & Formula Recap: Thermodynamics

### Core Equations & Domains of Validity
- **First Law of Thermodynamics**: $$dQ = dU + dW$$
  *Validity*: Valid for any thermodynamic process connecting initial and final equilibrium states
- **Reversible Adiabatic Process for Ideal Gas**: $$T V^{\gamma - 1} = \text{constant},\quad P V^{\gamma} = \text{constant}$$
  *Validity*: System must be thermally insulated and process must be quasi-static without dissipation
- **Adiabatic Expansion of Photon Gas**: $$u = a T^4,\quad P = \frac{1}{3} u = \frac{1}{3} a T^4,\quad T V^{1/3} = \text{constant} \implies T R = \text{constant}$$
  *Validity*: Relativistic photon dispersion relation E = pc yielding P = u/3
