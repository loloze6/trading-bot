# E-039 — Move the go/no-go after the backtest

**State:** new
**Owner:** Jérémy
**Updated:** 2026-08-31

## Why

Two gates currently kill a hypothesis **before** it is ever backtested: the
A8.6 power check at validation, and the signal prescreen at stage 7. Jérémy's
challenge, 2026-08-31:

> *"I am doubting we would find a strategy profitable one-shot. We would
> backtest, analyze results, find interesting behavioural aspects in the
> analysis of an unprofitable strategy, and iterate. If we kill the strategy
> before backtest, we maybe miss interesting findings that would allow us to
> iterate on that."*

### What "expensive" actually means, measured

The prescreen exists to avoid *"an expensive walk-forward backtest"*. Measured:

- `protocol_execution` is a **tool stage**: no LLM call, **no token cost**. It
  does not appear in the run audit log at all.
- LLM cost per run: **median $0.36**, max $1.15. **Median 8 minutes** of model
  time across all LLM stages.

So the backtest is expensive in **wall clock and a trial slot** — not money and
not tokens. The thing the prescreen protects is not the thing that costs.

### What the early kills throw away

| | |
|---|---|
| Runs reaching the prescreen | 10 |
| Killed there | **7 (70%)** |
| Killed runs carrying trade diagnostics | **0** |

A prescreen-killed run gets a **stub** `protocol_result.yaml`
(`source: prescreen_stub`) and no `trade_diagnostics.json`. No MAE/MFE, no exit
reasons, no cost attribution, no regime breakdown — exactly the material the
verdict rules and the failure-channel analysis are built to read.

### It has already happened once

**`run_057` was killed by the prescreen on 2026-07-11** with
`ic_active_bars = None` — *undefined by construction*, not a measured zero,
p=0.46. Someone backtested it anyway. The verdict two weeks later reads:

> *"Rule 6 CASE B (regime starvation: `min_trade_count=0` in multiple windows;
> median `cost_drag_pct=4.23%`, benign)…"*

That diagnosis — regime starvation, trade-count floor, cost drag — is
**structurally unavailable** to a prescreen. The kill was overridden and the
backtest produced a different, more specific, more actionable answer.

### The A8.6 gate is worse: it gates on a guess

`_run_a86_power_check` computes `mde = 1/√(n_eff − 3)` from `activation_rate`
and `plausible_ic_upper` — **both written by the LLM** in `hypothesis_card.yaml`.

Predicted activation vs what the prescreen later measured:

| Run | Predicted | Actual | Error |
|---|---|---|---|
| run_053 | 0.27 | 0.076 | 3.6× over |
| run_059 | 0.2 | 1.000 | **5× under** |
| run_060 | 0.125 | 0.500 | **4× under** |
| run_050 | 0.03 | 0.017 | 1.8× over |

**Five of eight wrong by 1.2×–5×**, in both directions. And
`power_check_discrepancy_log.yaml` — the file built in July specifically to
catch this divergence — **has never been written**.

**Jérémy's decision, 2026-08-31: drop it.** *"If the guess is wrong — no. It
falls back to my remark on pre-check: what's the benefit to check before
backtest? Just time, and we lose info given by an unprofitable strategy."*

Recorded as [E037-37](../E-037/FINDINGS.md#e037-37) and the prescreen analysis
in [E037-26](../E-037/FINDINGS.md#e037-26)'s neighbourhood.

---

## The proposed shape

1. **Always backtest.** The result, not a proxy for it, is the evidence.
2. **A deterministic go/no-go runs on the backtest output** — before any LLM
   reads it. Cheap, mechanical, and it protects the thing that actually costs
   money: the interpretation tokens.
3. **The cost gate survives, moved.** An edge below round-trip fees is
   arithmetic and needs no simulation — but it can be computed *from the
   backtest* just as well as before it, and then it is computed from measured
   turnover rather than a proxy.
4. **A8.6 is removed**, not relocated.

## Scope

### In

- Remove the A8.6 pre-flight from both call sites and the validation gate.
- Move the prescreen's cost check to run on `protocol_result.yaml`.
- A deterministic pre-interpretation gate: which results get an LLM verdict and
  which get a mechanical kill with diagnostics preserved.
- Decide what `validation_gate` is for once A8.6 leaves it — see below.
- Keep every killed run's `trade_diagnostics.json`.

### Out

- Removing the prescreen's *IC computation*. It is a useful diagnostic and
  cheap; the question is only whether it may **terminate** a run.
- The variant question — [E-033](../E-033/EPIC.md)'s D1/D2 (E-038 was drafted for
  this, then deleted as a duplicate once S1 was found to already cover it — see
  [E037-43](../E-037/FINDINGS.md#e037-43)), though the two are the same argument
  seen twice and must be sequenced together.

---

## The validation_gate question

With A8.6 removed, `validation_gate`'s remaining work overlaps
`refinement_planner`. Jérémy, 2026-08-31: *"indeed I would merge them."*

**One thing is worth preserving and is neither feasibility nor power:**
**pre-registering what would count as success before any result exists** — the
holdout split (A6.1) and the `pass_rule` the C7 evaluator later scores against.
That is scientific integrity, and removing it would let a verdict be written
after seeing the number.

**The design question for S1:** does pre-registration need a stage, or is it a
field on the brief validated at registration? If the latter, the merge is
clean; if the former, one stage survives with a much narrower job.

---

## Stages

- [ ] **S1 — Characterise and stop.** Re-score the 7 prescreen-killed runs *as
      if* they had been backtested, where the data allows. How many would have
      produced a different or more specific verdict? Measure a backtest's real
      wall clock. Decide where pre-registration lives. Report, then stop.
- [ ] **S2 — (blocked on S1) Remove A8.6.** Both call sites, the validation
      route, and the two stub-writing paths. Bit-identity proof on the runs it
      never blocked.
- [ ] **S3 — (blocked on S1) The post-backtest gate.** Deterministic, reading
      the real result, preserving diagnostics on every path.
- [ ] **S4 — (blocked on S3) Stage consolidation.** Merge `validation_gate` and
      `refinement_planner` per S1's answer on pre-registration.

## Risks

- **Wall clock becomes the binding constraint**, especially combined with
  [E-033](../E-033/EPIC.md) D1's per-variant backtests. S1 must measure it.
- **Trial count rises** — every hypothesis now touches market data. That is
  more honest, and it raises the promotion bar. State it before, not after.
- **Removing a gate is harder to reverse than adding one.** S1's re-scoring is
  the evidence that makes the removal defensible rather than a preference.

## Log

- 2026-08-31 — `new`. Raised by Jérémy during the E-037 review. The A8.6
  removal is his explicit call. `run_057` found while verifying the challenge:
  the pipeline has already overridden a prescreen kill once and learned more
  from the backtest than the kill could have told it.
