# Complex Engineering Problem and Complex Problem Solving Mapping

## Project Title
**Solving the Lorenz-1960 ODE System Using Optimal ANN Architectures**

## 5.4 Complex Engineering Problem

This project addresses a **complex engineering problem** because it goes beyond routine software development and requires the integration of mathematical modeling, numerical computation, machine learning, and experimental evaluation to solve a nonlinear coupled ordinary differential equation system. The target problem is the **Lorenz-1960 system**, which is a sensitive and nonlinear benchmark equation set used to study dynamic behavior in physical systems. Approximating its solution with Artificial Neural Networks (ANNs) is not a straightforward implementation task; it demands careful engineering decisions about model design, numerical reliability, validation strategy, and performance trade-offs.

The complexity of the problem arises from several interacting factors. First, the Lorenz-1960 system contains **multiple dependent variables that evolve simultaneously**, so the solution of one equation influences the others. This coupling makes the problem analytically and computationally challenging. Second, the system is **nonlinear**, meaning small changes in the network design, training configuration, or data representation can significantly affect the quality and stability of the predicted solution. Third, the project requires a dependable **numerical reference solution** using a conventional solver such as Runge-Kutta in order to generate trustworthy baseline data for training and evaluation. Without this baseline, ANN performance cannot be judged rigorously.

In addition, the project does not seek only to "solve an equation with ANN." Its central research question is to determine **which ANN architecture is most suitable** for approximating the Lorenz-1960 solution. That introduces a genuine engineering design problem involving the comparison of multiple network structures, activation functions, training settings, and evaluation criteria. The best architecture cannot be selected using intuition alone. It must be identified through systematic experimentation and evidence-based comparison.

Another source of complexity is the presence of **conflicting engineering requirements**. A deeper or wider neural network may improve approximation accuracy, but it may also increase computational cost, training time, and risk of overfitting. A simpler network may be faster and easier to reproduce, but it may fail to capture the nonlinear behavior of the system with sufficient precision. Therefore, the project requires balancing:

- solution accuracy
- computational efficiency
- model generalization
- stability of training
- reproducibility of results

Because of these factors, this work clearly qualifies as a complex engineering problem. It requires theoretical understanding, numerical correctness, method selection, experimental design, and engineering judgment rather than simple implementation of an existing template.

## Why This Problem Is Not Routine

This project is not a routine coding or software assignment for the following reasons:

- The target system is a **nonlinear coupled ODE model**, not a simple algebraic or single-variable problem.
- The ANN must approximate a **continuous dynamic solution** over time rather than perform a standard classification or regression task with independent samples.
- The project requires **comparison against validated numerical baselines**, which introduces additional mathematical and computational rigor.
- The final outcome depends on **architecture selection and trade-off analysis**, not only on successful code execution.
- The work involves **research-oriented experimentation**, where the methodology must be justified, repeatable, and defensible in an academic engineering context.

## Engineering Tasks Involved

To solve this problem, the project must address several technical tasks:

1. Formulate the Lorenz-1960 ODE system correctly with its parameters and initial conditions.
2. Generate a high-accuracy reference solution using a numerical method such as Runge-Kutta.
3. Prepare training and validation data from the numerical solution.
4. Design multiple ANN architectures by varying depth, width, activation functions, and training settings.
5. Train the models and evaluate them using quantitative error metrics.
6. Compare the models in terms of accuracy, runtime, convergence behavior, and reproducibility.
7. Identify the architecture that provides the best engineering trade-off for the problem.

Each of these tasks depends on technically sound decisions. An error in modeling, data generation, architecture design, or evaluation could invalidate the final conclusion. This further supports the claim that the project belongs to the category of complex engineering work.

## 5.4.1 Complex Problem Solving

### Mapping with Complex Problem Solving Categories

For this project, the most relevant complex problem solving attributes are:

- **P1: Depth of Knowledge Required**
- **P2: Range of Conflicting Requirements**
- **P3: Depth of Analysis Required**

The mapping is presented below.

| Category | Relevance to This Project | Justification |
|---|---|---|
| **P1: Depth of Knowledge** | High | The project requires combined knowledge of differential equations, numerical methods, neural networks, optimization, and error analysis. |
| **P2: Range of Conflicting Requirements** | High | The ANN architecture must balance accuracy, computational cost, generalization, training stability, and reproducibility. |
| **P3: Depth of Analysis** | High | The work demands comparative experimentation, interpretation of results, validation against numerical baselines, and evidence-based model selection. |

### P1: Depth of Knowledge Required

This project requires **deep and integrated knowledge from multiple technical domains**. A basic understanding of programming alone is not enough to complete the work correctly. The student must understand:

- **ordinary differential equations**, especially nonlinear coupled systems
- **initial value problems** and their mathematical interpretation
- **numerical solution techniques** such as Runge-Kutta methods
- **artificial neural networks**, including architecture design, training behavior, and optimization
- **performance metrics** such as mean squared error and convergence behavior
- **experimental validation and reproducibility** in engineering research

The challenge is not only knowing these topics separately, but also applying them together in a coherent workflow. For example, the ANN cannot be trained responsibly unless the reference solution is numerically reliable. Similarly, model accuracy cannot be interpreted correctly without understanding the underlying ODE behavior and the limitations of numerical approximations. This interdisciplinary dependency is a strong indicator of problem complexity and maps directly to **P1**.

### P2: Range of Conflicting Requirements

The project also maps strongly to **P2** because it involves several **conflicting design requirements** that cannot all be optimized at the same time. Some of the main conflicts are:

- **Accuracy vs. computational cost**: Larger or deeper networks may approximate the solution more accurately, but they require more parameters, longer training time, and greater computational resources.
- **Model complexity vs. generalization**: A highly flexible model may fit the reference data very well, but it may generalize poorly or become sensitive to training conditions.
- **Training speed vs. stability**: Fast optimization settings may reduce training time, but they can also cause unstable convergence or poor final performance.
- **Performance vs. reproducibility**: Some configurations may yield very low error in one run but may be difficult to reproduce consistently across repeated experiments.

Because these requirements compete with one another, the project cannot be solved by choosing the largest network or the most advanced optimizer by default. Instead, it requires engineering judgment to determine a balanced solution that is accurate, efficient, and defensible. This trade-off structure is a defining feature of complex problem solving.

### P3: Depth of Analysis Required

This project also demonstrates **P3** because solving it requires substantial analytical work rather than straightforward implementation. The student must carry out:

- **comparative analysis** of multiple ANN architectures
- **interpretation of quantitative metrics** such as approximation error and convergence trend
- **validation against a trusted numerical baseline**
- **assessment of model behavior** under different hyperparameter settings
- **reasoned selection** of the best-performing architecture based on evidence

The analysis is not limited to checking whether the code runs successfully. The student must explain **why one architecture performs better than another**, whether the result is stable, and whether the observed performance is meaningful for the Lorenz-1960 system. This requires examining trends across experiments, identifying limitations, and drawing conclusions from data in a scientifically defensible way. Therefore, the depth of analysis required is clearly consistent with **P3**.

## Overall Justification

In summary, this project satisfies the criteria of a complex engineering problem because it requires:

- advanced theoretical and computational knowledge
- careful handling of nonlinear coupled differential equations
- development and comparison of multiple ANN-based solution strategies
- balancing of conflicting technical requirements
- rigorous validation and interpretation of experimental results

Therefore, the project is appropriately classified as a **complex engineering problem**, and its problem-solving process strongly maps to **P1, P2, and P3** of complex problem solving.

## Short Proposal-Ready Version

This project qualifies as a complex engineering problem because it requires the integration of mathematical modeling, numerical analysis, artificial neural networks, and experimental validation to approximate the solution of the nonlinear coupled Lorenz-1960 ODE system. The work is not a routine software implementation task, since it involves selecting and evaluating suitable ANN architectures while balancing accuracy, computational cost, generalization ability, training stability, and reproducibility. The problem strongly maps to **P1** because it requires deep knowledge of ODEs, numerical methods, and machine learning; to **P2** because it contains conflicting requirements such as accuracy versus efficiency and complexity versus generalization; and to **P3** because it demands comparative analysis, validation against numerical baselines, and evidence-based architectural selection.
