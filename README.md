# Vigyan Industrial STEM Agent Skills Repository

> **A sovereign, industrial-grade engineering skills vault codifying exact mathematical models, deterministic Python solvers, and agentic runbooks across 8 major STEM engineering domains.**

Designed for direct autonomous ingestion into the **Vigyan Agentic Hub** and native tool calling across the **Vigyan-2B, Vigyan-7B, and Vigyan-32B** foundation models.

---

## 🏛️ Master Domain Catalog (8 Industrial Tracks)

| Track | Domain & Skill Name | Governing Physical Laws | Key Capabilities |
| :---: | :--- | :--- | :--- |
| **01** | [**`vlsi-cmos-timing-closure`**](skills/vlsi-cmos-timing-closure/SKILL.md) | Elmore RC Delay, Static Timing Analysis, Subthreshold Leakage | Setup/Hold slack calculation, max clock frequency, dynamic switching vs static power dissipation. |
| **02** | [**`aerospace-orbital-transfers`**](skills/aerospace-orbital-transfers/SKILL.md) | Vis-Viva Equation, Hohmann Transfer, Tsiolkovsky Staging | Coplanar orbital transfers, mission $\Delta v$ budgeting, transfer times, rocket propellant mass fraction sizing. |
| **03** | [**`power-grid-fault-analysis`**](skills/power-grid-fault-analysis/SKILL.md) | Fortescue Symmetrical Components, Per-Unit Impedance | 3-Phase balanced, Single Line-to-Ground (SLG), Line-to-Line fault currents, base impedance normalization. |
| **04** | [**`robotics-kinematics-control`**](skills/robotics-kinematics-control/SKILL.md) | Denavit-Hartenberg (DH) Transforms, State-Space Controllability | Multi-DOF forward kinematics, end-effector spatial poses, Kalman/PID closed-loop controllability verification. |
| **05** | [**`chemical-reactor-thermo`**](skills/chemical-reactor-thermo/SKILL.md) | Arrhenius Kinetics, CSTR & PFR Mass Balances, Antoine Equation | Ideal reactor sizing, space-time residence distributions, first-order conversion kinetics, saturation vapor pressure. |
| **06** | [**`mechanical-fea-stress-tensors`**](skills/mechanical-fea-stress-tensors/SKILL.md) | 3D Cauchy Stress Tensor, von Mises Yield Criterion, Beam Elasticity | Principal stress eigenvalues ($\sigma_1, \sigma_2, \sigma_3$), factor of safety (FoS), cantilever deflection & bending moments. |
| **07** | [**`materials-crystal-diffraction`**](skills/materials-crystal-diffraction/SKILL.md) | Bragg's X-Ray Diffraction ($n\lambda = 2d\sin\theta$), Vegard's Law | Interplanar $d$-spacings, cubic lattice parameters, semiconductor alloy bandgap and emission wavelength tuning. |
| **08** | [**`biomedical-signal-filtering`**](skills/biomedical-signal-filtering/SKILL.md) | Butterworth Digital Bandpass, Signal-to-Noise Ratio (SNR) | ECG/EEG baseline wander & 50/60 Hz powerline hum removal, R-peak detection, mean heart rate (BPM) & HRV metrics. |

---

## 🛠️ Architecture: The Three-Tier Production Standard

Every individual skill in this repository is built to an industrial standard:

```text
skills/<domain-skill-name>/
├── SKILL.md              # Antigravity/AGY compatible runbook, mathematical formulations & background
└── scripts/
    └── solver.py         # Production-grade deterministic Python solver class with verified self-tests
```

1. **`SKILL.md` (Agent Prompt & Procedural Runbook):**
   - Standard YAML frontmatter for progressive agent discovery.
   - Comprehensive LaTeX physical laws and parameter bounds.
   - Exact diagnostic procedures and mitigation strategies.
2. **`scripts/solver.py` (Deterministic Calculation Engine):**
   - Zero hallucination: Exact symbolic and floating-point computation using NumPy, SciPy, and SymPy.
   - Self-contained test suite in `__main__` asserting against real-world industrial benchmarks (e.g. 28nm FinFETs, LEO-GEO orbits, Silicon XRD angles).

---

## 🔄 Vigyan Agentic Hub Integration

An automated bridge script connects this repository directly into the **Vigyan Agentic Hub**:

```bash
python3 scripts/ingest_skills_to_hub.py --hub-dir /path/to/vigyan-agentic-hub
```

### What Ingestion Executes:
1. **Axiom Extraction:** Extracts physical equations and seeds them into the embedded **C++ KùzuDB GraphRAG** database.
2. **Semantic Indexing:** Chunks and indexes the procedural runbooks into **LanceDB v4** for sub-15ms vector retrieval.
3. **Tool Dispatch Registry:** Registers all 8 `solver.py` engines as native callable tools within the `VigyanNativeAgent`, allowing the **Vigyan-2B, 7B, and 32B** models to invoke exact calculations without parameter drift.

---

## 🧪 Verifying All Solvers

Run automated verification across all 8 industrial solvers:

```bash
for solver in skills/*/scripts/solver.py; do
    echo "Testing $solver..."
    python3 "$solver"
done
```

---

## 📜 License & Sovereign Attribution

All industrial skills, specifications, runbooks, and numerical solvers in this repository are released under the **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)** license.

- **Permitted Use:** University coursework, academic research, educational robotics/engineering projects, and personal non-commercial exploration.
- **Commercial Restrictions:** Enterprise integration, defense contractor use, commercial tutoring or industrial automation SaaS requires an explicit commercial license.
- **Founder & Chief Architect:** [Shreyansh Singh](https://github.com/shreyansh001boy-tech)
- **Organization:** Vigyan AI / [ExperimentLab.in](https://experimentlab.in)
