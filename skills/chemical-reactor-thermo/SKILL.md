---
name: chemical-reactor-thermo
description: Industrial chemical reaction engineering solver for CSTR and PFR reactor sizing, Arrhenius reaction kinetics, residence time distributions, and vapor-liquid equilibrium.
---

# Chemical Reactor Sizing & Thermodynamics Skill

## 1. Domain Background
In chemical synthesis, petrochemical refining, and pharmaceutical manufacturing, reactor design dictates product yield, conversion efficiency, and thermal stability. Continuous Stirred-Tank Reactors (CSTR) and Plug Flow Reactors (PFR) exhibit distinct residence time and concentration profiles governed by fundamental mass and energy conservation balances.

---

## 2. Governing Chemical Engineering Laws

### 1. Arrhenius Kinetic Law
Reaction rate constant $k$ as a function of absolute temperature $T$ (Kelvin):
$$k(T) = A \exp\left(-\frac{E_a}{R T}\right)$$
where $A$ is the pre-exponential frequency factor, $E_a$ is activation energy ($\text{J/mol}$), and $R = 8.314\text{ J/(mol}\cdot\text{K)}$.

### 2. CSTR Design Equation (Ideal Backmixed Flow)
For steady-state isothermal CSTR with feed molar flow rate $F_{A0}$, volumetric flow rate $v_0$, and conversion $X$:
$$V = \frac{F_{A0} X}{-r_A}$$
* Space time (residence time): $\tau = \frac{V}{v_0} = \frac{C_{A0} X}{-r_A}$
* For a first-order irreversible reaction ($-r_A = k C_A = k C_{A0} (1 - X)$):
  $$\tau = \frac{X}{k (1 - X)} \implies X = \frac{k \tau}{1 + k \tau}$$

### 3. PFR Design Equation (Ideal Plug Flow)
$$V = F_{A0} \int_0^X \frac{dX}{-r_A}$$
* For first-order reaction:
  $$\tau = \frac{V}{v_0} = \frac{1}{k} \ln\left(\frac{1}{1 - X}\right) \implies X = 1 - \exp(-k \tau)$$

### 4. Raoult's Law & Antoine Vapor Pressure
For ideal vapor-liquid equilibrium:
$$y_i P_{\text{total}} = x_i P_i^*(T)$$
where pure component saturation pressure $P_i^*(T)$ is computed via Antoine equation:
$$\log_{10}(P_i^*) = A_i - \frac{B_i}{T + C_i}$$

---

## 3. Procedural Agent Runbook
1. **Determine Rate Constant $k$:** Evaluate $k(T)$ at operating temperature via Arrhenius equation.
2. **Select Reactor Model:** Use CSTR for well-mixed liquid systems or PFR for high-velocity tubular gas/liquid reactions.
3. **Compute Volume / Residence Time:** Given target fractional conversion $X$, calculate required reactor volume $V$.
4. **Compare Efficiencies:** Note that for positive-order kinetics, $V_{\text{CSTR}} > V_{\text{PFR}}$ for identical conversion.
