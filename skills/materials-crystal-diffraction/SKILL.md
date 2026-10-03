---
name: materials-crystal-diffraction
description: Industrial materials science and crystallography solver for X-ray diffraction (XRD), Bragg's law, interplanar spacing, lattice constants, and semiconductor alloy bandgap tuning.
---

# Materials Science & Crystal Diffraction Skill

## 1. Domain Background
In semiconductor epitaxy, thin-film photovoltaics, and metallurgy, characterization of crystal structures relies on X-Ray Diffraction (XRD). Measuring the diffraction angle $\theta$ for monochromatic X-rays ($\text{Cu } K_\alpha$, $\lambda = 1.5406\text{ \AA}$) enables precise determination of interplanar spacing $d_{hkl}$, lattice constant $a$, and ternary semiconductor bandgaps (e.g. $\text{In}_{x}\text{Ga}_{1-x}\text{As}$).

---

## 2. Governing Crystallographic Laws

### 1. Bragg's Law
For constructive interference from parallel crystal planes:
$$n \lambda = 2 d_{hkl} \sin\theta$$
where $n$ is diffraction order (typically 1), $\lambda$ is X-ray wavelength, and $\theta$ is the Bragg angle (half the detector angle $2\theta$).

### 2. Interplanar Spacing ($d_{hkl}$)
For a cubic crystal system (FCC, BCC, Diamond cubic):
$$d_{hkl} = \frac{a}{\sqrt{h^2 + k^2 + l^2}}$$
where $a$ is the cubic unit cell lattice parameter and $(h, k, l)$ are Miller indices.

### 3. Vegard's Law & Bandgap Bowing
For ternary pseudobinary semiconductor alloys $A_{1-x}B_x C$:
* **Lattice Constant:**
  $$a(x) = (1 - x) a_{AC} + x a_{BC}$$
* **Direct Bandgap with Bowing Parameter $b$:**
  $$E_g(x) = (1 - x) E_{g, AC} + x E_{g, BC} - b \cdot x(1 - x)$$

### 4. Theoretical Density of Crystal
$$\rho = \frac{n \cdot M}{N_A \cdot V_C} = \frac{n \cdot M}{N_A \cdot a^3}$$
where $n$ is number of atoms per unit cell ($n=2$ for BCC, $n=4$ for FCC), $M$ is molar mass, $N_A = 6.022 \times 10^{23}\text{ mol}^{-1}$, and $V_C$ is cell volume.

---

## 3. Procedural Agent Runbook
1. **Convert Detector Angle:** Extract Bragg angle $\theta = (2\theta) / 2$.
2. **Compute $d$-spacing:** Apply Bragg's Law with X-ray wavelength $\lambda$.
3. **Determine Lattice Parameter:** Multiply $d_{hkl}$ by $\sqrt{h^2 + k^2 + l^2}$.
4. **Semiconductor Tuning:** Apply Vegard's law to size substrate lattice matching and target emission bandgap $E_g$.
