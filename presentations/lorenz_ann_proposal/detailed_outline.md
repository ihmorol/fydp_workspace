# Detailed Outline for Informal Supervisor Research Proposal Deck

## Presentation Goal
This is an informal supervisor-facing deck, so the structure should be direct, defensible, and easy to discuss. The slides should not try to present final results. Instead, they should show that the problem is worth doing, that the scope is technically meaningful, and that FYDP-I has a realistic boundary.

## Slide 1: Title and Problem Statement
**Purpose:** Open the presentation with the topic and the exact research problem.

**Main message:** The project is about solving the Lorenz-1960 ODE system with ANN methods and ultimately identifying the ANN architecture that works best.

**What to say:**
- The benchmark system is Lorenz-1960.
- The long-term question is whether a plain ANN can solve it well and which architecture is optimal.
- The comparison will eventually involve numerical references and PINN-style context.

## Slide 2: Background
**Purpose:** Give the minimum technical context the supervisor needs before the proposal logic begins.

**Main message:** ODEs are central to many physical systems, and Lorenz-1960 is a compact but meaningful nonlinear test problem already used in the literature.

**What to say:**
- ODEs model time-varying physical systems.
- Lorenz-1960 gives a three-equation coupled nonlinear benchmark.
- Paper 1 Section 4.2 is the direct benchmark source for this project.
- Paper 2 and Paper 3 help position the ANN and Neural ODE literature around it.

## Slide 3: Motivation
**Purpose:** Explain why this research direction is worth doing.

**Main message:** Numerical solvers are strong baselines, but ANN-based surrogates may offer useful reuse and comparison advantages if they can be made reliable.

**What to say:**
- Runge-Kutta is accurate, but it is still a solver, not a learned model.
- ANN is interesting because it could give fast reusable approximation after training.
- Lorenz-1960 is a manageable benchmark for studying solver behavior and architecture choices.

## Slide 4: Expected Contribution
**Purpose:** State the value of the project without overclaiming final results.

**Main message:** The proposal contributes a benchmark-driven research direction, an architecture-study plan, a comparison framework, and a reusable workflow.

**What to say:**
- This is not just “ANN solving an ODE.”
- The contribution is in the benchmark framing and the architecture question.
- The work also builds a clean workflow for later experimental phases.

## Slide 5: How Is It a Novel Problem?
**Purpose:** Defend the proposal against the question “hasn’t this already been done?”

**Main message:** Related work exists, but the exact question being asked here is still open enough to justify the project.

**What to say:**
- Existing work includes physics-informed or operator-learning approaches.
- Existing ANN literature does not clearly answer which plain ANN architecture is best for the Lorenz-1960 benchmark.
- The novelty is the architecture-level comparison on a fixed, literature-backed benchmark.

## Slide 6: How Is It a Complex Engineering Problem?
**Purpose:** Show that this is an engineering design and evaluation problem, not only a literature exercise.

**Main message:** The project combines mathematical correctness, numerical validation, implementation quality, model design, and trade-off analysis.

**What to say:**
- The system is nonlinear and coupled.
- The benchmark implementation must be validated carefully.
- ANN architecture search is a multi-factor design problem.
- Final decisions must balance accuracy, stability, runtime, and reproducibility.

## Slide 7: FYDP-I Scope
**Purpose:** Define a realistic current-phase boundary.

**Main message:** FYDP-I focuses on literature review and validated numerical baselines, not final ANN comparison results.

**What to say:**
- Complete the literature review and gap analysis.
- Implement the Lorenz-1960 equations using a Python ODE solver and a custom Runge-Kutta method.
- Optimize and validate the baseline outputs for later ANN work.
- Make it clear that final ANN architecture optimization is later-phase work.

## Slide 8: Discussion / Next Step
**Purpose:** End in a way that invites supervisor feedback rather than pretending the scope is already fully fixed.

**Main message:** The proposal is ready for scope confirmation and method feedback.

**What to say:**
- Confirm whether FYDP-I should remain benchmark-focused.
- Confirm which numerical solver should be treated as the main reference.
- Confirm whether a small ANN prototype is needed in FYDP-I or should wait.

## Suggested Delivery Style
- Keep the tone conversational and direct.
- Do not present the project as if final ANN results already exist.
- Emphasize that the proposal is strong because it is structured, bounded, and benchmark-driven.
