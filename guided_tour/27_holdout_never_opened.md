# Stop 27: The holdout (never opened)

## Speech (verbatim)

**Stop 27 of 29: The holdout (never opened).** Open on the side: `config/campaign_data_policy.yaml` (key names only), `tools/holdout_policy.py`, `tools/holdout_date_gate.sh`, `tools/hooks/pre-commit`, `docs/OPERATOR_UNLOCK_HOLDOUT.md`, `run_phase1_research.py`, `tools/run_protocol.py`, `trading-bot/data/data_manager.py`, `tools/run_viewer/sanitize.py`.

**In one sentence.**
The holdout is a sealed stretch of market history that no research run may touch: the final, single-use exam for an idea, opened only after the operator decides to spend it.

**Why it exists.**
Every month research looks at slowly becomes a month the campaign has tuned itself on. Folds (fixed sets of test months) reduce this, but they are reused. The holdout is never reused: one look per idea, and a fail ends that idea for good. Without it, nothing would tell a real edge from one found by searching.
So the seal matters as much as the exam. One peek, in a backtest, a chart or a committed file, spends it.

**What comes in, what goes out.**
- In: the data policy (the file holding the sealed range and the list of ideas that already spent it); a profit-bars stop (a variant beat every campaign-wide profit bar); the operator's decision file.
- Out: refusals everywhere else; when unlocked, a pause for one backtest run by hand; a result file; the idea added to the spent list; an ending, promoted or rejected.

**What happens here, step by step.**
1. The sealed range has one home, the data policy. One small reader parses it strictly; a missing or malformed policy is a refusal, never "no holdout".
2. Run protocols (the list of test windows) do not carry the dates; they carry a pointer to the policy.
3. The guards. The backtest tool refuses, before fetching anything, a window that reaches the seal. The data feed refuses a request that reaches into it, then any returned bar inside it; that refusal is never turned into "no data". The run viewer masks every date inside the seal. A commit check, as a local hook and in CI, blocks any file that would publish a date inside the seal unless it is registered as provenance or prose. The sealed store is the literal directory `local_data/holdout_sealed/`; git ignores it.
4. The only way in. A variant passes every profit bar; the run pauses. The operator writes a decision file: "continue" (holdout untouched, the run ends normally) or "spend", naming the variant, attesting that the trial ledgers (the record of every experiment) are merged, and signing it.
5. On "spend", code checks: the decision belongs to this run and this stop; the variant still passes under the same bars file; the idea is not on the spent list; no other run holds an unfinished spend; the deflated Sharpe (return per risk, discounted for the number of trials) still clears its bar on today's ledger; the brief declares the strategy tradable. Any failure: a refusal with a code, nothing spent.
6. The run pauses again. The operator runs the holdout backtest by hand, for that variant only, with two deliberate switches and the idea's name. The tool refuses again if the name is already spent or the protocol's holdout disagrees with the policy.
7. The operator writes the result. Code records the spend first (the intent, then the idea on the spent list), then decides: pass, promoted; fail, rejected. A result edited afterwards, or not matching the unlock, pauses and is never a promotion.
8. Any other route to the holdout pauses with nothing spent. A result found without an unlock is recorded as spent and never promoted.

Example: run_102's own files are not in this checkout. In this checkout the policy's spent list is empty: no idea has spent the holdout.

**What is switched off or not used here.**
- The older single-use gate is not reached under the current flags, skipped at RP:19856.
- This checkout's switchboard file (master) has the retired-routing switch off; the unlock path above runs only with it on, as in the tour's flag set (stop 03).
- In this checkout the setting that points git at the tracked hook is unset, so the local hook does not run here; CI runs the date check on Linux only.
- My grep found no engine caller that passes the data feed's switch for sealed bars: the backtester loads without it (`trading-bot/core/backtester.py:229`).
- The unlock one-pager lists three tickets to fix before the first real spend.

**Reading map.**

| Part | File:line | What it does |
|---|---|---|
| Policy keys (names only) | `config/campaign_data_policy.yaml:1-15` (header), `:23` `holdout_range`, `:41` `holdout_unchanged`, `:177-184` sealed Kraken store block (`quarantined`, `source_dir`, `era`, `span`, `sealed`, `single_use`, `status`), `:210` `binance_cache_holdout_contaminated` (`spans_holdout_range :214`), `:288` `holdout_contaminated_runs`, `:413-414` `holdout_overlap`, `holdout_range_unchanged`, `:535` `holdout_consumed_by` (empty), `:542` `holdout_failure_is_terminal` | The range's one home and the spent list |
| One strict reader | `tools/holdout_policy.py:1-29` (doc), `:39-48`, `:56-136` (day and range parse, `load_policy`, `load_holdout_range`), `:138-170` (protocol reference), `:173-189` (`consumed_hypothesis_ids`), `:192-226` (`check_windows_before`), `:229-247` (`windows_overlap`) | Deny by default |
| Protocol pointer | `run_phase1_research.py:10415` (`_load_holdout_range`), `:10444-10471` | The generated protocol carries the reference, not dates |
| Backtest tool | `tools/run_protocol.py:2022-2200` (policy, holdout window, refusals), `:2435-2438` (two switches), `:2461-2470` (pre-flight), `:2585-2641` (holdout mode: `holdout_result.json`, `holdout_log.jsonl`) | Refusals before any fetch |
| Data feed | `trading-bot/data/data_manager.py:67-100` (bounds from the policy), `:102-207` (`SealedDataError`, the two guards), `:1291`, `:1328-1329`, `:1333-1340` | Request guard, returned-rows guard, refusal propagated |
| Run viewer | `tools/run_viewer/sanitize.py:1-41` (doc), `:52-58`, `:98-113`, `:219` (`sanitize_text`), `:249` (`sanitize`) | Masks sealed dates in all output |
| Commit check | `tools/holdout_date_gate.sh:1-225`; `config/holdout_gate_exemptions.txt` (179 entries, 5 marked PROSE); `tools/hooks/pre-commit:1-97` (secret scan, then the gate); `tools/setup_hooks.sh`; `.github/workflows/tests.yml:48-60` | Self-test, index scan, provenance keys, registry |
| Ignore rule | `.gitignore:41` | `**/holdout_sealed/` |
| Registry entry | `run_phase1_research.py:251-255` | `holdout_evaluation`, tool stage, no AI call |
| Profit-bars stop | `run_phase1_research.py:15570-15623`, called `:20585` | The pause that opens the way |
| Unlock design and codes | `run_phase1_research.py:7013-7084` | Decision schema, pause flags, 12 refusal codes |
| Decision checks | `run_phase1_research.py:7106` (read), `:7414` (validate), `:7491` (refuse) | `holdout_decision.yaml` |
| Unlock route | `run_phase1_research.py:7515-7557`, called `:20590` | spend, continue, refused |
| Unlocked evaluation | `run_phase1_research.py:7628-7676`; ending `:7572-7625` | Re-check, pause, record first, ending |
| Spend record | `run_phase1_research.py:6976` (intent), `:6951` (marker), `:6694` (policy writer), `:6992` (spent without unlock) | `holdout_consume_record`, `holdout_consumed_by` |
| Stage branch | `run_phase1_research.py:19856-19910` | Unlocked, spent by hand, or refused |
| Tradable hold | `run_phase1_research.py:15626` | `_research_only_hold` |
| Older gate | `run_phase1_research.py:15699` (`_route_holdout_evaluation`), route `:20626` | Not reached under the current flags |
| Pause labels | `run_campaign.py:1523-1535`, `:1764-1769`, `:1916-1921` | Holdout pauses classified |
| Operator one-pager | `docs/OPERATOR_UNLOCK_HOLDOUT.md:1-92` | Tickets first (`:13-21`), decide, checks, backtest, result, never |

Remarks: send them as "stop 27: <remark>"; mark "direct" for an answer.

## Operator remarks (verbatim, with the guide's direct answers)

## Inspector notes

(Hard rule kept: no sealed date is written here; the policy was read by key name only (`grep` of top-level keys); the sealed store was not listed or opened. No `SR/runs/run_102/`.)

### (1) Design and mechanism

1. The seal is the pipeline's strongest invariant and each layer enforces it on its own: one strict deny-by-default reader of the range (`holdout_policy.py:1-29`, `:36-52`; a malformed policy refuses, never "no holdout"); generated protocols carry a reference, not dates (`RP:10444-10471`, `holdout_policy.py:43-48`); the backtest tool refuses before any fetch (`run_protocol.py:2026-2060`, `_preflight_training_windows :2140-2153`, `:2461-2470`); the data feed refuses a request reaching the seal and any returned sealed row, reads both bounds, and refuses everything when the policy is unreadable (`data_manager.py:67-110`, stop 14 note 1.1); the viewer masks every date shape and fails closed (`sanitize.py:1-58`); git ignores the store (`.gitignore:41`); CI runs the commit gate on every push, deny-by-default with a count-pinned exemption registry (`tests.yml:58-60`, `holdout_date_gate.sh:1-40`). Belt, braces and a third belt, each tested.
2. The unlock is a one-way door built with care: twelve refusal codes (`RP:7049-7063`), record-first on a spend (intent, then the consumed marker, then the ending; `_unlocked_holdout_evaluation :7628-7676`), the result bound to the unlock by variant, trial and decision hash (`_spent_holdout_ending :7572-7625`), a relabelled result detected by its hash and recorded, a result with no unlock recorded as spent and never promoted (`_record_spent_holdout :6992`, `:19887-19903`). Looking is spending, and the code says so at every step.
3. The exam has never been sat and, by the operator's own one-pager, is not ready to be: `holdout_consumed_by` is empty (speech), and `OPERATOR_UNLOCK_HOLDOUT.md:13-21` lists three tickets to fix before the first real spend (no second spend after a crash; the spent list moved out of the hand-edited policy; the bars-file hash sensitive to line endings). So the campaign's final step exists in code, is guarded twelve ways, and waits on engineering. For the goal: a strategy that passes the bars (none has, stop 20) would then wait for a person and three fixes.
4. The grid plays no part at the door, by design and in writing: "a refuted or inconclusive idea whose variant passed the bars may still be spent on" (`RP:7017-7019`; stop 20 note 1.4). The seal protects the data; it does not ask whether the belief that produced the strategy held. The operator is the only check that the money and the claim agree before a spend.
5. The exam is one draw. The holdout is single-use per hypothesis and a fail is terminal (`holdout_failure_is_terminal`, policy key; one-pager `:9-10`). The sealed range is one stretch of market, so a strategy meets one regime once; with the folds confounding regime and months (stop 06 note 1.3), a true edge that happens to be out of favour in that stretch dies, and nothing in the record says the exam was one regime. The operator's stop-06 wish to "decrease the importance of the holdout" meets this fact: the holdout decides a lot, from one look.
6. `research_only` has exactly one effect and it is here: `_research_only_hold` (`:15626-15648`) at the spend (stop 04 note 1.3). A brief on a venue the operator cannot trade is researched to its end, graded, recorded, and held at the door.
7. Two result files, two shapes, one hand between them: the backtest tool's holdout mode writes `holdout_result.json` and appends `holdout_log.jsonl` (`run_protocol.py:2617-2641`), while the orchestrator waits for `artifacts/holdout_result.yaml` with `status`, `variant_id`, `trial_id` and `decision_sha256` written by the operator (`RP:7653-7658`, `HOLDOUT_RESULT_BINDING_KEYS :7035`). The operator transcribes the one exam's result by hand from JSON to YAML; the binding checks catch a wrong id, not a wrong `status`. The one moment that matters most has a manual copy in it.
8. The repository's hard rule ("never write the dates out") is broken by two of its own enforcers in their comments: the gate script's header (`holdout_date_gate.sh:5`) and the data feed's docstring (`data_manager.py:75`) spell the range in clear, presumably exempted through the registry. Not a data leak; a rule its guards do not keep, and a reader of either file learns the dates the rule says not to write.
9. In this checkout the local hook is not wired (`core.hooksPath` unset), so the commit gate runs only in CI; the speech says so. The data feed's guard does not depend on any caller switch (stop 14 note 1.1), so `backtester.py:229` passing none is immaterial.

### (2) Legacy or simplifiable (leads)

1. The older gate `_route_holdout_evaluation` (`RP:15699`), its `promotion_audit.yaml` path with the hard-coded 0.95 (bars file header `:64-70`, stop 20 lead 2.1), the legacy pause rows (`provisional_promote_*`, `RC:1612-1620` relative) and `_mark_holdout_consumed`'s legacy caller (`:6694-6700`). Unreached under the retired route.
2. Pre-PR-9 protocols with literal holdout blocks, still accepted by every reader (`holdout_policy.py:47-50`, `run_protocol.py:2047-2060`): once `protocols/` carries only references, the dual read goes.
3. `holdout_result.json` versus `holdout_result.yaml` (note 7): one writer producing the file the orchestrator reads would remove the hand copy.
4. `config/holdout_gate_exemptions.txt` (462 non-blank lines; the gate's own header says most hits are provenance stamps): a registry that grows with every timestamped artifact; the `AUTHORSHIP_KEYS` list is the right mechanism, the per-file counts are the weight.
5. The `--holdout`/`--i-understand`/`--hypothesis-id` triple on the research backtest tool (`run_protocol.py:2435-2438`; stop 18 lead 2.4): a separate entry point for the exam would shorten `main()`.

### (3) Disagreements between the speech and the element

1. Step 5's list of checks: matches `_validate_holdout_decision` (stop 20) with the additions noted there (invalidated trial, another pending spend, the Sharpe basis); "the brief declares the strategy tradable" is checked in the unlocked evaluation (`:7651`), not in the decision check. Detail.
2. Step 6, "The operator runs the holdout backtest by hand ... with two deliberate switches and the idea's name": `:2435-2438`, `:2461-2470`; verified. Not stated: the tool writes JSON and the orchestrator reads YAML (note 7).
3. Step 7, "Code records the spend first": `:7668-7676`; verified. Step 8: `:19887-19909`; verified.
4. Section 6, "the setting that points git at the tracked hook is unset": verified. "My grep found no engine caller that passes the data feed's switch": `backtester.py:229`; verified and immaterial (note 9). "The unlock one-pager lists three tickets": `:13-21`; verified.
5. Reading map, "`config/holdout_gate_exemptions.txt` (179 entries, 5 marked PROSE)": the file has 462 non-blank lines and 21 lines mentioning PROSE (header comments included); the entry count was not separated from the header here. Figures differ by counting method.
6. Reading map verified: policy keys at `:17`, `:21`, `:23`, `:33`, `:48`, `:210`, `:288`, `:388`, `:535`, `:542` (top-level grep; `:41`, `:177-184`, `:214`, `:413-414` are nested keys, not read); `holdout_policy.py:1-29`, `:39-48`, `:56-136` (head), `:138-247` (by function); `RP:10415`, `:10444-10471`, `:251-255`, `:15570-15623` (stop 20), `:7013-7084`, `:7106`, `:7414`, `:7491`, `:7515-7557`, `:7628-7676`, `:7572-7625`, `:6976`, `:6951`, `:6694`, `:6992`, `:19856-19910`, `:15626`; `run_protocol.py:2022-2060`, `:2130-2160`, `:2435-2438`, `:2461-2470`, `:2585-2642`; `data_manager.py:67-110`, `:1291`, `:1328-1340` (stop 14); `backtester.py:229`; `sanitize.py:1-58`; `holdout_date_gate.sh:1-40`; `tools/hooks/pre-commit:1-30`; `tests.yml:48-63`; `.gitignore:41`; `OPERATOR_UNLOCK_HOLDOUT.md:1-30`; `RC:1523-1535`, `:1764-1769`, `:1916-1921`. Not opened: `RP:15699`, `:7281` (stop 20), `sanitize.py:98-113`, `:219`, `:249`, `tools/setup_hooks.sh`, the one-pager past `:30`.
