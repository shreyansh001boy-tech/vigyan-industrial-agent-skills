---
name: robotics-kinematics-control
description: Industrial robotics kinematics and control systems solver for Denavit-Hartenberg (DH) homogeneous transforms, state-space controllability matrices, and PID controller dynamics.
---

# Robotics Kinematics & State-Space Control Skill

## 1. Domain Background
In multi-axis robotic arm design (e.g. 6-DOF industrial manipulators, SCARA robots, and robotic surgery arms), computing the exact spatial pose (position and orientation) of the end-effector from joint angles is governed by Denavit-Hartenberg (DH) parameters. In automated closed-loop actuators, state-space controllability and PID feedback loops guarantee precision trajectory tracking without oscillatory instability.

---

## 2. Governing Mathematical Laws

### 1. Denavit-Hartenberg (DH) Homogeneous Transformation
Between successive link frames $i-1$ and $i$, parameterized by $(\theta_i, d_i, a_i, \alpha_i)$:
$$T_{i-1}^{i} = \begin{bmatrix} 
\cos\theta_i & -\sin\theta_i \cos\alpha_i & \sin\theta_i \sin\alpha_i & a_i \cos\theta_i \\
\sin\theta_i & \cos\theta_i \cos\alpha_i & -\cos\theta_i \sin\alpha_i & a_i \sin\theta_i \\
0 & \sin\alpha_i & \cos\alpha_i & d_i \\
0 & 0 & 0 & 1
\end{bmatrix}$$
* Overall forward kinematics: $T_{0}^{n} = T_{0}^{1} T_{1}^{2} \cdots T_{n-1}^{n}$
* End-effector coordinates: $(x, y, z) = (T_{0}^{n}[0,3], T_{0}^{n}[1,3], T_{0}^{n}[2,3])$.

### 2. Linear State-Space Representation & Controllability
Continuous-time dynamical system:
$$\dot{\mathbf{x}}(t) = \mathbf{A} \mathbf{x}(t) + \mathbf{B} \mathbf{u}(t), \qquad \mathbf{y}(t) = \mathbf{C} \mathbf{x}(t) + \mathbf{D} \mathbf{u}(t)$$
The system of dimension $n$ is **completely controllable** if the controllability matrix $\mathcal{C}$ has full rank $n$:
$$\mathcal{C} = \begin{bmatrix} \mathbf{B} & \mathbf{A}\mathbf{B} & \mathbf{A}^2\mathbf{B} & \cdots & \mathbf{A}^{n-1}\mathbf{B} \end{bmatrix}, \qquad \text{rank}(\mathcal{C}) = n$$

### 3. PID Closed-Loop Control Law
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
* Transfer function: $C(s) = K_p + \frac{K_i}{s} + K_d s$

---

## 3. Procedural Agent Runbook
1. **Define DH Table:** Tabulate link twist $\alpha_i$, link length $a_i$, link offset $d_i$, and joint variable $\theta_i$.
2. **Compute Homogeneous Chain:** Multiply $4 \times 4$ matrices to extract final end-effector position vector $\vec{P}$ and rotation matrix $\mathbf{R}$.
3. **Verify Controllability:** Form $\mathcal{C} = [B, AB, \dots]$ and compute determinant/rank before designing pole-placement or LQR controllers.
