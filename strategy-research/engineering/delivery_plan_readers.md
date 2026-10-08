# Delivery plan: readers that discover (E-072 to E-075)

**Status:** approved by the operator on 2026-10-08 (D-079), then **amended by the operator's
review the same day ("Amendment 1" at the end). A strong model reviewed the amendment and
the operator took decisions on it (A1.7).** Sections above the amendment that it changes
are marked *superseded*.

> **The current design, in one paragraph (read this first).**
> - **The thesis:** confirmed claims carry real information about how **the market**
>   behaves and how **the strategy** behaves in it. Combining confirmed claims leads to a
>   strategy that is profitable after costs.
> - **One or more analysts** (two to start: forecast and trade efficiency) replace today's
>   five readers. Each observes one run's backtest results, digs into its raw bars and
>   trades with fixed tools, and asks why. It ends with **one claim**, a statement about
>   market or strategy behaviour, together with **how a later backtest would confirm or
>   refute it**.
> - **A claim is never confirmed inside the run that inspired it.** There is no in-run
>   statistical check. Pattern checks are only the analyst's internal reasoning.
> - **A claim becomes a candidate in the idea backlog** (decide-next ranks it). If it is
>   picked, it is confirmed only on the output of a **real backtest on a fold of time
>   windows its lineage has not used** (three fixed folds; a line ends after three).
>   Confirmed claims become the building blocks that are combined (E-071).
> - **After the folds** come validation (2024-2025, single-use) and then the holdout.
> - **The analyst's instructions** are designed for that purpose (A1.8, draft v2, under
>   review).

It follows E-068, which closed on
2026-10-06 (`roadmap/E-068/CLOSE_OUT.md`, `delivery_plan_v26_continuation_2.md`). The epics
are in Linear: E-072 (P-CUL-80), E-073 (P-CUL-81), E-074 (P-CUL-82) and E-075 (P-CUL-83).
Each epic carries its own details and done-when criteria. This file records why the plan
looks the way it does.

## The goal

Find claims and observations that are **proven** and that lead to a **profitable strategy
when combined**. The operator values logical observation and asking **why**, and wants no
growing pile of code written for one case at a time.

*Sharpened by Amendment 1:* what we look for are **strategy changes** whose effect holds up
in a real backtest on data they were not observed on, and which combine into a strategy
that is profitable after costs. "Proven" means confirmed on unseen folds, counted against
the number of tries; it never means a statistic computed on the data where the idea was
found.

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

> *Superseded in part by Amendment 1:*
> - **items 1 and 3:** replaced, by the fold standard and by "no in-run check";
> - **item 4:** the analyst replaces the readers, and the pilot is redesigned;
> - **item 2:** kept, with its citation check reused for the analyst.
>
> The list is kept as the record of what was planned and built.

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
- **The honest bar** *(superseded by Amendment 1: the bar is now "the change held in a real
  backtest on unseen folds, counted against tries")*: with 3 exploration and 3 confirmation
  windows on 2 coins, "proven" is not reachable. The achievable bar is "the sign held on unseen windows, counted against the
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
removed. *(Amendment 1: trade_efficiency-run_073-1 has since been marked `superseded`, so
only component_attribution-run_071-1 is held. Under the fold standard (A1.7) it can run on
fold B rather than waiting for E-072's split.)*

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

**Step 8: the operator's decision on one analyst or five.**
> "I was initially thinking five, because each of them would have a specific focus of
> analysis. But we could start with two to see if having this focus really works: for
> example, one on regime and one on forecast. Each new one would replicate the same logic,
> with a separate objective in the design."

Assessment (agreed):
- **Start with two analysts: regime and forecast** *(changed after the review to forecast and
  trade efficiency, A1.7 decision D2)*. They share the same design (same
  tools, same output: one strategy-change proposal into the backlog). Only the objective
  differs, a short lens text, as today's reader lenses do.
- **Why two:**
  - it tests the lens idea itself (do focused analysts propose different, better ideas than
    one general analyst would?) at about 40% of the cost of five;
  - two lenses are enough to see whether their proposals overlap.
- **Adding one later** (profitability, trade efficiency, component attribution) is a new
  objective text, not new code. That is the design constraint.
- **Open for the pilot:** what tells us "the focus works"? A proposed signal: the two
  analysts' proposals differ (little overlap), and each one's proposals hold on unseen
  blocks at least as often as today's matching reader.

### A1.2 Before and after, per decision

| # | Before (plan of 2026-10-08 morning, E-072 as built) | After (operator review) |
|---|---|---|
| 1 | A reader's side finding is measured or becomes a run | A reader proposal becomes a **candidate in the idea backlog**, ranked by decide-next like any other. It is a possible run, not an automatic one (decide-next already does this) |
| 2 | Price-only claims get an in-run statistical check on the 2023 windows | **No in-run check.** Pattern checks are internal reasoning of the analyst, never a deliverable |
| 3 | Side findings may be market observations (pure claims), measured on the run that inspired them | ~~A proposal must be a strategy change~~ *(revised, Step 9)*: **the output is a claim** about market behaviour or strategy behaviour, with **the test a later backtest on an unused fold must pass**. A strategy change appears only as the vehicle that makes the claim observable |
| 4 | Inside a run: readers see 2022, confirmation on 2023 | **Every run records the windows its results came from. A run built from an idea uses windows the idea was not observed on** |
| 5 | Step 1a's all-window view made follow-up confirmations "weak" | Moot: the test happens on other windows |
| 6 | Windows fixed per brief (the same 2022-2023 windows since run_065) | **Windows from three fixed folds** (A1.3 as amended by A1.7, decision D1; the random draw is parked) |
| 7 | E-073: dictionary, then citation check + dedup for readers, then E-029/E-027 | **Dictionary, the output fixes (CUL-414..417), E-029/E-027.** Citation check (PR #346) held until the readers' fate is decided |
| 8 | E-074: a code-built exploration digest given to the readers, with a chance-line gate | **Folded into E-075 as analyst tools.** `trailing_vol` kept; no digest wiring to readers; query counting kept as a record, not a gate |
| 9 | E-075: a sixth reader (pilot), next to the five readers | **The analyst replaces the readers.** The pilot compares the analyst with today's readers, every proposal backtested on unseen blocks |
| 10 | Five reader lenses, one closed-book call each | **Two analysts to start, forecast and trade efficiency** (A1.7, decision D2; regime first proposed, but the regime lens has nothing to read while the detector is ungated): same design, separate objective. A new lens is a new objective text, not new code |

### A1.3 The proposed window standard

> *Superseded by A1.7, decision D1:*
> - **What changes:** the windows come from **three fixed folds** (`config/folds.yaml`), not
>   from the random draw in step 3 below. A child runs on the next fold its lineage has not
>   used, a config runs on a given fold only once, and a lineage ends after three folds.
> - **What stays:** steps 1, 2, 4 and 5 (calendar, coverage, protocol, "observed on"). The
>   end of the calendar is read from the data policy, with a test.
> - **The random draw** is kept as a parked epic.

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
  - the in-run split, masking and in-run confirmation are replaced by the fold standard
    (A1.3 as amended by A1.7, decision D1);
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
6. **The analyst replacing the readers (Steps 7-8):**
   - two analysts to start (regime, forecast), same design and separate objectives: is that
     the right first test of "focus works", and is the proposed signal (low overlap, and
     each holds on unseen blocks at least as often as today's matching reader) measurable
     with the data we have?
   - is the redesigned pilot (analyst vs today's readers on saved runs, every proposal
     backtested on unseen blocks, placebo as a sanity check) sound, and what does it cost
     in backtests?
   - should the citation check (PR #346) be dropped, or kept for the analyst's citations of
     its own query results?
7. **What did we miss?** Is there a simpler standard that meets "never test where you
   looked" without the data running out so fast?

**Reviewer: please give your opinion on both the reasoning (steps 1-8) and the outcome
(A1.2-A1.5), challenge it fairly, and propose changes.**

### A1.7 The strong-model review (Fable, 2026-10-08) and the operator's decisions

The review was read-only and verified against the code. Its main findings:

**Facts it established (verified):**
1. **The root cause sits in one function.** decide-next deep-copies the parent's
   `machine_constraints` into the child's brief (`tools/decide_next.py:2129-2131`). That
   copy is why every run since run_065 reuses 2022-2023, and it is the change site.
2. **Window shopping.** The repeat gate is keyed on the windows (`tools/novelty.py:186-204`,
   `windows_sha256`). With random draws, the same config could be re-run on new draws until
   one looks good.
3. **Memory holds pooled numbers.** It keeps pooled grid cells and idea_status per run, with
   no per-window numbers (`reader_findings.py:299-324`). So "nothing needs hiding" holds for
   a run's own windows, not for cross-run memory.
4. **More data than stated.** Runs since 065 use Kraken. Kraken BTC/ETH/XRP/LTC/XMR/ZEC
   cover 2018-2023 fully; SOL starts 2021-06 and UNI 2020-10. There are 18 four-month
   blocks.
5. **Nothing in code keeps a run out of 2024-2025** (the validation period). Only the
   holdout is guarded (`run_phase1_research.py:10467-10508`).
6. **The regime lens has nothing to read.** Every graded variant labels every bar `unknown`,
   and run_074's regime reader was skipped by rule.
7. **Trades per 4-month block:** about 1,500 at 1h (run_074), but only 70-87 at 1d
   (run_065).
8. **A child run costs about 36 backtests,** around 6 minutes of compute
   (`decide_next.py:126-131`).

**Verdicts on the reasoning:**
- Steps 1, 3 and 6 are sound.
- Step 2 is sound but missed the cause (fact 1).
- Step 4 is partly sound. "Strategy-behaviour claims cannot be measured" is a recording gap
  that E-029 closes. The better argument for dropping the cheap check is simplicity plus a
  cheap child run, not "saving unseen data".
- Step 5: the rule is right, but the random draw is the wrong mechanism, and two of the
  three "why" bullets were overstated (fact 3).
- Step 7 is mostly right. But holding #346 is wrong: its check is reused for the analyst's
  citations of its query log. And "the analyst replaces the readers" was decided before the
  pilot meant to inform it.
- Step 8 is partly right. The regime lens has nothing to read (fact 6), and the proposed
  "focus works" signal is not measurable (about 12 proposals per lens).

**Its simplest design:**
- **Three fixed folds:** A = 2022-2023 (consistent with history); B and C split 2018-2021,
  2 blocks per year each.
- **A child runs on the next fold its lineage has not used.**
- **A config runs on a given fold only once.**
- **A lineage ends after 3 folds,** then validation (2024-2025, single-use), then the
  holdout.
- **Every pooled number shown to an AI step carries its fold label.**
- **Daily ideas confirm on other coins,** because daily blocks have too few trades.
- In code: two functions change, and one YAML file (`config/folds.yaml`) is added.

**Operator decisions (2026-10-08):**

| # | Question | Decision |
|---|---|---|
| D1 | Random draw or fixed folds? | **Fixed folds** (the review's design). The random draw is kept as a **parked epic** |
| D2 | First two analysts | **Forecast and trade efficiency** (not regime: fact 6). Regime returns once the detector is gated |
| D3 | PR #346 (citation check) | **Merge it** (flag off). The operator merges |
| D4 | Pilot rule: process gates plus the operator's judgement, no statistical go rule | **Accepted (option a).** About 12 proposals per lens is too few for a statistical rule. Pre-registered process checks, hold rates reported per fold as information, and the operator decides |
| D5 | Validation period | **Add a single-use guard for 2024-2025** |

**The adjusted order:**
1. **Folds** (new epic): `config/folds.yaml` with a test; decide-next writes the child's
   protocol from the next unused fold; the fold is recorded in the brief, memory and trial
   row; the repeat gate works per (forecast_hash, fold). Then the fold label on every
   pooled number.
2. **E-073:** merge #345, #349, #346; then E-029 (reusing E-074's exit-cause classifier),
   then E-027.
3. **E-075, small:** tools (the E-074 grid as parameters, `trailing_vol`), then two lenses,
   then the pilot. Proposals go through decide-next onto folds B and C.
4. **The validation-period guard.**

**Retired:**
- E-072's split, masking and handoff (deleted when E-075's wiring lands; flag off until
  then);
- E-074 as a reader deliverable;
- the random draw (parked);
- the in-run confirmation.

### A1.8 The analyst's instructions (draft v2, under strong-model review)

**Step 9: how this section got here.**
- **The operator's request:**
  > "Make sure the skill instructions are designed for the analyst to find claims that fit
  > and reach this purpose: the core objective of all our work is to find a profitable
  > strategy."
- **Draft v1** made the analyst's objective *"propose the ONE change to this strategy most
  likely to raise its return after costs on unseen data."*
- **The operator rejected it:**
  > "The one change to this strategy is wrong. Let's step back, even totally. An analyst is
  > there to observe backtest results, possibly use available tools to deep-dive into bars
  > data, and then at the end generate a claim that will be tested after. This claim aims
  > to bring a confirmed observation once tested. Our thesis is that the combination of
  > observed and confirmed claims, which own information on the market and its behaviour,
  > and on the strategy and its behaviour, will lead to a profitable strategy."
- **Why v1 was wrong:**
  - it made the analyst a strategy tuner, so it would chase this run's P&L;
  - it skipped the step that builds lasting knowledge: a confirmed claim about the market or
    the strategy, which can be reused and combined.
- **Profit is the end of the chain, not each analyst's target.** It comes from combining
  confirmed claims.

Draft v2 follows. **It is a proposal for review, not a decision.** The exact SKILL wording
is written in E-075's wiring slice, then tried on two saved runs before the pilot.

**1. The analyst's objective (the first line of the skill):**
> "Observe this run's backtest results, dig into its bars and trades with your tools, and
> end with the ONE claim most worth confirming: a statement about how the market behaves,
> or how this strategy behaves in the market. A later backtest on data you have not seen
> must be able to confirm or refute it, and if it holds, it must be a reusable piece of
> knowledge toward a profitable strategy."

**2. Two kinds of claim:**
- **Market behaviour.** Example: "after a fall of more than 3% in 24 hours on BTC, the next
  24 hours return more than the average hour, by more than the round-trip cost."
- **Strategy behaviour.** Example: "in trending stretches, this strategy closes winning
  trades too early: trades closed by a signal flip during a trend would have earned more,
  after costs, if held 24 bars longer."

**3. What a claim must carry:**
1. **The statement and its kind** (market or strategy).
2. **The observation it came from:** the query-log entries it rests on.
3. **Why:** the mechanism, such as who is on the other side, or why the strategy behaves
   this way. Include the second query that the mechanism predicted and that a coincidence
   would not.
4. **The confirming test,** written before any backtest:
   - **what the next backtest must run** so the claim becomes observable. This can be the
     same strategy, or a variant that isolates the behaviour (e.g. a longer hold). This is
     the only place a strategy change appears: as the vehicle of the test;
   - **the measurement on that backtest's output,** in the claim-test slots (selector /
     outcome / baseline / statistic) over bars.csv and trades;
   - **what result confirms it, and what refutes it** (the falsifier).
5. **Its use if confirmed:** what it would let a strategy do (an entry filter, an exit
   rule, sizing, a regime gate), whether the effect is large enough to matter after costs,
   and which confirmed claims or blocks it would combine with (E-071).

**4. The working method** (a method, not a form to fill in):
1. **Observe the results:** where the outcome is made. For the strategy, that is gross
   edge against costs, and P&L by exit cause, holding time, side, coin and window. For the
   market, that is what the forecast does and does not predict.
2. **Dig in with the tools:** follow the most informative surprise, the thing the strategy
   or the market does that the run's design did not expect.
3. **Ask why,** and check the mechanism with a second query that it predicts.
4. **Rule out the simple rivals:** one coin or one window driving everything, costs, a data
   gap, or the strategy's own mechanics.
5. **Formulate the claim and its test** (item 3).
6. **Or stop.** If nothing survives steps 2-4: "no claim", with the reason. That is a
   valid, counted outcome.

**5. What makes a claim good** (in priority order):
1. **Informative:** if confirmed, we know something real about the market or the strategy
   that we did not know.
2. **Testable on unseen data by a backtest:** the test reads the output of a backtest on an
   unused fold, never the run that inspired it.
3. **Economically relevant:** the effect is big enough to matter after costs if exploited.
4. **Reusable and combinable:** it can serve as a building block with other confirmed
   claims, rather than only fixing this one strategy.
5. **New:** memory shows what was claimed and tested before.
6. **Falsifiable,** with the falsifier written in advance.

**6. What a claim is not:**
- a parameter nudge presented as a claim;
- a statement only measurable on the run that inspired it;
- anything using information after a bar's close (hindsight).

**7. Inputs:**
- **the full run context:** strategy config, variant patches, coins, venue, timeframe,
  fold windows, cost model;
- **the data dictionary** (E-073);
- **the tools:** about 6 fixed query functions, including E-074's grid and `trailing_vol`;
- **memory:** earlier claims and their fold-labelled confirmation outcomes;
- **the component catalogue and the claim-test vocabulary.**

**8. Fixed, generic guard rails** (the same for every lens):
- no hindsight;
- queries only on the run it reads;
- every query logged and counted;
- one claim per session;
- a cost cap;
- no free code.

**9. The two first lenses** (one objective text each; the rest is shared):
- **Forecast:** "What does the forecast tell us, and not tell us, about future returns?
  Where, when and why does it work or fail?"
- **Trade efficiency:** "How does the strategy turn forecasts into trades, and where does
  that conversion gain or lose money: entries, exits, holding time, turnover, costs?"

**10. How a claim is confirmed.**
- If decide-next picks the claim, the next run backtests the test's vehicle on a fold the
  lineage has not used.
- The claim measurement (the E-068 claim-card machinery) runs on **that** backtest's output.
- The result is recorded with its fold.
- A confirmed claim enters the registry as a building block for combination (E-071).

**11. Open points for the reviewer:**
- Is "one claim per session" right, or should the analyst return up to two of different
  kinds?
- Are market claims and strategy claims confirmed the same way, or does a market claim
  need no strategy vehicle at all? (The fold's bars exist, but bars.csv is only written by
  a backtest.)
- How does "economically relevant" get judged before the confirming backtest, without
  becoming the v1 profit-chasing again?
- How do confirmed claims actually combine into a strategy: what does E-071 need from a
  claim's record?

### A1.9 The review of the analyst skill (Fable, 2026-10-08) and the operator's response

The full review is in `roadmap/E-075/ANALYST_SKILL_REVIEW_1.md`. It was read-only and
verified against the code. Its verdict on draft v2: **the thesis is right and v2 mostly
follows it**, but four things would make it fail:

1. **Strategy-behaviour claims cannot be tested today.**
   - The claim tests read only the price bars (`claim_tests.py:407-437`).
   - There is no trade selector (by exit cause or holding time) and no "after the exit"
     outcome.
   - So v2's own example ("closes winners too early in trends") would become `tests: none`.
   - Fix: one trade-level test family, reusing E-074's trades reader and exit classifier.
2. **"Economic relevance" was judged by the analyst,** which is v1's profit-chasing in new
   clothes. The review's fix: a code-computed minimum effect from the cost model, and
   code-written grades.
3. **Memory biases the analyst.**
   - The findings summary shows effects measured where they were found, and "k of 6"
     counts (`reader_findings.py:285-334`).
   - That pushes the analyst to restate the grid: run_073's trade-efficiency idea was the
     run's own residual IC, re-proposed.
   - Fix: memory shows each claim's statement, kind, fold and status, with numbers only for
     confirmed claims.
4. **The combination gap.**
   - The combiner (`tools/composition.py:9-36`) blends forecast blocks and gates them by
     regime.
   - A strategy-behaviour claim (an execution rule) has no slot.
   - Fix: every claim records how it would combine.

Other points:
- confirming by sign only lets a null claim "hold" 30-50% of the time on one fold;
- refuted claims are knowledge;
- one claim or "no claim", both with the same evidence trail;
- a market claim could be confirmed on the next backtest's bars of that fold, at zero
  extra backtests ("piggyback");
- rank analyst candidates by code-computed effect, not self-scores;
- the bot has no minimum hold, time stop or stop-loss.

**Step 10: the operator's response (2026-10-08).**
- **On economic relevance:**
  > "An effect is an effect, independently from the cost. It should not be mixed. The v3
  > version adds complexity. I would go even on the other side, deleting the part about
  > comparing an effect to a cost."
- **On memory (3):** agreed.
- **On combination:**
  > "If it is only an additional field saying how the claim will combine, it is okay. If it
  > touches the combination logic, I am not sure I agree: the combination logic will be
  > revisited later, potentially with an LLM step instead of a mechanical one."
- **On the piggyback confirmation of market claims:**
  > "Again we redo a post-backtest analysis. The market claims will be integrated into the
  > agent: it does this market check in its own internal process."
- **On the order:**
  > "Stage 2 is very important: put it into stage 1, at least the trade-level test and the
  > trade-lens skill."
- **The review was meant to be about the skill only.** Most points sound valid, so the work
  is done iteratively.

**How these remarks are applied** (the interpretation is to be confirmed by the reviewer and
the operator):
- **No cost comparison anywhere in a claim's grading.** A claim's effect is reported as
  measured. Open point for the reviewer:
  - without any size rule, a null effect gets the right sign by luck on one fold 30-50% of
    the time;
  - the proposed default is a purely statistical rule, still independent of cost:
    *confirmed* only if the sign holds AND its uncertainty range excludes zero; otherwise
    *not confirmed*.
- **Combination:** one record field only, `combines_as` (forecast_block | regime_gate |
  execution_rule | knowledge_only). The combination logic is not touched.
- **No piggyback and no separate post-backtest check.**
  - Every claim, market or strategy, is confirmed only by **the run built from it**, on a
    fold its lineage has not used. The claim test is measured on that run's own backtest
    output.
  - Spotting market patterns stays inside the analyst's reasoning (its tools, on the run it
    reads).
  - Consequence: a market claim must come with the strategy (vehicle) that exploits it, so
    that its own run can test it.

### A1.10 The iterative plan (proposal v2, after Step 10; Stage 1 superseded by A1.11)

**Stage 1: both lenses, the smallest complete loop.**
1. **Folds:**
   - `config/folds.yaml` (A = 2022-2023; B and C split 2018-2021, 2 blocks per year), with
     a test;
   - decide-next gives a child the next fold its lineage has not used
     (`decide_next.py:2129` is the change site);
   - a config runs on a given fold once (the repeat gate per fold);
   - the fold is recorded with every run and claim.
2. **The validation-period guard:** 2024-2025, single-use, in code.
3. **Trade-level claim tests:**
   - one test family in `claim_tests`: select trades by a closed list of fields (exit
     cause, holding bars, side, entry hour, ...);
   - outcomes: trade net return, return after the exit;
   - baseline: the other trades;
   - with a lookahead test.

   It needs reliable exit causes: E-074 phase A's interim exit classifier (from
   `exit_forecast`) now, E-029 later.
4. **The analyst's tools:** the fixed query functions over bars and trades, including the
   E-074 grid as a parameterised tool and `trailing_vol`.
5. **The analyst skill (v3, simplified)** for both lenses, forecast and trade efficiency:
   - **objective:** observe, dig in, end with one claim (or "no claim" with what was
     examined), about market or strategy behaviour;
   - **claim fields:** statement, kind, evidence (query-log references), why, the vehicle
     (what the run built from it must run), the test in claim-test slots (bars or trades),
     the falsifier, `combines_as`;
   - **no profit or cost judgement** by the analyst.
6. **Grading by code** on the run built from the claim: confirmed / not confirmed / not
   measurable (statistical rule as above, no cost). Refuted claims are recorded as
   knowledge.
7. **The memory view:** past claims with statement, kind, fold and status; numbers only for
   confirmed claims.
8. **Pilot, both lenses:** process checks plus the operator's judgement (D4).

**Stage 2: making the record richer.**
- E-029 (the trade record carries the decision, replacing the interim classifier);
- E-027 (why a forecast is zero);
- analyst candidates ranked by code-computed effect, not self-scores;
- the output fixes CUL-416 and CUL-417.

**Stage 3: combination and the final checks.**
- the combination of confirmed claims, using `combines_as`; its logic is to be redesigned
  then, possibly as an LLM step;
- then validation, once;
- then the holdout.

Each stage ends with the operator's decision before the next begins.

**Questions for the strong-model judge:**
1. Is Stage 1 the smallest loop that can produce a confirmed claim of each kind?
2. Is the cost-free statistical confirmation rule right, and simple enough?
3. Does "every claim is confirmed by its own run" (no piggyback) hold up for market claims,
   whose vehicle must be a strategy exploiting them?
4. What is missing or over-built, given the operator's preference for simplicity?

### A1.11 The judgement of the iterative plan, and the final Stage 1 (2026-10-08)

The full judgement (Fable, read-only, verified against the code) is in
`roadmap/E-075/ITERATIVE_PLAN_JUDGEMENT.md`.

**What it confirmed:**
- **Cost has no place in whether an effect exists.** The cost floor and the "confirmed but
  too small" grade are dropped.
- **Combination is one record field,** `combines_as`, analyst-written from a closed list.
  The combination logic is unchanged.
- **Every claim is confirmed by its own run,** with no piggyback.
- **The trade-level tests belong in Stage 1.**

**What it added:**
- **Three gaps that would block Stage 1:**
  1. `CLAIM_KINDS` has no strategy kind (`tools/claim_card.py:50-54`): add
     `execution_behaviour`;
  2. E-072's `finding_route` still sends price-only claims in-run
     (`tools/explore_confirm.py:694`): replace it with one `confirm_on_fold`;
  3. the analyst's proposal must use the reader-proposal shape, so decide-next takes it
     unchanged.
- **Less to build:**
  - the per-fold repeat gate is already the novelty key (`windows_sha256`,
    `tools/novelty.py:186-207`): a test, not code;
  - the grid tool is already E-075's `conditional_effect(by=...)`;
  - the placebo arm is the largest piece of E-075's first slice and buys little under D4
    plus folds.
- **The folds are written as exact blocks.** SOL and UNI have almost no 2018-2021 bars, so
  a fold needs at least 4 windows, otherwise "not measurable".
- **A noise rule, labelled as such:**
  - a null claim points the right way by luck about half the time (`test_sign` needs only
    a positive oriented value per horizon, `explore_confirm.py:697-715`);
  - so: confirmed only if the pooled sign holds at every horizon AND the claimed sign holds
    in all but one window of the fold;
  - that is about 11% by chance per fold, about 1% after two folds;
  - it uses numbers every measurement already has (`claim_measure.py:185-189`, per-window
    values `claim_tests.py:1042-1045`).

**Step 11: the operator's answers (2026-10-08).**
1. **Market claims.**
   > "I was thinking B: a market claim will be transformed by the analyst's thinking into a
   > strategy claim that requires a backtest after. Running the same strategy twice, I'm not
   > sure I got the why. A block will be integrated into a strategy config, so it should be
   > a claim about the strategy."
   - Decided: **market observations stay inside the analyst's reasoning. Every output claim
     is a strategy claim**, with the strategy change (the vehicle) that its own run
     backtests.
   - Accepted cost: if a strategy claim is refuted, the record cannot say alone whether the
     market effect was wrong or was badly exploited. The claim keeps its market "why", and
     the child run's trades let the next analyst see which.
2. **Strength.**
   > "I didn't say we should not record the claim's strength; I said we should not compare
   > it to cost."
   - Decided: the effect size and the per-window agreement are recorded for every claim,
     never compared with costs. The noise rule is **all but one window**.
3. **Placebo:** dropped from Stage 1.

**Final Stage 1 (replaces A1.10's Stage 1):**
1. **Folds:**
   - `config/folds.yaml` with six exact blocks per fold (A = 2022-2023; B and C from
     2018-2021, each with a block in every year);
   - a child runs on the next fold its lineage has not used (replacing the deep copy at
     `decide_next.py:2129-2131`);
   - the fold is recorded on every run, claim and ledger row;
   - no window in 2024-2025 or the holdout (the validation guard rides in this PR);
   - the per-fold repeat gate is proven by a test.
2. **The claim record:**
   - one new kind, `execution_behaviour`;
   - on the proposal envelope: `vehicle` (the strategy change: a config change or a
     variant; required, since every claim is a strategy claim), `combines_as` (closed list,
     analyst-written, checked by code) and `fold_observed`.
3. **Confirmation by code, on the child run only:**
   - the claim's tests are measured on the child's vehicle variant over the new fold, with
     its base variant as the comparison where the claim compares;
   - confirmed when the pooled sign holds at every horizon and the claimed sign holds in
     all but one window (at least 4 windows);
   - not confirmed otherwise; not measurable with no events or too few windows;
   - the effect size and window agreement are recorded, with no cost anywhere;
   - a changed spec is not comparable;
   - every measurement is a ledger row with its fold;
   - refuted and not-measurable claims are kept as knowledge.
4. **Trade-level tests:**
   - one family: a trade selector over a closed field list;
   - outcomes: trade net return and post-exit return;
   - baseline: the other trades;
   - per-window values, and a lookahead test;
   - exit causes from E-074's interim classifier now, E-029 later.
5. **The analyst's tools:** E-075's six query functions on the run's own bars and trades,
   with no placebo arm and no separate grid tool. `trailing_vol` is a field they read.
6. **The skill, both lenses** (forecast, trade efficiency):
   - **objective:** observe, dig in, end with one strategy claim or no claim;
   - **claim:** statement, kind, evidence (query ids), why (the market or mechanical reason,
     with the second query it predicted), the vehicle, the test in the slots, the
     falsifier, `combines_as`;
   - **no claim:** what was examined, and the best rejected candidate;
   - the observation may read any column; the vehicle acts only on fields known at the
     close or the fill;
   - no profit or cost judgement by the analyst.
7. **The memory view:** statement, kind, fold and status per earlier claim; numbers only for
   confirmed claims.
8. **Pilot:** both lenses on saved runs 065-074 (fold A), proposals through decide-next onto
   fold B, graded by item 3. Process checks plus the operator's judgement (D4). No placebo.

**PR order:**
- 1, 2 and 3: one PR each;
- then 4, with 7 riding along;
- then 5 and 6 together;
- then the pilot.

The done-when of each PR is in the judgement file, section 4.

Stages 2 and 3 are unchanged from A1.10.
