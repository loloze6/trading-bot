# Review of the analyst's instructions (draft v2, A1.8) and a proposed v3

Read-only review, 2026-10-08. Line numbers are on the `plan-amend` worktree unless marked
"main checkout" (saved runs). No test, backtest or model call was run; no cache was opened.

## 0. What I verified in the code (the facts the review rests on)

- The claim-test engine reads **bars only**: `load_variant_bars` (`tools/claim_tests.py:407-437`)
  builds `Window` objects with `ts, close, forecast, regime, high, low` (`:247-264`). There is no
  trade loader and no trade selector. Selectors read `forecast`, `close`, `past_return` (`BAR_T_FIELDS`,
  `:146`), `regime`, `regime_change`, `calendar`, `quantile` (`:530-532`). Outcomes: `fwd_return`,
  `fwd_volatility`, `fwd_max_drawdown`, `trend_ends` (`:582-583`). Baselines: `complement`, `placebo`,
  `other_selector` (`:633-634`). Statistics: `mean_diff`, `rank_ic`, `hit_rate`, `decay_curve` (`:699-700`).
- Floors are **counts only** (`FLOOR_UNITS`, `:149`); nothing in the spec expresses "bigger than the
  round-trip cost". `alpha`/`significance` are code-fixed (`tools/claim_card.py:67`, `:118-121`).
- `CLAIM_KINDS` (`claim_card.py:50-54`) has no kind for strategy behaviour. `cost_turnover` and
  `robustness` are tested by **grid criteria** (`criteria_refs`, CLAIM_TESTS.md section 4), i.e. by the
  run's own P&L bars, which is exactly v1's territory.
- Confirmation today: `finding_route` (`tools/explore_confirm.py:677-695`) sends block claims to
  "pending" and price-only claims to in-run; `test_sign` (`:697-718`) holds when every horizon with a
  value has the claimed sign; `no_events` counts as not held. No effect-size floor.
- Side findings become decide-next candidates (`tools/decide_next.py:1557-1616`), collapse on
  `(spec_hashes, start config)` (`:1641-1649`), and are ranked by the reader's **self-assigned**
  `confidence_real` and `distance_to_profitable` then cost (`rank_key`, `:1900-1906`). The child's
  windows are the parent's `machine_constraints` deep-copied (`:2129-2131`).
- The brief pre-fills the claim and step 1a copies it unchanged (`PREFILLED_CLAIM.md`;
  `decide_next.py:2145-2168`).
- Memory shown to readers: `findings_summary_for_readers.yaml` carries each earlier claim's
  statement and, per variant, the **largest effect and "k/6 windows"** (`tools/reader_findings.py:285-334`;
  main checkout `runs/run_074/artifacts/findings_summary_for_readers.yaml` shows `effect: 0.000587889`,
  `claimed_sign_windows: 4/6`).
- What E-071/E-060 combine: forecast blocks only, same exact timeframe, weighted equal / inverse vol /
  residual IC; regime blocks gate (`tools/composition.py:9-36`, `SCHEMES` `:79`). Registry entry fields:
  `kind, config_fragment, numbers, residual_ic, ...` (`tools/block_registry.py:253-269`). Manifest kinds
  are `forecast` and `regime` only (`tools/block_manifest.py:57`). **There is no execution-layer block.**
- What a trade record carries: `trades.json` has `side, entry_time, exit_time, entry_forecast,
  exit_forecast, matched_quantity, net_profit_loss_percent, entry/exit_regime` (main checkout
  `runs/run_074/variants/base/results/<w>/trades.json`, first record). `trade_diagnostics.json` adds
  `exit_reason` (99% `signal_flip`, A5), `mae/mfe/exit_efficiency` (entry bar included, A6),
  `post_exit_return_5bars/20bars`, `cost_paid` (fee only, A7) (`docs/DATA_DICTIONARY.md:164-247`,
  audit `:666-694`). E-074 already classifies exits from `exit_forecast` + the exit row's allocation
  (`roadmap/E-074/PHASE_A.md:382-408`): 74% of run_074 base lots are same-sign reductions.
- No minimum-hold, time-stop or stop-loss exists in the bot (`grep -rni "min_hold|time_stop|stop_loss|hold_bars"`
  over `trading-bot/strategies`, `risk`, `execution/forecast_manager.py`: only the GatedSma entry latch
  and the risk gate's kill latch). The only "hold longer" levers are smoothing transforms (`ema`,
  `threshold_filter`, `trading-bot/strategies/registry.py:58-63`) and the no-trade band
  (`risk_management.controls.min_allocation_change`, default 0.20, `DATA_DICTIONARY.md:137`).
- Regime is `unknown` on every bar of every graded variant since run_065 (A1.7 fact 6; bars.csv
  header of run_074 confirms a single `regime` column with no detector components).
- What readers actually produced (main checkout): run_074 trade_efficiency and forecast_power both
  returned `side_findings: []` and an explanation that is the grid restated. run_073
  `trade_efficiency-run_073-1` is a `rank_ic` test on `all` bars, i.e. the run's own residual-IC
  criterion re-proposed as a "claim"; `-2` is `tests: none` on exit efficiency by trade outcome.
  That is the baseline v3 must beat: restatement, not observation.

## 1. Does draft v2 serve the thesis?

**Where the thesis is strong.** Never confirm where you observed; the analyst is not a tuner; a
claim is a unit of knowledge with a falsifier written first; refuted claims are kept. These four are
right and they are what killed v1. A1.2 row 3 ("a strategy change appears only as the vehicle of the
test") is the correct inversion.

**Where the thesis has gaps (fair criticism, not objections):**
1. "The combination of confirmed claims leads to a profitable strategy" is an assumption the
   pipeline cannot yet honour. The combiner adds forecast blocks linearly and gates by regime
   (`composition.py:9-36`). A confirmed **market** claim can become a forecast block (1b builds a
   component from the selector). A confirmed **strategy-behaviour** claim (exits, holding, band)
   has no slot in the combiner at all; it can only change the vehicle config of later runs. So
   the two claim kinds combine by different mechanisms, and v2 treats them as one.
2. "Confirmed" by the sign rule on one unseen fold is weak: `test_sign` needs only the claimed sign
   at every horizon with a value, horizons are nested (h=24 contains h=1), so a null claim holds
   roughly 30-50% of the time. Knowledge accrues only if every look is counted (the E-072 ledger,
   `explore_confirm.py:959-1056`) and only if a confirmed claim also carries a size. v2 has no size.
3. Refuted claims are information too ("after a 3% fall, nothing follows on fold B" rules out a
   family). v2 says what a confirmed claim becomes and nothing about a refuted one.
4. The observable surface is thin for the trade lens: exits are unlabelled (A5), MAE/MFE biased (A6),
   regime is `unknown` everywhere, the band decision is not a column. A trade-efficiency analyst
   without E-029 (or E-074's interim classifier) is observing shadows.

**Where v2 drifts back toward profit-chasing (v1's error):**
- Method step 1 tells the analyst to start from "gross edge against costs, and P&L by exit cause,
  holding time, side, coin and window" (A1.8 item 4.1). That is "explain this run's loss", which
  Haiku did in run_073/074 and which produces patches, not claims.
- Quality criterion 3 "economically relevant: big enough to matter after costs if exploited" and
  item 5 "its use if confirmed ... whether the effect is large enough" ask the analyst to **judge**
  relevance by thinking about profit, with no rule. Judged by a model, that is P&L chasing again.
- "The ONE claim most worth confirming": "worth" is undefined, so it defaults to "most likely to
  make money".
- Kinds `cost_turnover` / `robustness` are tested by the grid (`criteria_refs`): a claim of those
  kinds is a profit statement about this strategy.

**Where v2 drifts toward unfalsifiable observation:**
- v2's own strategy example ("trades closed by a signal flip during a trend would have earned
  more, after costs, if held 24 bars longer") cannot be measured by any existing slot: no trade
  selector, no post-exit outcome, no net-return outcome, no "trend" label. Under today's code it
  becomes `tests: none` + `missing_block` (`claim_card.py:184-194`) and is never confirmed. The
  trade-efficiency lens as written would produce unfalsifiable claims by construction.
- "Why: who is on the other side" is meaningless for a strategy claim; the "why" there is a
  mechanical cause in the pipeline (target = forecast/10, rebalance on every |delta| >= 0.20, LIFO
  lots). v2 does not say so, so the analyst will invent market stories for mechanical facts.
- Criterion 1 "informative: we know something we did not know" is not checkable by anyone.
- Item 6 "anything using information after a bar's close" forbids, read literally, every
  strategy-behaviour observation (exit fields are `after`/`exit` by the dictionary). The rule must
  be on the **use**, not on the observation.

**Is "profit is the end of the chain, not each analyst's target" right?** Yes, with one precision:
profit is the end of the chain, **cost is not**. Cost is a property of every claim's unit and must be
inside the claim from the start, as a number written before data by a fixed rule, not as a judgement.
Economic relevance then enters without corrupting the observation like this:
- every claim carries a `relevance_floor` in the claim's own unit, computed by a fixed formula from
  the run's cost model (e.g. for a `fwd_return` claim at horizon h: one round-trip cost of the run,
  fee + slippage both ways, A7-corrected; for a trade claim: one round-trip cost per lot);
- code, not the analyst, records after the confirming backtest whether the confirmed effect clears
  the floor: `confirmed` (sign held and >= floor), `confirmed_small` (sign held, below floor),
  `refuted`, `not_measurable`;
- all four are kept as knowledge; only `confirmed` can become a building block.
The analyst never asks "will this make money"; it asks "is the effect bigger than what trading it
costs", and the answer is measured, not predicted.

## 2. Concrete problems in v2, each with a fix

**P1. Strategy claims have no confirming test.** (`claim_tests.py:407-437`, `:146`, `:530`.)
Fix (minimum): add one trade-level test family to `claim_tests`, reusing E-074 S3's planned
`trades.json`+`bars.csv` reader and its exit-cause classifier (`E-074/PHASE_A.md:382-408`, `:544-552`):
- `selector: {kind: trade, where: [{field, op, value}]}` with a closed field list:
  entry-time `side, entry_forecast, regime_at_entry, entry_hour, entry_weekday, pre_entry_move_z`
  (E-074's z) and exit-time descriptors `exit_cause, holding_bars` (allowed because a strategy claim
  describes what the strategy did; the use-if-confirmed must still act on entry-time fields);
- `outcome: {kind: trade_net_return}` (lot net return, A7-corrected: fee + slippage) and
  `{kind: post_exit_return, horizons: [h]}` (signed by side, from the exit fill);
- `baseline: {kind: other_trades}` (the variant x coin's other lots), `statistic: mean_diff | hit_rate`.
Three blocks, one PR, same `spec_hash` machinery. Without it the trade-efficiency lens cannot produce
a falsifiable claim and should not be piloted.

**P2. "One claim per session" invites forced claims** (run_073's two findings restate the grid).
Fix: "one claim **or** no claim", both first-class, both with the same evidence trail (section 3,
`no_claim` block). Plus a cheap `discarded:` list (statement + one line why) so the operator sees what
was considered; never ranked, never confirmed.

**P3. The vehicle for market claims.** bars.csv is written only by a backtest, but a market claim's
measurement does not depend on the strategy: it reads `close`, `past_return`, `trailing_vol`,
`calendar`. Fix: a market claim needs **no vehicle**. It is confirmed on the bars.csv of the **first
backtest on the next fold for the same coin and timeframe, whichever lineage ran it** (a decide-next
rule plus a ledger `basis: piggyback`). This costs zero backtests, keeps "never confirmed in the run
that inspired it", and keeps "a strategy change appears only as the vehicle" true where it belongs:
only strategy claims need a vehicle. A market claim that later becomes a block then runs as a
**new config** on that fold (allowed: "a config runs on a given fold only once", A1.7).

**P4. What E-071 needs from a claim's record.** Today it needs a registry entry (`block_registry.py:253-269`)
which exists only after a `validated` grid. A claim is upstream of that. Fix: the claim record carries
`combines_as: forecast_block | regime_gate | execution_rule | knowledge_only`, derived by code from
`kind` (`KIND_BLOCK`, `claim_card.py:57-61`, extended), plus `scope {venue, coins, timeframe}`,
`fold_confirmed`, `effect {value, unit, horizon}` and, for `execution_rule`, the config pointer it would
change. E-071 then has what it needs to decide weight (forecast), gate (regime) or composite config
(execution). Nothing else is needed now; `execution` as a manifest kind is E-071's decision.

**P5. Memory biases.** The summary shows exploratory effects and k/6 window counts
(`reader_findings.py:285-334`). Fix: the analyst's memory view lists earlier claims as
`statement, kind, scope, spec_hash, fold_observed, fold_confirmed, status` and shows an effect
**only** for `confirmed`/`confirmed_small` claims (the confirmed value, with unit and fold). No
exploratory numbers, no window counts, no pending effects. "What is known", not "what looked good".

**P6. Repeats.** The `spec_hash` warning (`reader_findings.py:366-398`) catches identical specs only.
Fix: the claim carries `novelty: {nearest_prior: <claim id or none>, differs_by: <one line>}`,
written by the analyst from the memory view; code adds a `neighbour` warning when selector kind +
field + outcome kind + direction + coin + timeframe match an earlier claim (not a refusal; decide-next
ranks it below). No new vocabulary needed.

**P7. How many queries, how looks are counted.** Keep E-075's count of **comparisons** (horizons x
groups; `E-075/PHASE_A.md:179-185`) and its per-session cap. Do not fix a minimum number of queries.
Fix the **content**: the claim's own test and the mechanism's second query must both be present in
the session log with the claim's spec, or the claim is refused with one retry ("untested reasoning").
Code writes `looks` and `candidates_examined` into the record (already planned, `:240-243`); the
ledger counts the confirmation look.

**P8. "No claim" without laziness.** `no_claim` must carry `what_was_examined` (the spec hashes
queried), `best_rejected` (the strongest candidate and the rival or floor that killed it) and at least
one conditional/trade query in the log. The pilot's process check treats a no-claim session with an
empty examined list as a failed session, not a cautious one.

**P9. Ranking by self-scores inflates.** decide-next ranks reader candidates by their own
`confidence_real`/`distance_to_profitable` (`decide_next.py:1900-1906`). An analyst that wants its
claim run will score it 3/3. Fix (for analyst candidates only): rank by code-written fields:
exploration effect / relevance floor (desc), `n_events` (desc), neighbour warning (asc), cost (asc).
Self-scores are recorded, not ranked. This is the one place v2's "decide-next ranks it" needs a change.

**P10. No-hindsight rule misplaced.** Fix the wording: the observation may read any field; the
`use_if_confirmed` and any `vehicle.config_change` may act only on fields the dictionary marks
`close` or `fill` (`DATA_DICTIONARY.md:25-33`). Code checks the vehicle's config change resolves
(`resolve_patch`, existing) and scans the `use_if_confirmed` text for `after`/`exit` field names.

**P11. Kinds.** Add two block-less kinds to `CLAIM_KINDS`: `execution_behaviour` (entries, exits,
holding, lots) and `conversion` (forecast -> allocation -> trade, bands, sizing). Retire
`cost_turnover` and `robustness` from the analyst's list (they are grid criteria, i.e. profit bars).

**P12. "Mechanism" has two types.** `mechanism.type: market | mechanical`. Market: who pays, why it
persists, the second query it predicts. Mechanical: the pipeline rule that produces the behaviour,
named with its file (e.g. "target = forecast/10; rebalance on every |delta| >= 0.20; LIFO lots"), and
the second query it predicts (e.g. the distribution of |allocation_change| on rebalance bars).

## 3. The better version: SKILL v3 (structure and key wording)

### 3.1 Objective (first line)
> "You observe one finished backtest on one fold. With your fixed tools you dig into its bars and
> trades, ask why, and end with **one claim or no claim**. A claim is a statement about how the
> market behaves, or how this strategy behaves in the market, with the test a later backtest on a
> fold you have not seen must pass or fail. You are not asked to improve this strategy or to find
> profit. Confirmed and refuted claims are the knowledge the campaign builds strategies from."

### 3.2 Inputs
- Run context: config, variant patches, coins, venue, timeframe, **fold label and its windows**, cost
  model (fee + slippage per side).
- The data dictionary (analyst subset) and the tool list with their closed vocabularies.
- Memory view (P5 shape): earlier claims, their status and fold, confirmed effects only.
- The claim-test vocabulary (CLAIM_TESTS.md plus the trade family, P1).
- Not given: the grid verdict text, the five category reports' prose, reader explanations, the
  claim digest's exploratory numbers. (The grid's numbers are visible through `describe`/`trade_slice`
  if the analyst asks; it should not start from them.)

### 3.3 Method (a method, not a form)
1. **Orient** with `list_columns`, `describe(forecast)`, `describe(allocation_change)`,
   `trade_slice(all, count/by exit_cause)`. Know what this strategy does mechanically before reading
   any outcome.
2. **Find the surprise**: the one place the market or the strategy does what the run's design did
   not expect. A surprise is a conditional difference, not a level ("losing" is not a surprise;
   "same-sign lots lose and flip lots do not" is).
3. **Ask why**, choose the mechanism type, and write the second query the mechanism predicts and a
   coincidence would not. Run it. If it fails, drop the candidate (record it under `discarded`).
4. **Rule out rivals** with one query each: one window (`by=window`), one coin, a data gap, the cost
   model, end-of-window lots, the strategy's own mechanics masquerading as market behaviour.
5. **Write the claim** (3.4) with its test, its relevance floor, its falsifier and its novelty line.
   Or write `no_claim` with the same trail.
Stop when the comparison budget says so. A session that ends in `no_claim` with a full trail is a
good session.

### 3.4 Claim schema (the record; `code:` fields are written by code, never by the analyst)
```yaml
claim_id: <lens>-<run_id>-1                 # one per session
kind: <CLAIM_KINDS + execution_behaviour, conversion>
scope: {venue, coins: [...], timeframe}      # code: copied from the run
fold_observed: <A|B|C>                        # code
statement: >  one sentence a new joiner can test
observation:
  queries: [q7, q9]                           # ids in this session's log; code checks they exist
  effect: <code: the claim's test measured on this run, with unit, n_events, by window>
mechanism:
  type: market | mechanical
  text: >  who pays and why it persists | which pipeline rule produces it (file named)
  predicted_query: q9                         # the second query; code checks it is in the log
  result: >  what it showed, one line
rivals:
  - {rival: one_window, query: q11, verdict: ruled_out | not_ruled_out, why}
  - {rival: one_coin | data_gap | cost_model | end_of_window | own_mechanics, ...}
test:
  vehicle: none | same_strategy | variant     # none for a market claim (P3)
  config_change: [...]                        # variant only; resolved by code against the base config
  spec: {selector, outcome, baseline, statistic, direction, floor}   # the slots, 1 test
  relevance_floor: {value, unit, basis: "<formula from the cost model>"}   # code-computed default,
                                              # analyst may raise it, never lower it
  confirm_if: >  sign held at every horizon with a value and effect >= relevance_floor
  refute_if:  >  opposite sign at any horizon with a value, or no events on the fold
use_if_confirmed:
  combines_as: forecast_block | regime_gate | execution_rule | knowledge_only   # code from kind
  what_it_allows: >  an entry filter / a gate / a band change / rules out a family
  acts_on: [close/fill fields only]           # code scans against the dictionary
  config_pointer: <path>                      # execution_rule only
novelty: {nearest_prior: <claim_id | none>, differs_by: >  one line}
discarded: [{statement, why}]                 # optional, never confirmed
code:
  spec_hash, looks: {calls, comparisons}, candidates_examined: [spec hashes], cost_usd, model_id
```
`no_claim` record: `{reason, what_was_examined: [spec hashes], best_rejected: {statement, killed_by},
queries: [...]}`.

### 3.5 Quality criteria (what makes a claim good, in order; all checkable)
1. **Measurable by the slots** on a fold-B backtest's output. `tests: none` is allowed, recorded as a
   test request, and never confirmed; it counts as a look.
2. **Conditional**, not a level: a selected set against a baseline, or a rank correlation.
3. **A mechanism that predicted a second query, and the query is in the log.**
4. **Rivals ruled out** by queries, each named.
5. **New**: a novelty line against memory; no neighbour warning, or a stated difference.
6. **Relevance floor stated** before data, in the claim's own unit, from the cost model.
7. **Combinable kind stated** (code-derived; the analyst only checks it makes sense).
"Informative" and "economically relevant as judged" are dropped: 2, 3 and 6 are their checkable forms.

### 3.6 Guard rails (generic, same for every lens)
- Fixed tools only; every call logged and counted; no code, no paths, no free text that executes.
- Queries on this run's own fold only; the fold's label is in every result.
- Cite only query ids; code resolves every citation against the log (E-073 step 2, reused).
- The observation may read any column; `use_if_confirmed` and `config_change` act on `close`/`fill`
  fields only (dictionary "When known").
- One claim or no claim; a `discarded` list is free.
- Cost and comparison caps; a cap hit ends the session with whatever record exists.
- No date at or after the holdout start in any text (existing seal regex).
- No regime claims while every bar is `unknown` (code skips the selector; the lens text says so).

### 3.7 The two lens texts
**Forecast lens.** "What does the forecast know, and when? Where (hour, past move, trailing
volatility, forecast size) does its rank against forward returns rise or vanish, at which horizon, and
why would the market pay for that? Your claims are market claims or forecast claims: a conditional
return effect, or a conditional rank IC. You are not asked whether this strategy is profitable."

**Trade-efficiency lens.** "How does this strategy turn a forecast into lots, and which lots lose
after costs: by exit cause (flip, reduction, end of window), holding length, side, entry forecast,
the move before entry? The 'why' here is usually mechanical: name the pipeline rule (target =
forecast/10; rebalance on every |delta| >= the band; LIFO lots) and predict a second query it
implies. Your claims are strategy claims, measured on trades, and confirmed on the same strategy run
on a fold you have not seen. Exit fields are descriptions of what happened; a use-if-confirmed may
only act on what was known at entry."

### 3.8 Worked example A: a market claim (forecast lens, run_074 base, BTC 1h, fold A)
Numbers below are placeholders (`<m>`); nothing was measured here.
- Observe: `conditional_effect(base, {event past_return bars 24 <= -0.03}, horizons [6, 24],
  fwd_return, complement, mean_diff, greater)` -> `<m>` bps at h=24, n_events `<m>`, sign in `<m>`/6
  windows.
- Why (market): forced deleveraging after a fast fall overshoots; the other side is liquidated longs
  and margin calls, non-economic sellers; it persists because it is small per event and needs a
  24h holding. Predicted second query: the effect is larger when `trailing_vol` is in its top third
  (`conditional_effect({quantile trailing_vol top q 0.33 lookback 336}, [24], ...)`) and absent
  after small falls (`past_return bars 24 in [-0.01, 0]`) -> `<m>`.
- Rivals: `by=window` (not one window), one coin (BTC only in this run: stated as a limit), data gap
  (`describe(close, by=window)` NaN share), cost (floor), own mechanics (not applicable: price only).
- Claim: "After BTC falls more than 3% over 24 hours, the next 24 hours return more than other
  hours." kind `event_behaviour`; test spec as the first query; `relevance_floor`: 30 bps at h=24
  (2 x (5 + 2.5) bps round trip, A7-corrected, code-computed); `confirm_if`: oriented effect > 0 at
  h=6 and h=24 and >= 30 bps at h=24; `refute_if`: <= 0 at either.
- Vehicle: none. Confirmed on the bars.csv of the first fold-B BTC 1h backtest (piggyback); ledger
  look counted on fold B.
- If `confirmed`: `combines_as: forecast_block`; `what_it_allows`: an entry component "long after a
  24-bar fall below -3%, flat otherwise" (1b builds it from `PriceEvolutionOnPeriodComponent`
  period 24 + `threshold_filter`/`clip`); it runs as a new config on fold B, and on `validated` enters
  the registry and E-071's weighting. If `confirmed_small`: kept as knowledge ("exists, below cost").
  If `refuted`: kept; the family "24h shock continuation on BTC" is closed for this cost level.

### 3.9 Worked example B: a strategy claim (trade-efficiency lens, run_074 base, fold A)
- Orient: `trade_slice(all, count, by=exit_cause)` -> reductions `<m>`% (E-074 measured 74%),
  flips `<m>`%; `describe(allocation_change)` on rebalance bars peaks just above the band.
- Observe: `trade_slice({exit_cause == reduction}, [net_return mean, count], by=window)` versus
  `{exit_cause == flip}`: reduction lots net `<m>` bps (about minus one round trip), flip lots `<m>`.
- Why (mechanical): target = forecast/10 (`forecast_manager`), rebalance on every |delta| >= 0.20
  (`risk_manager._ctrl_min_allocation_change`), LIFO lots: a z-score forecast that drifts by 2 points
  opens a lot that carries no new information and pays a full round trip. Predicted second query:
  lots with `holding_bars == 1` and `exit_cause == reduction` have the worst net return
  (`trade_slice({exit_cause == reduction, holding_bars <= 1}, net_return mean)`); flip lots do not
  depend on holding length.
- Rivals: `by=window`; end-of-window lots excluded by the filter; cost model (A7: slippage inside the
  fill, fee outside; the floor is one round trip); own mechanics is the claim itself.
- Claim: "Lots opened by a same-direction rebalance lose one round-trip cost on average; lots
  opened by a sign flip do not." kind `execution_behaviour`. Test (needs P1): selector
  `{trade, where: [{exit_cause, ==, reduction}]}`, outcome `trade_net_return`, baseline `other_trades`,
  statistic `mean_diff`, direction `less`, floor `min_events 200, min_windows 4`; relevance floor: one
  round trip (15 bps) per lot. `confirm_if`: reduction lots' mean net return below the others' by
  >= 15 bps on fold B; `refute_if`: not below.
- Vehicle: `same_strategy` (the claim is about this strategy's behaviour, unchanged) **plus** a
  variant `config_change` raising the band to 0.5 (the lever that would act on it), so the child run
  carries both. The claim is measured on the base vehicle's trades on fold B; the variant's grid
  numbers are recorded for E-071, never used to confirm the claim.
- If `confirmed`: `combines_as: execution_rule`, `config_pointer:
  risk_management.controls.min_allocation_change.threshold` (whether `run_protocol` exposes it per
  variant must be checked; if not, the `ema` span transform is the available lever and the pointer
  names it). E-071 applies confirmed execution rules to the composite's own config; they are not
  weighted. If `refuted`: the mechanical story is wrong and the lens text's example is retired.

## 4. Answers to v2's open points (A1.8 item 11)
1. **One claim per session?** One claim **or** no claim, plus a free `discarded` list. Two claims of
   different kinds doubles confirmation looks for little gain and lets a weak second claim ride on a
   strong first one; the lens already gives the kind.
2. **Market vs strategy confirmation?** Different. A market claim needs no vehicle: it is measured
   on the bars.csv of the next fold's first backtest of the same coin and timeframe (P3). A
   strategy claim needs the same strategy run on the next fold (its vehicle) and the trade-level test
   family (P1). Both use the same sign rule plus the relevance floor.
3. **Economic relevance before the backtest?** Never judged. It is a `relevance_floor` computed by
   code from the run's cost model in the claim's unit, written before data; the analyst may raise it
   with a reason, never lower it; code grades `confirmed` vs `confirmed_small` after the fold-B
   measurement. The analyst's only relevance question is "is the observed effect above the floor on
   this run", and that number is in its own query result.
4. **What E-071 needs?** `combines_as`, `scope`, `fold_confirmed`, `effect {value, unit, horizon}`,
   and for execution rules a config pointer (P4). Forecast blocks still enter through the registry
   after a validated run; regime gates likewise; execution rules are applied to the composite config
   by E-071 (its decision whether `execution` becomes a manifest kind).

## 5. What must change in the wider plan (minimum, concrete)
1. **Trade-level claim slots** (P1): one PR in `tools/claim_tests.py` reusing E-074 S3's trades
   reader and exit-cause classifier; CLAIM_TESTS.md gains the family. Blocks the trade lens otherwise.
2. **Two kinds added, two retired for the analyst** (P11): `claim_card.CLAIM_KINDS`, `KIND_BLOCK`.
3. **Claim record fields** (3.4): `fold_observed`, `relevance_floor`, `mechanism.type/predicted_query`,
   `rivals`, `use_if_confirmed.combines_as`, `novelty`: a schema plus `check_claim` extensions; code
   writes the `code:` block (E-075 §2.4 already plans `looks`/`candidates_examined`).
4. **Confirmation grading** adds the floor: `confirmed | confirmed_small | refuted | not_measurable`
   on top of `test_sign` (`explore_confirm.py:697-731`); the ledger row carries the fold and basis.
5. **Market-claim piggyback rule** in decide-next and the ledger (`basis: piggyback`): confirm on the
   next fold's first same-coin/timeframe backtest; no vehicle, no backtest cost.
6. **Analyst memory view** (P5): a new compact builder next to `reader_findings_summary`, fold-labelled,
   confirmed effects only.
7. **decide-next ranking for analyst candidates** (P9): code-written effect/floor, n_events, neighbour
   warning, cost; self-scores recorded only.
8. **E-029 or the interim exit-cause classifier before the trade-lens pilot**; the forecast lens can
   pilot first. The regime lens stays off until the detector is gated (D2 stands).
9. **Pilot process checks** (D4) become: citations resolve; the claim's test and the predicted query
   are in the log; rivals listed with query ids; relevance floor present; no-claim sessions carry an
   examined list; hold rates reported per fold as information. The operator decides.
