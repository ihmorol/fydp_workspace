# FYDP-I Defense Speech

**Project:** Solving the Lorenz ODE System using Optimal ANN Architectures
**Team:** Paradox (UIU, CSE)
**Deck:** `slides.pptx` (16 slides)
**Length:** about 8 to 10 minutes
**Style:** plain spoken English. Read it like you are talking, not reading.

---

## How the talk is split

Five speakers, three to four slides each, about two minutes per person.

| Speaker | Slides | Topic |
|---|---|---|
| Member 1 | 1, 2, 3 | Open, roadmap, the problem |
| Member 2 | 4, 5, 6 | Goals, the Lorenz system, ANN vs PINN |
| Member 3 | 7, 8, 9 | Literature, the gap, our questions |
| Member 4 | 10, 11, 12 | Method, baseline, the one result |
| Member 5 | 13, 14, 15, 16 | Plan, conclusion, references, close |

(Slide numbers count the research-questions slide as slide 9. Adjust by one if your export differs.)

## Quick delivery tips

- Look up at the panel, not at the screen.
- Slow down on the equation slide and the result slide. Speed up on the roadmap and references.
- The handoff line is the last thing you say. Say the next person's name, then step back.
- If you blank, read the slide title out loud and keep going.
- Do not read the bullets word for word. The slide is the picture, you are the voice.

---

# The speech, slide by slide

---

## Slide 1 — Title
**Speaker: Member 1**
*On screen: project title, team, supervisor.*

> Good morning, everyone, and thank you for being here. My team and I will walk you through our FYDP-I work.
>
> Our project is "Solving the Lorenz ODE System using Optimal ANN Architectures." In plain words, we ask one question. Can a simple neural network, with no physics built into it, learn a hard set of linked equations? And if it can, which network shape does it best? Let me start with the map of our talk.

---

## Slide 2 — Roadmap
**Speaker: Member 1**
*On screen: six numbered cards.*

> We move through six parts. First the problem and what we set out to do. Then a little background on the Lorenz system, and how a plain network is different from a physics-informed one. After that, our method, which is a careful search across sixty-nine training runs. Then the numerical baseline we built and checked. We finish with our plan for the next phase and where we stand today.

---

## Slide 3 — The problem
**Speaker: Member 1**
*On screen: three cards, central question banner.*

> So why is this hard? Three reasons. First, equations like Lorenz-1960 have no clean formula. You cannot just solve them by hand. Second, the usual numerical solvers do work, but they are slow. They march step by step, and they redo all of that work for every new question. Third, most neural network methods get a little help. They push the physics into the training to make it easier.
>
> Our central question is in the box at the bottom. Can a plain network, trained only on numbers, with no physics in the loss, still learn the Lorenz solution? And which shape works best? For that, I will hand over to my teammate.

---

## Slide 4 — Objectives
**Speaker: Member 2**
*On screen: four goal cards.*

> Thank you. We set four goals. First, build a reference we can trust. We solve the system two ways, with our own RK4 code and with SciPy, then check one against the other. Second, search the network space. We change the depth, the width, and the activation function in a controlled way. Third, measure both sides at once, the accuracy and the cost. So the error, but also training time and run time. Fourth, compare our best plain network against the physics-informed results other people have already published.

---

## Slide 5 — The Lorenz system
**Speaker: Member 2**
*On screen: three equations, settings, long-run plot.*

> Here is the system itself. Three equations, and they are linked. Linked means each one feeds the others. The settings on the right are fixed. We start from these three values and run time from zero to one.
>
> The equations look small. But that linking, and the way the variables multiply each other, is exactly what makes them hard to solve accurately. The plot on the right shows the behavior over a longer window. It stays inside bounds and keeps looping.

---

## Slide 6 — ANN vs PINN
**Speaker: Member 2**
*On screen: two architecture images, scope banner.*

> This slide shows the difference between our approach and the popular one. On the left is the plain network. It just learns to map time to x, y, and z from data. On the right is a physics-informed network. It puts the equations right into its loss.
>
> Our scope is the left side only. We do not build a PINN. We only use published PINN numbers later, as a yardstick. Over to my teammate.

---

## Slide 7 — Literature
**Speaker: Member 3**
*On screen: comparison table, our row highlighted.*

> Thank you. We read seventeen papers. This table shows the closest ones. Matthews and Bihlo solved the same Lorenz system, but with a fixed PINN and DeepONet. Aslam and others tuned the weights with an optimizer, not the shape. Mall and Chakraverty used a tiny network with one activation. Lau and Werth found that tanh and sigmoid beat ReLU, but they did not study depth and width. The bottom row, in orange, is us. We do the systematic search that nobody else did on this system.

---

## Slide 8 — The gap
**Speaker: Member 3**
*On screen: four gap cards.*

> So the gap is clear. There is no proper depth-and-width study for a plain network on Lorenz. Nobody compares a plain network and a PINN on the very same problem. The activation function is almost never treated as a real variable. And past work changes one thing at a time, never depth and width together. That is the space we step into.

---

## Slide 9 — Research questions
**Speaker: Member 3**
*On screen: RQ1, RQ2, RQ3.*

> This turns into three questions. One, can a plain network learn the solution from data alone? Two, which mix of depth, width, and activation gives the best balance of accuracy and cost? Three, how close does our best plain network get to the physics-informed baselines? My teammate will take the method.

---

## Slide 10 — Methodology
**Speaker: Member 4**
*On screen: two phases, pipeline strip.*

> Thanks. Our study has two phases. In phase one we search the shape. Depth from one to four layers, width of twenty, fifty, or one hundred neurons, and five activation functions. With the optimizer fixed to Adam, that gives sixty runs. In phase two we take the three best networks and change only the optimizer, Adam, L-BFGS, and SGD with momentum. That is nine more runs. Sixty-nine in total.
>
> The strip at the bottom is the same loop every time. Generate the data, split it, train, score it on five measures, and pick the best.

---

## Slide 11 — Numerical baseline
**Speaker: Member 4**
*On screen: baseline settings, reference trajectory.*

> Before any network, we need a ground truth. We built it with care. Our RK4 code uses a tiny step and just over a thousand points. SciPy uses its high-accuracy DOP853 solver with very tight tolerances. We split the data eighty to twenty and fix the random seed, so anyone can repeat it. All errors are reported in the real physical units. The plot is that reference path for x, y, and z.

---

## Slide 12 — The result
**Speaker: Member 4**
*On screen: validation plot, big number.*

> And here is the one hard result we have so far. We checked the two solvers against each other. They agree down to about ten to the minus twenty-two. That is basically machine precision. Our target was only ten to the minus ten, so we are far past it.
>
> This matters because this path is the ground truth. Every network we train next will be measured against it. My teammate will close us out.

---

## Slide 13 — Plan and what's next
**Speaker: Member 5**
*On screen: three-phase timeline, next steps.*

> Thank you. Here is where this sits in the full timeline. Phase one, this phase, is done. We have the problem, the literature review, the requirements, and the verified baseline. Phase two is the experiments, the full set of runs with all the measures and plots. Phase three is the analysis and the final report.
>
> Our immediate next steps are to build the training pipeline, run the sixty phase-one networks, and pick the best three. Later we add repeated seeds, denser grids, and the direct PINN comparison.

---

## Slide 14 — Conclusion
**Speaker: Member 5**
*On screen: what's done, what it gives us.*

> To sum up where we stand. We have a clear, narrow question. We have a seventeen-paper review with a real gap. We have a locked two-phase design of sixty-nine runs. And we have a baseline that is verified.
>
> What this gives us is the first systematic plain-network study on Lorenz-1960. We can cleanly separate the effect of the shape from the effect of the optimizer. We are not claiming accuracy yet. Those claims wait for the evidence in phase two.

---

## Slide 15 — References
**Speaker: Member 5**
*On screen: selected references.*

> These are the main papers behind our work, from Lorenz's original 1960 paper to recent neural ODE methods. The full list of seventeen is in our report.

---

## Slide 16 — Thank you
**Speaker: Member 5**
*On screen: thank you, supervisor credits.*

> That is our FYDP-I work. Thank you for listening. We would be glad to take your questions.

---

## Timing check

| Block | Speaker | Target |
|---|---|---|
| Slides 1-3 | Member 1 | ~1:45 |
| Slides 4-6 | Member 2 | ~1:45 |
| Slides 7-9 | Member 3 | ~1:30 |
| Slides 10-12 | Member 4 | ~1:50 |
| Slides 13-16 | Member 5 | ~1:40 |
| **Total** | | **~8:30** |

Leaves a small buffer inside a 10-minute slot. If you run long, trim the long-run plot line on Slide 5 and the references line on Slide 15.
