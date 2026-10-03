---
name: vlsi-cmos-timing-closure
description: Industrial semiconductor VLSI analysis for CMOS timing closure, Elmore RC propagation delay, dynamic power dissipation, and subthreshold leakage modeling.
---

# VLSI CMOS Timing Closure & Leakage Power Skill

## 1. Domain Background
In deep submicron and FinFET digital integrated circuit design (from 65nm planar to 3nm GAA), achieving timing closure without violating power envelopes is a central engineering challenge. 
Static timing analysis (STA) determines whether a digital circuit operates reliably at the target clock frequency $f_{clk}$ by evaluating setup and hold time slacks across all flip-flop data paths.

---

## 2. Governing Physical & Mathematical Laws

### 1. Elmore Delay Approximation
For an RC ladder network with $N$ segments, the signal propagation delay $\tau$ is:
$$\tau_{\text{Elmore}} = \sum_{k=1}^{N} R_{k} \left(\sum_{j=k}^{N} C_{j}\right)$$

### 2. Setup & Hold Time Slack Formulation
To prevent metastability:
$$\text{Slack}_{\text{setup}} = T_{\text{clk}} - (T_{\text{cq}} + T_{\text{comb}} + T_{\text{setup}}) + T_{\text{skew}}$$
$$\text{Slack}_{\text{hold}} = (T_{\text{cq}} + T_{\text{comb}}) - T_{\text{hold}} - T_{\text{skew}}$$
* Violation condition: $\text{Slack} < 0$.

### 3. Dynamic Switching Power
$$P_{\text{dyn}} = \alpha \cdot C_L \cdot V_{DD}^2 \cdot f_{\text{clk}}$$
where $\alpha$ is switching activity factor, $C_L$ is capacitive load, and $V_{DD}$ is supply voltage.

### 4. Subthreshold Leakage Current
$$I_{\text{sub}} = \mu_0 C_{\text{ox}} \left(\frac{W}{L}\right) v_t^2 (n - 1) \exp\left(\frac{V_{GS} - V_{\text{th}}}{n v_t}\right) \left(1 - \exp\left(-\frac{V_{DS}}{v_t}\right)\right)$$
where $v_t = \frac{k_B T}{q} \approx 25.86\text{ mV}$ at 300 K.

---

## 3. Procedural Agent Runbook

When analyzing CMOS logic paths:
1. **Extract Timing Constraints:** Identify clock period $T_{clk} = 1/f_{clk}$, flip-flop $T_{cq}$, $T_{setup}$, $T_{hold}$, and intentional clock skew $T_{skew}$.
2. **Compute Wire & Gate Delay:** Evaluate combinatorial RC delay via Elmore or standard cell library lookup.
3. **Verify Slack Margins:** Check if $\text{Slack}_{setup} \ge 0$ and $\text{Slack}_{hold} \ge 0$.
4. **Compute Power Budget:** Calculate dynamic switching power $P_{dyn}$ and static leakage $P_{leak} = I_{sub} \cdot V_{DD}$.
5. **Mitigation Recommendations:**
   - If setup violated: Upsize drivers, insert repeaters, or reduce threshold voltage ($V_{th}$).
   - If hold violated: Insert delay buffers near capturing flop (hold is frequency-independent).
