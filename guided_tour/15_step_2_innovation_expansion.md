# Stop 15: Step 2, innovation_expansion

## Speech (verbatim)

**Stop 15 of 29: Step 2, innovation expansion.** Open on the side: `workflow_artifacts/skills/innovation-expansion/SKILL.md`, `templates/handoffs/hypothesis_to_innovation_expansion.yaml`, `run_phase1_research.py`, `tools/variant_coin.py`, run_102's `variant_patches.yaml`, `expanded_hypothesis_card.yaml`, `innovation_notes.yaml`.

**In one sentence.**
Step 2 is where an AI proposes a few variants of the base strategy, each a small, named edit of the base config (a patch), so the run tests the idea from more than one angle.

**Why it exists.**
One config on one coin can win or lose by accident. If the idea is real, it should survive a small change of one setting and work on a coin of another kind.
And if every variant fails, the failure blames the idea, not one unlucky setting. The variants are written before any backtest, so they cannot be tuned to a result.

**What comes in, what goes out.**
- In: the brief; the hypothesis card (the one-page idea, from step 1a); the base config (from step 1b, stop 10); the design guide and the component catalogue (stop 11); the coin universe; the list of ideas already tried.
- Out: `variant_patches.yaml` (each variant: an id, a kind, a coin, a list of edits, a reason); an expanded card and notes (diversity audits, what was not pursued, cautions).
- Next: step 5a (stop 16) applies the edits and checks every variant.

**What happens here, step by step.**
1. The AI (Haiku 5.5, the default model) reads its skill and inputs, closed book.
2. It always keeps the **base** variant, the config as step 1b wrote it, unchanged.
3. It adds **design** variants: each changes one parameter or one transform of the components under test, never adds, removes or swaps a component. When the forecast has two or more components, one design variant must halve the weight of the "modifier" component (the negated or subtracted term), a rule from decision D-195 (a row of the decision log).
4. It adds **asset** variants: the same config on a coin of a different category, with data covering every test window (asset generalisability).
5. A regime-gated idea also carries its ungated twin (the same config with no gate); for a regime-gate vehicle, code writes that twin over the AI's answer.
6. It checks diversity (do the variants differ in kind, not only in a number) and what was already tried, and writes its notes.
7. Code checks the variants' shape (one coin per variant, a valid file); an invalid shape gets one retry of step 2, then the run pauses.
8. If the brief gave an exact config and the variant loop were off, code would write step 2 itself (base only).

Example: run_102's step 2 wrote four variants: `base`; `split_stretch_weight` (the stretch leg's weight halved from 0.25 to 0.125, the D-195 split); `asset_xrp_payment` and `asset_ltc_altcoin_l1` (the same config on XRP and LTC). Its notes record that all variants are the same indicator family, so the asset variants carry the diversity, and that the pre-filled claim's rationale holds unfilled placeholders.

**What it costs and how long it takes.**
run_102: one call, 0.88 USD, 89 seconds, one turn (`runs/run_102/pipeline_state.yaml`, audit_log `innovation_expansion_attempt_0`).

**What is switched off or not used here.**
- The old step-2 retry on near-duplicate ideas was retired; the repeat check now runs at step 5a on the actual configs (stop 16).
- The "validation" stage that normally follows step 2 is not reached: the route goes straight to step 5a.
- The halved-weight split is text in the skill; code does not check that the variant was written.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Skill | `skills/innovation-expansion/SKILL.md:1-364` | Mission (`:8`), inputs (`:11`), outputs (`:16-31`), anti-confabulation (`:32`), ungated twin (`:41`), diversity (`:55-106`), asset variants (`:107-156`), tried ideas (`:157-203`), variant patches (`:204-317`; split variant `:287`), checklist (`:318`), forbidden (`:340`) |
| Handoff template | `templates/handoffs/hypothesis_to_innovation_expansion.yaml` | Brief, card, indicator library; deliverables |
| Inputs added | `run_phase1_research.py:9072-9100` | Base config, design guide, catalogue |
| Closed-book inputs | `run_phase1_research.py:3168-3190` | Coin universe, cost model; refine-only files |
| Exact-config step 2 | `run_phase1_research.py:17165` | Code-written base only (loop off) |
| Attempt outputs | `run_phase1_research.py:10096`, `:10113` | Cleared at entry, checked after |
| Route | `run_phase1_research.py:20225-20244` | validation → 5a; ungated twin (`:17021`); shape check (`:18810`) |
| Coin check | `tools/variant_coin.py` | One coin per variant |
| Model | `run_phase1_research.py:1140` | Default `claude-haiku-5-5` |
| Schemas | `workflow_artifacts/schemas/expanded_hypothesis_card`, `innovation_notes`, `variant_patches` | Checked on read-back |
| Examples | `runs/run_102/artifacts/variant_patches.yaml`, `expanded_hypothesis_card.yaml`, `innovation_notes.yaml` | 4 variants |

Remarks: send them as "stop 15: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

### (1) Design and mechanism

1. Of step 2's three deliverables, one is read by code and two by nobody on the live path. 5a reads `variant_patches.yaml` and "nothing else" (`RP:10065`); the exact-config writer says outright that `expanded_hypothesis_card.yaml` and `innovation_notes.yaml` are not written because "no stage on the config-direct route ... reads them" (`:17170-17172`); the closed-book table lists `innovation_notes.yaml` only for `validation` (refine-only) and the flag-off 5a (`:3178`, `:3186`). Whether the analyst's prompt builder reads either is stop 21's question. The skill spends about 150 of its 365 lines on what goes into those two files (IMPROVEMENT 04, 05, 06: `:55-200`), and run_102's step 2 wrote 17,655 output tokens for 0.88 USD (`pipeline_state.yaml:85-89`), the largest output of any stage call, most of it prose with no reader. The cheapest model (Haiku, `:1140`) on the step that decides what gets backtested, writing mostly for nobody: stop 03a note 1.4, made concrete.
2. The two unread files fail their schemas on every run. `expanded_hypothesis_card.schema.json` sets `additionalProperties: false` and `expanded_variants` items as strings (`:12-15`, `:35`); run_102's file has seven extra keys and object items (`expanded_hypothesis_card.yaml:2-7`, `:9-36`, `:38`). `innovation_notes.schema.json` requires `stage`, `recommended_test_order`, `risks_identified`, `integration_notes` and forbids everything else (`:5-15`, `:50`); run_102's notes lack the four and carry `diversity_audit`, `asset_diversity_audit`, `tried_ideas_check`, `refinement_response` (`innovation_notes.yaml:5-16`), the very sections the skill requires (`SKILL.md:88-95`, `:139-146`). So the read-back check (stop 05a note 1.5) warns on both files every run, to stderr, and the schemas describe the flag-off prose output the skill no longer produces. A schema that contradicts the skill that writes the file is worse than none: it makes every warning noise.
3. The design variant is a recipe, and the lineage shows what a recipe does. D-195 says: halve the modifier's weight (`SKILL.md:287-298`). run_101's base had the stretch leg at 1.0; the analyst's finding set it to 0.25 for run_102 (stop 10); run_102's split variant set it to 0.125 (`variant_patches.yaml:12-13`); the run_102-2 candidate puts it back to 1.0 with the trend leg at 0.25 (stop 01, `candidate_briefs/forecast_power-run_102-2.md:110`, `:121`). Three runs, about 8 USD and 24 backtests each, walking one weight ratio up and down. The rule is mechanical by design ("ONE design variant that halves the weight of the modifier"), and the notes record the alternatives it displaced (`innovation_notes.yaml:20-21`: a trend-leg parameter change "candidate for a later pass"). For the goal, a design axis fixed in advance is sound as a control; as the only design variant, it means the campaign's exploration of a two-component idea is a weight ratio.
4. The diversity audit cannot fail in this flow and still has to be written. IMPROVEMENT 04 rejects variants of one library category (`:63-67`); D-053 exempts design variants (`:74-77`) and asset variants are the same config by definition; so `categories_spanned: [trend_following]` with `verdict: real_diversity` (`innovation_notes.yaml:7-11`) is the only possible outcome, and the model says so ("Library-level diversity is nil ... verdict real_diversity on that basis", `:3`). The asset variants carry the real test (same mechanism on another coin, `:107-116`), and the model chose them with care: it ruled out SOL/AVAX/UNI/AAVE on fold-B coverage and LINK on run_101 (`:24-27`), computing coverage from the universe's prose notes that 5a then recomputes in code (`variant_coin.py:16-30`). That part works.
5. The shape check is right-sized: 3 or 4 variants, one base, at least one design, one or two asset, one coin each, asset from another category, base/design on the base coin (`variant_coin.py:668-743`, `:606-641`), one retry with the error then a pause (`RP:18810-18816`, `:18856-18879`); the base variant's config errors are routed to 1b, not to a step-2 retry (`:18829-18844`). What it does not check: that the split variant exists (speech section 6), that a design patch changes "one parameter or one transform" (the patch may change several), or that the halved weight is the modifier's. D-195 is enforced by prompt only.
6. "Written before any backtest, so they cannot be tuned to a result" holds inside a run and not across the lineage: the base of run_102 is the analyst's config change from run_101's result, and the split halves it again in the direction the finding pointed (`variant_patches.yaml:14`, "the direction the finding points"). The fold discipline (stop 06) is what keeps that honest, one generation deep (stop 06 note 1.1).
7. Step 2 caught a step-1a error and nothing acts on it: the notes say the card's `regime_affinity_for_target` is "a misreading" (`innovation_notes.yaml:4`, caution 1) and that the claim rationale carries unfilled placeholders (caution 3, stop 07 note 1.8). Both are true; both go into a file no code reads.

### (2) Legacy or simplifiable (leads)

1. `expanded_hypothesis_card.yaml` and `innovation_notes.yaml` as deliverables on the live path (note 1.1), with their schemas (note 1.2) and the skill sections that fill them (`:24-29`, `:55-106`, `:139-146`). If the analyst does not read them (stop 21), delete the two files, their schemas and the sections, and keep the `tried_ideas_check`/`variants_not_pursued` text (`innovation_notes.yaml:6`, `:17-31`) as a field of `variant_patches.yaml`.
2. `SKILL.md:107-156` (IMPROVEMENT 06) cites "`verdict_interpreter`'s SKILL.md already does exactly this lookup" (`:128-129`) and the old era labels (`:114-116`); `:157-203` (IMPROVEMENT 05) describes the legacy exclusion digest at length (`:169-172`), dead with a memory file present (stop 03a note 2.3).
3. `SKILL.md:321`, `:344`: a `research_brief.yaml` `constraints` field meaning "one variant only"; the live brief's `constraints` key is the exact-config list (stop 01), a different thing under the same name.
4. `SKILL.md:16-22`, `:204-213`, `:306-314`: three passages explaining the flag-off/flag-on branch by the presence of `backtest_spec.yaml`; `:41-49` (regime-gated variants and the deleted A2.3 rule). With the flag folded in, the skill is the IMPROVEMENT 07 section plus the asset rule.
5. `_exact_config_variant_patches` (`:17165-17183`) and `_exact_config_step2_mode` (`:17160-17162`): reachable only with the variant loop off, which no live run has. Not checked for tests.
6. The reading map's "Closed-book inputs `:3168-3190` Coin universe, cost model; refine-only files": for this stage the entry is the coin universe alone (`:3168-3172`); the cost model and refine-only files belong to `validation` (`:3173-3184`).
7. `coin_universe.yaml` has at least six categories (run_102's LTC is in `altcoin_l1_verified_kraken`, `variant_patches.yaml:21`): stop 11's speech and my stop-11 note counted five from the first hundred lines; the file's lines 110-200 were not read. Correction to my own note, lead for the post-tour count.

### (3) Disagreements between the speech and the element

1. Reading map "Schemas ... Checked on read-back": the check runs and fails on both prose files for every run of this flow (note 1.2); "checked" is true, "passing" is not. The speech does not say so.
2. Reading map "Closed-book inputs `:3168-3190` Coin universe, cost model; refine-only files": wrong for this stage (note 2.6).
3. Step 3, "one design variant must halve the weight of the modifier component ... D-195": `SKILL.md:287-298`; correct. Step 5, the ungated twin: `:41-43`, `RP:17021-17075`; correct. Step 7, shape check, one retry then pause: `RP:18810-18816`, `variant_coin.py:668-743`; correct. Step 8: `RP:17160-17183`; correct.
4. Example: four variants, 0.25 to 0.125, XRP and LTC, the two notes: `variant_patches.yaml:3-24`, `innovation_notes.yaml:3-4`; correct. Not stated: the two asset coins are named `XRPUSDT`/`LTCUSDT` in the patches and run as `XRPUSD`/`LTCUSD` on Kraken (`variant_coin.py:617-620`, stop 16).
5. Section 6, "The halved-weight split is text in the skill; code does not check that the variant was written": correct (note 1.5). "The validation stage ... is not reached": `RP:20233-20234`; correct.
6. Section 5: 0.88 USD, 89 s, one turn: `pipeline_state.yaml:81-93`; correct.
7. Reading-map ranges verified: `SKILL.md` sections at `:8`, `:11`, `:16`, `:32`, `:41`, `:55-106`, `:107-156`, `:157-203`, `:204-317`, `:287`, `:318`, `:340` (file ends `:365`, the map says `:364`); `RP:9072-9100`, `:17165`, `:10096`, `:10113`, `:20225-20244`, `:17021`, `:18810`, `:1140`; the handoff template (stop 05a); the three example files; the three schema files.
