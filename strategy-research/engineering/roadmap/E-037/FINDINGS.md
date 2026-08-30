# E-037 — FINDINGS

Doc-vs-code disagreements found while writing E-037.

**Rule: findings are RECORDED, never fixed here.** No code and no
`USER_GUIDE.md` text has been changed on their account. They become cards or
issues at S3, where Jérémy decides which get worked.

**Status of this file:** seeded by **S1** (2026-08-30), which audited exactly
one stage (7, `signal_prescreen`) and one artifact (`prescreen_result.yaml`)
to prove the templates in [`S1_TARGET_SHAPE.md`](S1_TARGET_SHAPE.md). S2
appends the remaining 12 stages and ~30 artifacts to this same file.

**Reviewed against:** `master` at `753c9ac3`, working tree at branch
`docs/e037-s1-target-shape`. Every `file:line` below was verified against that
tree, not inferred.

That eleven findings came out of **one** stage and **one** artifact is itself
the finding the epic predicted: the pipeline has no written input/output
contract, so nobody could see them.

## Summary

| ID | Severity | Type | Lands on |
|---|---|---|---|
| [F1](#f1) | medium | doc-vs-code | `docs/USER_GUIDE.md §2.2` |
| [F2](#f2) | medium | doc-vs-code | `docs/USER_GUIDE.md §3` |
| [F3](#f3) | low | doc-incomplete | `docs/USER_GUIDE.md §3` |
| [F4](#f4) | medium | doc-vs-code | `docs/USER_GUIDE.md §3` |
| [F5](#f5) | medium | doc-vs-code | `docs/USER_GUIDE.md §2.2 + §3` |
| [F6](#f6) | low | doc-vs-code | `docs/USER_GUIDE.md §2.2` |
| [F7](#f7) | **high** | doc-missing-contract | `docs/USER_GUIDE.md §3` |
| [F8](#f8) | low | doc-incomplete | `docs/USER_GUIDE.md §2.2 + §3` |
| [F9](#f9) | medium | doc-vs-doc | `strategy-research/CLAUDE.md` |
| [F10](#f10) | **high** | code-defect | `strategy-research/tools/episode_significance.py:209` |
| [F11](#f11) | medium | code-fragility | `strategy-research/workflow/run_phase1_research.py:3237` |

**Counts:** 2 high · 6 medium · 3 low. By type: 5 doc-vs-code, 2
doc-incomplete, 1 doc-missing-contract, 1 doc-vs-doc, 1 code-defect, 1
code-fragility.

**The two that are code, not documentation** — F10 and F11 — are the ones that
do not go away by editing a sentence. F10 in particular is a fix that looked
complete and was not.

---

## F1

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 (stage 7)`

**Found by:** S1 worked sample, 2026-08-30


§2.2 stage 7's Objective opens "A8.6 pre-flight first (blocks if power insufficient)", under Engine = *Python tool*. `tools/prescreen_signal.py` contains **no power check at all**. A8.6 runs in the orchestrator, at `run_phase1_research.py:6217` (immediately before the tool subprocess) and again at `:2287` inside `determine_post_validation_route`. The stage row conflates orchestrator wrapper logic with tool logic — exactly the confusion E-037 exists to remove. §2.1's stage map is *not* wrong here: it correctly attaches A8.6 to both validation_gate and signal_prescreen.


**Proposed disposition (S3 decides, not this file):** Correct the stage-7 row to attribute A8.6 to the orchestrator, not the tool.


---

## F2

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3's `prescreen_result.yaml` `route` enum lists 6 values and **omits `no_signal_artifact`**, which the code emits at `prescreen_signal.py:1481` and which **overrides every other route**. A reader of §3 cannot know the most consequential route exists.


**Proposed disposition (S3 decides, not this file):** Add `no_signal_artifact` to the route enum and mark it as overriding.


---

## F3

**Severity:** low · **Type:** doc-incomplete · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3's field table lists 6 fields; the written artifact has roughly 30 top-level keys. Load-bearing omissions: `forecast_hash` (dedup key for trial counting), `sigma_is_placeholder` (invalidates `cost_check` when true), `significance_methodology_used`, `gap_stats_by_symbol`, `a86_power_check`. Not an error — but nothing marks the table as a selection, so absence reads as non-existence.


**Proposed disposition (S3 decides, not this file):** Mark the table as a selection; add the five load-bearing omissions.


---

## F4

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (prescreen_result.yaml)`

**Found by:** S1 worked sample, 2026-08-30


§3 says **Created by:** "signal_prescreen tool (`tools/prescreen_signal.py`)". On the insufficient-power path the file is created by the **orchestrator** (`run_phase1_research.py:6232` and `:2297`) and the tool never runs. The `Created by` line is wrong for one of its three creation paths, and the resulting artifact has a completely different shape (4 keys, no IC/cost/provenance fields) that §3 does not mention.


**Proposed disposition (S3 decides, not this file):** List all three creation paths; document the 4-key stub shape.


---

## F5

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 + §3`

**Found by:** S1 worked sample, 2026-08-30


Both §2.2 stage 7 ("block-bootstrap significance") and §3 (`ic_significance` — "block-bootstrap") name the **fallback** method as if it were the default. The default is block-deflated **Fisher z** (`z = IC * sqrt(n_eff - 3)`, `prescreen_signal.py:643`, labelled `block_{n}_fisher_z` at `:1377`). A stationary block bootstrap runs only on the degenerate-active-forecast path (`:730`), and A8.5.1a episode-blocking is a third method (`:1402`). Three methods, one name in the doc.


**Proposed disposition (S3 decides, not this file):** Name the three methods separately; default is block-deflated Fisher z.


---

## F6

**Severity:** low · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 (stage 7)`

**Found by:** S1 worked sample, 2026-08-30


§2.2 stage 7 says "Records trial in `campaign_state.trial_sharpes` (A6.2)". Done by the orchestrator (`_record_prescreen_trial`, `run_phase1_research.py:4039`, called at `:1130`, `:6215`, `:6235`), not by the tool. Same class as F1.


**Proposed disposition (S3 decides, not this file):** Attribute A6.2 trial recording to the orchestrator.


---

## F7

**Severity:** **high** · **Type:** doc-missing-contract · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §3 (regime_audit_decision.yaml)`

**Found by:** S1 worked sample, 2026-08-30


**Undocumented cross-stage write.** `run_prescreen` writes into **stage 10's** artifact: it opens `runs/{run_id}/artifacts/regime_audit_decision.yaml` and resolves `ungated_escape_eligible` in place (`prescreen_signal.py:1582` → `_resolve_ungated_escape`, `:1092`). §3's `regime_audit_decision.yaml` entry says **Created by:** "regime-auditor skill" and has **no** `Updated by` line, so no reader of the guide could discover that stage 7 rewrites it. This is precisely the input/output-contract blind spot the EPIC blames for the bug list feeling uncontrollable — and it is the strongest evidence that the `Updated by` normalisation in §2 of this document is load-bearing rather than cosmetic.


**Proposed disposition (S3 decides, not this file):** Add an `Updated by` line naming signal_prescreen. Consider whether a cross-stage in-place write is the design you want -- that part is a CODE question, not a doc one.


---

## F8

**Severity:** low · **Type:** doc-incomplete · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md §2.2 + §3`

**Found by:** S1 worked sample, 2026-08-30


Two significance thresholds live in `_determine_route` and only the stricter one is documented anywhere: `_SIG_THRESHOLD = 0.10` gates IC significance (`prescreen_signal.py:87`), while a second `p > 0.05` test inside the cost branch decides `kill_cost_hurdle` vs `refine_cost_hurdle` (`:1042`). Neither §2.2 nor §3 mentions either number.


**Proposed disposition (S3 decides, not this file):** Document both thresholds and what each decides.


---

## F9

**Severity:** medium · **Type:** doc-vs-doc · **Status:** open, untriaged

**Lands on:** `strategy-research/CLAUDE.md`

**Found by:** S1 worked sample, 2026-08-30


`strategy-research/CLAUDE.md` — loaded into every session in this directory — contradicts `USER_GUIDE.md` twice. (a) It lists a **10-stage** workflow (`screening_backtest`, `walk_forward_validation`, `final_holdout_test`, `robustness_analysis`, `research_decision`) that does not match the guide's canonical 13 stages; four of those five names exist nowhere in the guide. (b) Its global rule "Validate outputs against schemas before moving to the next stage" asserts exactly the schema enforcement that §3's own 2026-08-27 correction records as **false**. The guide's §2 preamble claims to be "the only place that is maintained as authoritative", but the file an agent reads *first* says something else. Out of scope to fix here; noted because S4's cross-linking work has to decide whether `CLAUDE.md` points at the guide or restates it.


**Proposed disposition (S3 decides, not this file):** Decide whether CLAUDE.md points at USER_GUIDE.md or restates it. It currently restates it wrongly, and it is what an agent reads first.


---

## F10

**Severity:** **high** · **Type:** code-defect · **Status:** open, untriaged

**Lands on:** `strategy-research/tools/episode_significance.py:209 (+ :59)`

**Found by:** S1 worked sample, 2026-08-30


**A stale hardcoded `24` survives in the A8.5.1a label, and a real run proves it.** `prescreen_signal.py:1371-1376` records that the method label used to read `block_24_fisher_z` while `block_size` had become a derived per-timeframe value, and that this was fixed on 2026-08-28 so "the name is what a later reader reconstructs the method from; it has to track the arithmetic." That fix was applied to the **default path only**. The A8.5.1a dense-fallback branch still returns the hardcoded string `"block_24_dense_fallback"` (`tools/episode_significance.py:209`) while passing the derived `block_size` into `_block_adjusted_significance`. `runs/run_060/artifacts/prescreen_result.yaml` (2026-08-28) carries `significance_methodology_used: block_24_dense_fallback` next to `ic_significance_block24.block_size: 6` — the artifact asserts 24 and the arithmetic used 6, which is exactly the defect the comment claims closed. **Not a one-line fix:** the literal is also a member of `VALID_METHODS` (`episode_significance.py:59`), which the orchestrator's F4d conformance gate matches against, so the label and the gate must change together.


**Proposed disposition (S3 decides, not this file):** Derive the label from block_size, and update VALID_METHODS and the F4d conformance gate in the same change. Needs a decision on already-archived artifacts carrying the wrong label.


---

## F11

**Severity:** medium · **Type:** code-fragility · **Status:** open, untriaged

**Lands on:** `strategy-research/workflow/run_phase1_research.py:3237 (+ the stamp site)`

**Found by:** S1 worked sample, 2026-08-30


`protocol_version` is stamped as a **platform-dependent path string**. run_060 recorded `protocols\funding_mr_4h_retest_v1.json` with a Windows backslash. `_check_prescreen_conformance` compares it by bare filename via `Path(executed_identity).name` (`run_phase1_research.py:3237-3241`); on Windows that yields `funding_mr_4h_retest_v1.json`, but on macOS/Linux `PosixPath` does not treat `\` as a separator, so `.name` returns the **entire string** and the pre-registration check reports a spurious violation. Reachability, stated honestly: within a single run the artifact is produced and checked on the same machine, so this does not bite today. It bites when an artifact crosses platforms — which is precisely the dual-writer research model the fork operates under, and the fork's standing rule is that Mac and Windows results should be identical.


**Proposed disposition (S3 decides, not this file):** Normalise protocol_version to a POSIX-style relative path at write time, or compare by basename in a separator-agnostic way.


---

## Log

- 2026-08-30 — file created by S1. F1-F9 came from reading
  `tools/prescreen_signal.py` and `workflow/run_phase1_research.py` against
  `USER_GUIDE.md` §2.2 and §3. F10 and F11 came from a second pass, filling
  the artifact template's example-value column from a real run
  (`runs/run_060/artifacts/prescreen_result.yaml`, 2026-08-28) — neither was
  visible from the code alone. Reading real output found defects that reading
  the source did not.
