# Workflow v2: the spine on one page (draft for the operator, 2026-11-05)

A proposal, written from the operator's tour remarks. The operator corrects it; nothing here is built.

## The rule of v2
v2 starts empty. A v1 piece enters v2 only by hand, one at a time, with a one-line reason, when a v2 run asks for it. Nothing is copied by default. Complexity has to earn its place.

## The goal
A pipeline that finds a profitable trading strategy by itself, runs on its own, and does not fool itself. The operator decides; the pipeline discovers.

## The path, one idea at a time
1. **Brief.** The operator writes what to research and where to trade. Four mandatory lines: research goal, venue, product, strategy domain. Everything else is optional and decided later by the pipeline.
2. **Ideas.** An AI reads the brief and writes many distinct ideas, each as a claim: what is believed, how it will be measured, and what counts as pass. The claim is the judge of its own run, fixed before any backtest.
3. **Config.** An AI turns one claim into one strategy config for the engine. Code checks the config.
4. **Backtest.** The engine runs the config on one fold (a fixed set of test months the idea has never seen). The holdout stays sealed.
5. **Three answers, from the backtest's bars and trades.**
   - Branch 1, the claim: was the idea right? Pass or fail.
   - Branch 2, the analyst: what did we see, what should we try next? Proposals only.
   - Branch 3, profit: is it profitable enough? Pass or fail. The only door to the holdout.
6. **Record.** One structured record per run: the idea, the claim, the config, the three answers, and why. Ideas, claims, runs and results are separate and referenced, so any question about them is one query.
7. **Next idea.** The pipeline picks the next idea from the record and runs it. The operator approves only new ideas (a new brief) and the holdout.

## What the operator keeps in hand
- Writing briefs.
- Approving a new idea that leaves a lineage.
- The holdout: name a config, test it, record the result. One command.
- A periodic step back, by hand, on a strong model, on the process itself.
- Their own decisions and lessons, stored in their words, read by every session.

## What v2 does not have
No criterion menu. No fold confirmation. No deflated Sharpe. No information-only steps. No flags for core behaviour. No stage that cannot run. No record nobody reads.

## Fresh start
New runs, memory, registry, queue and records. The old campaign is frozen read-only and never read by v2. The holdout was never opened and stays sealed.

## Candidate v1 pieces for day one (the operator strikes any)
Used as they are, not copied into v2's loop:
- The trading engine, the backtester and the strategy config format.
- The config validator.
- The claim measurement engine (the part that measures a claim on the bars).
- The holdout seal: the policy reader and the data feed refusal.
- The fold loader.
- The analyst's fenced query tools with their log (the model sees only what it measured).
- The run viewer.
Everything else waits for a run to ask for it.

## First run
run_101's brief, end to end, as the acceptance test of v2.
