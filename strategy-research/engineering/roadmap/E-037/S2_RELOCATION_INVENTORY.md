# E-037 S2 — Relocation inventory

The evidence that S2 lost nothing. Required by the EPIC's hard constraint and
by [`S1_TARGET_SHAPE.md` §4](S1_TARGET_SHAPE.md#4-information-loss-checklist).

**Range:** `e4f2f229` (S1 tip, the S2 branch point) → `9f9f9b4d`
**File:** `strategy-research/docs/USER_GUIDE.md`
**Size:** 976 → 1965 lines · **+1013 added, −24 removed**

---

## 1. Mechanical residue check

Run per §4.3, over the whole range rather than per commit:

| Category | Result |
|---|---|
| Amendment codes, issue refs, run ids (`A8.6`, `#50`, `F5c`, `run_044`, …) | **zero decrease** |
| Numbers and dates | **zero decrease** |
| Backticked identifiers | **zero decrease** |

No token that existed at `e4f2f229` occurs fewer times at `9f9f9b4d`.

---

## 2. Every removed line, with its destination

24 lines were removed. **All 24 come from four field tables that were replaced
with richer ones.** 8 are table scaffolding (`| Field | Definition |` headers
and `|---|---|` separators) carrying no content. The remaining 16 are field
rows, every one of which is accounted for below.

Three destinations are used:

- **kept** — the field is real; its description was carried into the new table.
- **preserved as intended-design** — the field does **not** exist in any real
  artifact ([F22](FINDINGS.md#f22), [F24](FINDINGS.md#f24)). Its name and
  description are quoted **verbatim** in a ⚠️ note directly above the new
  table, explicitly marked as absent. Nothing was deleted; it was relabelled
  from *this is the artifact* to *this was the intended design*.
- **relocated** — moved to a different part of the same entry.

### `validation_decision.yaml` (lines 3–5)

| Removed | Destination | Verbatim? |
|---|---|---|
| `status` — "`approve`, `conditional_approve`, `refine`, or `reject`" | kept — new `Values / range` column, each value now glossed | expanded |
| `rationale` — "Brief explanation of the decision" | kept — expanded with a real example | expanded |
| `blocking_issues` — "List of specific problems that must be fixed before backtest (only present when status = refine)" | kept | expanded |

### `decision.yaml` (lines 8–10)

| Removed | Destination | Verbatim? |
|---|---|---|
| `stage` — "Stage that produced this decision" | kept | expanded |
| `status` — "`approved`, `blocked`, etc." | **preserved as intended-design** — both values quoted verbatim in the ⚠️ note; measured 0 occurrences in 39 files ([F23](FINDINGS.md#f23)) | yes |
| `blocking_issues` — "Any config problems found during validation" | kept | expanded |

### `verdict_interpretation.yaml` (lines 13–18)

| Removed | Destination | Verbatim? |
|---|---|---|
| `altitude` — "Numeric altitude of the decision (1 = refine, 2 = pivot, 3 = escalate)" | **preserved as intended-design** — quoted in the ⚠️ note; 0 of 39 | yes |
| `verdict` — "`refine`, `pivot`, `escalate`, `promote`, or `kill`" | **preserved as intended-design**; 0 of 39 | yes |
| `diagnostic_rule_applied` — "Which named diagnostic rule triggered this verdict (e.g., `cost_drag`, `signal_inversion`)" | **preserved as intended-design**; 0 of 39 | yes |
| `root_cause` — "The underlying problem identified from diagnostics" | kept — real (11 of 39), expanded with its `mechanism_failure` values | expanded |
| `parameter_bracket` — "If refining a parameter, the [min, max, step] range to search next" | **preserved as intended-design**; 0 of 39 | yes |
| `next_altitude` — "Fallback altitude if the current verdict fails again" | **preserved as intended-design**; 0 of 39 | yes |

### `regime_detector_report.yaml` (lines 21–24)

| Removed | Destination | Verbatim? |
|---|---|---|
| `detector_version` — "Hash of the detector config (used to tag findings in KB, per A5.3)" | kept — A5.3 reference retained | expanded |
| `persistence_score` — "Fraction of regime transitions that persist ≥ dwell_period" | kept as a row **and** noted as absent at top level; the real field is `regime_persistence_median_bars`, nested under `per_symbol_per_timeframe[].metrics` ([F24](FINDINGS.md#f24)) | yes |
| `class_conditional_sensitivity` — "Per-label flip rate under ±10% parameter perturbation" | as above; real name `class_conditional_sensitivity_per_label` | yes |
| `activation_rate` — "Fraction of bars per regime label (must be in [10%, 40%] for trend labels)" | as above; real name `trending_activation_rate` | yes |

**Nothing else was removed.** Every other S2 change is an insertion: 13 stage
blocks, 5 new artifact entries, 27 rationale headliners, the flag-gate
subsection, the tools inventory, the §4 scope note, and the ⚠️ notes above.

---

## 3. Anchors

Every `file:line` introduced by S2 was verified against the working tree.
**Nine were wrong on first write and were corrected** before the commit that
introduced them, or in the commit immediately after:

`:712`→`:711` · `:2431`→`:2433-2434` · `:2443`→`:2445-2447` ·
`:5790-5796`→`:5788-5796` · `:1150`→`:1147` · `:2457`→`:2459` ·
`:2280`→`:2278` · `:6278`→`:6280` · `:2189`→`:6048`

That nine of roughly forty were wrong on first write is the argument for the
re-verification step being mandatory rather than advisory.

---

## 4. One self-correction

S1 stated `prescreen_result.yaml` has "two shapes… a four-key stub". It has
**three**: the full result, plus two *different* A8.6 stubs — the
validation-gate writer emits five keys including `stage_blocked_at`
(`run_phase1_research.py:2297`), the `run_loop` pre-flight emits four without
it (`:6226`). Found by opening `runs/run_060/prescreen_result.VOID_block_size_bug.yaml`.
Corrected in both `S1_TARGET_SHAPE.md` and the guide.

---

## 5. Landing criteria (§4.5)

- [x] Relocation inventory committed, every removed line has a destination
- [x] Mechanical residue check run, output recorded, zero decreases
- [x] All `file:line` anchors re-verified; nine corrected
- [ ] **Reviewed by someone other than the author** — outstanding; this is
      Jérémy's step, and it is the one control the author cannot perform

---

## 6. What S2 did not do

- Did not change any code.
- Did not fix any finding. All 25 are recorded in [`FINDINGS.md`](FINDINGS.md)
  with a proposed disposition marked as S3's decision.
- Did not restructure §2.1's stage map, compress the §2.2 index table's
  Objective column, or hyperlink glossary terms — all S4.
- Did not normalise the five `**Objective:**`-style artifact entries; doing so
  silently would have destroyed the evidence for [F20](FINDINGS.md#f20) and
  [F21](FINDINGS.md#f21).
