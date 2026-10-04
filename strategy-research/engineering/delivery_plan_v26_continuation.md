# Delivery plan v26 — continuation (from "built" to "runs for real")

**Status:** approved by the operator 2026-09-27 (D-033). Continues `delivery_plan_v26.md`, whose
slices 0–8 are built behind flags (see `review_2026-09-27/DELIVERY_REVIEW.md`). Source of the
*what*: the roadmap v27 cards plus `DECISION_LOG.md` (every operator decision since
2026-09-20). This file is the *in which order, proven how*. Review finding ids (A1…, B1…,
C1…, D) refer to `review_2026-09-27/DELIVERY_REVIEW.md`; the walk-through detail is in
`review_2026-09-27/A3_all_flags_on.md`.

**CLOSED 2026-10-03.** C0–C3 done; C4 done with caveats; C5 and C6 partly done, the rest
superseded or moved (status line under each section). Real-run evidence and what broke:
`POST_COMPLETION_plan_v26.md`. Open work now lives in E-066, E-067, E-068 and E-070 (C7).

## In plain words

Plan v26 built every piece, each switched off and tested alone. The review showed that with
everything switched on, a real run crashes before its first backtest, and five pieces drift
from the roadmap. This continuation, in order:

1. **C0 — Get the machine ready** (Python environment for the bot, merge CUL-336).
2. **C1 — Make one full run work**, proven by an end-to-end test that uses the real run set-up
   and fake AI answers, written *first* so it fails, then fixed until it passes.
3. **C2 — Fix the five vision drifts** (one coin per variant; experts see every variant;
   "distance" scored as card I; a crashed variant can never validate an idea; variant shape).
4. **C3 — Profit bars v2** (whole-period drawdown and Sharpe on the portfolio, ≥100 trades per
   coin, beat buy-and-hold, survive 2× costs, the agreed values).
5. **C4 — Two real runs**, switched on together, cost and behaviour measured.
6. **C5 — Remaining gaps**, each its own ticket, some needing an operator decision first.
7. **C6 — Close-out**: Linear, stale docs, operator guides, roadmap v28, post-completion report.

C0 → C1 → (C2 ∥ C3) → C4. C5 and C6 run alongside, never blocking C4 unless marked.

---

## 0. Rules

The seven rules of `delivery_plan_v26.md` §0 still apply (two-phase S1/S2, off by default and
bit-identical when off, run budgets, legacy never rewritten, measurement channel, dispatch
header, docs move with code). Added, from what the review taught us:

8. **Test the joined-up path, not only the piece.** Any slice that changes a stage's inputs or
   outputs extends the C1 end-to-end wiring test; a green suite with a broken real path is
   exactly what the review found (A9).
9. **Decisions are logged.** A decision is added to `DECISION_LOG.md` in the same PR as its S1
   "Decision" section; S1 dispatches read the log's entries for their theme before proposing
   anything (a 2026-09-22 decision was lost between slices, B2).
10. **Ask only what is open.** Before an S1 puts a question to the operator it checks the code
    and the cards/log; if they already answer it, it is a fix, not a question
    (`tasks/lessons.md` 2026-09-27).
11. **Review cycle stays:** build → code-review skill → fix → test (suite in two halves on this
    machine) → PR merge → Linear update. Implementation agents on Opus, inventory/docs on
    Sonnet, the orchestrator verifies top findings.

---

## C0 — Machine ready (no design; small)

**Status: done** (C0.1 = CUL-336, PR #235).

| # | Item | Evidence | Done when |
|---|---|---|---|
| C0.1 | Merge CUL-336 (closed-book stage agents) after its review fixes — incl. switching off the CLI auto-memory the stage agents still load, and restoring legacy stages' cross-run inputs. | branch `fix/cul-336-closed-book-stages` | merged |
| C0.2 | Create the trading-bot Python environment the tool stages call: `venv/` at the repo root (Windows: `venv/Scripts/python.exe`) from `trading-bot/requirements.txt` (pandas<3 trap), never committed. Fix `RUNBOOK.md`'s interpreter paths. | A3 §3.2; `_resolve_tbot_python` | `_resolve_tbot_python()` returns it; e054/k3 tool-worker tests pass without a junction |
| C0.3 | Claude calls go through the Claude CLI logged in with the operator's account (no API key; credentials present; runs count against the account's usage limits); `GEMINI_API_KEY` is set. Verify one real stage call still authenticates after CUL-336 (neutral cwd, no settings). | A3 §3.6 | one real stage call works |

## C1 — One full run works (E-061, new epic: "Run the new pipeline end to end")

**Status: done** (PRs #238, #241–#243; C1.1 green).

**S1 is not needed:** A3 already characterized it. **S2a first, test before fixes:**

| # | Item | Review id |
|---|---|---|
| C1.1 | **End-to-end wiring test** (`tests/test_e061_end_to_end_wiring.py`): real `setup_run` + real handoff templates in a sandbox root, the full target flag set (A3 §1), stubbed LLM at `run_claude_worker`/`_invoke_reader_llm`, stubbed subprocesses (validate_config, data gate, run_protocol writing per-variant `results/`, `bars.csv`, `trade_diagnostics.json`), driven by `run_campaign.process_once()` twice (run 1 → decide_next mints a candidate → run 2 sees run 1 in memory). Asserts per A3 §5 items 8–9, incl. argv (no `--validation-protocol` to a missing file) and a profit-bars stop → `holdout_decision.yaml: continue` → resume. Written first; expected to fail on A1/A2. | A9 |
| C1.2 | Port the handoff contract to config-direct: `backtest_specification` and `protocol_execution` handoffs without `validation_protocol.yaml`; create `backtest_spec_to_data_availability_gate.yaml` on the config-direct branch; make `variant_patches.yaml` a checked deliverable of stage 2; fix the duplicated `required_inputs` key in `hypothesis_to_innovation_expansion.yaml`. | A1 |
| C1.3 | `run_tool_worker`: pass `--validation-protocol` only when the file exists (or teach `run_protocol.py` it is optional under config-direct) — verified before any backtest spend. | A2 |
| C1.4 | Uncaught stage exceptions become a classified pause (`status: paused_for_human`, a RUNBOOK row, `last_error`), never a crashed campaign process that restarts into the same crash. | A4 |
| C1.5 | Pre-flight before any LLM spend: every flag dependency (variant_loop→config-direct, composition_runs→4 prerequisites, anti-adjacency gate→regroup_record) and the brief's protocol (D-3 `promotion_unratified`) are checked at launch; strict boolean flag readers (a quoted `"false"` refused). | A6, A8 |
| C1.6 | `_era_id_for_timestamp`: open-ended last era (`hi: null`) handled; test on a window reaching `era_2026_h2_forward_recorded`. | A7 |
| C1.7 | First-run kit: a new operator brief template for the new pipeline (`machine_constraints`, `protocol_ref` to a protocol without the generic promotion block, `criteria_from: hypothesis_generation`) + a RUNBOOK "start a campaign on the new pipeline" section. | A6 |

Variant-count handling (A5) moves to C2.5 because it depends on one-coin-per-variant.
**Done when:** C1.1 passes; all fixes are flag-on paths only, flag-off byte-identity pinned.
**Run budget:** none (the test is the proof).

## C2 — Vision fixes (decisions already taken: D-003, D-014, D-015, D-016, D-017)

**Status: done** (PRs #237, #248, #251–#253, #256). Follow-ups CUL-344/345/347 moved to their epics.

One S1 for the whole slice (it touches stage 2, the protocol runner, the grid, the reports and
the readers), then S2a–S2e.

| # | Item | Review id | Card / decision |
|---|---|---|---|
| C2.1 | **One coin per variant.** A variant carries its coin; `protocol_execution` runs that variant's backtests on that coin only; the asset variant uses a coin from a different `coin_universe.yaml` category; the skill's "asset" example fixed. Grid cells are then per variant = per coin; `symbol_reducer` only for cross-sectional ideas (variant = universe). **S1 must settle:** how the equal-weight-portfolio profit bars apply when a variant is one coin (likely: the portfolio of that variant's coins, i.e. the coin itself; branch 3 passes if any one variant clears every bar), and how a variant's coin interacts with the data gate and composites. | B1, B5 | cards C, D |
| C2.2 | **Experts see every variant.** `build_reports` reads `variants/<id>/` (protocol_result, bars, trade diagnostics) and produces per-variant slices; readers' skills say how to use them. | B2 | E-033 S1 decision 2026-09-22 |
| C2.3 | **"Distance to profitable" as card I** (3 = fills a missing block type with low correlation to the registry; 0 = neighbour of something validated). Readers receive a compact registry summary; rubric and `rubric_version` updated; decide_next ranking unchanged in code. | B3 | card I |
| C2.4 | **A crashed variant can never validate an idea:** a variant with no graded result becomes an INCONCLUSIVE column; the failed trial row stays. Fix the tie-break comment's source to the new decision number. | B4, C1 | log 2026-09-27 |
| C2.5 | **Variant shape:** 3 variants, cap 4, checked on stage 2's output (retry, not a late raise); the data-gate floor counts only variants lost to data, with honest labels when a config error removes one. | A5 | card D |

**Done when:** each item has its tests, C1.1 extended (per-coin variants, per-variant reports),
flag-off byte-identical. **Run budget:** none here (C4 proves it).

## C3 — Profit bars v2 (E-062, new epic; decisions D-034..D-039, D-041, D-042)

**Status: done** (PRs #236, #240, #254–#259, #261, #265–#267, #269; bars signed 2026-09-29, PR #269). Follow-ups CUL-346/348/349/350 moved to E-067.

**Amended 2026-09-28 (D-041, D-042):** S2b also unifies scoring — the Sharpe bar, the deflated-Sharpe score and the trial ledger all use the whole-test daily Sharpe (no separate sparse path; legacy trial rows recomputed from saved results where possible) — and normalises the time-dependent bars for partial-coverage variants (trades per year + absolute floor; drawdown limit scaled to period length).

Short S1 (how walk-forward windows chain into one curve: are they contiguous, overlapping,
gapped; what "whole test" means per protocol), then S2.

| # | Item |
|---|---|
| C3.1 | Drawdown = worst drawdown over the whole test on the equal-weight portfolio curve (windows chained). |
| C3.2 | Trade count = at least 100 trades per coin over the whole test. |
| C3.3 | Sharpe = on the portfolio's daily returns over the whole test. |
| C3.4 | New bar: beats equal-weight buy-and-hold of the tested coins, after costs. |
| C3.5 | New mandatory bar: survives 2× costs (realized gross edge / cost > 2.2). |
| C3.6 | Values written and ratified in one PR with the new definitions: Sharpe 1.0, avg daily return 0.0005, deflated Sharpe 0.95, max drawdown 20% (whole-period), cost ratio 2.2 with ≥100 trades, residual IC > 0.02 at one-sided p < 0.05, `min_n_eff` 30; `ratified_by`/`ratified_at` filled by the operator. |

The bars file's sha256 changes, so any earlier evaluation is not spendable (by design, 6c S2d).
**Run budget:** none (C4).

## C4 — Two real runs (operator go needed)

**Status: done with caveats.** run_065 (Donchian daily, Kraken perp) resumed twice by hand after
CUL-379 and CUL-380; run_066 (vol-managed trend, Kraken perp) hands-off. Both `refuted`.
C4.4 report: `POST_COMPLETION_plan_v26.md`.

| # | Item |
|---|---|
| C4.1 | Pre-conditions: C0–C3 merged; C1.1 green with the C2/C3 extensions; operator has signed the bars file. |
| C4.2 | Operator switches the target flag set in one edit (A3 §1, unquoted booleans, no campaign running) and registers the first brief from the C1.7 template. |
| C4.3 | Two consecutive real runs (= E-059 S4 two-run proof; also satisfies the slice 4/5/6 run budgets). Measured per stage: turns (CUL-336: must be 1), tokens, cost, wall time, pauses; trial rows `run:variant`; memory/registry/decision record written. The holdout is never touched. |
| C4.4 | Report: what worked, what broke, cost per run; then the operator decides on models per stage (today every stage runs on Haiku 4.5) and on continuing the campaign. |

Deferred until blocks exist: E-060 S4 (first real composition run, needs two validated blocks)
and E-060 S5 (regime blocks).

## C5 — Remaining gaps (own tickets; ⚑ = needs an operator decision in its S1)

**Status: partly done.** Done: C5.1, C5.6, C5.7, C5.8. **C5.2 superseded by E-068**
(composable claim tests). C5.3, C5.4, C5.5 moved to backlog decision tickets. C5.9 (CUL-335)
moved to E-067. C5.10 (E-035) stays parked.

| # | Item | Review id |
|---|---|---|
| C5.1 | Scale-free refusal + extend the registration lint (slice 2.4 promise). | C4 |
| C5.2 ⚑ | Criterion menu: add IC, correlation, regime-conditional criteria. | C5 |
| C5.3 ⚑ | Composite configs: keep code-written, or let 1b design them (card F); `target_instrument_set` read or dropped. | C6 |
| C5.4 ⚑ | Reader patches re-graded on the same windows that prompted them: fresh windows or accept with DSR + holdout as the guard. | C7 |
| C5.5 ⚑ | Revisit two accepted defaults: residual-IC composite backtest without a trial row; the campaign-review "reframe" brief placed ahead of reader candidates unscored. | C8 |
| C5.6 | **Moved before C4 (D-043):** drop the promotion-threshold requirement for config-direct runs now; full retirement of promotion blocks goes to the post-C4 clean-up epic. | C9 |
| C5.7 | Missing schemas (`grid_evaluation`, `idea_status`, `variant_patches`); score provenance (model id from the call, not self-reported). | C11, C12 |
| C5.8 | Stop feeding the legacy promote/kill/refine label to readers; retire base-only `pass_rule_evaluation.yaml` under the flags. | C13 |
| C5.9 | CUL-335 (holdout consume ledger) — before the first real holdout spend. | — |
| C5.10 | E-035 external dispatch — parked epic. | — |

## C7 — Legacy clean-up epic (after C4, D-043)

**Status: moved** to the parked epic E-070 · Legacy clean-up (C7).

After the two real runs work: make the new pipeline the default (declared change); then an inventory of legacy code (S1) and its removal in tested steps — old routing, verdict_interpreter, validation stage, escalation, families, promotion blocks; legacy re-readers last.

## C6 — Close-out (Sonnet, alongside)

**Status: done, two items deferred.** C6.1, C6.2 done. C6.3: two of three one-pagers written
(`docs/OPERATOR_START_CAMPAIGN.md`, `docs/OPERATOR_UNLOCK_HOLDOUT.md`); "read a run's results"
deferred until after E-068 (the readers change). **C6.4 (roadmap v28) deferred until after
E-068.** C6.5 = `POST_COMPLETION_plan_v26.md`.

| # | Item |
|---|---|
| C6.1 | Linear: move plan-v26 epics to their real state, link slice tickets to epics, tick milestones, create E-061/E-062 and the C-tickets. |
| C6.2 | Stale docs (review D list + A3 §4), and annotate `delivery_plan_v26.md` where decisions superseded its text. |
| C6.3 | Operator one-pagers: start a campaign on the new pipeline; read a run's results; unlock the holdout. Written after C4 so they describe the real flow. |
| C6.4 | Roadmap v28: fold DECISION_LOG into the cards. |
| C6.5 | Post-completion report of plan v26 + this continuation, with C4's real-run evidence. |

---

## Dispatch order

**Status: superseded** (plan closed 2026-10-03).

1. Now: C0.1 (review in progress), C0.2, C6.1 (Linear) — independent.
2. C1 S2a: the wiring test (red), then C1.2–C1.7 until green.
3. In parallel after C1: C2 S1 and C3 S1 (read-only); operator nods; C2 and C3 builds.
4. C4 with the operator.
5. C5 tickets by priority (C5.1, C5.6, C5.8 first — no decision needed), C6 alongside.
