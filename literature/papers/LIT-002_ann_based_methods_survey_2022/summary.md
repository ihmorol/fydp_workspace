# LIT-002 — ANN-based methods for solving partial differential equations: a survey

## Metadata
- **Title:** ANN-based methods for solving partial differential equations: a survey
- **Authors:** Danang A. Pratama, Maharani A. Bakar, N. B. Ismail, Mashuri M.
- **Year:** 2022
- **Venue:** Arab Journal of Basic and Applied Sciences
- **DOI / URL:** https://doi.org/10.1080/25765299.2022.2104224
- **Topic tag(s):** ANN, differential equations, PDE, survey, NeuroDiffEq, PyDEns, Nangs
- **Status:** detailed
- **Priority:** high

## Why this paper matters
- It is the best plain-ANN-adjacent source currently in the local FYDP set.
- It gives a structured comparison of three ANN-based differential-equation solvers.
- It helps defend the methodological position of our work against PINN-heavy literature.

## TL;DR
This survey compares three ANN-based methods for solving PDEs without relying on classical discretization in the usual way: PyDEns, NeuroDiffEq, and Nangs. The paper reports that NeuroDiffEq and Nangs perform better than PyDEns on higher-dimensional PDEs, while PyDEns is better suited to lower-dimensional cases. For our FYDP, its value is not that it solves Lorenz-1960 directly, but that it clarifies plain-ANN design choices, comparison criteria, and methodological language.

## Problem addressed
How different ANN-based approaches can be used to solve PDEs efficiently and accurately, and how they compare against one another.

## Method / approach
- Compares three ANN-based PDE-solving approaches.
- Reviews the modeling idea behind each method.
- Evaluates them in terms of accuracy and efficiency.
- Uses the comparison to discuss suitability across problem settings.

## Experimental setup
- PDE-focused, not ODE-focused.
- Methods discussed: PyDEns, NeuroDiffEq, Nangs.
- Highlights architecture defaults such as 3 hidden layers, 32 neurons, tanh activation in the compared setups.

## Key results
- NeuroDiffEq and Nangs outperform PyDEns on high-dimensional PDEs.
- PyDEns is more suitable for lower-dimensional problems.
- ANN solver design choices strongly affect performance and suitability.

## What is useful for our FYDP
- Gives concrete ANN-based solver families to cite in Chapter 2.
- Supports framing plain ANN methods as a valid research direction.
- Suggests useful comparison axes: accuracy, efficiency, dimensionality, and architecture choices.
- Gives a literature-backed reason to discuss tanh and trial-solution-based approaches.

## Limitations / gaps
- Focuses on PDEs rather than ODEs.
- Does not study the Lorenz-1960 system.
- Does not perform an architecture optimization study on a fixed benchmark like ours.
- Does not directly compare plain ANN against PINN on the same Lorenz-type benchmark.

## What to look at carefully
- How each method represents the solution function.
- How initial/boundary conditions are handled.
- What architecture choices are fixed versus tuned.
- What evaluation metrics and efficiency claims are actually reported.

## Reusable citations / claims
- ANN methods can solve differential equations without the standard discretization-first workflow.
- Solver performance depends on the ANN method and problem setting; one approach is not best everywhere.

## My take
This is not the closest benchmark paper, but it is one of the most useful framing papers. It gives you methodological vocabulary and a comparison mindset. Its main value is strategic: it helps define where our work sits in the landscape of differential-equation solvers.
