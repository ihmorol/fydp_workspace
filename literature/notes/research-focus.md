# Research Focus Notes

## Core question
Which plain ANN architecture best solves the Lorenz-1960 ODE system under a unified evaluation setup?

## What the literature review must optimize for
- identifying the closest benchmark papers
- separating PINN / operator-learning / plain-ANN / Neural-ODE paradigms
- extracting architecture choices: depth, width, activation, optimizer, losses
- extracting evaluation choices: metrics, baselines, intervals, initial conditions
- finding the cleanest defensible research gap
- supporting the long-term FYDP goal, not just immediate proposal writing

## Screening preference order
1. Papers directly solving Lorenz-1960 or very close Lorenz-family systems
2. Papers using plain ANNs for ODE solution approximation
3. Papers comparing ANN architectures for differential equations
4. PINN / DeepONet papers that act as baselines or contrast
5. Broader survey / paradigm papers only when they sharpen framing

## Exclusion rule
Do not count the three seed papers already present in the workspace as recurring finds. They remain background references only.
