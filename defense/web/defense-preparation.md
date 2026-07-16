# FYDP-I Defense Preparation

**Project:** Solving the Lorenz ODE System using Optimal ANN Architectures
**Team:** Paradox (UIU, CSE)
**Supervisor:** Dr. Muhammad Nomani Kabir
**Course teacher:** Dr. Md. Motaharul Islam
**Defense date:** 15 June 2026

This is your full prep sheet. The goal is simple. Know your numbers, know your one big framing, and have a calm answer ready for every likely question. Sections 1–9 are what you rehearse; sections 10–11 are the deep technical fallback if the panel pushes hard on the math.

---

## 1. Numbers to memorize

You should be able to say these without looking.

- **The system:** Lorenz-1960, three linked nonlinear equations.
- **The equations:** dx/dt = -0.10 yz, dy/dt = +1.60 xz, dz/dt = -0.75 xy.
- **Constants come from:** the reduced form with k = 2, l = 1.
- **Start values:** x = 0.5, y = 0.75, z = 1. Time runs from 0 to 1.
- **RK4 setup:** step size 0.001, 1001 points.
- **SciPy setup:** DOP853 solver, rtol = 1e-10, atol = 1e-12.
- **Split:** 80 train, 20 validation. Seed fixed at 42. z-score normalization on the targets.
- **Training (Phase 1):** Adam, learning rate 1e-3, up to 10,000 epochs, full-batch, early stopping with patience 500 (restore best-validation weights).
- **The one result:** the two solvers agree to about **1.8e-22 MSE** (that is **RMSE ≈ 1.3e-11**). Target was RMSE under 1e-10.
- **Search size:** Phase 1 is 60 runs. Phase 2 is 9 runs. Total 69.
- **Phase 1 grid:** depth 1 to 4, width 20 / 50 / 100, five activations (tanh, ReLU, sigmoid, GELU, Swish), Adam fixed.
- **Phase 2:** three best networks, three optimizers (Adam, L-BFGS, SGD with momentum).
- **Five metrics:** MSE, MAE, max error, training time, inference time. Plus convergence behavior.
- **Papers read:** 17.

> **Know this one cold:** MSE is the *square* of the error. So an MSE of 1.8e-22 means a typical pointwise error (RMSE) of about 1.3e-11 — which is why the error plot is drawn at the 1e-11 level, not 1e-22. They are the same fact stated two ways. See Q in section 7 if a panelist probes this.

---

## 2. The one big framing (say this if you forget everything else)

This is **FYDP-I**. We have **not trained the networks yet**. That is on purpose. Phase one is about building a solid base. So if a question feels like an attack on "where are your results," answer with this:

> The hard part of any machine learning study is a reference you can trust. If the ground truth is shaky, every later number is meaningless. In phase one we defined a narrow question, found the gap from seventeen papers, locked a controlled sixty-nine-run design, and built a baseline that two independent solvers agree on down to about ten to the minus eleven. Phase two plugs straight into that base.

Keep it confident. The baseline is a real achievement, not a placeholder.

---

## 3. The 60-second pitch (if asked "explain your project")

> Many real systems are described by differential equations that have no clean solution. The normal fix is a numerical solver, but solvers are slow and have to redo the work for every new query. A trained neural network could act as a fast stand-in. Most methods, though, lean on physics-informed tricks. We ask a simpler question. Can a plain network, trained only on data, learn a hard coupled system like Lorenz-1960, and which network shape does it best? In phase one we built and verified the reference data both solvers agree on. In phase two we run a controlled search over depth, width, and activation to find the best plain network and compare it to published physics-informed results.

---

## 4. Anticipated questions and answers

### A. Scope and "why bother"

**Q: You have not trained a single network. What did you actually do?**
Defined a narrow question, found the gap from 17 papers, locked a 69-run controlled design, and built a numerical baseline whose two solvers agree to RMSE ~1e-11. The trustworthy ground truth is the foundation everything else stands on.

**Q: RK4 already solves this small system fast and perfectly. Why use a network at all?**
For this small case, RK4 is cheaper, and we are honest about that. The point is not to beat RK4 here. It is to test whether a plain network can learn a coupled nonlinear system at all, and to find which shape does it best. That lesson carries to larger systems where a trained network gives an instant answer without re-solving. It is also a research and learning goal.

**Q: Why not just build a PINN, since they work better?**
Scope. The open question we found is how far a plain, data-only network can go, with the architecture as the variable. PINNs are already well studied, so we use their published numbers as a benchmark. Keeping physics out of the loss lets us see the effect of the network shape on its own.

**Q: What is the contribution?**
The first systematic depth-by-width-by-activation study for a plain ANN on Lorenz-1960, with a clean separation between architecture effects and optimizer effects, all against a verified baseline.

### B. The Lorenz system and the math

**Q: Why these exact constants, minus 0.1, 1.6, minus 0.75?**
They are the reduced Lorenz-1960 form with k = 2 and l = 1, taken from the original paper. We fix them so the problem is well defined and repeatable. If you want, I can derive them: with k=2, l=1 the prefactor kl = 2, and for dy/dt the bracket is 1/l² − 1/(k²+l²) = 1 − 0.2 = 0.8, times 2 gives 1.60. The other two follow the same way.

**Q: What does coupled and nonlinear actually mean here?**
Coupled means each equation depends on the others. The change in x uses y and z. Nonlinear means the variables multiply each other, like yz and xy. That mix is why there is no simple formula.

**Q: Why only time 0 to 1? Is that not too short?**
For phase one we use a short, smooth window so the baseline and the first networks stay clean. The long-run plot on the background slide shows the bounded, looping behavior over a wider window. Longer intervals and denser grids are listed as future work.

**Q: Is this the chaotic Lorenz attractor?**
No. This is the earlier 1960 "maximum simplification" system, not the famous 1963 chaotic one. In our window it is bounded and quasi-periodic, which makes it a good, controlled test bed. (If a panelist points to the word "chaotic" in our report, see section 7 — it is a loose wording on our side and you clarify it verbally.)

### C. The numerical baseline

**Q: What does the 1.8e-22 number mean? That looks impossibly good.**
It is not the network error. It is the disagreement between two independent solvers, our own RK4 and SciPy's DOP853, on the same problem, measured as MSE. As an RMSE that is about 1.3e-11. When two good solvers agree that closely, it tells us the reference data is trustworthy. That is the only result we are claiming so far.

**Q: Is your RK4 your own code or a library?**
RK4 is our own implementation, with step 0.001 and 1001 points. SciPy DOP853 is the independent cross-check. Two separate routes that agree raise our confidence.

**Q: Why DOP853 and those tolerances?**
DOP853 is a high-order (eighth-order Dormand–Prince), adaptive, high-accuracy solver, good for a smooth problem. The tight tolerances, 1e-10 and 1e-12, push its error well below our target so it can serve as a reference.

**Q: Why fix the seed and report physical units?**
The fixed seed makes the work repeatable by anyone. Reporting in real units (after un-normalizing) keeps the errors meaningful rather than hidden behind scaling.

### D. Methodology and the 69 runs

**Q: Why 69 runs? Where does that number come from?**
Phase 1 is depth 1 to 4, times width 20 / 50 / 100, times five activations, with Adam fixed. That is sixty. Phase 2 takes the three best networks and tries three optimizers, which is nine. Sixty plus nine is sixty-nine.

**Q: Why keep the optimizer fixed in phase one?**
So any difference we see comes from the network shape, not the optimizer. If we changed both at once, we could not tell which one caused the change. Phase two then isolates the optimizer on the best shapes.

**Q: Why these depths and widths and not larger?**
The range is small enough that we can run every combination fully, and wide enough to show clear trends. We are not chasing a record, we are mapping the effect of each choice.

**Q: How do you avoid overfitting on such a small dataset?**
We use an 80/20 split and report the validation error, not the training error, with a fixed seed. Early stopping with patience 500 restores the best-validation weights so a model cannot keep memorizing. Repeated seeds for stability are on the future-work list.

**Q: Why these five activations?**
They cover the common families. tanh and sigmoid are smooth and classic for ODE work, ReLU is the modern default, and GELU and Swish are smooth modern choices. This lets us test the claim from prior work that smooth activations help on ODEs.

**Q: Why Adam, L-BFGS, and SGD with momentum in phase two?**
Adam is the robust default. L-BFGS is a quasi-Newton method that often refines small, smooth problems well and is common in the PINN literature. SGD with momentum is the classic baseline. Comparing them on the best shapes shows how much the optimizer matters.

**Q: Why the waterfall methodology?**
Our goals were clear from the start and each phase feeds the next. That makes waterfall a natural fit and easy to track.

### E. Literature and the gap

**Q: Matthews and Bihlo already solved Lorenz-1960. How are you different?**
They used a fixed PINN and DeepONet (4 hidden layers, 40 nodes, tanh, Adam), with physics in the loss. We use a plain, data-only network and treat the architecture itself as the thing we study. Different method, different question. Theirs is the closest baseline, which is exactly why we benchmark against it.

**Q: How did you pick which papers matter?**
We grouped them by approach. Plain ANN for ODEs, physics-informed networks, operator learning, Lorenz-specific studies, neural ODEs, and hybrid methods. The table in Chapter 2 shows the closest works and what each one leaves open.

### F. Future work and risk

**Q: What if the plain network simply cannot learn it?**
That is still a real result. It would mark the limit of plain networks on coupled nonlinear systems and would justify physics-informed methods. We report either outcome honestly.

**Q: Can the network predict beyond the training window?**
Inside the trained window it fills in time points well (interpolation). Predicting outside the window is harder and is a known weakness of data-only models. We will test on held-out points and note extrapolation as future work.

**Q: What tools and framework will you use?**
Python, with PyTorch for the training pipeline in phase two. The numerical baseline is already done in Python with NumPy and SciPy.

---

## 5. Concept cheat sheet (plain words)

Use these if a panelist asks you to explain a term simply.

- **ODE:** a rule for how something changes over time. Give it a starting point and it tells you what happens next.
- **Coupled:** the equations are tied together. You cannot solve one without the others.
- **Nonlinear:** variables multiply or bend, so doubling the input does not double the output.
- **Initial value problem (IVP):** an ODE plus a known starting state; you integrate forward in time.
- **RK4:** a step-by-step numerical method. Accurate, but it has to walk through every step.
- **DOP853:** a high-accuracy adaptive solver in SciPy. We use it as a second opinion.
- **Ground truth / reference:** the trusted "correct" answer the network is trained and graded against.
- **ANN (plain feedforward):** layers of simple units that learn a mapping from input to output, here from time t to (x, y, z).
- **Depth:** how many hidden layers.
- **Width:** how many units in each layer.
- **Activation function:** the small bend inside each unit that lets the network learn curves.
- **Optimizer:** the method that adjusts the network's weights during training.
- **Epoch:** one full pass of the training data through the network.
- **MSE:** mean squared error. The average of the squared gaps between prediction and truth. Lower is better.
- **RMSE:** the square root of MSE — back in the same units as the error itself.
- **Overfitting:** the network memorizes the training points but fails on new ones.
- **Early stopping:** stop training when validation error stops improving, keep the best weights.
- **Normalization (z-score):** rescale each variable to mean 0, standard deviation 1 so no single variable dominates the loss.
- **PINN:** a network that puts the equations into its loss so physics guides training.
- **DeepONet / operator learning:** methods that learn whole families of solutions, not just one.
- **Surrogate model:** a fast stand-in that gives the answer without re-solving the equations.
- **Generalization:** doing well on data the network did not see in training.

---

## 6. Things to avoid saying

- Do not claim any accuracy result for the networks. You have not run them.
- Do not call the 1960 system "chaotic." It is bounded and quasi-periodic in your window. (See section 7 if asked.)
- Do not say the network will "beat" RK4 on this small problem. The value is the lesson, not the speed here.
- Do not promise PINN-level accuracy. You compare to PINNs, you do not match a claim yet.
- Do not call 1.8e-22 "machine precision." The real error scale (RMSE) is ~1e-11; quote that.
- Do not guess at exact tool versions or numbers you are unsure of. Say you will confirm.

---

## 7. Sharp / trap questions (rehearse these)

These are the ones a careful examiner is most likely to use to test whether you really understand your own work.

**Q: Your slide says MSE 1.8e-22 but the error plot is at the 1e-11 level. Which is it?**
Both — they are the same fact. The plot shows the raw pointwise disagreement, around 1e-11, peaking near 6e-11. MSE squares those errors and averages them, so (≈1.3e-11)² ≈ 1.8e-22. RMSE, the square root of MSE, is about 1.3e-11, which matches the plot. Our NFR target was RMSE below 1e-10, and we are comfortably under it.

**Q: Is 1e-11 machine precision?**
Not quite. Double-precision machine epsilon is about 2e-16. Our solver agreement is at 1e-11, which is several orders above raw machine precision but far below our 1e-10 requirement — exactly what you expect from two well-tuned solvers on a smooth problem.

**Q: By how much did you beat the target — one order or ten?**
Our requirement (NFR2) is RMSE below 1e-10, and we achieve RMSE ≈ 1.3e-11, so about an order of magnitude on RMSE. If you compare squared errors (MSE 1.8e-22 against a 1e-10 scale) the gap looks much larger, but the honest, like-for-like statement is RMSE ~1.3e-11 versus a 1e-10 tolerance.

**Q: Your report calls Lorenz-1960 "chaotic" in places. Is it?**
That is a loose wording we will tighten. The 1960 maximum-simplification system, in our interval, is bounded and quasi-periodic — it is not the chaotic 1963 Lorenz attractor. The dynamics we actually train on are smooth and non-chaotic, which is what makes the baseline so clean.

**Q: There is a typo in your conclusion ("bracelet").**
Thank you, that is a typo for "baseline" and we will fix it in the final version. (Stay calm; do not let one typo rattle the whole answer.)

**Q: If RK4 is the ground truth, how will you ever beat it?**
We will not beat RK4 on accuracy for this small problem, and we do not claim to. The trained network's value is constant-time evaluation at any t without re-solving, and the research value is learning which architecture approximates the system best. Accuracy is judged as closeness to RK4, not superiority over it.

**Q: Why benchmark against PINNs if you never build one?**
The PINN numbers are published (Matthews & Bihlo). Re-implementing a PINN would not answer our question, which is about plain-ANN architecture. Using their numbers as a yardstick is cheaper and keeps our variable — the network shape — clean.

**Q: With only ~1000 points and one initial condition, is this enough?**
For FYDP-I, yes, because the goal is a controlled, repeatable architecture comparison, not a generalization study. Denser grids, more initial conditions, and repeated seeds are explicitly listed as future work.

---

## 8. If you do not know an answer

Stay calm and use one of these:

> That is a good point. We have not tested that yet, but it fits into phase two, and here is how we would approach it.

> I am not certain of the exact figure. I do not want to guess, so I will confirm it from our records and follow up.

> That is outside our current scope, which is the plain network. It would be a fair extension though.

Never invent a number. A calm "we will confirm" looks better than a wrong figure.

---

## 9. Who fields which question

Decide this in advance so there is no awkward silence. Rough split that matches the speech:

| Topic area | Primary | Backup |
|---|---|---|
| Lorenz system, the math, the equations | Member 2 | Member 1 |
| Literature, the gap, research questions | Member 3 | Member 5 |
| Methodology, the 69 runs, training setup | Member 4 | Member 1 |
| Numerical baseline, the result, the numbers | Member 4 | Member 2 |
| Plan, scope, future work, conclusion | Member 5 | Member 3 |
| Activation / optimizer internals (deep math) | whoever is strongest on ML | — |

Whoever owns a question answers first; one teammate may add one sentence, then stop. Do not pile on.

---

## 10. Deep technical reference (fallback for a hard panel)

You will mostly use plain answers. This section is the backup if a panelist wants the real internals. Read it once, understand it, do not memorize word for word.

### 10.1 The Lorenz-1960 system

- Lorenz's 1960 paper, "Maximum simplification of the dynamic equations," reduces atmospheric convection to three coupled modes — the smallest non-trivial truncation. The variables x, y, z are spectral coefficients (mode amplitudes), not positions in space.
- General reduced form (from the paper, Section 4.2): each derivative is a constant times a product of the *other two* variables. With k=2, l=1 the constants become −0.10, +1.60, −0.75.
- It is **conservative and quasi-periodic**, not chaotic. The famous chaotic butterfly is the **1963** system (σ, ρ, β parameters). Do not confuse the two. Our long-run plot over [0, 50] shows smooth bounded oscillation — visual proof it is not chaotic.
- Why it is a good test bed: compact to write, genuinely nonlinear and coupled, no closed-form solution, but smooth enough that a numerical reference is rock-solid.

### 10.2 Numerical methods and the error budget

- **Euler** is first-order: global error O(h). **RK4** evaluates the slope four times per step (k1–k4, weighted 1:2:2:1) for **fourth-order global accuracy**, error O(h⁴). With h=1e-3 that is on the order of (1e-3)⁴ = 1e-12 per the scaling — which is why RK4 lands near machine-level agreement here.
- **DOP853** is an explicit eighth-order Dormand–Prince method with an embedded lower-order estimate for adaptive step-size control. rtol=1e-10, atol=1e-12 force its local error very low.
- The two solvers come from completely different families (fixed-step custom RK4 vs adaptive library DOP853). Independent methods agreeing to RMSE ~1e-11 means the agreement is the *true solution*, not a shared bug. That is the whole point of using two.
- **Mesh dependence:** a classical solver only produces values at its grid points and must re-integrate for any new initial condition or finer grid. A trained ANN learns the continuous map t → (x, y, z) and is evaluated anywhere in the trained range in constant time. That is the motivation for a surrogate.

### 10.3 ANN fundamentals

- Input is scalar time t; output is the 3-vector (x, y, z). Each neuron computes σ(w·input + b); layers stack these. The output layer is linear with 3 units.
- **Universal Approximation Theorem** (Hornik / Cybenko, 1989): a feedforward net with one hidden layer and a non-polynomial activation can approximate any continuous function on a compact set to any accuracy, given enough width. This guarantees a good architecture *exists* — it does **not** tell you which depth/width/activation is best. That gap is exactly our research question.
- Training = minimize the loss over weights by gradient descent; **backpropagation** computes those gradients via the chain rule. We use full-batch (the dataset is tiny, so mini-batch noise would just be a confound).

### 10.4 Activation functions (the part they asked about)

| Activation | Formula | Derivative | Character |
|---|---|---|---|
| Sigmoid | 1/(1+e⁻ˣ) | σ(1−σ) | Smooth, range (0,1), saturates both ends → vanishing gradients, not zero-centered |
| Tanh | (eˣ−e⁻ˣ)/(eˣ+e⁻ˣ) | 1−tanh²x | Smooth, range (−1,1), zero-centered (usually trains better than sigmoid), still saturates |
| ReLU | max(0, x) | 1 if x>0 else 0 | Cheap, no positive saturation, but non-smooth (a kink at 0) and can "die" (stuck-off neurons) |
| GELU | x·Φ(x) (Φ = normal CDF) | smooth | Smooth, slightly non-monotonic near 0, strong modern default |
| Swish / SiLU | x·σ(x) | smooth | Smooth, non-monotonic, self-gated; often edges out ReLU |

- **Why smoothness matters here:** the targets x(t), y(t), z(t) are smooth, analytic curves. A network built from smooth activations is itself smooth with well-behaved derivatives, so it fits smooth curves efficiently. ReLU's output is piecewise-linear — it approximates a smooth curve with many small straight segments and has a discontinuous derivative, which tends to need more capacity for the same smooth fit.
- **What the literature predicts:** Lau & Werth (ODEN) found tanh/sigmoid outperform ReLU/ELU on ODEs and need less training. We do not assume this — we *test* it as a controlled variable (RQ2). That is the contribution.
- **Saturation / vanishing gradient (be ready):** for large |x|, sigmoid and tanh flatten, so their gradient → 0 and deep stacks learn slowly. ReLU avoids that on the positive side but has the dead-neuron issue. GELU/Swish keep a usable gradient while staying smooth.

### 10.5 Optimizers (Phase 2)

- **Adam** = momentum (running mean of gradients, the 1st moment) + RMSProp-style per-parameter scaling (running mean of squared gradients, the 2nd moment), both bias-corrected. Robust, low-tuning, our Phase 1 default at lr 1e-3.
- **L-BFGS** = limited-memory quasi-Newton. It approximates the inverse Hessian (curvature) from a short history of recent gradient/step pairs, so it takes much smarter steps than first-order methods. It shines on **smooth, low-dimensional, full-batch** problems — which is exactly the ODE-fitting setting, and why the PINN/ODE-NN literature leans on it. Downsides: heavier per step, and it needs full-batch (it dislikes gradient noise).
- **SGD + momentum** = first-order with a velocity term that accumulates the gradient direction to damp oscillation. The classic baseline; learning-rate sensitive.
- **Why this comparison is clean:** Phase 1 fixes the optimizer (Adam) so differences come only from architecture. Phase 2 fixes the architecture (top 3 nets) so differences come only from the optimizer. You could not separate the two effects if you searched both at once.

### 10.6 Metrics, normalization, evaluation

- **MSE** (primary) penalizes large errors heavily (squared), good single number for ranking 69 runs. **MAE** is the average absolute error, interpretable in physical units. **Max absolute error** is worst-case (L∞) deviation along the trajectory. **Training time** = cost to fit an architecture; **inference time** = cost to predict the full 1001-point trajectory once trained. Together they map the accuracy-versus-cost trade-off in RQ2.
- **z-score normalization** is computed from the training set only, applied to x, y, z so the loss is not dominated by whichever variable has the largest range. All reported errors are un-normalized back to physical units.
- **Overfitting control:** 80/20 split, validation-based early stopping (patience 500, restore best weights), report validation not training error, fixed seed for reproducibility.

---

## 11. Final checklist before you walk in

- [ ] Everyone knows their slides and handoff line.
- [ ] Each person can say the 60-second pitch alone.
- [ ] The whole team agrees on the one big framing in section 2.
- [ ] The number story is straight: MSE 1.8e-22 = RMSE ~1.3e-11, target RMSE < 1e-10 (section 7).
- [ ] You can say, calmly, that Lorenz-1960 is quasi-periodic, not chaotic.
- [ ] You have run the full talk out loud at least three times with a timer.
- [ ] Numbers in section 1 are memorized.
- [ ] Laptop, backup PDF, and adapter are ready.
- [ ] Question routing in section 9 is agreed (who fields math, method, results, future work).
