import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ss2tf, lti, step

# Given longitudinal model
A = np.array([[-0.0558, -0.9968,  0.0802, 0.0415],
              [ 0.5980, -0.1150, -0.0318, 0    ],
              [-3.0500,  0.3880, -0.4650, 0    ],
              [ 0,       0.0805,  1.0000, 0    ]])
B = np.array([[ 0.0073],
              [-0.4750],
              [ 0.1530],
              [ 0      ]])
C = np.array([[1, 0, 0, 0],
              [0, 1, 0, 0]])
D = np.zeros((2,1))

# Augment angle filter and actuator dynamics
tau_act = 0.1
tau_alpha = 0.05
A_aug = np.block([
    [A,           B,                np.zeros((4,1))],
    [np.zeros((1,4)), -1/tau_act,   0             ],
    [C[0],        np.zeros((1,1)), -1/tau_alpha  ]
])
B_aug = np.vstack([np.zeros((4,1)), 1/tau_act, 0])
C_aug = np.hstack([C, np.zeros((2,2))])
D_aug = np.zeros((2,1))

# Root locus for angle feedback (alpha filter state index 5)
K_vals = np.linspace(0, 100, 500)
eig_vals_alpha = [np.linalg.eigvals(A_aug - B_aug @ (K * np.array([[0,0,0,0,0,1]]))) for K in K_vals]

plt.figure()
for eigs in eig_vals_alpha:
    plt.scatter(np.real(eigs), np.imag(eigs), s=1)
plt.title('Root Locus for Angle Feedback (alpha)')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True)

# Choose K_alpha
K_alpha = 20
A_cl_alpha = A_aug - B_aug @ (K_alpha * np.array([[0,0,0,0,0,1]]))

# Root locus for rate feedback (q state index 1)
eig_vals_q = [np.linalg.eigvals(A_cl_alpha - B_aug @ (K * np.array([[0,1,0,0,0,0]]))) for K in K_vals]
plt.figure()
for eigs in eig_vals_q:
    plt.scatter(np.real(eigs), np.imag(eigs), s=1)
plt.title('Root Locus for Pitch-Rate Feedback (q)')
plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.grid(True)

# Combined feedback gains
K_q = 5
feedback_matrix = K_alpha * np.array([[0,0,0,0,0,1]]) + K_q * np.array([[0,1,0,0,0,0]])
A_cl = A_aug - B_aug @ feedback_matrix

# Transfer functions: angle output
num_no, den_no = ss2tf(A, B, C[0:1], D[0:1])
sys_no = lti(num_no[0], den_no)
num_sas, den_sas = ss2tf(A_cl, B_aug, C_aug[0:1], D_aug[0:1])
sys_sas = lti(num_sas[0], den_sas)

# Step responses
t = np.linspace(0, 5, 500)
t1, y1 = step(sys_no, T=t)
t2, y2 = step(sys_sas, T=t)

plt.figure()
plt.plot(t1, y1, label='No SAS')
plt.plot(t2, y2, linestyle='--', label='With SAS')
plt.title('Step Response Comparison (Angle)')
plt.xlabel('Time (s)')
plt.ylabel('Angle (deg)')
plt.legend()
plt.grid(True)

plt.show()
