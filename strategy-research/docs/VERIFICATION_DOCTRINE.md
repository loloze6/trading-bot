# VERIFICATION_DOCTRINE.md

Purpose: how to verify a claim, a metric, or a written artifact in this
research pipeline before it is allowed to feed a decision. This is not
timeframe-specific — it applies to every hypothesis, every run, regardless of
bar interval. It answers four different questions that get conflated if kept
in one undifferentiated pile:

1. Is this metric even a valid input to a decision rule, given what it's
   computed over (§1)?
2. Given fragment-level trade data exists, what is it actually allowed to be
   used for (§2)?
3. Before trusting a new code path's verdict on a real hypothesis, has it
   been proven to tell a known-good answer from a known-bad one (§3)?
4. When two stages compute the "same" number, do they actually agree, and
   when a shared artifact gets written, did the write actually land (§4, §5)?

(Content bundled from `docs/TIMEFRAME_CHANGE_PLAYBOOK.md` §§2(c)/3/4/5/7 as
part of E-045's documentation split; that file's bar-count/signal-shape half
of §2 went to a separate destination doc.)

---

## 1. Metric-basis validity — bar / episode / LIFO-fragment

Every decision-consumed metric has a BASIS (what unit of observation it's
computed over), and the basis matters as much as the formula. Three bases
exist in this codebase, in order of validity for feeding a kill/promote/
refine rule:

- **bar-level**: computed over the raw bars.csv series (forecast vs forward
  return, regime forward-return means, a bar-level equity/portfolio-value
  curve). Valid for signal-quality and risk-adjusted-return decisions.
- **episode-level**: computed over real position episodes — one open-to-close
  span of market exposure, using the activity-transition definition (a
  sign-flip-only trade counter is blind to `0 → +10` transitions and silently
  merges every long-only or short-only signal's separate episodes, across flat
  gaps, into "one giant trade" — so episode boundaries must use the
  activity-transition definition, not a sign-flip counter). Valid, but must be
  built by GROUPING real fragment PnL into episode boundaries, not by
  re-deriving PnL from bar close prices (a bar-close approximation can
  disagree with the real transacted PnL by enough to flip an individual
  win/loss classification even when the fragment/episode count already
  matches 1:1 — always defer to real trade data when it's available).
- **LIFO-fragment**: one row per `performance/metrics.py` `CompletedTrade` —
  i.e. one row per `trades.json` entry. **Engine note: this codebase's
  matching is LIFO, not FIFO** (`EnhancedPerformanceTracker`, "Enhanced
  performance tracker supporting iterative long/short positions with LIFO
  matching") — say this explicitly in any writeup so it doesn't get
  re-litigated as a search-term mismatch later. The LIFO engine and its
  `trades.json` output are an intentional, correct accounting design — the
  risk is purely downstream: a position that scales up/down over its life
  gets split into multiple fragment rows, each with its own "entry forecast"
  that was never an independent prediction about that fragment's
  profitability, and its own PnL slice that LIFO assigned somewhat
  arbitrarily. **Fragment-level statistics are never decision-consumed** —
  trade_count, win_rate, Sharpe, or any per-trade average/rate computed
  directly over `trades.json` rows must not feed a kill/promote/refine rule.
  They remain valid as descriptive reporting (holding times, win rate,
  `entry`/`exit_efficiency`) as long as they're explicitly labeled
  `basis: lifo_fragment, descriptive_only` and no decision rule reads them.

Every decision-consumed metric must declare which of these three bases it
uses, in the artifact that reports it.

**Concrete demonstration (run_054, P4_SMA_TREND_LONGONLY_DAILY,
2026-07-09/10)**: `median_sharpe` computed by `calculate_sharpe_ratio` from
LIFO-fragment rows (reindexing the daily-return calendar only from
first-trade-exit to last-trade-exit, and renormalizing each trade against its
own entry-time portfolio value) read **-1.78 (BTCUSDT) / -1.54 (ETHUSDT)** —
both below the hardcoded `median_sharpe < -1` kill threshold in
`run_protocol.py`, driving `protocol_verdict: kill`. Recomputed on a
bar-level basis (each window's own `bars.csv` `total_portfolio_value`, full
181-bar span, `sqrt(365)` annualization — same convention already labeled by
`sharpe_annualization`), median Sharpe was **+0.579 (BTCUSDT) / +0.032
(ETHUSDT)** — both positive. Run through the exact same rule, the verdict
flips to `refine`. This was NOT a fragmentation bug — the 117-trade count
reconciled exactly against an independent bar-level episode count in every
one of 30 window-symbol results — it was a basis problem in the trade-level
Sharpe formula surfacing specifically under sparse trading (1-8 trades per
181-bar window). `performance/metrics.py` was left untouched (out of scope,
intentionally); the fix lives entirely in the research decision layer,
consuming `bars.csv` as an existing artifact. See
`strategy-research/campaign_record/campaign_knowledge_base.yaml`'s
`p4_sma_trend_longonly_daily_auto` entry and
`strategy-research/runs/run_054/artifacts/verdict_interpretation.yaml` for the
full corrected numbers.

**Producer/consumer table as audit template**: for every decision-consumed
metric, record `{metric name, consuming rule(s), producing function/file,
basis}` before trusting a verdict. Worked example (run_054's decision layer,
2026-07-09/10):

| Metric | Consumed by | Producer | Basis |
|---|---|---|---|
| `forecast_return_corr` | Rule 2/3, A2.3 IC gates | `run_artifact.py::build_core` (bars_df) | bar-level |
| `regime_validity.forward_return_mean` | Rule 4 | `run_artifact.py::build_regime_validity` | bar-level |
| `median_sharpe` | kill/promote rule, Rule 5, A3.4 | `metrics.py::calculate_sharpe_ratio` (trades.json) | **was** lifo_fragment, descriptive_only after correction — decision input now a new bar-level equity-curve calc |
| `win_rate` / `median_win_rate` | Rule 5, approve criteria | `metrics.py` (`net_win_rate_pct`, from trades.json) | lifo_fragment, but == episode-level here (no fragmentation occurred) |
| `trade_count` / `min_trade_count` | Gate B (cumulative, per-window) | `run_artifact.py::build_core` `len(completed_trades)` | lifo_fragment row count — must be cross-checked against an episode count before trusting as a sample-size gate |
| `gross_pnl`, `cost_drag_pct` | Rule 1 | `run_artifact.py::build_core` (sums over trades.json) | lifo_fragment, but sums are invariant to fragmentation — defensible |
| `entry_efficiency`, `exit_efficiency`, `pnl_concentration`, `per_trade_expectancy_bps` | STEP 03 trade attribution, A3.4 fallback | `run_protocol.py::_aggregate_trade_diagnostics` (trades.json rows) | lifo_fragment |

**Producer AND consumer rule**: a sweep for a metric-basis problem must check
every CONSUMER of a statistic, not just the sites that compute it. Fixing
`build_core`'s correlation calculation (the producer) left
`evaluate_against_decision_rules` (a consumer, computing its OWN pooled
median from the producer's output) still silently reporting the criterion as
permanently UNTESTED, because the field it needed was never populated for the
degenerate case either. The bug and the gap were in different functions, in
different files, at different architectural layers — a sweep that stops at
the first fix finds only half the problem.

---

## 2. The three-role model for fragment data

LIFO trade fragments (`trades.json` rows) are real, useful data — the mistake
§1 above corrects is treating them as independent decisions when they're
bookkeeping artifacts of one continuous position. Fragment data has exactly
three legitimate roles, and mixing them is the recurring failure mode:

- **Verdict: bar-level and episode-level metrics only. Fragments never
  vote.** Anything that feeds a kill/promote/refine rule must be computed
  over the bar-level series (forecast vs. forward return, a mark-to-market
  equity curve) or over real position episodes (fragments grouped by
  activity-transition boundary, real PnL summed per episode). A LIFO fragment
  row is never itself an independent observation in a decision statistic.
- **Diagnosis: fragments fully in play — attribution, composition, cost
  anatomy.** `fragment_patterns.yaml` (`strategy-research/tools/fragment_patterns.py`)
  lives entirely here: forecast-bin outcome tables, entry/exit component
  attribution, initial-entry-vs-scale-up cost comparison, duration/regime
  cross-tabs. This is where per-fragment detail is not just permitted but
  necessary — you cannot diagnose entry/exit execution quality or cost
  structure from a bar-level equity curve alone.
- **Ideation: fragment patterns become candidate hypotheses, which earn
  verdict-grade status only through their own pre-registered test.** A
  pattern noticed in diagnosis (e.g. "fragments with entry forecast <5
  carried 70% of losses") motivates a new brief; it does not retroactively
  validate or invalidate anything about the run it came from. See the
  `motivating_observation` convention in
  `workflow_artifacts/skills/campaign-review/SKILL.md`.

### Why entry-forecast-vs-episode-outcome correlation is banned from verdicts, but bar-level IC is fine

Both look like "does the forecast predict the outcome" questions, and it's
tempting to treat them as the same statistic at different granularities.
They are not, for two independent reasons:

1. **Per-bar claim vs. whole-episode-result conflation.** Bar-level IC
   correlates the forecast AT EACH BAR against that bar's own forward
   return — a claim and its own immediate outcome, matched one-to-one. An
   entry-forecast-vs-episode-outcome correlation instead correlates the
   forecast at ONE bar (the episode's opening bar) against a PnL number that
   accumulated over every bar the episode held the position — a claim at
   time T being scored against an outcome realized over T through T+N. The
   entry forecast never claimed anything about what would happen at
   T+1..T+N; scoring it against the whole episode's result is answering a
   question the signal was never actually asked.
2. **LIFO slicing artifact.** Even setting aside (1), which fragment's "entry
   forecast" gets matched against which slice of PnL is a LIFO bookkeeping
   choice, not a fact about the signal. A scaled position's later increments
   carry an entry forecast that was never an independent prediction that
   THAT SLICE would be profitable — it's just the value the forecast
   happened to hold when the position was topped up. Correlating that value
   against the fragment's (or episode's) PnL is measuring the
   position-tracking mechanism, not the signal.

Bar-level IC has neither problem: it never leaves the bar it was computed on,
so there's no accumulation-window mismatch, and it doesn't touch
`trades.json` at all, so there's no LIFO slicing to be an artifact of. It is
the verdict-grade form of "does the forecast predict returns" for exactly
that reason — same underlying question, asked at the only granularity where
the answer means what it appears to mean.

---

## 3. Shakedown doctrine

**First traversal of any new code path gets known-answer synthetic tests
before it judges a real hypothesis.** A synthetic null (must correctly
fail/kill) and a synthetic positive-control (must correctly pass), with
outcomes known BY CONSTRUCTION (not by running the real signal and eyeballing
whether the result looks plausible), kept as permanent regression tests — not
deleted after the shakedown passes. This is what actually catches "the gate
can only ever produce one answer for this signal shape" bugs, which look
completely unremarkable from a single real run (a real run just shows one
number; you need the null/positive PAIR to see that the gate can't tell them
apart).

Where this campaign's suite lives:
- `strategy-research/tests/test_prescreen_degenerate_signal_gate.py` — null
  and positive synthetic signals through the full prescreen path.
- `strategy-research/tests/test_turnover_proxy.py` — exact trade counts known
  by construction (long-only with N round trips, two-sided with flat gaps,
  symbol-boundary non-merging).
- `strategy-research/tests/test_pooled_ic_bootstrap_fallback.py` — the
  keyword-collision regression (a p-value criterion must never resolve to an
  IC-magnitude field) plus the degenerate/non-degenerate fallback split.
- `trading-bot/tests/test_signal_statistics.py`,
  `trading-bot/tests/test_build_core_degenerate_forecast.py` — the shared
  statistics module and its integration into the full-backtest diagnostic
  path.
- `trading-bot/tests/test_warmup_prefetch_bit_identical.py` — proves the
  `warmup_prefetch` engine parameter is a true no-op when unused.

---

## 4. Cross-check doctrine

**Where two stages compute the same quantity, a material disagreement must
raise a loud warning in the run's own artifacts — never coexist silently.**
This campaign's prescreen stage and its full-backtest stage each compute an
IC/correlation for the same hypothesis, independently, at different points in
the pipeline. When `build_core`'s bug made the backtest report a fabricated
`corr=0.0, p=1.0` in every window, it directly contradicted prescreen's own
`pooled_ic=0.0359, p=0.004, significant` — and nothing noticed. The
LLM-authored verdict narrative cited the backtest number as "confirmed no
edge, high confidence" without anyone (human or model) checking it against
the number the SAME hypothesis had already produced two stages earlier.

Template: `strategy-research/tools/run_protocol.py::_cross_check_prescreen_vs_backtest`.
Reads the sibling `prescreen_result.yaml`, compares its significance/sign
against the backtest's own resolved value (post any degenerate-case
fallback — check the RESOLVED value, not just the raw one, or the check
itself will flag a disagreement that's already been reconciled elsewhere in
the same artifact), and writes the comparison into `protocol_result.yaml`
either way (agreement is also worth recording, not just disagreement) —
auditable by design, not just alarming by exception.

---

## 5. Read-back verification doctrine

**Every write to a shared decision artifact (KB entries, verdicts, campaign
review, wishlist state, queue state) must be followed by re-reading the file
and asserting the specific fields you intended to change — not assumed to
have landed because the write call didn't error.** A tool call reporting
success writes bytes; it does not confirm those bytes still say what you
think two turns later, or that nobody else touched the same file in between.

**Incident (2026-07-10, `strategy-research/docs/analysis-reports/INCIDENT_20260710.md`)**:
a metric-basis correction to `campaign_knowledge_base.yaml`'s
`p4_sma_trend_longonly_daily_auto` finding and
`runs/run_054/artifacts/campaign_review.yaml` was silently reverted — twice —
by a parallel agent operating from a context horizon that predated the
correction, acting in good faith on the belief that the correction was
tampering. Both agents were honest; the contexts simply conflicted, and
nothing forced either agent to notice the conflict before building further
reasoning on top of a file whose content had changed out from under it. The
fix that closed this: arbitrate by **recomputation, not narrative** — when
two agents disagree about a KB/verdict artifact's content, don't diff the
prose or trust whichever version is "yours"; independently recompute the
underlying number (bar-level Sharpe from `bars.csv`, in this case) from the
immutable source artifacts and let that arithmetic decide, then re-verify
every write with a fresh read afterward.

Concretely, after any write to a file more than one process/session might
touch:
1. Re-open the file (not from memory/cache — a fresh read).
2. Assert the specific field values you just wrote, by exact match where
   possible (not just "the file is non-empty" or "it parses").
3. If an assertion fails, stop and diagnose why before writing anything
   downstream that depends on it — do not silently re-write and move on, and
   do not assume your own last edit is still there.
4. For any file writable by more than one process (a live orchestrator, a
   parallel agent, a human operator), prefer a single designated writer
   function over ad-hoc hand-edits scattered across call sites — see
   `workflow/run_campaign.py::evaluate_and_persist_wishlist_predicate` for
   the pattern (one function owns the write, computes a content hash of its
   source so staleness is mechanically detectable, and every consumer must
   check that hash before trusting the persisted value instead of assuming
   freshness).

---

Cross-linked from `strategy-research/DOC_INDEX.md` and
`workflow_artifacts/skills/verdict-interpreter/SKILL.md`. Bundled out of
`docs/TIMEFRAME_CHANGE_PLAYBOOK.md` (E-045 S5); see that epic for the rest of
the split (light data-availability doc, trading-bot user guide, concealment-
instruction doctrine doc).
