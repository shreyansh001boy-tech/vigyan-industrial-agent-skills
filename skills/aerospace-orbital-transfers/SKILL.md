---
name: aerospace-orbital-transfers
description: Industrial astrodynamics and aerospace engineering solver for Keplerian orbital mechanics, Vis-Viva calculations, Hohmann transfer delta-v, and rocket staging mass fractions.
---

# Aerospace & Orbital Mechanics Skill

## 1. Domain Background
Orbital trajectory design and launch vehicle sizing require deterministic solutions to the two-body Kepler problem and the Tsiolkovsky rocket equation. Precision in velocity changes ($\Delta v$) dictates propellant mass, payload capacity, and launch window feasibility for satellites transitioning from Low Earth Orbit (LEO) to Geostationary Transfer Orbit (GTO) or interplanetary trajectories.

---

## 2. Governing Physical Laws

### 1. Vis-Viva Equation
The orbital speed $v$ at distance $r$ from the central body with gravitational parameter $\mu = GM$:
$$v = \sqrt{\mu \left(\frac{2}{r} - \frac{1}{a}\right)}$$
* For circular orbit ($r = a$): $v_{\text{circ}} = \sqrt{\frac{\mu}{r}}$
* Parabolic escape trajectory ($a \to \infty$): $v_{\text{esc}} = \sqrt{\frac{2\mu}{r}}$

### 2. Hohmann Transfer Orbit
To transfer between two coplanar circular orbits of radius $r_1$ and $r_2$:
* Semi-major axis of transfer ellipse: $a_{\text{tx}} = \frac{r_1 + r_2}{2}$
* First impulse (periapsis burn):
  $$\Delta v_1 = \sqrt{\frac{\mu}{r_1}} \left( \sqrt{\frac{2 r_2}{r_1 + r_2}} - 1 \right)$$
* Second impulse (apoapsis burn):
  $$\Delta v_2 = \sqrt{\frac{\mu}{r_2}} \left( 1 - \sqrt{\frac{2 r_1}{r_1 + r_2}} \right)$$
* Total mission velocity budget: $\Delta v_{\text{total}} = |\Delta v_1| + |\Delta v_2|$
* Transfer time: $t_{\text{tx}} = \pi \sqrt{\frac{a_{\text{tx}}^3}{\mu}}$

### 3. Tsiolkovsky Rocket Staging
$$\Delta v = I_{\text{sp}} g_0 \ln\left(\frac{m_0}{m_f}\right) \implies m_0 = m_f \exp\left(\frac{\Delta v}{I_{\text{sp}} g_0}\right)$$
where $g_0 = 9.80665\text{ m/s}^2$ and $I_{\text{sp}}$ is specific impulse in seconds.

---

## 3. Standard Planetary Parameters
* Earth $\mu = 3.986004418 \times 10^{14}\text{ m}^3/\text{s}^2$
* Earth mean radius $R_E = 6,371,000\text{ m}$
* Low Earth Orbit (LEO) altitude: $\sim 300\text{ km} \implies r_1 = 6,671,000\text{ m}$
* Geostationary Orbit (GEO) radius: $r_2 = 42,164,000\text{ m}$

---

## 4. Procedural Agent Runbook
1. **Identify Central Body & Radii:** Convert altitudes $h$ to orbital radii $r = R_E + h$.
2. **Compute Circular Velocities:** Calculate $v_1$ and $v_2$.
3. **Solve Transfer Ellipse:** Compute $a_{tx}$, $\Delta v_1$, $\Delta v_2$, and transfer time $t_{tx}$.
4. **Propellant Sizing:** Apply Tsiolkovsky equation to determine wet-to-dry mass ratio $m_0 / m_f$.
