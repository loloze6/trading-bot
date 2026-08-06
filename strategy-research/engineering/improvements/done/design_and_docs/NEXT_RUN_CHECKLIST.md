# Next-Run Checklist

Use before launching the first new hypothesis run after plan closure. Items marked **[VERIFY]** require a concrete output check, not a visual scan.

---

## 1. Trial recording — live confirmation

**Context:** The A6.2 recording hook was fixed on 2026-07-04. Two new code paths now call `_record_prescreen_trial()`:
- Validation-gate A8.6 bypass (when `prescreen_result.yaml` already exists with `route=insufficient_power_a_priori`)
- Pre-flight A8.6 bypass (when `_run_a86_power_check` fires before prescreen tool)

Both paths include an idempotency guard (`any(t.get("trial_id") == run_id for t in trial_sharpes)`) to prevent duplicate recording on resume.

**[VERIFY] After the run completes:**
```
grep "trial_sharpes" strategy-research/campaign_record/campaign_state.yaml
```
Expect the new `run_0XX` entry to appear. The `source` field should be `prescreen` (for A8.6 kills) or `backtest` (for full-backtest runs). If the run is killed at prescreen via IC/cost gate, source=prescreen and statistic_valid=neither. If it passes prescreen and runs the backtest, `_record_backtest_trial()` fires and statistic_valid will be sharpe or expectancy.

**[VERIFY] Idempotency:** Run the pipeline with `--resume` on a completed run. The trial_sharpes entry count must not increase.

---

## 2. KB auto-recompute — live confirmation

**Context:** `_recompute_kb_views()` is called inside `_write_kb_findings_entry()`, which fires at verdict_interpreter stage completion. The `exhausted_mechanisms` and `coverage_matrix` views are recomputed from the findings list every time a new finding is written.

**[VERIFY] After verdict_interpreter completes:**
```
grep -A5 "exhausted_mechanisms:" strategy-research/campaign_record/campaign_knowledge_base.yaml
```
Expect the list to be populated (6 entries currently). If a new finding qualifies (evidence_count >= 3 OR analytic basis), it should appear. If the run adds no new finding, the views are unchanged — that is correct behavior.

**[VERIFY] No new finding added:** If the run is killed at prescreen, no KB entry is written and the views are not recomputed. That is expected — prescreen kills are trials, not findings.

---

## 3. Improvement 04 generation audit

**Context:** Improvement 04 seeded the indicator library and added a lookup protocol and diversity check. This audit has not been exercised on a live run yet. The first batch should be evaluated against all three criteria.

**[AUDIT] After hypothesis_generation completes, check hypothesis_card.yaml for:**
- `library_lookup`: the hypothesis must name the indicator used and cite the library entry (id, category, regime_affinity).
- `deviation_justification` (if applicable): if the signal deviates from the library's empirical findings, a one-sentence mechanism reason must be present — not boilerplate.
- `diversity_audit` in expanded_hypothesis_card.yaml (after innovation_expansion): at least 2 of the 3 expanded variants must differ in `library_category` OR `data_requirements`. Cosmetic parameter changes (RSI(14) → RSI(21)) sharing the same category and data source are flagged as redundant.

**[AUDIT] After innovation_expansion completes:**
```
grep "diversity_audit" strategy-research/runs/run_0XX/artifacts/expanded_hypothesis_card.yaml
```
Expect a `diversity_audit.verdict: pass` field. If `verdict: reject`, the run must loop back — do not proceed to validation with a cosmetic expansion.

---

## 4. Pre-registration ceremony

**Context:** Per standing rule 2, every run that will touch walk-forward data must have a pre-registered expected outcome. This is written BEFORE the component is built, not after. Pre-registration is the defence against post-hoc narrative fitting.

**[WRITE BEFORE RUNNING] Create `pre_registration.yaml` in the run artifacts dir before launching:**
```yaml
run_id: run_0XX
hypothesis_id: H-0XX-Y
registered_at: "2026-07-XX"  # date written, not run date

# Power check (A8.6 — deterministic, compute before component build)
expected_active_n: <integer>   # bars where signal fires (from hypothesis_card)
n_eff_symbols: <float>         # n / (1 + (n-1)*rho_bar); for market-wide signals rho_bar ~ 0.82
min_detectable_ic: <float>     # 2.0 / sqrt(n_eff)
plausible_ic_upper: <float>    # from hypothesis prior (literature or mechanism reasoning)
power_verdict: power_adequate | insufficient_power_a_priori

# Outcome range (for the walk-forward; if prescreen passes)
# Write these BEFORE any backtest result is observed
expected_sharpe_range:
  pessimistic: <float>    # Sharpe below which you'd be surprised but not shocked
  base_case: <float>      # Most likely outcome given the mechanism
  optimistic: <float>     # Sharpe above which you'd be surprised — overfit territory
expected_ic_range: [<lo>, <hi>]   # active-bar IC expected range
expected_cost_ratio: <float>      # gross edge / round-trip cost; must be >= 2.0 to pass
disconfirming_outcome: >
  [One sentence: what specific result would falsify the mechanism hypothesis,
   not just miss the hurdle. e.g., "IC < 0 on active bars with p < 0.10
   would indicate the signal is anti-predictive, not merely weak."]
```

**[VERIFY] Before running the backtest, confirm pre_registration.yaml exists and expected_sharpe_range is written.** The holdout stage enforces `expected_range` was written before execution — the same discipline applies to the walk-forward run even though it is not mechanically enforced there.

---

## 5. Feed alignment check (non-OHLCV only)

**Context:** Standing rule 5. If the hypothesis uses funding rate or F&G:
- Funding rate (8h): signal bar is the bar AFTER settlement (not the settlement bar itself). Verify the component uses `funding_next_bar` or equivalent offset-corrected join.
- Fear & Greed (daily): the index for day D is published at EOD D. The signal for 1h bar at D+1 00:00 is the EARLIEST bar that can use the D index without lookahead. Verify the join offsets this correctly.

If IC passes > 0.15 on a feed-based signal, alignment re-verification is mandatory before crediting the result.

---

## 6. Holdout gate reminder

**Context:** Holdout (2026-H1: 2026-01-01 to 2026-06-30) is consumed once per hypothesis, pre-registered, and failure is terminal (standing rule 1). The holdout evaluation stage enforces:
- `holdout_consumed_by` check in `campaign_data_policy.yaml`
- `expected_range` must exist in `holdout_result.yaml` BEFORE `holdout_evaluation` is triggered
- Failure verdict writes to `completed_rejected` — no appeal path

The campaign currently has no hypothesis in promote status, so the holdout gate will not fire on the next batch. This checklist item becomes live when the first `verdict_label: promote` appears.
