---
name: mechanical-fea-stress-tensors
description: Industrial mechanical structural analysis and FEA solver for 3D Cauchy stress tensors, von Mises yield criteria, principal stresses, and Euler-Bernoulli beam deflections.
---

# Mechanical FEA Stress Tensors & Yield Criteria Skill

## 1. Domain Background
In mechanical structural engineering, aerospace airframe design, and finite element analysis (FEA), multi-axial stress states dictate material failure. Under complex combined loading (tension, bending, torsion), isotropic ductile materials yield according to the octahedral shear stress or von Mises energy-distortion criterion rather than simple uni-axial stress.

---

## 2. Governing Solid Mechanics Laws

### 1. 3D Cauchy Stress Tensor
A general symmetric state of stress at any point:
$$\boldsymbol{\sigma} = \begin{bmatrix}
\sigma_{xx} & \tau_{xy} & \tau_{xz} \\
\tau_{xy} & \sigma_{yy} & \tau_{yz} \\
\tau_{xz} & \tau_{yz} & \sigma_{zz}
\end{bmatrix}$$

### 2. Principal Stresses ($\sigma_1 \ge \sigma_2 \ge \sigma_3$)
The principal stresses are the eigenvalues of $\boldsymbol{\sigma}$, satisfying the characteristic equation:
$$\det(\boldsymbol{\sigma} - \lambda \mathbf{I}) = 0 \implies \lambda^3 - I_1 \lambda^2 + I_2 \lambda - I_3 = 0$$
where stress invariants are:
* $I_1 = \text{tr}(\boldsymbol{\sigma}) = \sigma_{xx} + \sigma_{yy} + \sigma_{zz}$
* $I_2 = \sigma_{xx}\sigma_{yy} + \sigma_{yy}\sigma_{zz} + \sigma_{zz}\sigma_{xx} - \tau_{xy}^2 - \tau_{yz}^2 - \tau_{xz}^2$
* $I_3 = \det(\boldsymbol{\sigma})$

### 3. von Mises Equivalent Stress ($\sigma_v$)
$$\sigma_v = \sqrt{\frac{1}{2} \left[ (\sigma_{xx} - \sigma_{yy})^2 + (\sigma_{yy} - \sigma_{zz})^2 + (\sigma_{zz} - \sigma_{xx})^2 + 6(\tau_{xy}^2 + \tau_{yz}^2 + \tau_{xz}^2) \right]}$$
Alternatively expressed in principal stresses:
$$\sigma_v = \sqrt{\frac{1}{2} \left[ (\sigma_1 - \sigma_2)^2 + (\sigma_2 - \sigma_3)^2 + (\sigma_3 - \sigma_1)^2 \right]}$$
* **Factor of Safety (FoS):** $\text{FoS} = \frac{\sigma_{\text{yield}}}{\sigma_v}$. Yielding occurs when $\text{FoS} < 1.0$.

### 4. Euler-Bernoulli Cantilever Deflection
For a cantilever beam of length $L$, Young's modulus $E$, and second moment of area $I$ subjected to end load $P$:
$$\delta_{\max} = \frac{P L^3}{3 E I}, \qquad \sigma_{\max} = \frac{M_{\max} c}{I} = \frac{P L c}{I}$$

---

## 3. Procedural Agent Runbook
1. **Construct Stress Tensor:** Populate normal and shear stress components from FEA element output.
2. **Compute von Mises & Principals:** Calculate eigenvalues and $\sigma_v$.
3. **Evaluate Factor of Safety:** Compare against material yield strength $\sigma_y$ (e.g. Structural Steel A36 $\sigma_y = 250\text{ MPa}$, Ti-6Al-4V $\sigma_y = 880\text{ MPa}$).
