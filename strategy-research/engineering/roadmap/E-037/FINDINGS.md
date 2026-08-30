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
| [F12](#f12) | medium | doc-unresolvable-reference | `docs/USER_GUIDE.md` (whole document) |
| [F13](#f13) | medium | wrong-citation | `strategy-research/tools/prescreen_signal.py:1089,1100,1580` |
| [F14](#f14) | medium | phantom-field | `docs/USER_GUIDE.md:613` |
| [F15](#f15) | medium | doc-vs-code | `docs/USER_GUIDE.md` §2.2 · `run_phase1_research.py:88` |
| [F16](#f16) | **high** | stage-does-not-run | `docs/USER_GUIDE.md` §2.1/§2.2 (stage 10) |
| [F17](#f17) | medium | silent-no-op | `run_phase1_research.py:2410` |
| [F18](#f18) | **high** | unenforced-rule | `docs/USER_GUIDE.md` §2.2 (stage 3) |

**Counts:** 4 high · 11 medium · 3 low. By type: 5 doc-vs-code, 2
doc-incomplete, 1 doc-missing-contract, 1 doc-vs-doc, 1
doc-unresolvable-reference, 1 wrong-citation, 1 phantom-field, 1 code-defect,
1 code-fragility.

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

## F12

**Severity:** medium · **Type:** doc-unresolvable-reference · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` (whole document)

**Found by:** S1 review follow-up, 2026-08-30

`USER_GUIDE.md` cites **14 distinct amendment codes across 26 mentions**
(`A1.1`, `A1.3`, `A1.4`, `A2.1`, `A2.2`, `A2.3`, `A3.4`, `A3.6`, `A5.3`,
`A6.1`, `A6.2`, `A8.1`, `A8.6`, `A9.1`) and **never once says where any of
them is defined**. The definitions live in
`engineering/improvements/done/design_and_docs/AMENDMENTS_01-06.md`, a file
the guide does not reference at any point — verified by grep for
`AMENDMENT` across all 976 lines: zero hits. A reader who meets "records
trial in `campaign_state.trial_sharpes` (A6.2)" has no path to what A6.2
actually says, which is that deflated Sharpe needs the *variance* across
trials and therefore every evaluation counts as a trial, kills included.
That reason is the entire justification for the sentence, and it is one
unreferenced file away.

This is the epic's central complaint in miniature — the knowledge exists and
is correct, but cannot be assembled from one place. It is also a known
failure mode with a recorded incident: **C4, "Rule-citation confabulation"**
(`engineering/improvements/done/IMPROVEMENTS_DONE_20260712.md:216`) records a
card citing *"A3.6, n_episodes >= 8 per window"* where the label was wrong
(the real rule was A8.5.1a-spec rule 3) and the qualifier was invented, and
concludes: *"Plausible-looking fake citations survive until someone quotes
the source verbatim."* Its prescribed fix was a machine-readable rule index
(id → verbatim text → source line) plus a lint step. **No such index exists**,
and the guide is the document most likely to be cited from.

Note: S1's own first draft reproduced the defect — it used `A6.2` four times
without ever expanding it. That is how cheaply this propagates.

**Proposed disposition (S3 decides, not this file):** Either add a rule index
(id → one-line gloss → `file:line`) to `USER_GUIDE.md` §6 and link every
citation to it, or at minimum reference `AMENDMENTS_01-06.md` once and gloss
each code on first use. The S1 stage template now requires the gloss-and-link
on first use within a block; that convention is worth applying guide-wide.

---

## F13

**Severity:** medium · **Type:** wrong-citation · **Status:** open, untriaged — needs the author's confirmation

**Lands on:** `strategy-research/tools/prescreen_signal.py:1089`, `:1100`, `:1580`

**Found by:** S1 review follow-up, 2026-08-30

Three sites label the `ungated_escape_eligible` write-back as an "A9.1 side
effect": the section comment at `:1089`, the `_resolve_ungated_escape`
docstring at `:1100`, and the call site at `:1580`.

**A9.1 as defined** (`AMENDMENTS_01-06.md:156`) is *"Named must-reject
fixture: `keltner_163`"* — an Improvement 09 acceptance criterion requiring
the cost gate to reject the Keltner config despite its passing IC. It says
nothing about ungated escape. There is exactly one `A9.1` heading in the
repository, so this is not a renumbering collision — verified by grep across
all markdown.

The rules that **do** govern the behaviour are cited correctly in the same
docstring's body: A2.1 (detector-confidence deadlock escape) supplies the
`ungated_escape_eligible` concept, and A2.3 rule 5 supplies the requirement
that the metric be all-bars IC. So the docstring contradicts its own heading.

Stated fairly: the same file uses A9.1 **correctly** at five other sites
(`:20`, `:1607`, `:1614`, `:1651`, `:1656`), all about the keltner_163
two-stage rejection. This looks like a label attached to the wrong paragraph
rather than a systematic misunderstanding, and it has **no runtime effect** —
it is comment text. It is recorded because it misleads readers and because
S1 propagated it into the documentation before catching it, which is exactly
the C4 pattern described in [F12](#f12).

**Proposed disposition (S3 decides, not this file):** Confirm with the author
whether A9.1 was intended, then relabel the three sites to A2.1 / A2.3 rule 5
if not. Cheap to fix, but it is a citation correctness question, so it should
be answered rather than guessed.

---

## F14

**Severity:** medium · **Type:** phantom-field · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md:613`

**Found by:** S1 information-loss check, 2026-08-30

`USER_GUIDE.md:613` documents the `cost_check` field as
`{pass: bool, edge_to_cost_ratio, required_gross_edge_bps}`.
**`required_gross_edge_bps` does not exist.** It is emitted by no Python file
in the repository — verified by grep across `strategy-research/` and
`trading-bot/` — and it is absent from every real artifact, including
`runs/run_060/artifacts/prescreen_result.yaml`.

The dict the code actually emits has **eight** keys: `symbol`,
`implied_trades_per_window`, `estimated_gross_edge_bps_per_trade`,
`cost_bps_per_trade`, `edge_to_cost_ratio`, `safety_factor_required`, `pass`,
`ic_used`. So the guide names three keys, one of which is imaginary, and omits
six real ones — including `safety_factor_required`, which is the threshold the
gate compares against, and `ic_used`, which records *which* IC fed the
estimate.

**How it was found is the point.** This did not turn up by reading the guide;
it turned up because the epic's own information-loss check flagged
`required_gross_edge_bps` as a token that disappeared between drafts. The
check asked "where did this fact go?", and the answer was "it was never a
fact." A mechanical residue check catches phantom content as well as lost
content — an argument for running it on every S2 and S4 section rather than
treating it as a formality.

**Proposed disposition (S3 decides, not this file):** Replace the three-key
description with the real eight, or mark it explicitly as a partial list.
Worth checking the other artifact entries for the same defect during S2 —
this one was invisible until an artifact was opened.

---

## F15

**Severity:** medium · **Type:** doc-vs-code · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.2 · `strategy-research/workflow/run_phase1_research.py:88`

**Found by:** S2, 2026-08-30

The guide numbers **13 stages**. The engine's own registry, `STAGE_CONFIGS`
(`run_phase1_research.py:88`), has **10 entries**. Three of the guide's stages
are not in it:

- **stage 1 `research_brief`** — a human input, not an orchestrator stage.
- **stage 9 `regime_detector_validation`** — a helper function, see [F17](#f17).
- **stage 10 `regime_auditor`** — never dispatched at all, see [F16](#f16).

Separately, **stage 4 is named `validation` in code and `validation_gate` in
the guide** (`STAGE_CONFIGS["validation"]`, `determine_post_validation_route`,
`_SKILL_MAP["validation"]`). The guide uses `validation_gate` in §2.1, §2.2 and
§2.3. Neither name is wrong, but only one is the key you would grep for.

This matters for the epic's core purpose: a reader trying to trace "which
sub-steps does my change reach?" cannot map the guide's numbering onto the
code's dispatch table.

**Proposed disposition (S3 decides, not this file):** Mark which entries are
engine stages and which are not, and give stage 4 both names.

---

## F16

**Severity:** high · **Type:** stage-does-not-run · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.1 and §2.2 (stage 10)

**Found by:** S2, 2026-08-30

**The guide documents `regime_auditor` as an automated Claude stage. The
orchestrator never dispatches it.**

- It is absent from `STAGE_CONFIGS` (`:88`), so it is never a `current_stage`.
- It is absent from `_SKILL_MAP` (`:689`), which maps the **7** dispatchable
  Claude stages. `_build_stage_prompt` raises `ValueError(f"No SKILL file
  mapped for stage: {stage_name}")` for anything not in that map (`:711`), so
  it could not be dispatched even if it were reached.
- **No code writes `regime_audit_decision.yaml`.** The orchestrator only
  *reads* it if it happens to exist (`:6251`, `:6382`), and the only writer
  anywhere is `prescreen_signal.py:1118`, which updates an existing file and
  returns early if there is none.

What actually happens: on the `regime_misattribution` path the pipeline
**pauses for a human** (`status="paused_for_human"`) and prints *"consult
regime-auditor skill and regime_detector_report.yaml"* (`:5788-5796`). The
skill at `workflow_artifacts/skills/regime-auditor/` is real; it is invoked by
a person, not the engine, and only on that one path.

§2.1's map draws it inline between stages 9 and 11 as if it always runs, and
§2.2 gives it Engine = *Claude*, which reads as automated.

**Consequence:** every downstream statement that assumes
`regime_audit_decision.yaml` exists — including the A2.2 retune firewall check
and stage 7's `ungated_escape_eligible` write-back — is conditional on a human
having produced it. Nothing says so.

**Proposed disposition (S3 decides, not this file):** Re-label stage 10 as a
human-invoked skill on a paused pipeline, or make it a real stage. This is a
design question, not a wording fix.

---

## F17

**Severity:** medium · **Type:** silent-no-op · **Status:** open, untriaged

**Lands on:** `strategy-research/workflow/run_phase1_research.py:2410`
(`_ensure_regime_detector_report`)

**Found by:** S2, 2026-08-30

Stage 9 is a helper called from inside the `verdict_interpreter` stage
(`:6250`, `:6381`), not a registry stage. Three facts about it that the guide
does not carry:

1. **It can silently do nothing.** If `candidate_strategy_config.json` is
   missing it prints a warning and returns `None` (`:2433-2434`); if
   `validate_regime_detector.py` exits non-zero it prints and returns `None`
   (`:2445-2447`). Neither raises. The verdict then proceeds with no detector
   report, and the only trace is stdout.
2. **The report is campaign-level, not per-run.** It is written to
   `ROOT / "regime_detector_report.yaml"` — one file shared by every run.
   §3 does not say this, and the artifact's placement implies per-run.
3. **"Stale" means older than 30 days** (`:2425`), a threshold documented
   nowhere.

Point 1 sits badly next to the project's own standing rule that anything
feeding decisions should raise on degenerate inputs — the rule that produced
the run_060 guards in `prescreen_signal.py`.

**Proposed disposition (S3 decides, not this file):** Document all three.
Whether the silent return should raise is a separate code decision.

---

## F18

**Severity:** high · **Type:** unenforced-rule · **Status:** open, untriaged

**Lands on:** `docs/USER_GUIDE.md` §2.2 (stage 3)

**Found by:** S2, 2026-08-30

§2.2 states stage 3 **"Must: pass real-diversity check (≥2 `library_category`
OR `data_requirements`; cosmetic = rejected)."** That reads as a mechanical
gate. **Nothing enforces it.**

`library_category` appears exactly **once** in all of `workflow/` and `tools/`
— inside a prompt string at `run_phase1_research.py:490`. No code reads the
field from `expanded_hypothesis_card.yaml`, counts distinct categories, or
rejects an expansion. The rule lives entirely in
`workflow_artifacts/skills/innovation-expansion/SKILL.md:74-105`, as an
instruction to the model, including the `diversity_audit` block the model is
asked to self-report with `verdict: real_diversity`.

So the "check" is the model grading its own homework, and "cosmetic =
rejected" describes an outcome no code can produce.

This is the **same defect class** the guide already corrected once: §3's
preamble was fixed on 2026-08-27 after "all artifacts are validated against
JSON schemas" turned out to be false. The pattern is a stated guarantee whose
enforcement was never built — and the guide's phrasing ("Must:", "rejected")
is what makes it look built.

**Proposed disposition (S3 decides, not this file):** Restate as
skill-guidance, or build the check. Worth a sweep of every other "Must:" in
§2.2 for the same pattern — this is now two confirmed instances of a stated
guarantee with no enforcement, which makes it a class, not an incident.

---

## Log

- 2026-08-30 — file created by S1. F1-F9 came from reading
  `tools/prescreen_signal.py` and `workflow/run_phase1_research.py` against
  `USER_GUIDE.md` §2.2 and §3. F10 and F11 came from a second pass, filling
  the artifact template's example-value column from a real run
  (`runs/run_060/artifacts/prescreen_result.yaml`, 2026-08-28) — neither was
  visible from the code alone. Reading real output found defects that reading
  the source did not.
