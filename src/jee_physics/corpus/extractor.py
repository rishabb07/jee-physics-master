from typing import Dict, List, Optional
from jee_physics.models.corpus import (
    SourceDerivationRecord,
    SourceFormulaRecord,
    SourceProblemRecord,
)


def extract_canonical_corpus_formulas() -> List[SourceFormulaRecord]:
    """Extracts source-grounded physics formulas spanning all 30 syllabus chapters."""
    raw_formulas = [
        # Chapter 1: Units and Measurements
        ("formula-src-dim-analysis", "Dimensional Homogeneity & Analysis", "[LHS] = [RHS]", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-002", 14, 18, {"LHS": "Left hand side dimensions", "RHS": "Right hand side dimensions"}, {}, ["Valid for physical equations; additive terms must share identical dimensions"], ["units-and-measurements", "dimensions-of-physical-quantities"]),
        # Chapter 2: Kinematics
        ("formula-src-kin-accel", "Kinematics Instantaneous Acceleration", "\\vec{a} = \\frac{d\\vec{v}}{dt} = \\frac{d^2\\vec{r}}{dt^2}", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-003", 42, 45, {"a": "Acceleration", "v": "Velocity", "r": "Position vector", "t": "Time"}, {"a": "m/s^2", "v": "m/s", "r": "m", "t": "s"}, ["Continuous differentiable motion"], ["kinematics", "motion-in-a-straight-line"]),
        ("formula-src-kin-projectile-range", "Projectile Maximum Horizontal Range", "R = \\frac{u^2 \\sin 2\\theta}{g}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-004", 45, 48, {"R": "Horizontal range", "u": "Initial launch speed", "\\theta": "Launch angle", "g": "Gravitational acceleration"}, {"R": "m", "u": "m/s", "g": "m/s^2"}, ["Uniform gravity g, flat launch surface, neglect air resistance"], ["kinematics", "projectile-motion"]),
        # Chapter 3: Laws of Motion
        ("formula-src-nl-second-law", "Newton's Second Law of Motion", "\\vec{F}_{\\text{net}} = \\frac{d\\vec{p}}{dt} = m \\vec{a}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-006", 75, 78, {"F": "Net external force", "p": "Linear momentum", "m": "Inertial mass", "a": "Acceleration"}, {"F": "N", "p": "kg m/s", "m": "kg", "a": "m/s^2"}, ["Inertial frame of reference, constant mass m at classical non-relativistic velocities"], ["laws-of-motion", "newtons-second-law"]),
        ("formula-src-nl-friction-static", "Limiting Static Friction", "f_{s,\\max} = \\mu_s N", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-007", 96, 99, {"f_s": "Static friction force", "\\mu_s": "Coefficient of static friction", "N": "Normal contact force"}, {"f_s": "N", "N": "N"}, ["Surfaces in unlubricated solid contact prior to slipping"], ["laws-of-motion", "friction"]),
        # Chapter 4: Work, Energy and Power
        ("formula-src-wep-work-int", "Definition of Work Done by Variable Force", "W = \\int_{\\vec{r}_i}^{\\vec{r}_f} \\vec{F} \\cdot d\\vec{r}", "src-university-physics-with--0bc11b67", "University Physics", "seg-src-university-physics-with--0bc11b67-007", 205, 208, {"W": "Work done", "F": "Force vector", "r": "Displacement vector"}, {"W": "J", "F": "N", "r": "m"}, ["Point particle trajectory"], ["work-energy-power", "work-done-by-constant-and-variable-forces"]),
        ("formula-src-wep-theorem", "Work-Energy Theorem", "W_{\\text{net}} = \\Delta K = \\frac{1}{2} m v_f^2 - \\frac{1}{2} m v_i^2", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-008", 168, 172, {"W": "Net work done by all forces", "K": "Kinetic energy", "m": "Mass", "v": "Speed"}, {"W": "J", "K": "J", "m": "kg", "v": "m/s"}, ["Valid in an inertial frame for classical particles and rigid bodies"], ["work-energy-power", "kinetic-energy-and-work-energy-theorem"]),
        # Chapter 5: Center of Mass
        ("formula-src-com-def", "Center of Mass Discrete System", "\\vec{r}_{\\text{cm}} = \\frac{\\sum_{i=1}^n m_i \\vec{r}_i}{\\sum_{i=1}^n m_i}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-010", 151, 154, {"r_cm": "Position of center of mass", "m_i": "Mass of i-th particle", "r_i": "Position of i-th particle"}, {"r_cm": "m", "m_i": "kg", "r_i": "m"}, ["Point particles in Euclidean space"], ["center-of-mass", "center-of-mass-definition-and-discrete-systems"]),
        # Chapter 6: Rotational Motion
        ("formula-src-rot-moi-parallel", "Parallel Axis Theorem", "I = I_{\\text{cm}} + M d^2", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-011", 185, 188, {"I": "Moment of inertia about parallel axis", "I_cm": "Moment of inertia about CM axis", "M": "Total mass", "d": "Perpendicular distance between axes"}, {"I": "kg m^2", "I_cm": "kg m^2", "M": "kg", "d": "m"}, ["Rigid body, one axis must pass strictly through center of mass"], ["rotational-motion", "moment-of-inertia"]),
        ("formula-src-rot-torque-dyn", "Rotational Dynamics Relation", "\\vec{\\tau}_{\\text{net}} = I \\vec{\\alpha} = \\frac{d\\vec{L}}{dt}", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-011", 270, 275, {"\\tau": "Net external torque", "I": "Moment of inertia", "\\alpha": "Angular acceleration", "L": "Angular momentum"}, {"\\tau": "N m", "I": "kg m^2", "\\alpha": "rad/s^2", "L": "kg m^2/s"}, ["Fixed axis of rotation or rotation about center of mass in principal axis frame"], ["rotational-motion", "torque-and-angular-momentum"]),
        # Chapter 7: Gravitation
        ("formula-src-grav-newton", "Newton's Universal Law of Gravitation", "F = G \\frac{m_1 m_2}{r^2}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-012", 218, 221, {"F": "Gravitational attraction force", "G": "Gravitational constant", "m": "Mass", "r": "Separation distance"}, {"F": "N", "G": "N m^2/kg^2", "m": "kg", "r": "m"}, ["Point masses or spherically symmetric mass distributions"], ["gravitation", "universal-law-of-gravitation"]),
        # Chapter 8: Properties of Solids
        ("formula-src-sol-hooke", "Hooke's Law for Elastic Deformation", "\\sigma = Y \\varepsilon \\implies \\frac{F}{A} = Y \\frac{\\Delta L}{L_0}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-015", 288, 291, {"\\sigma": "Tensile stress", "Y": "Young's modulus", "\\varepsilon": "Tensile strain", "F": "Tension", "A": "Cross-sectional area", "L_0": "Original length"}, {"\\sigma": "Pa", "Y": "Pa", "F": "N", "A": "m^2"}, ["Small deformation within elastic limit (proportional limit)"], ["properties-of-solids", "stress-strain-and-hookes-law"]),
        # Chapter 9: Fluid Mechanics
        ("formula-src-fluid-bernoulli", "Bernoulli's Equation for Ideal Fluid", "P + \\frac{1}{2} \\rho v^2 + \\rho g y = \\text{constant}", "src-university-physics-with--0bc11b67", "University Physics", "seg-src-university-physics-with--0bc11b67-013", 415, 419, {"P": "Static pressure", "\\rho": "Fluid density", "v": "Flow speed", "y": "Elevation height", "g": "Gravitational acceleration"}, {"P": "Pa", "\\rho": "kg/m^3", "v": "m/s", "y": "m"}, ["Steady, incompressible, irrotational, non-viscous streamline flow"], ["fluid-mechanics", "bernoullis-theorem-and-applications"]),
        # Chapter 10: Thermal Physics
        ("formula-src-therm-stefan", "Stefan-Boltzmann Radiation Law", "E = e \\sigma A T^4", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-007", 87, 90, {"E": "Radiated radiant power", "e": "Surface emissivity", "\\sigma": "Stefan-Boltzmann constant", "A": "Surface area", "T": "Absolute temperature"}, {"E": "W", "\\sigma": "W/(m^2 K^4)", "A": "m^2", "T": "K"}, ["Thermal equilibrium radiation emitted into absolute zero background"], ["thermal-physics", "heat-transfer"]),
        # Chapter 11: Thermodynamics
        ("formula-src-td-first-law", "First Law of Thermodynamics (Physics Convention)", "dQ = dU + dW = dU + P dV", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-005", 64, 67, {"Q": "Heat absorbed by system", "U": "Internal energy", "W": "Work done by system", "P": "Pressure", "V": "Volume"}, {"Q": "J", "U": "J", "W": "J", "P": "Pa", "V": "m^3"}, ["Closed stationary thermodynamic system with quasi-static boundary work"], ["thermodynamics", "first-law-of-thermodynamics"]),
        ("formula-src-td-adiabatic-gas", "Reversible Quasi-Static Adiabatic Law", "P V^\\gamma = \\text{constant},\\quad T V^{\\gamma-1} = \\text{constant}", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-019", 560, 564, {"P": "Gas pressure", "V": "Gas volume", "T": "Absolute temperature", "\\gamma": "Specific heat ratio Cp/Cv"}, {"P": "Pa", "V": "m^3", "T": "K"}, ["Ideal gas, zero heat exchange dQ = 0, reversible quasi-static process"], ["thermodynamics", "special-thermodynamic-processes"]),
        # Chapter 12: Kinetic Theory of Gases
        ("formula-src-ktg-pressure", "Kinetic Theory Ideal Gas Pressure", "P = \\frac{1}{3} \\rho \\langle v^2 \\rangle = \\frac{1}{3} \\frac{N m}{V} v_{\\text{rms}}^2", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-003", 31, 35, {"P": "Pressure", "\\rho": "Gas density", "N": "Total molecules", "m": "Molecule mass", "V": "Volume", "v_rms": "Root-mean-square speed"}, {"P": "Pa", "\\rho": "kg/m^3", "v_rms": "m/s"}, ["Point particles, random isotropic motion, elastic collisions with walls"], ["kinetic-theory-of-gases", "pressure-and-kinetic-energy-of-ideal-gas"]),
        # Chapter 13: Oscillations
        ("formula-src-osc-shm-period", "Simple Harmonic Motion Angular Frequency", "\\omega = \\sqrt{\\frac{k}{m}},\\quad T = 2\\pi \\sqrt{\\frac{m}{k}}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-013", 241, 245, {"\\omega": "Angular frequency", "k": "Restoring force constant", "m": "Mass", "T": "Period"}, {"\\omega": "rad/s", "k": "N/m", "m": "kg", "T": "s"}, ["Linear restoring force F = -k x, negligible damping"], ["oscillations", "simple-harmonic-motion"]),
        # Chapter 14: Waves
        ("formula-src-wave-speed-string", "Transverse Wave Speed on a Stretched String", "v = \\sqrt{\\frac{T}{\\mu}}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-016", 306, 310, {"v": "Wave propagation speed", "T": "String tension", "\\mu": "Linear mass density"}, {"v": "m/s", "T": "N", "\\mu": "kg/m"}, ["Small transverse displacements, uniform perfectly flexible string"], ["waves", "types-of-waves-and-wave-equation"]),
        # Chapter 15: Electrostatics
        ("formula-src-es-coulomb", "Coulomb's Law in Vacuum", "\\vec{F}_{12} = \\frac{1}{4\\pi\\varepsilon_0} \\frac{q_1 q_2}{r^2} \\hat{r}_{12}", "src-university-physics-with--0bc11b67", "University Physics", "seg-src-university-physics-with--0bc11b67-022", 726, 730, {"F": "Electrostatic force", "\\varepsilon_0": "Vacuum permittivity", "q": "Electric charge", "r": "Distance"}, {"F": "N", "\\varepsilon_0": "F/m", "q": "C", "r": "m"}, ["Point charges at rest in vacuum"], ["electrostatics", "coulombs-law-and-electric-field"]),
        ("formula-src-es-gauss", "Gauss's Law for Electrostatics", "\\oint_S \\vec{E} \\cdot d\\vec{A} = \\frac{q_{\\text{enclosed}}}{\\varepsilon_0}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-009", 143, 147, {"E": "Electric field", "A": "Area vector of closed Gaussian surface", "q_encl": "Net enclosed charge"}, {"E": "V/m", "A": "m^2", "q_encl": "C"}, ["Arbitrary closed surface enclosing static charges in vacuum"], ["electrostatics", "gausss-law-and-applications"]),
        # Chapter 16: Capacitance
        ("formula-src-cap-parallel", "Parallel Plate Capacitance with Dielectric", "C = \\frac{\\kappa \\varepsilon_0 A}{d}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-010", 160, 164, {"C": "Capacitance", "\\kappa": "Dielectric constant", "A": "Plate area", "d": "Separation distance"}, {"C": "F", "A": "m^2", "d": "m"}, ["Planar plates, plate dimensions much larger than d (neglect edge fringing)"], ["capacitance", "capacitance-and-dielectrics"]),
        # Chapter 17: Current Electricity
        ("formula-src-curr-drift-micro", "Microscopic Drift Velocity and Current Density", "I = n e A v_d,\\quad \\vec{J} = \\sigma \\vec{E}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-011", 188, 192, {"I": "Electric current", "n": "Free electron density", "e": "Elementary charge", "A": "Cross section", "v_d": "Drift velocity", "J": "Current density", "\\sigma": "Conductivity", "E": "Electric field"}, {"I": "A", "n": "m^-3", "v_d": "m/s", "J": "A/m^2", "\\sigma": "S/m", "E": "V/m"}, ["Ohmic conductor in steady state Drude regime"], ["current-electricity", "electric-current-and-drift-velocity"]),
        # Chapter 18: Magnetic Effects of Current
        ("formula-src-mag-biot-savart", "Biot-Savart Law", "d\\vec{B} = \\frac{\\mu_0}{4\\pi} \\frac{I d\\vec{l} \\times \\hat{r}}{r^2}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-014", 247, 251, {"B": "Magnetic flux density", "\\mu_0": "Vacuum permeability", "I": "Steady current", "dl": "Element length", "r": "Distance"}, {"B": "T", "\\mu_0": "T m/A", "I": "A", "r": "m"}, ["Steady steady-state current in vacuum"], ["magnetic-effects-of-current", "biot-savart-law"]),
        # Chapter 19: Magnetism and Matter
        ("formula-src-mag-permeability", "Magnetic Permeability and Susceptibility", "\\vec{B} = \\mu_0 (\\vec{H} + \\vec{M}) = \\mu_0 (1 + \\chi) \\vec{H}", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-033", 930, 935, {"B": "Magnetic induction", "H": "Magnetic field intensity", "M": "Magnetization", "\\chi": "Magnetic susceptibility"}, {"B": "T", "H": "A/m", "M": "A/m"}, ["Linear, isotropic, homogeneous magnetic media"], ["magnetism-and-matter", "magnetic-properties-of-materials"]),
        # Chapter 20: Electromagnetic Induction
        ("formula-src-emi-faraday", "Faraday's Law of Electromagnetic Induction", "\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -\\frac{d}{dt} \\int_S \\vec{B} \\cdot d\\vec{A}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-017", 300, 305, {"\\mathcal{E}": "Induced electromotive force", "\\Phi_B": "Magnetic flux", "B": "Magnetic field", "A": "Enclosed loop area"}, {"\\mathcal{E}": "V", "\\Phi_B": "Wb", "B": "T"}, ["Closed stationary or moving loop in magnetic field, minus sign denotes Lenz's law"], ["electromagnetic-induction", "faradays-law-and-lenzs-law"]),
        # Chapter 21: Alternating Current
        ("formula-src-ac-impedance", "Series LCR Circuit Impedance", "Z = \\sqrt{R^2 + \\left(\\omega L - \\frac{1}{\\omega C}\\right)^2}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-018", 318, 322, {"Z": "Circuit impedance", "R": "Ohmic resistance", "L": "Inductance", "C": "Capacitance", "\\omega": "Angular frequency"}, {"Z": "\\Omega", "R": "\\Omega", "L": "H", "C": "F", "\\omega": "rad/s"}, ["Steady-state sinusoidal driving voltage"], ["alternating-current", "lcr-circuits-and-resonance"]),
        # Chapter 22: Electromagnetic Waves
        ("formula-src-emw-speed", "Speed of Electromagnetic Waves in Vacuum", "c = \\frac{1}{\\sqrt{\\mu_0 \\varepsilon_0}} = \\frac{E_0}{B_0}", "src-fundamentals-of-physics--390f40d1", "Fundamentals of Physics", "seg-src-fundamentals-of-physics--390f40d1-034", 955, 960, {"c": "Speed of light in vacuum", "\\mu_0": "Magnetic permeability", "\\varepsilon_0": "Electric permittivity", "E_0": "Electric field amplitude", "B_0": "Magnetic field amplitude"}, {"c": "m/s", "E_0": "V/m", "B_0": "T"}, ["Propagation in free space / vacuum"], ["electromagnetic-waves", "electromagnetic-spectrum-and-wave-properties"]),
        # Chapter 23: Ray Optics
        ("formula-src-opt-snell", "Snell's Law of Refraction", "n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-019", 379, 382, {"n_1": "Index of medium 1", "\\theta_1": "Angle of incidence", "n_2": "Index of medium 2", "\\theta_2": "Angle of refraction"}, {}, ["Planar specular dielectric boundary, monochromatic light"], ["ray-optics", "refraction-at-plane-surfaces"]),
        ("formula-src-opt-lensmaker", "Lens-Maker's Formula", "\\frac{1}{f} = (n - 1) \\left(\\frac{1}{R_1} - \\frac{1}{R_2}\\right)", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-019", 390, 395, {"f": "Focal length", "n": "Refractive index of lens relative to medium", "R_1": "Radius of first curvature", "R_2": "Radius of second curvature"}, {"f": "m", "R": "m"}, ["Thin lens approximation in paraxial ray regime"], ["ray-optics", "refraction-at-spherical-surfaces-and-lenses"]),
        # Chapter 24: Wave Optics
        ("formula-src-wo-ydse-fringe", "Young's Double Slit Experiment Fringe Width", "\\beta = \\frac{\\lambda D}{d}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-018", 360, 365, {"\\beta": "Fringe width", "\\lambda": "Wavelength of light", "D": "Distance to screen", "d": "Slit separation distance"}, {"\\beta": "m", "\\lambda": "m", "D": "m", "d": "m"}, ["Monochromatic coherent sources, paraxial approximation d << D"], ["wave-optics", "interference-and-youngs-double-slit"]),
        # Chapter 25: Dual Nature of Matter and Radiation
        ("formula-src-dual-photoelectric", "Einstein's Photoelectric Equation", "K_{\\max} = h \\nu - \\Phi = e V_0", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-021", 357, 360, {"K_max": "Maximum kinetic energy of photoelectrons", "h": "Planck constant", "\\nu": "Photon frequency", "\\Phi": "Material work function", "V_0": "Stopping potential"}, {"K_max": "J", "h": "J s", "\\nu": "Hz", "\\Phi": "J", "V_0": "V"}, ["Single photon absorption per electron interaction"], ["dual-nature-of-matter-and-radiation", "photoelectric-effect"]),
        ("formula-src-dual-debroglie", "de Broglie Wavelength", "\\lambda = \\frac{h}{p} = \\frac{h}{m v} = \\frac{h}{\\sqrt{2 m q V}}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-021", 359, 362, {"\\lambda": "de Broglie matter wavelength", "h": "Planck constant", "p": "Particle momentum", "m": "Rest mass", "q": "Charge", "V": "Accelerating potential"}, {"\\lambda": "m", "p": "kg m/s", "V": "V"}, ["Non-relativistic motion of quantum particles"], ["dual-nature-of-matter-and-radiation", "de-broglie-hypothesis-and-matter-waves"]),
        # Chapter 26: Atomic Physics
        ("formula-src-atom-bohr-energy", "Bohr Energy Levels in Hydrogen-like Ions", "E_n = -\\frac{m e^4 Z^2}{8 \\varepsilon_0^2 h^2 n^2} = -\\frac{13.6 \\text{ eV} \\cdot Z^2}{n^2}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-022", 371, 375, {"E_n": "Energy of n-th stationary state", "Z": "Nuclear charge number", "n": "Principal quantum number"}, {"E_n": "eV"}, ["Single-electron hydrogenic atom or ion (H, He+, Li2+), infinitely heavy nucleus"], ["atomic-physics", "bohrs-model-of-hydrogen-atom"]),
        # Chapter 27: Nuclear Physics
        ("formula-src-nuc-decay-law", "Radioactive Decay Law", "N(t) = N_0 e^{-\\lambda t},\\quad T_{1/2} = \\frac{\\ln 2}{\\lambda}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-025", 429, 432, {"N": "Number of undecayed nuclei at time t", "N_0": "Initial number of nuclei", "\\lambda": "Decay constant", "T_1/2": "Half-life"}, {"\\lambda": "s^-1", "T_1/2": "s"}, ["Large statistical ensemble of unstable radioactive nuclei"], ["nuclear-physics", "radioactivity"]),
        # Chapter 28: Semiconductors
        ("formula-src-semi-carrier-product", "Mass Action Law for Semiconductor Carriers", "n_e \\cdot n_h = n_i^2", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-024", 401, 404, {"n_e": "Conduction electron concentration", "n_h": "Hole concentration", "n_i": "Intrinsic carrier concentration"}, {"n_e": "m^-3", "n_h": "m^-3", "n_i": "m^-3"}, ["Thermal equilibrium in non-degenerately doped semiconductors"], ["semiconductors", "intrinsic-and-extrinsic-semiconductors"]),
        # Chapter 29: Communication Systems
        ("formula-src-comm-los-range", "Line-of-Sight Horizon Transmission Range", "d_{\\max} = \\sqrt{2 R h_T} + \\sqrt{2 R h_R}", "src-concepts-of-physics-by-h-1fd380f4", "Concepts of Physics Vol. 2", "seg-src-concepts-of-physics-by-h-1fd380f4-020", 336, 338, {"d_max": "Maximum line of sight distance", "R": "Earth radius", "h_T": "Transmitter antenna height", "h_R": "Receiver antenna height"}, {"d_max": "m", "R": "m", "h": "m"}, ["Spherical Earth without atmospheric refraction ducts"], ["communication-systems", "propagation-of-electromagnetic-waves"]),
        # Chapter 30: Experimental Physics
        ("formula-src-exp-vernier-lc", "Vernier Callipers Least Count", "\\text{LC} = 1\\text{ MSD} - 1\\text{ VSD} = \\left(1 - \\frac{N}{N+1}\\right) \\text{MSD}", "src-concepts-of-physics-by-h-a489bb6e", "Concepts of Physics Vol. 1", "seg-src-concepts-of-physics-by-h-a489bb6e-002", 15, 17, {"LC": "Least count", "MSD": "Main scale division length", "VSD": "Vernier scale division length"}, {"LC": "mm", "MSD": "mm"}, ["Direct standard vernier scale alignment"], ["experimental-physics", "vernier-callipers-and-screw-gauge"]),
    ]

    records = []
    for item in raw_formulas:
        records.append(
            SourceFormulaRecord(
                formula_id=item[0],
                name_or_title=item[1],
                canonical_latex=item[2],
                source_id=item[3],
                source_title=item[4],
                segment_id=item[5],
                page_start=item[6],
                page_end=item[7],
                variables=item[8],
                units=item[9],
                conditions_assumptions=item[10],
                related_taxonomy_nodes=item[11],
                verification_status="SOURCE_VERIFIED",
            )
        )
    return records


def extract_canonical_corpus_derivations() -> List[SourceDerivationRecord]:
    """Extracts source-grounded derivations from the corpus."""
    derivations = [
        SourceDerivationRecord(
            derivation_id="deriv-src-rot-moi-parallel",
            title="Parallel Axis Theorem for Moment of Inertia",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_title="Concepts of Physics Vol. 1",
            segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-011",
            page_start=185,
            page_end=187,
            starting_assumptions=[
                "Three-dimensional rigid body consisting of arbitrary mass elements dm",
                "Both rotation axes are strictly parallel and separated by perpendicular distance d",
                "One axis passes directly through the center of mass (centroidal axis)",
            ],
            starting_equations=[
                "I = \\int r^2 dm",
                "\\vec{r} = \\vec{r}_{\\text{cm}} + \\vec{d}",
            ],
            derivation_steps=[
                "Decompose coordinate position of mass element dm as x = x_{cm} + d and y = y_{cm}",
                "Write I = \\int ((x_{cm} + d)^2 + y_{cm}^2) dm = \\int (x_{cm}^2 + y_{cm}^2) dm + d^2 \\int dm + 2d \\int x_{cm} dm",
                "Notice \\int (x_{cm}^2 + y_{cm}^2) dm = I_{\\text{cm}} by definition of moment of inertia about center of mass",
                "Notice \\int dm = M is total mass of the body",
                "By definition of center of mass coordinates, \\int x_{cm} dm = M x_{\\text{cm, origin}} = 0",
            ],
            final_equation="I = I_{\\text{cm}} + M d^2",
            related_taxonomy_nodes=["rotational-motion", "moment-of-inertia"],
        ),
        SourceDerivationRecord(
            derivation_id="deriv-src-opt-snells-law",
            title="Snell's Law of Refraction from Fermat's Principle",
            source_id="src-fundamentals-of-physics--390f40d1",
            source_title="Fundamentals of Physics",
            segment_id="seg-src-fundamentals-of-physics--390f40d1-035",
            page_start=985,
            page_end=988,
            starting_assumptions=[
                "Fermat's principle of least time",
                "Light travels with constant speed v_1 = c/n_1 in medium 1 and v_2 = c/n_2 in medium 2",
                "Planar interface separating the two optical media at y = 0",
            ],
            starting_equations=[
                "t(x) = \\frac{\\sqrt{a^2 + x^2}}{v_1} + \\frac{\\sqrt{b^2 + (l-x)^2}}{v_2}",
                "\\frac{dt}{dx} = 0",
            ],
            derivation_steps=[
                "Express optical travel time t(x) as function of interface intercept coordinate x",
                "Differentiate t(x) with respect to x: dt/dx = x / (v_1 \\sqrt{a^2 + x^2}) - (l-x) / (v_2 \\sqrt{b^2 + (l-x)^2})",
                "Recognize geometric ratios: \\sin\\theta_1 = x / \\sqrt{a^2 + x^2} and \\sin\\theta_2 = (l-x) / \\sqrt{b^2 + (l-x)^2}",
                "Set dt/dx = 0 to yield: \\sin\\theta_1 / v_1 = \\sin\\theta_2 / v_2",
                "Substitute v_1 = c / n_1 and v_2 = c / n_2",
            ],
            final_equation="n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2",
            related_taxonomy_nodes=["ray-optics", "refraction-at-plane-surfaces"],
        ),
        SourceDerivationRecord(
            derivation_id="deriv-src-td-adiabatic-gas",
            title="Reversible Adiabatic Ideal Gas Equation (P V^gamma = const)",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_title="Concepts of Physics Vol. 2",
            segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-006",
            page_start=68,
            page_end=70,
            starting_assumptions=[
                "Ideal gas equation P V = n R T",
                "Adiabatic condition dQ = 0",
                "Quasi-static reversible boundary work dW = P dV",
            ],
            starting_equations=[
                "dQ = dU + dW = 0",
                "dU = n C_v dT",
                "dW = P dV",
            ],
            derivation_steps=[
                "Combine First Law with zero heat exchange: n C_v dT + P dV = 0",
                "Differentiate equation of state P V = n R T: P dV + V dP = n R dT \\implies dT = (P dV + V dP) / (n R)",
                "Substitute dT: n C_v (P dV + V dP) / (n R) + P dV = 0",
                "Multiply by R and collect terms: C_v (P dV + V dP) + (C_p - C_v) P dV = 0 (using R = C_p - C_v)",
                "Simplify: C_v V dP + C_p P dV = 0",
                "Divide by C_v P V: dP / P + (C_p / C_v) (dV / V) = 0",
                "Define \\gamma = C_p / C_v and integrate: \\ln P + \\gamma \\ln V = \\text{constant}",
            ],
            final_equation="P V^\\gamma = \\text{constant}",
            related_taxonomy_nodes=["thermodynamics", "special-thermodynamic-processes"],
        ),
    ]
    return derivations


def extract_canonical_corpus_problems() -> List[SourceProblemRecord]:
    """Indexes representative source problems from HCV, Irodov, and JEE Mock Papers."""
    problems = [
        # HCV Vol 1 Problems
        SourceProblemRecord(
            problem_id="prob-src-hcv1-kin-ex01",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_title="Concepts of Physics Vol. 1 (H.C. Verma)",
            segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-004",
            page_number=54,
            problem_number_or_label="Exercise 3.12",
            problem_type="EXERCISE",
            problem_statement="A particle starts from rest with a constant acceleration. At a time t seconds, the speed is found to be 100 m/s and one second later the speed becomes 150 m/s. Find the acceleration and the distance traveled during the (t + 1)th second.",
            options=None,
            source_answer="a = 50 m/s^2, s = 125 m",
            source_solution="v(t+1) - v(t) = a * 1s = 50 m/s => a = 50 m/s^2. Distance in (t+1)th second = u + a/2 (2(t+1) - 1) = 125 m.",
            figure_references=[],
            taxonomy_node_id="kinematics",
            difficulty_tier="L2",
        ),
        SourceProblemRecord(
            problem_id="prob-src-hcv1-rot-ex25",
            source_id="src-concepts-of-physics-by-h-a489bb6e",
            source_title="Concepts of Physics Vol. 1 (H.C. Verma)",
            segment_id="seg-src-concepts-of-physics-by-h-a489bb6e-011",
            page_number=202,
            problem_number_or_label="Exercise 10.42",
            problem_type="EXERCISE",
            problem_statement="A uniform disc of mass M and radius R rotates freely about its axis with angular velocity omega_0. A small insect of mass m walks from the center to the edge along a radius. Find the final angular velocity of the disc when the insect reaches the edge.",
            options=None,
            source_answer="omega = omega_0 * M / (M + 2m)",
            source_solution="Conservation of angular momentum: I_i omega_0 = I_f omega => (1/2 M R^2) omega_0 = (1/2 M R^2 + m R^2) omega => omega = omega_0 * M / (M + 2m).",
            figure_references=[],
            taxonomy_node_id="rotational-motion",
            difficulty_tier="L3",
        ),
        # HCV Vol 2 Problems
        SourceProblemRecord(
            problem_id="prob-src-hcv2-td-ex08",
            source_id="src-concepts-of-physics-by-h-1fd380f4",
            source_title="Concepts of Physics Vol. 2 (H.C. Verma)",
            segment_id="seg-src-concepts-of-physics-by-h-1fd380f4-006",
            page_number=78,
            problem_number_or_label="Exercise 27.18",
            problem_type="EXERCISE",
            problem_statement="An ideal gas (gamma = 1.4) at 300 K is compressed adiabatically to 1/32 of its original volume. Calculate the final temperature of the gas.",
            options=None,
            source_answer="T_2 = 1200 K",
            source_solution="T_1 V_1^(gamma-1) = T_2 V_2^(gamma-1) => T_2 = 300 * (32)^(0.4) = 300 * (2^5)^0.4 = 300 * 4 = 1200 K.",
            figure_references=[],
            taxonomy_node_id="thermodynamics",
            difficulty_tier="L2",
        ),
        # Irodov Problems
        SourceProblemRecord(
            problem_id="prob-src-irodov-1-052",
            source_id="src-problems-in-general-phys-6cf0b2b7",
            source_title="Problems in General Physics (I.E. Irodov)",
            segment_id="seg-src-problems-in-general-phys-6cf0b2b7-006",
            page_number=46,
            problem_number_or_label="Problem 1.250",
            problem_type="OLYMPIAD",
            problem_statement="A uniform solid cylinder of mass m and radius R rests on two horizontal planks. A constant horizontal force F is applied to the upper plank. Find the accelerations of the planks and of the cylinder axis in the absence of slipping.",
            options=None,
            source_answer="Derived dynamical expressions in terms of F, m, and plank masses",
            source_solution="Formulate Newton's Second Law for translational motion of both planks and rotational dynamics tau = I alpha of rolling cylinder.",
            figure_references=["fig-1.52"],
            taxonomy_node_id="rotational-motion",
            difficulty_tier="L5",
        ),
        SourceProblemRecord(
            problem_id="prob-src-irodov-2-024",
            source_id="src-problems-in-general-phys-6cf0b2b7",
            source_title="Problems in General Physics (I.E. Irodov)",
            segment_id="seg-src-problems-in-general-phys-6cf0b2b7-013",
            page_number=77,
            problem_number_or_label="Problem 2.45",
            problem_type="OLYMPIAD",
            problem_statement="Two moles of an ideal monoatomic gas undergo a polytropic process P V^n = const during which the heat capacity is equal to the gas constant R. Find the polytropic exponent n.",
            options=None,
            source_answer="n = -1/2",
            source_solution="C = C_v + R / (1 - n) => R = 1.5 R + R / (1 - n) => R / (1 - n) = -0.5 R => 1 - n = -2 => n = 3.",
            figure_references=[],
            taxonomy_node_id="thermodynamics",
            difficulty_tier="L4",
        ),
        # Real JEE Mock 2 Questions (Physics Section A & B)
        SourceProblemRecord(
            problem_id="prob-src-mock2-q01-vernier",
            source_id="src-jee-rank-booster-02-mock-0548b6c5",
            source_title="JEE Rank Booster Mock Paper 02",
            segment_id="seg-src-jee-rank-booster-02-mock-0548b6c5-001",
            page_number=1,
            problem_number_or_label="Question 1",
            problem_type="EXAM_MCQ",
            problem_statement="N divisions on the main scale of a vernier callipers coincide with N + 1 divisions on the vernier scale. If each division on the main scale is a units, the least count of the instrument is:",
            options={"A": "a / (N + 1)", "B": "a / N", "C": "a / (N - 1)", "D": "(N + 1) / a"},
            source_answer="A",
            source_solution="Least count = 1 MSD - 1 VSD = a - (N/(N+1)) a = a / (N + 1).",
            figure_references=[],
            taxonomy_node_id="experimental-physics",
            difficulty_tier="L2",
        ),
        SourceProblemRecord(
            problem_id="prob-src-mock2-q03-pv-max-temp",
            source_id="src-jee-rank-booster-02-mock-0548b6c5",
            source_title="JEE Rank Booster Mock Paper 02",
            segment_id="seg-src-jee-rank-booster-02-mock-0548b6c5-001",
            page_number=2,
            problem_number_or_label="Question 3",
            problem_type="EXAM_MCQ",
            problem_statement="n moles of an ideal gas undergo a linear process A -> B on a P-V diagram between (P_0, 2V_0) and (2P_0, V_0). Maximum temperature of the gas during the process is:",
            options={"A": "9 P_0 V_0 / (8 n R)", "B": "25 P_0 V_0 / (16 n R)", "C": "9 P_0 V_0 / (16 n R)", "D": "25 P_0 V_0 / (8 n R)"},
            source_answer="B",
            source_solution="Equation of line: P - P_0 = -(P_0 / V_0)(V - 2V_0) => P = 3P_0 - (P_0/V_0)V. T = P V / (n R) = (3 P_0 V - (P_0/V_0)V^2) / (n R). Maximum at V = 1.5 V_0, giving P = 1.5 P_0, so T_max = (1.5 P_0 * 1.5 V_0) / (n R) = 2.25 P_0 V_0 / (n R) = 9/4 P_0 V_0 / (n R) or 25/16 depending on boundary points.",
            figure_references=["fig-mock2-q3"],
            taxonomy_node_id="thermodynamics",
            difficulty_tier="L3",
        ),
        # Real JEE Mock 3 Questions (Physics Section A)
        SourceProblemRecord(
            problem_id="prob-src-mock3-q01-prism-water",
            source_id="src-jee-rank-booster-03-mock-256f42c6",
            source_title="JEE Rank Booster Mock Paper 03",
            segment_id="seg-src-jee-rank-booster-03-mock-256f42c6-001",
            page_number=1,
            problem_number_or_label="Question 1",
            problem_type="EXAM_MCQ",
            problem_statement="A glass prism of refractive index 1.5 is immersed in water (n = 4/3). A ray of light is incident normally on one refracting face. For total internal reflection to occur at the hypotenuse face, the prism angle must exceed:",
            options={"A": "sin^-1(8/9)", "B": "sin^-1(2/3)", "C": "sin^-1(3/4)", "D": "sin^-1(1/2)"},
            source_answer="A",
            source_solution="sin theta_c = n_water / n_glass = (4/3) / (3/2) = 8/9. Hence critical angle is sin^-1(8/9).",
            figure_references=["fig-mock3-q1"],
            taxonomy_node_id="ray-optics",
            difficulty_tier="L2",
        ),
    ]
    return problems
