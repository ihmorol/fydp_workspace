# FYDP-I: RK4 and SciPy Solver Educational Guide

**Purpose**: A clear guide to understanding the numerical methods used in our Lorenz-1960 baseline implementation.

**Last Updated**: April 4, 2026

---

## Table of Contents

1. [Understanding ODEs](#1-understanding-odes)
2. [Euler's Method: The Foundation](#2-eulers-method-the-foundation)
3. [Runge-Kutta 4th Order (RK4)](#3-runge-kutta-4th-order-rk4)
4. [SciPy's DOP853 Solver](#4-scipys-dop853-solver)
5. [Understanding Error Metrics](#5-understanding-error-metrics)
6. [Understanding the Trajectory](#6-understanding-the-trajectory)
7. [Interpreting Our Results](#7-interpreting-our-results)
8. [Visualization Guide](#8-visualization-guide)
9. [Practical Implications for FYDP](#9-practical-implications-for-fydp)
10. [Lorenz-1960 vs Lorenz-1963](#10-lorenz-1960-vs-lorenz-1963)
11. [Quick Reference](#11-quick-reference)

---

## 1. Understanding ODEs

### What is an ODE?

An **Ordinary Differential Equation (ODE)** describes how a quantity changes based on its current state. The Lorenz-1960 system is:

```
dx/dt = -0.1·y·z
dy/dt =  1.6·x·z
dz/dt = -0.75·x·y
```

**Simple explanation**: "At any moment, how fast x changes depends on the current values of y and z."

### Why Numerical Methods?

Most ODEs (including ours) have **no closed-form solution**—we can't write `x(t) = formula(t)`. Instead, we use **numerical methods**: step-by-step approximations that march forward in time.

---

## 2. Euler's Method: The Foundation

### The Core Idea

If you know:
- Current position: `y(t)`
- Current rate of change: `dy/dt = f(t, y)`
- Time step: `h`

Then:
```
y(t + h) ≈ y(t) + h·f(t, y)
```

**Analogy**: Driving at 60 mph, after 1 hour you'll travel 60 miles.

### The Problem with Euler

Euler assumes the slope stays constant over the entire step. For curves, this creates error.

```
Position
    |
    |     Euler follows the tangent line
    |    ↗
    |   /  ← tangent at current point
    |  /
    | /
    |/_________ Time
     t    t+h
```

### Euler's Code

```python
def euler_step(f, t, y, h):
    """Single step of Euler's method."""
    slope = f(t, y)           # current slope
    return y + h * slope      # move along tangent
```

### Accuracy: 1st Order

Euler is **1st-order accurate**: error ∝ h¹

| Step Size (h) | Error | Halve h → error... |
|---------------|-------|---------------------|
| 0.01          | ~0.01 | — |
| 0.005         | ~0.005| ÷ 2 |
| 0.0025        | ~0.0025| ÷ 2 |

**Problem**: To get 10× better accuracy, you need 10× more steps. **Inefficient!**

---

## 3. Runge-Kutta 4th Order (RK4)

### The Big Idea

Instead of **one slope**, RK4 uses **four carefully chosen slopes** and combines them with a weighted average.

**Analogy**: 
- Euler asks: "Where am I heading right now?"
- RK4 asks four questions:
  1. "Where am I heading now?" (k₁)
  2. "Where will I be heading at the midpoint?" (k₂)
  3. "Let me check again with better info" (k₃)
  4. "Where will I be at the end?" (k₄)

Then combines them intelligently.

### RK4 Algorithm

```python
# Step 1: Slope at the beginning
k₁ = f(tₙ, yₙ)

# Step 2: Slope at midpoint, using k₁
k₂ = f(tₙ + h/2, yₙ + (h/2)·k₁)

# Step 3: Slope at midpoint, using k₂ (better estimate)
k₃ = f(tₙ + h/2, yₙ + (h/2)·k₂)

# Step 4: Slope at the end
k₄ = f(tₙ + h, yₙ + h·k₃)

# Final update: weighted average
yₙ₊₁ = yₙ + (h/6)·(k₁ + 2k₂ + 2k₃ + k₄)
```

### Why These Weights? (1 : 2 : 2 : 1)

The weights come from **Simpson's Rule** for numerical integration:

```
∫f(x)dx ≈ (h/6)[f(a) + 4f((a+b)/2) + f(b)]
```

- k₁ = f(a) → weight 1
- k₂, k₃ = midpoint estimates → combined weight 4
- k₄ = f(b) → weight 1

This minimizes truncation error and achieves **4th-order accuracy**.

### What "4th Order" Means

**Order of accuracy** = how fast error decreases as step size shrinks.

| Method | Error | At h=0.001 | Halve step → error... |
|--------|-------|------------|----------------------|
| Euler | O(h¹) | ~10⁻³ | ÷ 2 |
| RK2 | O(h²) | ~10⁻⁶ | ÷ 4 |
| **RK4** | **O(h⁴)** | **~10⁻¹²** | **÷ 16** |

**Key insight**: RK4 error ∝ h⁴

- If h = 0.001: Error ~ (0.001)⁴ = 10⁻¹²
- If h = 0.0005: Error ~ (0.0005)⁴ = 6.25 × 10⁻¹⁴ (16× smaller!)

### Our Implementation

```python
def rk4_step(f, t, y, h):
    """Single step of 4th-order Runge-Kutta."""
    k1 = f(t, y)
    k2 = f(t + 0.5*h, y + 0.5*h*k1)
    k3 = f(t + 0.5*h, y + 0.5*h*k2)
    k4 = f(t + h, y + h*k3)
    return y + (h/6.0) * (k1 + 2*k2 + 2*k3 + k4)


def rk4_solve(f, t_span, y0, h):
    """
    Solve ODE using fixed-step RK4.
    
    Parameters
    ----------
    f : callable - Right-hand side function f(t, y)
    t_span : tuple - (t_start, t_end)
    y0 : array-like - Initial condition
    h : float - Step size (fixed)
    """
    t_start, t_end = t_span
    n_steps = int(round((t_end - t_start) / h))
    
    t_array = np.linspace(t_start, t_end, n_steps + 1)
    y_array = np.zeros((n_steps + 1, len(y0)))
    y_array[0] = np.asarray(y0, dtype=float)
    
    for i in range(n_steps):
        y_array[i + 1] = rk4_step(f, t_array[i], y_array[i], h)
    
    return t_array, y_array
```

### When to Use RK4

**Pros**:
- ✅ Simple to understand and implement
- ✅ Fast for smooth problems
- ✅ Predictable behavior
- ✅ Good accuracy for moderate step sizes

**Cons**:
- ❌ Fixed step (can't adapt to problem difficulty)
- ❌ Not suitable for stiff problems
- ❌ Lower order than modern methods

---

## 4. SciPy's DOP853 Solver

### What is DOP853?

**DOP853** = **D**ormand-**P**rince **8**(5)**3**

- **Dormand-Prince**: The mathematicians who developed it
- **8**: 8th-order method (higher than RK4's 4th)
- **5**: 5th-order error estimator
- **3**: 3rd-order dense output

### Fixed vs Adaptive Step

| Feature | RK4 | DOP853 |
|---------|-----|--------|
| Step size | **Fixed** (h=0.001) | **Adaptive** (changes dynamically) |
| Order | 4th | 8th |
| Error control | None built-in | Built-in with tolerances |
| Function evaluations | 4000 total | ~62 for our problem |

### How Adaptive Stepping Works

**The Problem**: Some regions need small steps (rapid changes), others allow large steps (smooth behavior). Fixed steps waste computation or miss detail.

**Adaptive Solution**:
```
1. Take a step with current h
2. Estimate the error
3. If error < tolerance: 
   - Accept step
   - INCREASE next step size
4. If error > tolerance:
   - REJECT step
   - DECREASE step size
   - Retry with smaller h
```

### Error Estimation

DOP853 computes **two solutions** simultaneously:
- **8th-order solution** (primary, more accurate)
- **5th-order solution** (for error checking)

```python
error_estimate = |y_8th_order - y_5th_order|
```

The difference estimates the error because the 5th-order solution has larger error.

### Parameters Explained

#### `rtol = 1e-10` (Relative Tolerance)

```python
acceptable_error = rtol × |y|
```

Ensures: `|actual_error| ≤ rtol × |current_solution|`

- If y ≈ 1.0: Max error = 10⁻¹⁰ × 1.0 = 10⁻¹⁰
- If y ≈ 0.001: Max error = 10⁻¹⁰ × 0.001 = 10⁻¹³

**Why relative?** Error scales with solution magnitude.

#### `atol = 1e-12` (Absolute Tolerance)

A floor for error tolerance:
```python
acceptable_error = max(atol, rtol × |y|)
```

When y ≈ 0, `rtol × |y|` would be 0, so `atol` kicks in.

### DOP853 Implementation

```python
from scipy.integrate import solve_ivp

def scipy_solve(f, t_span, y0, t_eval):
    """Solve ODE using SciPy's high-accuracy DOP853."""
    sol = solve_ivp(
        f,
        t_span,
        y0,
        method='DOP853',
        t_eval=t_eval,
        rtol=1e-10,
        atol=1e-12
    )
    
    if not sol.success:
        raise RuntimeError(f"Solver failed: {sol.message}")
    
    return sol.t, sol.y.T
```

### When to Use DOP853

**Pros**:
- ✅ Very high accuracy (8th order)
- ✅ Automatic step size adjustment
- ✅ Built-in error control
- ✅ Efficient (fewer function evaluations)

**Cons**:
- ❌ More complex to understand
- ❌ Black box (less transparent)
- ❌ Can be slower for simple problems
- ❌ May struggle with stiff problems

---

## 5. Understanding Error Metrics

### Our Results

```
MSE:  1.82 × 10⁻²²
RMSE: 1.35 × 10⁻¹¹  
Max Error: 6.06 × 10⁻¹¹
```

### Step-by-Step Calculation

#### Step 1: Both Solvers at 1001 Time Points

```python
t = [0.000, 0.001, ..., 1.000]  # 1001 points

# RK4 solution (shape: 1001 × 3)
sol_rk4 = [
    [0.500000, 0.750000, 1.000000],  # t=0.000
    [0.499825, 0.752341, 0.999625],  # t=0.001
    ...
]

# SciPy solution at same points
sol_scipy = [
    [0.500000, 0.750000, 1.000000],  # t=0.000
    [0.499825, 0.752341, 0.999625],  # t=0.001 (tiny differences!)
    ...
]
```

#### Step 2: Compute Error

```python
error = sol_rk4 - sol_scipy  # element-wise

# Example at t=0.5:
error[500] = [1.23×10⁻¹², 4.56×10⁻¹², 2.34×10⁻¹²]
```

#### Step 3: Square Errors

```python
squared_error = error²

# At t=0.5:
# (1.23×10⁻¹²)² = 1.51×10⁻²⁴
# (4.56×10⁻¹²)² = 2.08×10⁻²³
# (2.34×10⁻¹²)² = 5.48×10⁻²⁴
```

#### Step 4: Average (MSE)

```python
# Average across 1001 points × 3 variables = 3003 measurements
MSE = (1/3003) × Σ(all squared errors) = 1.82 × 10⁻²²
```

#### Step 5: Square Root (RMSE)

```python
RMSE = √MSE = √(1.82 × 10⁻²²) = 1.35 × 10⁻¹¹
```

**Interpretation**: On average, RK4 differs from SciPy by ~10⁻¹¹.

#### Step 6: Maximum Error

```python
Max_Error = max(abs(error)) = 6.06 × 10⁻¹¹
```

**Interpretation**: At the worst point, solutions differ by 6×10⁻¹¹.

### Why Are These Numbers So Small?

**Machine epsilon** (smallest difference in double precision): ε ≈ 2.22 × 10⁻¹⁶

Our error (~10⁻¹¹) is near machine epsilon because:
- RK4 with h=0.001 has truncation error ~10⁻¹²
- DOP853 has even smaller error
- We're near the limit of double precision

---

## 6. Understanding the Trajectory

### Common Question

**Q**: "If the final outcome is one point, why do we have 1001 points?"

**A**: We visualize the **entire journey**, not just the destination!

### The Trajectory Concept

Think of tracking a particle moving through space over time:

```
Time (t)    Position (x, y, z)
--------    ------------------
0.000       (0.500, 0.750, 1.000)  ← Start
0.001       (0.499, 0.752, 0.999)  ← Move a bit
0.002       (0.499, 0.755, 0.999)  ← Keep moving
...
1.000       (0.412, 1.358, 0.631)  ← Final position
```

The ODE tells us how to move from one point to the next.

### Why 1001 Points?

```
Number of steps = (1 - 0) / 0.001 = 1000
Number of points = 1000 + 1 (initial) = 1001
```

### Visualization

#### Time Series Plot
Shows how each variable evolves over time:
```
    y
    │
1.4 │                    ●●●
    │                 ●●
1.0 │              ●●
    │           ●●
0.5 │        ●●
    │     ●●
0.0 │  ●●
    └──────────────────────→ t
       0   0.25  0.5  0.75  1.0
```

#### 3D Trajectory Plot
Shows the path through (x, y, z) space:
```
        z
        │
      1.0 ●
          │  ╲
      0.5 │   ╲  ●●●
          │    ●●
        0 └──────────→ y
          0   0.5   1.0
         /
        ●
       0.5
```

### Analogy: Video vs Photo

- **Photo (final point only)**: Shows where you ended up
- **Video (full trajectory)**: Shows every moment, reveals dynamics, validates the path

**Our visualization is like a video**—all 1001 frames, not just the last one.

---

## 7. Interpreting Our Results

### The Numbers

#### Final States Match (6 decimal places)

```
Method    x          y          z
------    --------   --------   --------
RK4:      0.412011   1.358844   0.630987
SciPy:    0.412011   1.358844   0.630987
```

✅ Both methods converge to the same trajectory. Our RK4 is correct.

#### MSE = 1.82 × 10⁻²²

- Average squared difference is 10⁻²²
- RMSE = √(10⁻²²) = 10⁻¹¹
- Typical difference: ~10⁻¹¹

#### RMSE = 1.35 × 10⁻¹¹

**Interpretation**: On average, solutions differ by 0.0000000000135 (13.5 trillionths).

#### Max Error = 6.06 × 10⁻¹¹

At the worst point, solutions differ by 6×10⁻¹¹.

Relative to solution values (~1.0): 6×10⁻¹¹ / 1.0 = **0.000000006%**

✅ **This is essentially perfect agreement!**

### Why Error Isn't Zero

1. **Different algorithms**: RK4 uses 4 slopes, DOP853 uses 8th-order
2. **Different step sizes**: RK4 fixed at 0.001, DOP853 adaptive
3. **Truncation error**: Different Taylor series truncation
4. **Roundoff error**: Finite precision (~15-16 decimal digits)

**The error (~10⁻¹¹) is the "numerical floor"**—we can't do better with double precision.

---

## 8. Visualization Guide

### Left Panel: Solution Comparison

**What you see**:
- Three curves: x(t), y(t), z(t) over time
- **Solid lines** = RK4 solution
- **Dotted lines** = SciPy reference (nearly invisible behind solid)

**What it means**:
- Two different methods give visually identical results
- High confidence our implementation is correct
- Error is microscopic

**Trajectory interpretation**:
- **x (blue)**: Decreases 0.5 → ~0.41
- **y (orange)**: Increases 0.75 → ~1.36 (largest final value)
- **z (green)**: Decreases 1.0 → ~0.63

The three modes exchange energy in a coupled nonlinear way.

### Right Panel: Error Curves

**What you see**:
- Three wavy lines: δx, δy, δz
- Scale: 10⁻¹¹ (very small!)
- Lines oscillate around zero

**Why oscillate?**
- Different methods accumulate error differently
- Sometimes RK4 overshoots, sometimes undershoots
- Pattern reflects Lorenz-1960 dynamics

**Scale interpretation**:
```
Error ≈ 10⁻¹¹ means:
- If true value is 1.0, RK4 gives 1.00000000001
- This is 11 decimal places of accuracy
```

---

## 9. Practical Implications for FYDP

### What This Baseline Enables

#### 1. Training Data Generation

```python
# Generate training data
t_train = np.linspace(0, 1, 100)
x_train, y_train, z_train = solve_lorenz1960(t_train)

# Train ANN: t → (x, y, z)
ann.fit(t_train, [x_train, y_train, z_train])
```

**Why validated baseline matters**: Garbage in, garbage out. Our ~10⁻¹¹ error is negligible compared to ANN's ~10⁻⁴ typical error.

#### 2. ANN Validation

```python
# Compare ANN predictions to true solution
ann_error = np.sqrt(np.mean((x_pred - x_true)**2))

# Interpretation:
# > 10⁻⁴: ANN needs improvement
# ≈ 10⁻⁶: Good but not great
# < 10⁻⁸: Excellent (near numerical precision)
```

### When to Use Which Solver

| Scenario | Recommended | Reason |
|----------|-------------|--------|
| Learning/Education | RK4 | Transparent, easy to understand |
| Quick experiments | RK4 | Fast, predictable |
| Production accuracy | DOP853 | Automatic error control |
| Unknown behavior | DOP853 | Adapts to problem difficulty |
| Long time spans | DOP853 | Adaptive steps more efficient |

### Parameter Guidelines

**RK4 Step Size**:
```
Start with: h = 0.001 (for t ∈ [0, 1])

If error too large: h_new = h / 2 (error reduces 16×)
If error very small: h_new = h × 2 (speed doubles)
```

**DOP853 Tolerances**:
```
Standard:     rtol=1e-6,  atol=1e-8
High accuracy: rtol=1e-10, atol=1e-12 (what we used)
Ultra-high:   rtol=1e-12, atol=1e-14
```

---

## 10. Lorenz-1960 vs Lorenz-1963

### Critical Distinction

**These are completely different systems!**

| Feature | Lorenz-1960 (Ours) | Lorenz-1963 (Butterfly) |
|---------|-------------------|------------------------|
| **Year** | 1960 | 1963 |
| **Behavior** | **Smooth, predictable** | **Chaotic** |
| **Trajectory** | Simple curve | Butterfly attractor |
| **Long-term** | Well-behaved | Never repeats |
| **Famous?** | Less known | Very famous |

### The Equations

**Lorenz-1960 (What we solve):**
```
dx/dt = -0.1·y·z
dy/dt =  1.6·x·z
dz/dt = -0.75·x·y
```
- k=2, l=1 parameters
- Smooth on [0,1]
- Simple curve in 3D

**Lorenz-1963 (Butterfly system):**
```
dx/dt = σ·(y - x)
dy/dt = x·(ρ - z) - y
dz/dt = x·y - β·z
```
- σ=10, ρ=28, β=8/3
- Chaotic—tiny changes → huge differences
- Never repeats, infinitely complex

### Why We Use Lorenz-1960

**Advantages for ANN training:**
1. ✅ Well-behaved: Smooth, predictable
2. ✅ Validatable: Can check against accurate reference
3. ✅ Short interval: [0,1] is manageable
4. ✅ Non-chaotic: Small errors don't explode

**Lorenz-1963 disadvantages:**
1. ❌ Chaotic: Tiny numerical errors grow exponentially
2. ❌ Hard to validate: No "true" solution exists
3. ❌ Sensitive: 15th decimal changes cause divergence
4. ❌ Long-term only: Butterfly emerges over long time

### Historical Relationship

Both created by **Edward N. Lorenz** at MIT:

**Lorenz-1960**: "Maximum simplification of atmospheric motion"
- Start with fluid dynamics
- Truncate to 3 Fourier modes
- Result: Simple coupled ODEs

**Lorenz-1963**: "Deterministic Nonperiodic Flow" (famous butterfly paper)
- Purpose: Simplest system exhibiting chaos
- Different Fourier mode selection
- Result: **Chaos emerges**

**The Discovery (1961-1962)**:
> Lorenz restarted a simulation with rounded values (6 decimals instead of full). The trajectory **completely diverged**.

**This was the birth of chaos theory.**

**Realization**: The 1960 system was **too simple** to show chaos. He needed different modes.

### Summary

```
         Edward Lorenz (MIT)
              │
    ┌─────────┴─────────┐
    │                   │
Lorenz-1960        Lorenz-1963
(The Setup)        (The Discovery)
    │                   │
    ▼                   ▼
Smooth ODEs         Chaotic ODEs
    │                   │
    ▼                   ▼
Usable for          Foundation of
validation          chaos theory
```

**Bottom line**: 1960 and 1963 are **cousins**—same researcher, same purpose (understanding weather), but different behaviors (predictable vs chaotic). We use 1960 because it's scientifically validatable; 1963 is famous but too chaotic for our ANN benchmarking.

---

## 11. Quick Reference

### RK4 in 4 Lines

```python
def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h, y + h*k3)
    return y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
```

**Key facts**:
- 4 slope evaluations per step
- Error ∝ h⁴
- Halve step → error ÷ 16

### SciPy DOP853 in 4 Lines

```python
from scipy.integrate import solve_ivp

sol = solve_ivp(f, t_span, y0, 
                method='DOP853',
                rtol=1e-10, atol=1e-12)
```

**Key facts**:
- 8th-order adaptive method
- Automatic step size adjustment
- Error controlled by rtol/atol

### Error Metrics

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **MSE** | mean((y_pred - y_true)²) | Average squared error |
| **RMSE** | √MSE | Average error (same units as data) |
| **Max Error** | max\|y_pred - y_true\| | Worst-case deviation |

### Our Results Summary

```
RK4 Configuration:
  Step size: h = 0.001
  Grid points: 1001
  Method: Fixed-step 4th-order Runge-Kutta

SciPy Configuration:
  Method: DOP853 (8th-order adaptive)
  Relative tolerance: rtol = 1e-10
  Absolute tolerance: atol = 1e-12

Validation Results:
  MSE:  1.82 × 10⁻²²
  RMSE: 1.35 × 10⁻¹¹
  Max Error: 6.06 × 10⁻¹¹
  
Interpretation:
  ✓ Agreement to ~11 decimal places
  ✓ Error at numerical precision floor
  ✓ Baseline validated and ready for ANN experiments
```

---

## Key Takeaways

1. **RK4** uses 4 slope estimates, achieving O(h⁴) accuracy
2. **DOP853** adapts step size based on error estimates
3. **rtol/atol** control acceptable error (relative and absolute)
4. Our **MSE ~ 10⁻²²** means perfect agreement for practical purposes
5. This validated baseline is the foundation for ANN experiments

**Bottom line**: We have a numerical solution we can trust to 11 decimal places. Any ANN that matches this within 10⁻⁴ is doing very well.

---

## FAQ

**Q: Where do the error numbers come from?**  
A: By comparing RK4 and SciPy at all 1001 time points, then applying MSE/RMSE formulas.

**Q: Why visualize 1001 points if the final outcome is just one point?**  
A: We show the entire journey from t=0 to t=1, not just the destination. This validates the solution path.

**Q: Why don't we see the butterfly-shaped Lorenz attractor?**  
A: The butterfly is from **Lorenz-1963** (chaotic). We solve **Lorenz-1960** (different equations).

**Q: What is the relationship between Lorenz-1960 and Lorenz-1963?**  
A: Same researcher (Edward Lorenz), same field. 1963 evolved from 1960 and discovered chaos.

---

*Document created for FYDP-I Lorenz-1960 Numerical Baseline*  
*Last updated: April 4, 2026*
