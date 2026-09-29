import json
import uuid
import datetime
import os

results = [
    {
        'atom_id': 'kinematics-question-b29767c8',
        'blind_package_hash': '7e4d541cd9e3c195682db0f6a15be1b9baa74924aa232d12c0b3128df2b119c7',
        'content_hash': '75a50f78ef107d1abfddbc5ccff76b0166dbb7d41f4e877fb6f0fe3032875d5b',
        'ans': 'C',
        'raw_ans': 'tan^-1(7/4)',
        'reasoning': [
            '1. Position vector at t=2s is r = 40i + 50j.',
            '2. Horizontal motion: x = u*cos(theta)*t => 40 = u*cos(theta)*2 => u*cos(theta) = 20.',
            '3. Vertical motion: y = u*sin(theta)*t - 1/2*g*t^2 => 50 = u*sin(theta)*2 - 0.5*10*4 => u*sin(theta)*2 = 70 => u*sin(theta) = 35.',
            '4. tan(theta) = (u*sin(theta)) / (u*cos(theta)) = 35 / 20 = 7/4.',
            '5. theta = tan^-1(7/4).'
        ]
    },
    {
        'atom_id': 'rotational-motion-question-f7cbecda',
        'blind_package_hash': '762971ec073a0db8fcac144b5f054efeee108518a11e36347f41c0214d4655fc',
        'content_hash': '729335ea8d2363b7b4f02d4c22c2c28352bc06a5093b5760855b1c5a20a7ff38',
        'ans': 'C',
        'raw_ans': 'first increases and then decreases',
        'reasoning': [
            '1. No external torque acts on the disc-insect system about the vertical axis.',
            '2. Angular momentum L is conserved. L = I * omega = constant.',
            '3. As the insect moves from rim to center, the moment of inertia I decreases, so omega increases.',
            '4. As the insect moves from center to the opposite rim, I increases, so omega decreases.',
            '5. Thus, angular speed first increases and then decreases.'
        ]
    },
    {
        'atom_id': 'current-electricity-question-d2492f7f',
        'blind_package_hash': '45c1c1eb3d4e364aeca7d798e2a54c3109f195567ed7069c90ed7ca749afd1c5',
        'content_hash': '5191a1c0c5850b6fa92086f0bf29a9b6544e9692f7cafc452719aebd3abff836',
        'ans': 'B',
        'raw_ans': '3.00 A, 5 V',
        'reasoning': [
            '1. The voltmeter has infinite resistance and ammeter has zero resistance.',
            '2. R1 (5 ohms) and R2 (15 ohms) are in parallel. Equivalent resistance R_p = (5*15)/(5+15) = 3.75 ohms.',
            '3. This is in series with R3 (1.25 ohms). Total resistance R_eq = 3.75 + 1.25 = 5.00 ohms.',
            '4. Total current from battery I = E / R_eq = 20 / 5 = 4 A.',
            '5. Current through ammeter (in R1 branch) = I * R2 / (R1 + R2) = 4 * 15 / 20 = 3 A.',
            '6. Voltmeter is across R3 (based on option values), so V = I * R3 = 4 * 1.25 = 5 V.'
        ]
    },
    {
        'atom_id': 'thermodynamics-question-71b685c0',
        'blind_package_hash': '5f271ba083f0adbb2d9731efd6f6b9139643f42845a7bccda05536255a66cdde',
        'content_hash': '989a378467ccf659bd7bd108e19c9956e6d7e862c73e86043bd81d15e4e2aab1',
        'ans': 'A',
        'raw_ans': '4T_0',
        'reasoning': [
            '1. The container and piston are nonconducting, meaning the process is adiabatic.',
            '2. For a monoatomic ideal gas, gamma = 5/3.',
            '3. The relation between temperature and volume in an adiabatic process is T * V^(gamma - 1) = constant.',
            '4. T_f = T_i * (V_i / V_f)^(gamma - 1).',
            '5. V_f = 12.5% of V_i = V_i / 8.',
            '6. T_f = T_0 * (8)^(5/3 - 1) = T_0 * 8^(2/3) = T_0 * 4 = 4T_0.'
        ]
    },
    {
        'atom_id': 'electrostatics-question-132c25d1',
        'blind_package_hash': 'a3b434e1bb06f04e4336a43dd2f351b10012aaa683b6d2ad099379cca44e8e62',
        'content_hash': '55511314791636289281fa986d2b38358fd33945eb154d89f87d5bc7ea6a59a7',
        'ans': 'C',
        'raw_ans': 'Q / (8*epsilon_0)',
        'reasoning': [
            '1. Place a point charge +Q at the center of the base of the square pyramid.',
            '2. By symmetry, imagine a second identical pyramid placed inverted below the first one to form a regular octahedron.',
            '3. The charge Q is now at the center of the octahedron.',
            '4. The total flux emanating from the charge Q is Q / epsilon_0.',
            '5. The octahedron has 8 identical triangular faces, so the flux through each face is (Q / epsilon_0) / 8.',
            '6. The flux through one of the upper faces of the pyramid is Q / (8 * epsilon_0).'
        ]
    },
    {
        'atom_id': 'fluid-mechanics-question-71ea5e08',
        'blind_package_hash': '40858b1ef0827664e98fbe8a36d9e4faf6b0d4af88388a457bb57256e73177e9',
        'content_hash': '4f8473663e36491674455ad903d7f97af23d3aca69a7268dff8caa6ecb403a7c',
        'ans': 'D',
        'raw_ans': 'rho_1 < rho_3 < rho_2',
        'reasoning': [
            '1. The ball comes to equilibrium at the interface between liquid 1 and liquid 2.',
            '2. It sinks in liquid 1, meaning its density is greater than liquid 1: rho_3 > rho_1.',
            '3. It floats on liquid 2, meaning its density is less than liquid 2: rho_3 < rho_2.',
            '4. Therefore, rho_1 < rho_3 < rho_2.'
        ]
    },
    {
        'atom_id': 'oscillations-question-d21a08b6',
        'blind_package_hash': '1f2fce38a58935b23e192153d58d1a5dc3c680101635042ce002aabadfaf7843',
        'content_hash': '143acbc0d6713ef9815870159f577f998760ee612e2d56405d59f2fc4ec134a4',
        'ans': 'B',
        'raw_ans': 'y = 0.1 sin(6t + pi/4)',
        'reasoning': [
            '1. Given m = 0.1 kg, A = 0.1 m.',
            '2. At mean position, velocity is maximum: v_max = A * omega.',
            '3. Maximum kinetic energy = 1/2 m v_max^2 = 18 * 10^-3 J.',
            '4. 1/2 * 0.1 * (0.1 * omega)^2 = 0.018 => 0.0005 * omega^2 = 0.018 => omega^2 = 36 => omega = 6 rad/s.',
            '5. Equation of SHM is y = A sin(omega*t + phi).',
            '6. With phi = 45 degrees = pi/4, y = 0.1 sin(6t + pi/4).'
        ]
    },
    {
        'atom_id': 'properties-of-solids-question-2d7d920e',
        'blind_package_hash': '5ddfc16a3fdbd4067d8f908d226324203e02d8c89b7a6bb525e7469fad0155dd',
        'content_hash': 'ac8311ce50f56ee203ac025c2b65c4a7fec09676ff7d9c4603ebeb4feab9422a',
        'ans': 'A',
        'raw_ans': 'The area of wire goes on decreasing and wire extends and breaks.',
        'reasoning': [
            '1. When the applied load increases up to breaking stress, the material passes the yield point and undergoes plastic deformation.',
            '2. During this plastic phase, particularly near the ultimate tensile strength, necking occurs.',
            '3. Necking causes the cross-sectional area of the wire to decrease rapidly as it extends further.',
            '4. Eventually, the wire breaks at this narrowed section.'
        ]
    },
    {
        'atom_id': 'laws-of-motion-question-ba0b4106',
        'blind_package_hash': '21c57352c017f717b7fa7200f76bdec418faca82346575289810f96fe2e9234c',
        'content_hash': 'ed05220acebdaf00fbb9dbf39e2a0d8441e4058a97ad7049def7d36dc0f66427',
        'ans': 'A',
        'raw_ans': 'cot alpha = 3',
        'reasoning': [
            '1. The normal force on the insect is N = mg * cos(alpha).',
            '2. The downward tangential force due to gravity is mg * sin(alpha).',
            '3. For the insect not to slip, the frictional force must balance this: mg * sin(alpha) <= mu * N.',
            '4. mg * sin(alpha) <= mu * mg * cos(alpha) => tan(alpha) <= mu.',
            '5. Given mu = 1/3, the maximum angle is when tan(alpha) = 1/3.',
            '6. Therefore, cot(alpha) = 3.'
        ]
    },
    {
        'atom_id': 'magnetism-and-matter-question-3c3af9c7',
        'blind_package_hash': '39db62574ec8bef81a53ffc7130cbdd22529fb8fdba14b2c82ba0202ee27254a',
        'content_hash': '4f75f153a39d8442a12e351b16adff316cd56e03e4bbdd92bdd30b0ca759faf3',
        'ans': 'C',
        'raw_ans': '2 s',
        'reasoning': [
            '1. Original time period T = 2*pi * sqrt(I / MB) = 2 s.',
            '2. When the magnet is cut into three equal parts along its length, each part has mass m/3 and magnetic moment M/3.',
            '3. The moment of inertia of a long bar magnet depends primarily on its length: I approx m*L^2 / 12.',
            '4. When placed on each other with like poles together, total mass is m and total magnetic moment is 3 * (M/3) = M.',
            '5. The length of the combination remains L, so the new moment of inertia I_new = m*L^2 / 12 = I.',
            '6. New time period T_new = 2*pi * sqrt(I / MB) = 2 s.'
        ]
    }
]

out_dir = 'c:/Users/Win11/OneDrive/Desktop/Rishab/jee physics master book test/verification/incoming'
output_files = []

for r in results:
    run_id = f"run-solver_a-{r['atom_id']}-{uuid.uuid4().hex[:8]}"
    filename = f"{out_dir}/solver_{r['atom_id']}_{run_id}.json"
    
    doc = {
        'solver_run_id': run_id,
        'solver_agent_name': 'solver_a',
        'atom_id': r['atom_id'],
        'atom_version': 1,
        'content_hash': r['content_hash'],
        'verification_protocol_version': '1.0.0',
        'blind_package_hash': r['blind_package_hash'],
        'independent_answer': r['ans'],
        'raw_answer': r['raw_ans'],
        'reasoning_steps': r['reasoning'],
        'assumptions_used': ['Standard physics assumptions apply'],
        'diagram_interpretation': None,
        'uncertainty': None,
        'possible_ambiguities': [],
        'created_at': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(doc, f, indent=2)
    output_files.append((filename, run_id))

print(json.dumps(output_files))
