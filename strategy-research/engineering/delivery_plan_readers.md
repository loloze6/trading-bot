# Delivery plan: readers that discover (E-072 to E-075)

**Status:** approved by the operator on 2026-10-08 (D-079). It follows E-068, which closed on
2026-10-06 (`roadmap/E-068/CLOSE_OUT.md`, `delivery_plan_v26_continuation_2.md`). The epics
are in Linear: E-072 (P-CUL-80), E-073 (P-CUL-81), E-074 (P-CUL-82) and E-075 (P-CUL-83).
Each epic carries its own details and done-when criteria. This file records why the plan
looks the way it does.

## The goal

Find claims and observations that are **proven** and that lead to a **profitable strategy
when combined**. The operator values logical observation and asking **why**, and wants no
growing pile of code written for one case at a time.

## Where we started (facts, 2026-10-06/08)

- **The readers see a run only through metrics chosen in advance.** Each of the five readers
  (profitability, trade efficiency, forecast power, regime power, component attribution)
  makes one closed-book Haiku call. It receives instructions, the vocabulary (component
  catalogue, claim-test blocks), the idea (hypothesis card, manifest), the strategy (config,
  variant patches), pre-computed results (its own report, the grid, the claim digest) and
  memory (findings summary, registry summary). It receives **no raw data**.
- **How readers find a new idea today:** by free observation, with no method. The only
  instruction is "a side finding is something else the evidence shows".
- **Every run since run_065 uses the same six windows** (2022-01 to 2023-12). A reader
  proposes an idea after seeing 2022-23 results, and the next run "tests" it on the same
  bars. That is in-sample, and it will tend to confirm. run_074's "+0.054, 6/6 windows" is
  exploratory, not independent evidence.
- **The backtest output records most of the calculation but not every decision.** Missing:
  why a forecast is zero (including a forced flatten after a data gap, or the end of the
  backtest), and the decision on each trade. Those are E-027 and E-029, which already exist.
  No document explains what each output field means.

## How the plan was made

- **Two independent model reviews of the question list.** The draft asked readers 8
  questions, from observe to why. The reviews moved the checking to code and left the
  readers the thinking: a "why" that must be checked in the data, a falsifier on every
  proposal, and each reader kept in its own lens.
- **A third review of that version** found it had become a form that a small model fills in
  mechanically, without discovering anything.
- **The operator then asked whether readers should see the raw data.** Pasting raw data into
  a prompt does not work: millions of tokens, and a model skims a large table instead of
  analysing it. A tool does work: the reader asks questions and our code answers them.
- **Two reviews of the restructured plan** (one on the goal, one on feasibility) found:
  - the windows problem above;
  - that free code cannot be contained on Windows: it can open any file (including the data
    cache with the sealed holdout) and read the environment, where exchange keys may exist;
    it also hides how many comparisons were made;
  - that a looks count must count comparisons, not calls;
  - that some planned "guard rails" were case-by-case patching.
- **A last review adjusted the plan into four epics.** The operator decided the points where
  it differed from earlier decisions (below).

## The plan, in order

1. **E-072: ideas are confirmed on data the proposer never saw** (first: a validity defect).
   - Exploration windows (e.g. 2022) and confirmation windows (e.g. 2023) are fixed in
     advance. Readers see exploration results only.
   - Each proposal is measured on the confirmation windows: in the same run for price-only
     ideas, in the next run for strategy-block ideas. The result is recorded as "sign held:
     yes / no / pending".
   - Confirmation looks are counted, because the confirmation set gets used up over time.
     More years come from E-066.
2. **E-073: observable backtest.**
   - First, a data dictionary for every field the AI steps read, audited against the engine.
   - Then two small generic reader checks: citations checked against their values (with one
     retry), and duplicates removed within the run.
   - Then E-029 (the trade record carries the decision) and E-027 (why a forecast is zero).
3. **E-074: exploration digest.**
   - Code computes a fixed, pre-declared grid on the exploration windows, from the per-bar
     data and the trades, adapted to the timeframe.
   - It carries one chance line, judged across the whole digest. Cells are ranked by effect
     size, never by how many windows agree.
   - It is given to the readers.
4. **E-075: the analyst, a pilot.**
   - A sixth reader explores the raw data through about 6 fixed query functions with free
     parameters, over both the per-bar data and the trades. Our code runs them on the
     exploration windows only. It has the full run context. Every query is logged and
     counted.
   - The pilot runs offline on saved runs: 10 real sessions and 10 placebo sessions, about
     $10-15 (estimate).
   - Go only if real proposals hold on unseen windows clearly more often than placebo ones.

## Decisions taken (operator, 2026-10-08)

- **The analyst pilot runs right after the digest.** It does not wait for 6 normal runs:
  that would take weeks, and 6 runs are too few to decide anything.
- **Engine outputs:** the dictionary and the audit first, then E-029 and E-027. The
  regime-rule inputs and the intermediate transform steps are added only when a query needs
  them.
- **Dropped:**
  - the code-built "rivals table": case-by-case patching; the readers rule rivals out from
    the slices they already have;
  - counting two readers' identical proposals as agreement: they share inputs, so they are
    not independent.
- **Deferred:** a fixed reasoning-question format for the readers. The reviewed list is
  kept in the reviews' conclusions above, for later.
- **The honest bar:** with 3 exploration and 3 confirmation windows on 2 coins, "proven" is
  not reachable. The achievable bar is "the sign held on unseen windows, counted against the
  number of looks". Proof needs more data (E-066).
- **Flags:** one switch per epic. The old v2 readers are retired once v3 is the only path in
  use.

## Parked

- the rivals table;
- agreement weighting;
- the reasoning-question format;
- regime-rule inputs and transform steps;
- E-019 (one leak-checked feature table);
- CUL-394 (automatic verdicts);
- E-069 (one model per AI step);
- E-071 (combining blocks), which this plan feeds.

## The held ideas

component_attribution-run_071-1 and trade_efficiency-run_073-1 stay held until E-072 exists.
Both came from readers that saw the 2022-23 results, so running them now would be
in-sample. trade_efficiency-run_073-1 is also an old-format patch idea, which PR #336
removed.
