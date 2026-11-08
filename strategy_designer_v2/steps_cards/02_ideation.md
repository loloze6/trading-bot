# Step card: Ideation (draft for the operator, 2026-11-08)

## Objective, one question
From a research question (the brief), produce many distinct trading ideas, each one testable with numbers and each one usable as the thesis of a linear strategy.

## What an idea is, in the operator's words
A pattern in market data that can be computed at a bar's close, that says what the market will do next, that has a reason to exist, and that can be tested against a pass mark fixed before the data is seen. The stronger the pattern, the larger the position in its direction; never on or off.

## Hand-over
A list of ideas. Each idea carries:
1. **Statement**: one sentence, plain words, what pattern and what it predicts.
2. **Reason**: why the pattern should exist (who pays, who is forced, who is slow).
3. **Kind**: signal (predicts the next move), state (says when a signal can be trusted), or rule (how to hold, size or exit). One idea may combine a signal with a state inside its rule.
4. **Position rule**: how the idea becomes a graded position each bar, computable from past bars only, in words first and as a few lines of code.
5. **Horizon**: over how many bars the prediction is meant to hold.
6. **Test**: what number would show the idea is real, and how it is computed from a backtest's output. The pass mark itself is not the idea's to set.
7. **Why it cannot look ahead**: one line.

## Quality criteria on the hand-over
- Distinct: two ideas that differ only by a parameter are one idea.
- Numerous: a brief with scope should yield eight or more; a narrow brief may yield fewer, with the reason stated.
- Testable: every idea's test can be computed from bars and from a backtest's output; no idea needs data the brief does not give.
- Linear: no position rule is a switch; a state gates the size, it does not flip it.
- Honest: ideas that contradict each other are allowed; an idea already tried is not repeated.
- Faithful to the brief: nothing outside its scope, everything in its scope considered.

## Fixed inputs for the iterations
Three briefs, already written: the operator's daily breadth brief; the hourly overreaction brief; the time-of-week brief. One list of ideas already tried per brief.

## Variants to compare
- Instructions: (a) the current prompt; (b) a prompt built from this card, the three kinds named; (c) variant (b) with a worked example of each kind.
- Models: two, the one used today and a stronger one.
- Inputs: the brief alone; the brief plus the tried list; the brief plus a short note on what a linear strategy can and cannot express.
Twelve runs of one model call each; outputs side by side in one folder.

## Who judges the output
The operator, reading the lists against the quality criteria, idea by idea. Code checks only shape (every field present, code parses, no future reference). Nothing is backtested in this iteration.

## Done when
The operator can read a list and say for each idea "yes, that is an idea" or "no, and here is why", and the "no" reasons stop recurring across two consecutive iterations.

## What this step does not do
It does not design the strategy config, run a backtest, judge profitability or pick the next idea. Those are other steps with their own cards.
