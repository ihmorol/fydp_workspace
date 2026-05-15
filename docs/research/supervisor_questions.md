# Supervisor Questions for the Lorenz-1960 ANN FYDP

The current research direction is promising, but several methodological decisions are still under-specified. These questions should be clarified with the supervisor before implementation starts so that the scope, evaluation, and novelty are fixed early.

## 1. Research framing and contribution

1. Is the main contribution expected to be an architecture comparison only, or do you want a stronger methodological contribution such as a new loss design, a hard initial-condition constraint, or a comparison against PINNs?
2. Should the project be framed mainly as a scientific machine learning study, a numerical analysis study, or an application of ANN to a physics problem?
3. Is the title "Optimal ANN Architecture for Solving the Lorenz-1960 ODE System" acceptable, or do you want the title to explicitly mention benchmark comparison, PINNs, or surrogate modeling?

## 2. Exact problem formulation

4. Should the ANN input be only the scalar time variable $t$, or should the model also take initial conditions as input so that it can generalize across multiple starting states?
5. Are we solving only one fixed initial value problem on $t \in [0,1]$, or should we also test generalization to other time intervals or initial conditions?
6. Should the initial condition be enforced as a hard constraint in the model design, used as a soft loss penalty, or left to be learned purely from data?
7. Should the Lorenz-1960 parameter setting remain fixed at $k=2$ and $l=1$, or do you want sensitivity experiments over parameter values as part of the study?

## 3. Baselines and fairness

8. What should be treated as the primary baseline: RK4, SciPy RK45, the DeepONet result from PinnDE, or all of them?
9. If we compare against the physics-informed result from the literature, do you expect us to reproduce that model experimentally or only compare against the published description and reported behavior?
10. Do you want one literature-inspired ANN baseline, such as the 3-layer 32-neuron tanh model from the survey paper, to be fixed as the default comparison point?

## 4. Architecture search scope

11. How large should the architecture search be for FYDP-I and FYDP-II? For example, should we test a full grid of layers, widths, activations, and optimizers, or a smaller literature-guided subset?
12. Which framework do you prefer for implementation: PyTorch or TensorFlow?
13. Are there any architecture choices you specifically want included or excluded, such as GELU, Swish, residual connections, or L-BFGS optimization?

## 5. Evaluation criteria

14. What metric should define the "optimal" architecture: minimum MSE, training stability, inference speed, parameter efficiency, or a weighted combination of these?
15. Is there any target performance threshold that would make the result acceptable, such as a specific MSE level relative to the numerical reference?
16. Do you want repeated runs with multiple random seeds so that the reported best architecture is also stable and not just lucky?
17. Should we evaluate only interpolation on the training interval, or also extrapolation and robustness under changed conditions?

## 6. FYDP deliverables and writing expectations

18. For FYDP-I, do you expect only proposal-stage work and a strong literature review, or do you also want preliminary implementation results in the report or presentation?
19. How many papers do you consider sufficient for Chapter 2, and do you want more recent sources beyond the three currently identified core references?
20. Do you want the report to remain strictly within the department template, or may we adapt section naming and tables slightly to better fit a research-style thesis?

## 7. Practical execution

21. Should we prioritize fast completion with a simpler fixed-time supervised ANN, or invest early in a more general formulation that can support later journal publication?
22. Are there preferred software engineering expectations for this project, such as experiment logging, GitHub reproducibility, or a comparison notebook for each model?
23. Is there any supervisor-specific concern about the novelty claim that we should avoid overstating in Chapter 1 and Chapter 2?

If these questions are answered clearly, the project scope becomes concrete enough to begin implementation and to write the remaining proposal chapters with much less uncertainty.
