# Delivery plan: readers that discover (E-072 to E-075)

**Status:** approved by the operator on 2026-10-08 (D-079), then **amended by the operator's
review the same day: see "Amendment 1" at the end. The amendment is a proposal, waiting for
a review by a strong model before anything is built.** It follows E-068, which closed on
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
removed. *(Amendment 1: under the new window standard, a held idea can run on blocks other
than 2022-2023 rather than waiting for E-072's split.)*

---

## Amendment 1 (operator review, 2026-10-08): never test an idea where it was observed

**Status: proposal, not built.** The operator reviewed what was built overnight (E-072, PR
#340; E-073 steps 1-2; CUL-414; CUL-415; E-074 slice 1) and changed the design in a
conversation. This section records the reasoning step by step (what we had, what we
observed, what we decided), so that a reviewer can follow it and judge both the reasoning
and the outcome. **Nothing in this amendment is built yet.**

### A1.1 The path to this amendment

**Step 1: what E-072 built (PR #340, merged, flag `explore_confirm`, off).**
- Inside one run, the six windows are split in time order: 2022 = exploration, 2023 =
  confirmation (`tools/explore_confirm.py::split_windows`).
- Readers get reports rebuilt from the 2022 windows only (`build_reports.restrict_sources`).
  Totals over all windows are withheld, and numbers in AI-written text are masked as
  `<n>` (`mask_numbers`).
- A reader's side finding is then routed (`finding_route`):
  - a price-only claim is measured straight away on the 2023 bars, with the existing claim
    measurement (statistics on bars.csv, not a backtest);
  - a strategy-block claim is "pending" until the run built from it is backtested
    (`resolve_pending`). That result is labelled "weak", because step 1a, which writes the
    next run's card, still reads all-window results from the knowledge base.

**Step 2: the operator's first question.** "Readers take the raw data and observe; what does
'their ideas were tested on the same years' mean?"
- Clarified:
  - Readers do not get raw data. They read code-computed reports. The analyst (E-075, not
    built) is the one that would query raw data.
  - The problem was exactly the operator's reading: the next run was backtested on the same
    windows where the idea was observed (run_070's readers → run_074, same six windows). So
    "+0.054, 6/6 windows" was found where it was looked for.

**Step 3: the operator's second question.** "Do readers code and re-measure? That would
duplicate the backtest in a post-backtest analysis."
- Clarified: readers only fill a fixed 4-slot test (selector / outcome / baseline /
  statistic). The existing `claim_measure` computes one statistic on saved bars, with no
  positions, trades or costs. So it answers "does the pattern exist in prices?", not "does a
  strategy make money?". The latter always goes through the real engine in the next run.

**Step 4: the operator's objection, which changed the design.**
> "For a more complete claim, like 'the strategy in a trending regime seems to close the
> order too early', it cannot be done straight after. I'm not convinced a cheap statistical
> check is worth it. It should not be a claim in that way, but internal thinking of the
> analyst that gives a claim at the end. It should never be mentioned here."

Assessment (agreed):
1. The product is a strategy, not a pattern. A pattern that holds says nothing about profit
   after costs.
2. Strategy-behaviour claims (exits, regimes) cannot be measured in-run anyway. Two routes,
   one per claim type, add complexity for little value.
3. The cheap check spends the only unseen data (2023) on patterns, leaving less for the
   real test.
4. Pattern checks belong in the analyst's reasoning (E-075 queries), not in the deliverable.
5. Cost of the change: we lose a cheap filter before a run. The analyst's own queries, on
   the data it reads, play that role, without touching unseen data.

**Step 5: the operator's generalisation, which replaced the 2022/2023 split.**
> "We are designing the engine on what is available right now. I would like it
> standardised: test an idea observed on one window on a different window. Proposal: link
> the idea to the protocol (its time windows) where it was observed, and make the run about
> the idea use another protocol with separate windows. Or: randomly generated windows with
> fixed characteristics (e.g. 6 separate windows, a minimum and a maximum length), picked
> automatically from the available data. I don't want to over-engineer."

Assessment (agreed):
- **The general rule:** never test an idea on the windows where it was observed.
- **Why it beats the in-run split:**
  - readers can see everything about the run they read, so nothing needs hiding;
  - step 1a's leak disappears (it is no longer about one run's 2023);
  - masking, withheld totals and the "weak" label become unnecessary.
- **Combined proposal**, the operator's two ideas made as simple as possible: fixed blocks,
  then a seeded random draw (A1.3).

**Step 6: the operator's question on the blocks.** "Is it pre-made?"
- Today's state:
  - nothing is pre-made;
  - a run's brief gives start, end and window length;
  - `_generate_monthly_windows` (`run_phase1_research.py`) cuts them into back-to-back
    windows;
  - `_assert_windows_clear_of_holdout` and the data-availability gate check them.
- So three of the four steps below reuse existing code. Only the draw and the "observed on"
  record are new.

**Step 7: the operator's review of E-073 to E-075 under the new design.**
> "E-073: I think it is still needed. The agent may observe raw prices internally and need
> the numbers explained and checked, but we will no longer have the cheap statistical
> check, so maybe the epic needs revisiting. E-074: the exploration digest is a statistical
> check; it might be incorporated into the analyst's way of thinking as tools, not exposed
> and coded outside the agent. And E-075, for me, was to replace the readers: a switch from
> readers that observe based on metrics and generate a claim, to an analyst (that will be
> the reader) that applies a set of tools to raw data to observe and propose, then
> generates the claim."

Assessment (agreed, with one nuance per epic):
- **E-073 stays, with more weight.**
  - The data dictionary: an analyst querying raw data must know each column.
  - The output fixes CUL-414 to CUL-417: they fix the numbers that decide whether a
    *backtest* passes, whatever the readers become.
  - E-029 and E-027: a claim like "closes too early in trends" needs the trade record to
    carry regime_at_exit and the exit cause.
  - *Nuance:* step 2 (PR #346, citation check against the reports) is transitional, because
    the analyst's evidence is its own logged query results. Proposed: hold #346 unmerged
    until the readers' fate is decided; in-run dedup may return for analyst sessions.
- **E-074 folds into E-075 as analyst tools.**
  - The code-built digest handed to readers is the pre-chewed statistical check that Step
    4 dropped.
  - What survives: its grid as a callable tool (a conditional effect by hour, regime or
    volatility), and `trailing_vol` (PR #348) as a field those tools use.
  - The family-wise chance line loses its role as a gate: the protection against chance
    findings is now the backtest on unseen blocks. Counting the analyst's queries stays as
    a record.
- **E-075 replaces the readers.** One step reads the metrics, queries the raw data with
  tools, reasons about why, then proposes one strategy change into the backlog. Open: one
  analyst or five lens sessions (cost ≈ $0.7-1.2 per session, estimate, against ≈ $0.39
  per run for today's five readers), and a pilot redesigned as "analyst vs today's readers"
  on the same saved runs, each proposal backtested on unseen blocks, with the placebo as a
  sanity check.

### A1.2 Before and after, per decision

| # | Before (plan of 2026-10-08 morning, E-072 as built) | After (operator review) |
|---|---|---|
| 1 | A reader's side finding is measured or becomes a run | A reader proposal becomes a **candidate in the idea backlog**, ranked by decide-next like any other. It is a possible run, not an automatic one (decide-next already does this) |
| 2 | Price-only claims get an in-run statistical check on the 2023 windows | **No in-run check.** Pattern checks are internal reasoning of the analyst, never a deliverable |
| 3 | Side findings may be market observations (pure claims) | **A proposal must be a strategy change** (a setting, a block, an exit rule). Market observations stay in its explanation, as the "why" |
| 4 | Inside a run: readers see 2022, confirmation on 2023 | **Every run records the windows its results came from. A run built from an idea uses windows the idea was not observed on** |
| 5 | Step 1a's all-window view made follow-up confirmations "weak" | Moot: the test happens on other windows |
| 6 | Windows fixed per brief (the same 2022-2023 windows since run_065) | **Windows drawn from a block calendar** (A1.3) |
| 7 | E-073: dictionary, then citation check + dedup for readers, then E-029/E-027 | **Dictionary, the output fixes (CUL-414..417), E-029/E-027.** Citation check (PR #346) held until the readers' fate is decided |
| 8 | E-074: a code-built exploration digest given to the readers, with a chance-line gate | **Folded into E-075 as analyst tools.** `trailing_vol` kept; no digest wiring to readers; query counting kept as a record, not a gate |
| 9 | E-075: a sixth reader (pilot), next to the five readers | **The analyst replaces the readers.** One or five sessions to decide; the pilot compares the analyst with today's readers, every proposal backtested on unseen blocks |

### A1.3 The proposed window standard

1. **Calendar:** call `_generate_monthly_windows` once over the research period. For
   example, 2018-01-01 → 2023-12-31 in 4-month blocks gives 18 blocks. It is deterministic
   and nothing is stored by hand.
2. **Usable blocks per coin and timeframe:** the existing coverage checks
   (`data_availability_gate.py`, `variant_coin.window_coverage`) drop blocks without enough
   data.
3. **The draw (new):** take N blocks (e.g. 6) at random, with a seed recorded in the
   protocol:
   - excluding the blocks the idea was observed on;
   - at most 2 per year, so a draw cannot sit in one market phase;
   - never the sealed holdout, never the validation period (2024-2025, CLAUDE.fork.md data
     splits).
4. **Into the protocol:** the drawn blocks become the run's `windows`, where they are
   written today. The backtest, reports and grid work unchanged.
5. **"Observed on" (new):** each candidate in the backlog carries the windows of the run(s)
   whose results produced it.

### A1.4 Known limits

- **Data runs out.** 18 blocks with 6 per run: one idea's line goes about 3 generations deep
  before unseen blocks run out. More years and coins (E-066) push this back.
- **Another coin is also unseen data.** An idea observed on BTC can be tested on ETH over
  the same period, so a unit could be coin × block. That gives more room, but coins are
  correlated, so it is weaker evidence.
- **Comparisons are within the run.** A child run's numbers cannot be compared with its
  parent's, because the windows differ. It is judged against its own base variant,
  buy-and-hold and flat, as the grid does today.

### A1.5 Impact on what was built and planned

- **E-072 (merged, flag off):**
  - the in-run split, masking and in-run confirmation are replaced by A1.3;
  - proposed: keep the flag off and retire that code in a later cleanup PR;
  - still useful: the confirmation ledger idea (counting looks), reused to count how often
    each block has been used.
- **E-073:** the dictionary (merged) and the output fixes (CUL-414, CUL-415, then CUL-416,
  CUL-417) stay; E-029 and E-027 gain weight. The citation check (PR #346) is held as
  transitional (Step 7).
- **E-074:** folded into E-075 as analyst tools (Step 7). `trailing_vol` (PR #348) stays.
  The digest grid becomes a callable tool, computed on the windows of the run the analyst
  reads. There is no wiring to readers and no chance-line gate.
- **E-075 (analyst):**
  - its queries run on the run's own windows, as internal reasoning;
  - its output is a strategy-change proposal into the backlog;
  - **the pilot changes cost and shape:** confirming a strategy proposal now needs a
    backtest on unseen blocks. For saved runs 065-074 (all 2022-2023), that means blocks
    from 2018-2021. Backtests are local compute, not API cost, but each pilot session needs
    one, so the pilot takes longer.

### A1.6 Open questions for the reviewer

1. **Scope of "observed".** Readers also read earlier runs' findings and the registry
   summary, and step 1a reads the whole knowledge base. So an idea's author has seen
   summaries of every earlier run's windows, not only its parent's.
   - Should the excluded set be the idea's own lineage, or every window whose results
     reached any AI step (campaign-wide)?
   - Campaign-wide is stricter, but with 18 blocks it is used up in about 3 runs.
   - Is there an honest middle (e.g. memory keeps verdicts and no per-window numbers), or
     must we accept and record the exposure?
2. **Block length and count.** 4-month blocks and 6 per run is today's shape. Shorter blocks
   give more of them but each has fewer trades (the 100-trade floor). What is the right
   trade-off, and should the draw ensure each block has enough bars for warm-up?
3. **Random draw vs a fixed rotation** (e.g. a seeded shuffle of the calendar, taken in
   order). Is randomness needed, or is a fixed rotation simpler and as honest?
4. **Was dropping the in-run check right?** It was the only fast filter before spending a
   run. Is the analyst's internal reasoning (its queries on the run it reads) a sufficient
   replacement?
5. **Retire E-072's code, or keep it as an option?**
6. **The analyst replacing the readers (Step 7):**
   - one analyst, or five lens sessions?
   - is the redesigned pilot (analyst vs today's readers on saved runs, every proposal
     backtested on unseen blocks, placebo as a sanity check) sound, and what does it cost
     in backtests?
   - should the citation check (PR #346) be dropped, or kept for the analyst's citations of
     its own query results?
7. **What did we miss?** Is there a simpler standard that meets "never test where you
   looked" without the data running out so fast?

**Reviewer: please give your opinion on both the reasoning (steps 1-7) and the outcome
(A1.2-A1.5), challenge it fairly, and propose changes.**
