---
name: power-grid-fault-analysis
description: Industrial electrical power engineering solver for 3-phase symmetrical and unsymmetrical fault analysis, Fortescue symmetrical components, per-unit impedances, and transformer sizing.
---

# Electrical Power Grid Fault Analysis Skill

## 1. Domain Background
In high-voltage transmission networks, microgrids, and industrial distribution systems, sizing switchgear and setting protective relays requires calculating fault currents under short-circuit conditions. 
Fortescue's symmetrical components decompose unbalanced three-phase currents into positive ($I_1$), negative ($I_2$), and zero ($I_0$) sequence components.

---

## 2. Governing Electrical Laws

### 1. Per-Unit Impedance Normalization
Given three-phase base power $S_{\text{base}}$ (MVA) and line-to-line base voltage $V_{\text{base}}$ (kV):
$$Z_{\text{base}} = \frac{V_{\text{base}}^2}{S_{\text{base}}}\quad (\Omega), \qquad I_{\text{base}} = \frac{S_{\text{base}}}{\sqrt{3} V_{\text{base}}}\quad (\text{kA})$$
Changing base impedance:
$$Z_{\text{pu, new}} = Z_{\text{pu, old}} \cdot \left(\frac{V_{\text{base, old}}}{V_{\text{base, new}}}\right)^2 \cdot \left(\frac{S_{\text{base, new}}}{S_{\text{base, old}}}\right)$$

### 2. Symmetrical Components (Fortescue Transformation)
Let operator $a = e^{j 120^\circ} = -\frac{1}{2} + j \frac{\sqrt{3}}{2}$:
$$\begin{bmatrix} I_0 \\ I_1 \\ I_2 \end{bmatrix} = \frac{1}{3} \begin{bmatrix} 1 & 1 & 1 \\ 1 & a & a^2 \\ 1 & a^2 & a \end{bmatrix} \begin{bmatrix} I_a \\ I_b \\ I_c \end{bmatrix}$$

### 3. Fault Current Formulations (Subtransient State)
With pre-fault phase voltage $E_a \approx 1.0\text{ pu}$ and fault impedance $Z_f$:
* **Balanced Three-Phase Fault ($3\Phi$):**
  $$I_f^{(3\Phi)} = \frac{E_a}{Z_1 + Z_f}$$
* **Single Line-to-Ground Fault (SLG):**
  $$I_f^{(\text{SLG})} = 3 I_{a0} = \frac{3 E_a}{Z_0 + Z_1 + Z_2 + 3 Z_f}$$
* **Line-to-Line Fault (L-L):**
  $$I_f^{(\text{L-L})} = \frac{-j \sqrt{3} E_a}{Z_1 + Z_2 + Z_f}$$

---

## 3. Procedural Agent Runbook
1. **Convert to Common Base:** Convert all generators, transformers, and lines to common $S_{\text{base}} = 100\text{ MVA}$.
2. **Build Sequence Networks:** Determine Thevenin positive ($Z_1$), negative ($Z_2$), and zero ($Z_0$) sequence impedances at the fault bus.
3. **Select Fault Type:** Apply the appropriate fault formula.
4. **Convert Back to Physical Units:** Multiply per-unit fault current by $I_{\text{base}}$ to obtain physical Amperes (kA) for circuit breaker ratings.
