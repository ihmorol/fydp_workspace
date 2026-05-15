# Understanding the Lorenz-1960 Equations for This Project

This document is a project-focused guide to the Lorenz-1960 equations used in the current FYDP work. Its purpose is to explain what the equations are, why they matter scientifically, why they are valuable for an engineering research project, how researchers use them, and how they should be implemented and solved numerically before any neural-network-based approximation is attempted. In this project, the correct name is the **Lorenz** equations, after Edward N. Lorenz. This is different from **Lorentz**, which usually refers to electromagnetism and the Lorentz force. That distinction matters because these are completely different mathematical and physical contexts.

## Historical Background and Scientific Meaning

The Lorenz-1960 system comes from Edward Lorenz's effort to derive a strongly simplified model of atmospheric dynamics from a more complicated fluid system. The idea was not to produce a toy equation with no physical meaning, but to keep only a very small number of interacting modes from a much larger physical model. That reduction creates a coupled nonlinear system of ordinary differential equations that is still rich enough to display meaningful dynamics. In modern language, this is a low-dimensional reduced-order model. The scientific value of such models is that they preserve core interactions while remaining small enough to analyze carefully, simulate repeatedly, and use as a benchmark.

In the literature, many people are more familiar with the Lorenz-1963 system, which is the famous three-variable chaotic model often written with parameters sigma, rho, and beta. The current project is not using that model. It is using the Lorenz-1960 three-equation system that appears in Section 4.2 of the PinnDE paper. That is an important distinction because the coefficients, interpretation, and benchmark role are different. Mixing Lorenz-1960 and Lorenz-1963 would confuse the mathematical setup, the literature review, and the implementation.

## Why the Lorenz-1960 System Is Valuable

The Lorenz-1960 system is valuable because it sits in a useful middle ground. It is much smaller than a full atmospheric or fluid dynamics simulation, so it is computationally manageable and easy to visualize. At the same time, it is not trivial. The equations are coupled, nonlinear, and sensitive to parameter choices and initial conditions. Because of that, the system is a strong benchmark for numerical methods, surrogate models, and learning-based solvers. A weak solver may still work on a linear or decoupled ODE, but it will often fail or lose reliability on a nonlinear coupled system like this one.

For this project, the system is especially valuable because it creates a clean research pipeline. First, it allows a trustworthy numerical reference solution to be generated with classical methods such as Runge-Kutta or an adaptive Python ODE solver. Second, it gives a compact but meaningful target for comparing ANN architectures. Third, it makes it possible to discuss engineering trade-offs such as accuracy, stability, computational cost, and reproducibility without needing massive simulation infrastructure. That is why it is a good fit for a comparative FYDP project.

Researchers also value systems like this because they expose core issues that matter in much larger problems. Numerical analysts use such systems to test integrator accuracy and convergence. Scientific machine learning researchers use them to evaluate PINNs, DeepONets, neural surrogates, and operator learners. Applied mathematicians use them to study nonlinear interaction, reduced-order modeling, and dynamical behavior. In short, the model is small enough to teach from and serious enough to publish on.

## The Exact Lorenz-1960 System Used in This Project

The project should follow the equations printed in Section 4.2 of `paper1`, not the appendix code snippet. In the benchmark problem described there, the Lorenz-1960 system is written as

```text
dx/dt = kl(1/(k^2 + l^2) - 1/k^2) yz
dy/dt = kl(1/l^2 - 1/(k^2 + l^2)) xz
dz/dt = (k l^2 / 2)(1/k^2 - 1/l^2) xy
```

with parameter values `k = 2` and `l = 1`, initial conditions `x(0) = 0.5`, `y(0) = 0.75`, `z(0) = 1`, and time interval `t in [0, 1]`.

When these parameter values are substituted into the equations, the system becomes

```text
dx/dt = -0.1 yz
dy/dt =  1.6 xz
dz/dt = -0.75 xy
```

This simplified form is the most practical one to implement in code. It removes symbolic clutter and makes sign mistakes easier to spot. It also aligns with the original Lorenz-1960 model structure and with the benchmark setup discussed in the PinnDE paper. One important project note is that the appendix code extracted from `paper1` does not match the printed equations cleanly. For implementation and reporting, the printed equations should be treated as authoritative, and the numerical solver should be validated against them directly.

## Why Researchers Use This Kind of System

Researchers use the Lorenz-1960 equations for several reasons. One reason is methodological clarity. Because the state dimension is only three, every implementation choice can be inspected closely. One can plot the full trajectory, compare methods point-by-point, monitor local and global error, and detect divergence or instability quickly. Another reason is model richness. Even though the system is small, it is still nonlinear and coupled, which means that improvements in a solver are meaningful rather than cosmetic.

In the scientific machine learning setting, such systems are often used as stepping stones between textbook examples and large real-world PDE models. A researcher can test whether a network learns the solution accurately, whether it respects the structure of the dynamics, whether the training is stable, and whether the predictions remain reliable under changed initial conditions. This is especially important when comparing a physics-informed approach against a purely data-driven ANN approach. Without a dependable numerical baseline, those comparisons are not defensible.

The system also matters educationally. It teaches a general lesson that appears across many ODE and PDE problems: a simple-looking equation can still be hard because coupling and nonlinearity create complexity. Learning to solve this system properly helps build the habits needed for much larger systems, including writing the model cleanly, checking parameter substitutions, selecting solvers responsibly, and validating results before moving to machine learning.

## How to Implement the System Correctly

The implementation should begin by defining the state vector and the right-hand side function. The state is the vector `u(t) = [x(t), y(t), z(t)]`. The right-hand side is the vector field that returns the derivatives at a given time and state. Even though the system is autonomous in this form, the numerical solver API should still accept `t` as an argument because standard ODE interfaces expect a function of the form `f(t, u)`.

The simplest correct Python implementation is the following.

```python
import numpy as np

def lorenz1960_rhs(t, state):
    x, y, z = state
    dx = -0.1 * y * z
    dy =  1.6 * x * z
    dz = -0.75 * x * y
    return np.array([dx, dy, dz], dtype=float)
```

This function is the mathematical core of the whole project. Everything else, including RK4, adaptive solvers, plotting, and ANN training data generation, depends on this vector field being correct. If this function is wrong, every later result is wrong. That is why it should be tested first and kept simple.

## Solving It with Manual RK4

A manual fourth-order Runge-Kutta solver is worth implementing even if Python already provides adaptive ODE solvers. The reason is not that RK4 is always the best solver, but that it is transparent. It shows exactly how one advances the state from one time step to the next, how intermediate slopes are combined, and how fixed-step numerical error behaves. For an FYDP, that transparency is valuable because it supports explanation, reproducibility, and technical understanding.

For a step size `h`, the RK4 update computes four slopes from the same vector field and combines them in the familiar weighted average. A compact implementation is shown below.

```python
import numpy as np

def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def solve_rk4(f, t0, t1, y0, h):
    n_steps = int(round((t1 - t0) / h))
    ts = np.linspace(t0, t1, n_steps + 1)
    ys = np.zeros((n_steps + 1, len(y0)), dtype=float)
    ys[0] = y0
    t = t0
    y = np.array(y0, dtype=float)
    for i in range(n_steps):
        y = rk4_step(f, t, y, h)
        ys[i + 1] = y
        t = ts[i + 1]
    return ts, ys
```

This solver should be used first with a reasonably small step size such as `h = 1e-3` and then with a smaller step such as `h = 1e-4` to check convergence. If halving the step size barely changes the result, that is good evidence that the implementation is behaving correctly on this time interval.

## Solving It with Python's Built-In Scientific Solver

Standard Python itself does not include a full scientific ODE solver in the language core. In practice, the normal Python choice is `scipy.integrate.solve_ivp`, which is the modern SciPy interface for initial value problems. This is the solver that should be used to create a high-accuracy reference solution for the ANN study. For a non-stiff problem like this one, explicit Runge-Kutta methods are the right first choice. Among them, `DOP853` is especially useful when high precision is desired, while `RK45` is a common general-purpose default.

The implementation is straightforward.

```python
import numpy as np
from scipy.integrate import solve_ivp

y0 = np.array([0.5, 0.75, 1.0], dtype=float)
t_eval = np.linspace(0.0, 1.0, 1001)

solution = solve_ivp(
    lorenz1960_rhs,
    (0.0, 1.0),
    y0,
    method="DOP853",
    t_eval=t_eval,
    rtol=1e-12,
    atol=1e-14,
)
```

In a local verification run for this project, the state at `t = 1` was approximately `x(1) = 0.4120105447756977`, `y(1) = 1.358843985120531`, and `z(1) = 0.6309874543505187`. A manual RK4 solution with `h = 1e-3` agreed with the adaptive `DOP853` result to near machine precision on this interval. That is exactly the kind of agreement needed before generating training targets for ANN models.

## How This Should Be Understood as a Learning Problem

The right way to learn this system is not to memorize one solver call and move on. It should be understood in layers. The first layer is mathematical understanding. One should be able to read the equations, identify the state variables, identify the parameters, and distinguish between the state vector and the derivative vector. The second layer is numerical understanding. One should be able to explain why initial conditions are necessary, what a time interval means, what a step size is, what local and global error mean, and why an adaptive solver may outperform a fixed-step solver in efficiency. The third layer is modeling understanding. One should be able to explain why this small system is still a meaningful benchmark and why neural networks should not be introduced until the numerical baseline is solid.

Learning this properly also means learning how to generalize the workflow to similar ODE systems. The same broad procedure applies to many coupled initial value problems. First, write the system in vector form. Second, define the right-hand side as code. Third, choose a solver that matches the problem type, beginning with non-stiff explicit methods unless stiffness suggests otherwise. Fourth, test convergence by changing the step size or tolerances. Fifth, visualize the result and check whether the behavior is plausible. Sixth, only after the numerical side is validated, use the solution data for downstream tasks such as regression, surrogate modeling, or neural approximation.

## How Researchers Learn to Solve Similar ODE Systems

A strong researcher does not treat each new ODE as a completely new world. Instead, the researcher looks for structure. Is the system linear or nonlinear? Is it coupled or decoupled? Is it autonomous or time-dependent? Is it stiff or non-stiff? Are there conserved quantities, monotonic trends, or symmetry properties that can be used as checks? These questions help determine not only how to solve the system, but how to trust the solution.

For similar systems, the learning process should move from simple to difficult. One begins with single first-order equations, then small coupled systems, then nonlinear systems, then systems where solver selection matters. Along the way, one compares Euler, RK4, and adaptive solvers to understand the trade-off between simplicity and accuracy. Once that foundation is built, systems like Lorenz-1960 stop looking mysterious. They become examples of a general pattern: define the vector field, choose the solver, validate the trajectory, and interpret the dynamics.

## Common Mistakes That Must Be Avoided in This Project

Several mistakes are easy to make here. One mistake is confusing Lorenz-1960 with Lorenz-1963 and accidentally implementing the wrong benchmark. Another is copying code fragments without re-deriving the coefficients from the printed equations. Another is trusting a solver result without checking convergence. Another is using too coarse a step size in RK4 and then blaming the neural network when the real problem is a weak ground-truth trajectory. Another is starting ANN experiments before the numerical baseline has been verified. All of these mistakes weaken the project, and all of them are avoidable with a careful mathematical and numerical workflow.

The most important practical rule is simple: the numerical baseline comes first. The ANN is not the first solver. It is the second solver. The first solver is the classical one, and it is the standard against which the ANN is judged. This rule should shape the whole project.

## What This Means for the Current FYDP

For the current FYDP, the Lorenz-1960 equations should be treated as the benchmark dynamical system on which the project's whole methodology is built. The immediate engineering task is not yet architecture optimization. The immediate task is to define the equations correctly, solve them with both manual RK4 and `solve_ivp`, confirm that both methods agree on the interval of interest, and store a dense high-accuracy trajectory as reference data. After that, ANN models can be trained to approximate the solution map `t -> (x(t), y(t), z(t))`. Only then does it make sense to compare depth, width, activation functions, and training settings.

This also clarifies the role of the three papers already in the repository. The PinnDE paper provides the direct benchmark problem and a DeepONet-based reference. The ANN survey paper provides method ideas for plain ANN approaches, especially trial-solution style thinking, but it is not itself a Lorenz-1960 paper. The Neural ODE paper is background that helps position the literature, but it is not the same problem because it learns dynamics in a different way. This separation is important for writing a clean literature review and a defensible methodology chapter.

## Conclusion

The Lorenz-1960 equations matter in this project because they are a compact, nonlinear, physically motivated benchmark that is ideal for connecting numerical analysis and neural approximation. They are valuable not because they are large, but because they are structurally meaningful. They teach the discipline of mathematical modeling, numerical verification, and careful comparison. If this system is understood and implemented correctly, it becomes an excellent foundation for learning how to solve similar ODE systems and for building a credible ANN-based solver study on top of a trustworthy reference solution.

## References

Lorenz, E. N. (1960). *Maximum simplification of the dynamic equations of the atmosphere*. Tellus, 12(3), 243-254.

Matthews, J., and Bihlo, A. (2025). *PinnDE: Physics-Informed Neural Networks for Solving Differential Equations*. arXiv:2408.10011v2.

Pratama, D. A., Bakar, M. A., Ismail, N. B., and Mashuri, M. (2022). *ANN-based methods for solving partial differential equations: a survey*. Arab Journal of Basic and Applied Sciences, 29(1), 233-248.

Chen, R. T. Q., Rubanova, Y., Bettencourt, J., and Duvenaud, D. (2019). *Neural Ordinary Differential Equations*. NeurIPS 2018 proceedings version and arXiv:1806.07366.

SciPy Developers. *scipy.integrate.solve_ivp* documentation. This is the practical reference for solver choice and parameter settings in Python.
