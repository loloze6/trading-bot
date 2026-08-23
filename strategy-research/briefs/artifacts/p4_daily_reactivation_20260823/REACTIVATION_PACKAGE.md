# P4_ts_trend parent-rule reactivation package (2026-08-22/23)

**Status: for operator ratification. Nothing in this package flips the queue
entry to `ready`, runs a backtest, or launches a campaign.** Precedent for
ratifying a pass_rule before any run: H-041-C-v2 (2026-07-15).

**Bottom line, conclusion first: condition (d) fails.** Measured
correlation-adjusted breadth of the daily Kraken panel (n_eff ≈ 1.66–1.69)
falls well short of the ≈3.0 an honest, pre-registered sample floor requires.
**This reactivation is not powered** to support a reliable per-window
`median_sharpe` criterion under the ruled floor-5 gate. Conditions (a) and
(b) are resolved; (c) is drafted but deliberately left without a numeric
threshold for the reason (d) gives. No rule is proposed for ratification that
would only pass by weakening a floor after seeing this number.

## Task 1 — ruling recorded (condition (b) resolved)

The operator ruling (2026-08-22): `config/campaign_config.yaml:141`'s A3.4
gate (`trade_floor_per_window: 5`) governs. `protocols/ts_trend_daily_v1.json:132`'s
`promotion.min_trade_count_gte`, set to 1 by the 2026-07-08 revision, is
superseded — changed to 5. The 2026-07-08 revision's reasoning is retained in
that file (not deleted), with a new dated note explaining the ruling and
supersession.

Locations updated (4 of 4 living/authoritative documents found that state the
1-vs-5 conflict; denominator below):

1. `strategy-research/protocols/ts_trend_daily_v1.json` — `min_trade_count_gte`
   changed 1 → 5. Found at line 133 pre-edit-line-count / 132 at the time the
   task brief was written (the task's own line refs are explicitly stale-
   tolerant; a new `_note_min_trade_count_ruling_20260822` key was inserted
   just above it, which is why the field itself is now one line further down,
   at 133); new note key added alongside the retained `_note_min_trade_count`.
2. `strategy-research/campaign_record/campaign_knowledge_base.yaml` —
   `p4_sma_trend_longonly_daily_auto.reactivation_condition` field starts at
   line 1230; condition (b)'s own text is a few lines further into that
   block. Resolution appended in place (this file's own established
   convention: dated in-line corrections inside prose fields, e.g.
   `engine_provenance_caveat`'s "Label correction 2026-07-24").
3. `strategy-research/config/campaign_queue.yaml` — the `P4_ts_trend` entry's
   `notes` field (found starting at line 4/10, matching the task's
   reference) — new `STATUS AS OF 2026-08-23` block prepended above the
   2026-08-05 entry, per this file's own newest-first convention.
4. `strategy-research/engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md`
   P4-D2 item (found at line 2294, matching the task's reference) — resolution
   bullet appended after the original "NOT RESOLVED HERE" line.
5. `strategy-research/engineering/roadmap/E-030/EPIC.md` Log — the 2026-08-22
   entry (found at line ~317) records the conflict as it stood that day and
   is left untouched (it is an accurate historical statement of what was true
   at HEAD on 2026-08-22); a **new** dated entry was appended after the
   epic-closing 2026-08-23 entry, explicitly marked as unrelated to the
   epic's own scope/Done-when, recording the resolution.

That is 5 living-document locations edited (protocol, KB, queue, ledger,
epic log — items 1–5 above; the epic log carries both the original statement,
left alone, and a new resolution entry, counted once).

**2 locations found but deliberately NOT edited:**
`strategy-research/engineering/sessions/session_reports/20260723_p4_density_probe.md`
and `.../20260724_p4_density_probe_archive.md` both state the Floor-A-vs-Floor-B
conflict explicitly (with line numbers, e.g. `20260724_...:363-386`). Both are
dated, read-only "compliance record" artifacts that explicitly assert in their
own text "No edit to the knowledge base, campaign queue, protocols, tools,
briefs, or the price cache" as part of their own audit trail. Editing them
after the fact would falsify that record and breaks the project's own
established convention for historical snapshots (append-only, dated,
new-entry corrections in *living* documents — KB, queue, ledger, epic log —
never rewriting a closed session report). Flagging this explicitly in case
the operator wants them touched too; I did not, on the judgment that doing so
would be inconsistent with how every other correction in this campaign is
recorded.

**Search denominator:** `grep -rn` for `min_trade_count_gte|trade_floor_per_window`
across `strategy-research/` returned 43 files; the large majority are
unrelated protocols/tests with their own, different, floor values (e.g.
`baseline_v1.json`, `baseline_v2.json`, per-hypothesis protocol files) that
happen to share a key name, not a statement of the P4 1-vs-5 conflict. A
second, targeted grep for `P4-D2|1 vs 5|five-trade floor` plus manual review
of every hit's surrounding context is what produced the 7 locations above (5
edited + 2 found-not-edited). `SESSION_LOG.md:1636`,
`20260722_c7ext_audit.md:203`, and
`K2_verdict_machinery_design_20260713.md:184` also matched the key-name grep
but describe unrelated protocols (`baseline_v2.json`'s own floor of 20) — not
this conflict — and were excluded.

## Task 2 — daily-panel n_eff (MEASURED)

Script: `compute_daily_neff.py` (this directory). Raw output:
`daily_neff_output.txt` (this directory, captured verbatim from the script
run). Data: `trading-bot/local_data/kraken_*USD_1d.csv` (19 files, landed
2026-08-07, commit 8cff3f24; no holdout data touched — every source file's
own last row is 2025-12-31).

**power_check.py does not fit this task.** It computes `n_eff_symbols` from a
single, pre-supplied scalar `rho` (`campaign_config.yaml`'s
`symbol_correlation.btc_eth_return_correlation_1h`, a fixed 2-symbol BTC/ETH
constant) — it has no facility to compute a pairwise correlation MATRIX over
an arbitrary N-symbol panel from raw price data, which is what this task
requires. Bending it to do so would mean rewriting its core loop; writing a
fresh, small script that reuses only its `n_eff = n/(1+(n-1)*rho)` formula
(the one piece that does fit) was the smaller change. The new script's
methodology otherwise exactly mirrors
`engineering/sessions/session_reports/_verify_xs_neff.py` — the script that
produced the ratified 1h prior — so the two numbers are apples-to-apples: same
19-symbol set, same pairwise-complete Pearson correlation on log returns, same
formula.

**MEASURED (primary method — pairwise-complete Pearson correlation on daily
log returns, `min_periods=100`, matching the 1h prior's own methodology):**

| Population | n | rho_bar | n_eff | minEig | PSD |
|---|---|---|---|---|---|
| all-19 (Kraken daily) | 19 | +0.5800 | **1.661** | −0.0940 | No |
| primary-17 (BTC/ETH excluded) | 17 | +0.5646 | **1.694** | +0.0251 | Yes |

**Cross-check (listwise common-window, all 19 symbols required present —
truncates to the 548 days from 2024-07-02 where even the shortest-history
symbols, TAO/ONDO, have data):**

| Population | rows | rho_bar | n_eff |
|---|---|---|---|
| all-19 | 548 | +0.5837 | 1.651 |
| primary-17 | 548 | +0.5654 | 1.692 |

The two methods agree closely (n_eff within 0.01–0.02 of each other for both
populations), so the pairwise-complete number is not an artifact of unequal
history lengths across symbols. The all-19 pairwise-complete matrix has a
mildly negative minimum eigenvalue (−0.094, a known artifact of averaging
correlations computed over non-identical sample windows when symbols have
very different history lengths — TAO/ONDO start mid-2024) — this does not
affect `rho_bar` (a simple mean of the off-diagonal entries, well-defined
regardless of the matrix's definiteness) and the primary-17 population (which
excludes nothing for history-length reasons, only for the BTC/ETH
contamination ruling) is fully PSD.

**Reconciliation against the known 1h prior (rho_bar=+0.5419, n_eff=1.767,
same 19-symbol universe, `_verify_xs_neff.py`):** the daily rho_bar
(+0.5800, all-19) is 3.8 percentage points HIGHER than the 1h figure, giving
a LOWER n_eff (1.661 vs 1.767, ≈6% lower). **This is the expected direction**
per the task's own framing — daily returns average out more of the
idiosyncratic, venue-microstructure noise that suppresses HOURLY cross-asset
correlation, so daily correlations run higher and daily n_eff runs lower.
The magnitude of the shift (≈6% lower n_eff) is modest, not an order-of-
magnitude divergence, and both the pairwise-complete and listwise methods
agree on it independently — no reconciliation concern, no adjustment made
toward the 1h prior.

## Task 3 — pass_rule draft (condition (c)): NOT AUTHORED TO A PASSABLE FORM

Draft: `pass_rule_draft_NOT_RATIFIED.yaml` (this directory), run_059-shaped
(top-level `pass_rule` with `criteria`/`outcomes`, top-level
`machine_constraints`) so `tools/verdict_criteria_evaluator.py`'s
`_find_pass_rule` resolves it without a code change.

**Criteria (a) and (b) are complete and pre-registered, inherited unmodified**
from `protocols/ts_trend_daily_v1.json`'s own promotion block
(`median_sharpe_gt: 0` at line 130, `max_abs_drawdown_pct_lt: 30` at line
131), both dated 2026-07-08 — before runs 053/054/057 executed. Not tuned to
any measurement.

**Contamination (operator ruling, this package):** primary universe = the 17
non-BTC/ETH Kraken pairs. BTC/ETH excluded by ASSET (already measured under
this family on Binance in runs 053–057; Kraken BTC/ETH are the same assets,
different venue, not an untouched sample), not by symbol string. BTC/ETH may
be reported separately, descriptively, never gating.

**Criterion (c), the evaluability/sample-floor gate tied to the floor-5
ruling, could not be given a passable, honestly-derived threshold — this is
the MANDATORY EXIT BRANCH.**

Derivation, in order (threshold fixed BEFORE consulting Task 2's number):

1. Two distinct power questions exist for this hypothesis and must not be
   conflated:
   - The **pooled-all-bars block-bootstrap IC significance test**
     (`ts_trend_daily_v1.json`'s own `significance_methodology_for_
     single_magnitude_signals: block_bootstrap_all_bars_v1`) — already
     established `adequately_powered` in the KB
     (`power_disposition.status`, `expected_n_eff: 117`, for the original
     2-symbol registration) and, if anything, reinforced by pooling more
     symbols (more total bars). **Unaffected by this finding.**
   - The **per-window `median_sharpe` criterion (a)'s own reliability**,
     which depends on how many window-symbol observations survive the A3.4
     floor-5 exclusion and how INDEPENDENT (correlation-discounted) those
     surviving observations are. This is what KB condition (d) and this
     task ask for, and what criterion (c) was meant to gate.
2. The applicable pre-existing, project-standing bar for (2) is
   `CLAUDE.fork.md`'s own global rule: **"Sample floor: ≥100 trades or
   ≥30 independent episodes before quoting a Sharpe."** Criterion (a) is
   literally a Sharpe (`median_sharpe`), so the ≥30-independent-episode leg
   is the directly on-point standard (the ≥100-raw-trades leg does not apply:
   the brief itself insists on a *correlation-adjusted* count — "Breadth
   across ~15 symbols with correlation adjustment is what makes this powered
   at all" — so a raw, non-discounted trade tally is not the right test).
3. The brief's own `power_preregistration` (`research_brief_P4_ts_trend.md:47-50`)
   gives `expected_active_n`: "signal transitions ≈ 10–25 per symbol over
   6y." The protocol's OWN floor-1 derivation (`ts_trend_daily_v1.json`'s
   retained `_note_min_trade_count`) already anchors on the LOWER end (10)
   of this same range for a conservative floor — this draft follows the
   same, already-established, conservative-anchor convention, not a new
   choice made to produce a particular answer.
4. Required breadth: 30 independent episodes ÷ 10 episodes/symbol (low-end
   anchor) = **n_eff ≥ 3.0**.
5. **Sensitivity, shown in full rather than picking one number:** anchoring
   at the brief's midpoint (17.5/symbol) requires n_eff ≥ 1.71 — essentially
   tied with, and still just above, the measured 1.694/1.692. Only the
   brief's own UPPER bound (25/symbol) drops the requirement to n_eff ≥ 1.20,
   which the measured breadth clears. Selecting the upper bound now, after
   seeing n_eff, would be exactly the after-the-fact threshold selection
   this project's research protocol forbids ("No thresholds after seeing
   data — ever").
6. Measured n_eff (Task 2, primary 17-pair universe): **1.694** (pairwise) /
   **1.692** (listwise). Against the conservative, already-anchored
   requirement of 3.0, this clears only ≈56–57%. Against even the midpoint
   anchor (1.71), it does not clear.

**Conclusion: the daily Kraken panel, correlation-adjusted, does not supply
enough independent bets to responsibly quote a per-window `median_sharpe`
under the ruled floor-5 gate.** No criterion (c) with a numeric threshold is
proposed. `pass_rule_draft_NOT_RATIFIED.yaml` records criteria (a)/(b) as
complete and criterion (c) as explicitly blocked, with the reasoning above,
so the record shows what was tried and why it stopped rather than silently
omitting the attempt.

## What this does NOT do

- Does not flip `config/campaign_queue.yaml`'s `P4_ts_trend` entry to `ready`.
- Does not edit `protocols/ts_trend_daily_v1.json`'s `symbols` list to the
  17/19-pair universe (a live-run precondition, not attempted here).
- Does not run any backtest, prescreen, or campaign.
- Does not touch `local_data/holdout_sealed/` in any way.
- Does not relitigate or reopen the closed gated ER(20)≥0.30 variant.

## Recommended next step (for the operator, not decided here)

This is a "not powered as specified" finding, which is itself the requested
deliverable. If the operator wants to pursue this family further, the
options this package surfaces (none pursued, none prescribed) are: (i)
widen the universe with additional, less-correlated assets before
re-measuring n_eff; (ii) evaluate the parent rule on a POOLED/bar-level
statistic (e.g. the `bar_equity` block from `fix/metrics-bar-equity`) that
does not depend on a per-window median and therefore is not exposed to the
same sparse-window sample-floor problem; or (iii) accept a materially
different, independently-justified episodes-per-symbol anchor with its own
a-priori justification, pre-registered before any further measurement. None
of these is authorized or recommended by this package — they are listed only
because the task asked for the reactivation package, and a dead end with no
map of the exits is a less useful deliverable than one with the exits
labeled.
