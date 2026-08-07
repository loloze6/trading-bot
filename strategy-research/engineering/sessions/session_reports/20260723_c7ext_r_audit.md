# Bounded re-audit of 2c8b8d1 (C7-EXT-R remediation) + archive rule-shape census

**Auditor:** Claude Opus 4.8 — independent of the session that wrote 2c8b8d1 (and
independent of the session that wrote a83084b, the round this remediates).
**Date:** 2026-07-23
**Mode:** READ-ONLY, bounded. Per the dispatch, G1–G5, G7, the five repointed tests,
and the run_057 sparsity recomputation are **not** re-verified here — a83084b already
confirmed them and nothing in this commit touches that ground. Only `git checkout --
trading-bot/results/trades.json` (known D4, fired twice during this session — once
after the test suite, once implicitly available if needed again) was written to the
tracked tree. All bypass attempts were run against temporary directories
(`tempfile.TemporaryDirectory()`) with `ROOT`/`QUEUE_PATH` monkeypatched, never against
`strategy-research/`'s real files — confirmed by `git status --porcelain` before and
after every attack.

---

## 0. Precondition manifest — PASS

```
$ git log --oneline -1
2c8b8d1 C7-EXT-R: remediate the independent audit (D-4/D-5/D-6/D-3/D-1)
$ git status --porcelain
(empty)
```

---

## 1. G6 attack — **BYPASSED. STOP condition fires.**

Attacked empirically against the live, imported `verdict_criteria_evaluator` module
(`tools/verdict_criteria_evaluator.py`), not by reading the code and guessing. Eight
attack shapes tried; **five succeed**, two of the five in exactly the categories the
dispatch named as the most likely holes.

### Confirmed bypasses (exact inputs, exact outcome)

**Attack 1 — path traversal, borrowing a real run's real FAIL as fabricated
provenance.** The single most consequential bypass found.

```python
entry = {
    "id": "FAKE_HYPOTHESIS_NEVER_RAN",
    "outcome": "kill_mechanism_falsified",
    "evidence_runs": ["run_999_FAKE"],            # a run that does not exist
    "pass_rule_evaluation_ref":
        "runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml",
}
vce.validate_verdict_provenance(entry, root=ROOT)   # -> ACCEPTED, no exception
```

`resolve_evaluation_ref`'s "belongs to this entry's own runs" check
(`tools/verdict_criteria_evaluator.py:546-552`) is a **substring match on the
unresolved path string** — `f"/runs/{rid}/" in norm`. It runs *before* the OS
collapses `..`. The literal text `runs/run_999_FAKE/../run_059/artifacts/...`
contains the substring `/runs/run_999_FAKE/`, so the membership check passes — but
`path.exists()` and `open(path)` are resolved by the OS, which *does* collapse `..`,
and actually reads `run_059`'s real, genuine `FAIL` evaluation. Verified the resolved
path directly:

```
literal ref            = runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml
base/ref (unresolved)  = .../strategy-research/runs/run_999_FAKE/../run_059/artifacts/pass_rule_evaluation.yaml
.resolve()              = .../strategy-research/runs/run_059/artifacts/pass_rule_evaluation.yaml
exists()                = True
```

A completely fabricated hypothesis, citing a run that was never executed, is accepted
as gated by borrowing another hypothesis's real result. This is precisely the "an
entry may not borrow another run's evaluation as its provenance" property the D-4 fix
claims to enforce (`resolve_evaluation_ref`'s own docstring, point 2) — and it does not
hold under a relative-path traversal. Every legitimate ref currently on disk is a
clean relative path with no `..`, so no live entry exploits this today — but the check
exists specifically to stop a hand-authored entry from doing exactly this, and a
hand-authored entry can write a traversal string as easily as a clean one.

**Attacks 2–3 — verdict field one level of nesting away, or inside a list.**

```python
{"id": "FAKE_NESTED", "details": {"hypothesis_verdict": "kill", "verdict_c7": "kill"}}
{"id": "FAKE_LIST", "decisions": [{"verdict_c7": "kill", "note": "buried in a list"}]}
```

Both **ACCEPTED**. `strict_fields` (`verdict_criteria_evaluator.py:607-613`) is built
from `entry.items()` — one dict-comprehension pass over the entry's own top-level keys.
It does not recurse into dict or list *values*. A verdict field one level deeper than
the top, or inside a list element, is invisible to it, and — critically — there is no
top-level `outcome` key in either shape to catch it on the other check. This is exactly
the "nested one level deeper" / "inside a list" shape the dispatch asked about,
confirmed live.

**Attack 4 — plain field names that don't contain the string "verdict".**

```python
for fname in ("status", "disposition", "resolution", "result", "decision", "conclusion"):
    {"id": f"FAKE_{fname.upper()}", fname: "kill"}
```

**All six ACCEPTED.** The shape-matcher (`_VERDICT_NAME_MARKER = "verdict"`) only
catches keys whose name literally contains that substring. `status: kill`,
`disposition: kill`, `resolution: kill`, `result: kill`, `decision: kill`,
`conclusion: kill` all sail through with no exception, no `outcome` key needed. This is
the exact concern the dispatch named ("a key like status/disposition/resolution") and
it reproduces on the live code, not hypothetically — the D-4 fix replaced a
three-name denylist with a substring-of-one-word marker, which is a **broader** but
still finite and guessable set, not the general fix the commit message's "New name,
same gate" framing implies.

**Attack 5 — non-English verdict field names.**

```python
for fname in ("veredicto_c7", "urteil", "verdikt", "verdicto", "final_veredicto"):
    {"id": f"FAKE_{fname}", fname: "kill"}
```

Four of five **ACCEPTED** (`veredicto_c7`, `urteil`, `verdikt`, `final_veredicto`).
Only `verdicto` was correctly rejected — and only by coincidence: the English word
"verdict" (v-e-r-d-i-c-t) is a literal prefix substring of the Spanish "verdicto",
so the ASCII/English-only marker matches it by accident, not by design. German
`urteil`, Spanish `veredicto`, and the constructed `verdikt`/`final_veredicto` all
evade it cleanly. Confirms the dispatch's "non-English" concern exactly.

### Correctly-held negative cases (not bypasses — verifying the fix's real claims)

**Attack 6** — ref to a real file, correctly scoped to the right run, but recording no
binding result (`runs/run_059/artifacts/prescreen_result.yaml`, which has no top-level
`result` key at all):

```
REJECTED -- ...has result='', which is not a resolved verdict (expected one of
['FAIL', 'PASS']) -- the evaluator declined to decide, so there is no verdict to cite.
```

Correct. This specific negative case — the one the dispatch explicitly asked to
verify — holds.

**Attack 7** — absolute path entirely outside `runs/`, pointing at a hand-fabricated
`result: PASS` file in the OS temp directory:

```
REJECTED -- ...does not lie under any of this entry's own runs ['run_059'] -- an entry
may not borrow another run's evaluation as its provenance.
```

Correct — the *non-traversal* absolute-path escape is caught. Only the traversal
variant (Attack 1) gets through; a plain absolute path outside the run tree does not.

**Attack 8 (reasoned, not executed)** — a hand-authored `result: PASS` file dropped
directly inside a *real* run's own `artifacts/` directory, with no genuine evaluator
invocation behind it, was not empirically tested (would require writing into
`strategy-research/runs/`, outside this audit's read-only remit). Structurally: nothing
in `resolve_evaluation_ref` ties a `pass_rule_evaluation.yaml` file to having actually
been *produced* by the evaluator — only to existing, being path-scoped to the run, and
parsing with `result` in `{PASS, FAIL}`. This is a different-in-kind limitation (any
filesystem-provenance check short of a cryptographic/log-based tie has it) and is noted
as a carry-forward, not claimed as a confirmed bypass.

### Queue-writer coverage — this specific D-4 claim holds

Checked the narrower, explicit question: does `_save_queue` validate on **every** path
into it, including partial/append writes? `grep` confirms `_save_queue` is the queue's
**only** writer (9 call sites, all in `run_campaign.py`; no other file opens
`campaign_queue.yaml` for writing). Read the function directly
(`run_campaign.py:101-134`): it iterates `queue.get("queue") or []` — the **entire**
list — and calls `validate_verdict_provenance` on every dict entry, unconditionally,
before the temp-file-then-`os.replace` write. Verified empirically, not just read:

```python
queue = {"queue": [
    {"id": "legit_entry", "status": "ready"},
    {"id": "BAD_HAND_EDIT", "outcome": "kill_mechanism_falsified",
     "evidence_runs": ["run_999_never_ran"]},
]}
rc._save_queue(queue)
# -> UngatedVerdictError raised; file NOT written (verified: QUEUE_PATH.exists() == False)
```

A bad entry mixed into an otherwise-legitimate write is rejected **and the file is not
written at all** — no partial write occurs, confirming the atomic temp-then-replace
never reaches `os.replace`. This specific claim in D-4 is correct.

### Net on G6

**One STOP condition (G6 bypassable) fires, on five independent routes.** The commit's
own framing — replacing a 3-name denylist with name-shape matching closes the class,
not just the instance — does not hold: name-shape matching only closes names containing
the literal ASCII substring "verdict", which `status`/`disposition`/`resolution` and
any non-English term never will. And the newly-added ref-resolution defense (which
correctly closes the *unresolved-ref* and *wrong-run* bypasses from the prior round)
has its own new hole: the run-ownership check operates on an unresolved path string,
so a `..`-bearing ref defeats it while `path.exists()`/`open()` follow the traversal to
a real file. The queue-writer coverage claim (item D) is the one part of D-4 that fully
holds under direct testing.

---

## 2. Independent verdict count — **1. Confirmed by a third, distinct route.**

Two routes already exist: the lint tool (`lint_verdict_provenance.py` → calls
`vce.honest_verdict_count`) and the prior round's artifact-glob
(`ls runs/*/artifacts/pass_rule_evaluation.yaml`). Per the dispatch, I used neither —
instead, raw `yaml.safe_load` on both stores directly, with **my own** judgment of
which `outcome` strings are verdict-bearing, no `vce` import at all:

```
KB findings: 19 entries, Queue: 4 entries.
```

Scanning every entry's `outcome` / `pass_rule_evaluation_ref` / `verdict_status` by
eye: 15 of the 19 KB outcomes are non-terminal/engineering states
(`invalidated_artifact`, `blocked_feed_unavailable`, `inconclusive`,
`unusable_for_this_symbol_timeframe`) or verdict-shaped claims that are **all**
paired with an explicit `verdict_status: ungated` (or `stage_discretion`) self-declaration
and **no** ref — `no_edge_observed` ×6, `era_conditional_instability`,
`stage_discretion_rejection_no_gated_verdict` (H-041-C-v2),
`ungated_er_gate_variant_too_sparse_to_evaluate`,
`measurement_only_no_admissible_verdict` (xs_momentum). None of these carries a ref.

**Exactly one entry** carries both a verdict-bearing outcome and a
`pass_rule_evaluation_ref`: `FUNDING_MR_DAILY_RETEST`, `outcome: completed_rejected`,
`verdict_status: gated`, `ref: runs/run_059/artifacts/pass_rule_evaluation.yaml` —
identically in both the KB and the queue. Manually opened the cited file (not via
`resolve_evaluation_ref`): it exists, is 803 bytes, `result: FAIL` at the top, and the
entry's own `evidence_runs: ['run_059']` genuinely names the run the file lives under.

**Count = 1. Matches the claim. Not a STOP condition.**

---

## 3. Archive rule-shape census — all 59 runs

Independently walked every `runs/*/artifacts/pre_registration.yaml`, re-implementing
`_find_pass_rule`'s top-level-then-`machine_constraints` lookup myself (not importing
the function), and cross-checked `pass_rule_evaluation.yaml` existence per run.

| Class | Count | Runs |
|---|---:|---|
| **(a) structured and evaluated** | 1 | run_059 |
| **(b) structured but never evaluated** | 1 | run_058 |
| **(c) prose / legacy_not_evaluable — human-adjudicated** | 1 | run_057 |
| **(d) no rule at all** — of which: | 56 | |
| — has `pre_registration.yaml`, no `pass_rule` field anywhere | 6 | run_043, 044, 047, 048, 050, 053 |
| — no `pre_registration.yaml` file at all (pre-K2 legacy runs) | 50 | all remaining |
| **Total** | **59** | |

Spot-verified rather than trusted:
- **run_058** genuinely has a fully-conformant top-level structured `pass_rule`: 3 real
  criteria (`median_sharpe`, `max_abs_drawdown_pct`, `zero_trade_slot_pct`, each with
  per-symbol thresholds) and 4 real outcome branches — confirmed by direct read, not
  the file's field names alone. No `pass_rule_evaluation.yaml` exists for it (matches
  a83084b's finding that it was rejected at a validation stage before the pass_rule
  ever ran).
- **run_057**'s nested `machine_constraints.pass_rule` is genuinely `type(str)` — real
  prose, not a mis-shaped dict — confirming D-6's "honest limit" claim precisely:
  finding the rule does not make it evaluable.
- The 6 "no rule at all but has a file" runs were checked at both locations
  (`pre_registration.get("pass_rule")` and
  `pre_registration.get("machine_constraints", {}).get("pass_rule")`) — both `None`
  for all six, independently confirming a83084b's "9 runs have pre_registration.yaml"
  figure (6 + run_057 + run_058 + run_059 = 9) from a completely different angle (a
  full filesystem walk of all 59, not the prior round's targeted check).

**The honest denominator.** Only run_059 passed through the C7 structured pass-rule
evaluator to a binding result — **1/59 = 1.7%** of the campaign's runs were
mechanically gated. Layered further, since not every one of the other 58 reached even
a human/LLM-adjudicated terminal verdict: cross-referencing all 59 run directories
against every KB-finding/queue-entry `evidence_runs`/`run_ids`/`run_id` reference finds
**22 runs** named by at least one terminal-outcome entry (some findings cite multiple
runs as supporting evidence for one hypothesis) and **37 runs** named by **none** —
intermediate/superseded steps within a lineage, never independently adjudicated at all.

So, precisely: **58/59 (98.3%) of the campaign's runs never had their fate decided by
the C7 mechanical gate.** Of those 58, a minority — around 21, run_058's own inclusive
count depending on exactly how multi-run findings are attributed — reached a
recorded outcome via prescreen IC thresholds or LLM/stage-discretion judgment (that is
the "human judgment" component proper); the remainder have no terminal disposition
recorded against them at all. Either way, **the campaign's "zero confirmed edges"
claim rests on exactly one mechanically-gated result out of 59 runs** — every other
"no edge" finding in the archive is a human/LLM call, a prescreen-threshold kill, or an
intermediate step with no independent verdict, not a C7-gated one.

---

## 4. Nine unratified protocol files — **confirmed to fail loudly, on every reachable branch.**

Independent scan of `protocols/*.json` (not the pinning test, a fresh
`promotion_is_generic()` sweep over every file in the directory) finds exactly the same
nine: `baseline_v1.json`, `baseline_v2.json`, `escalation_{avaxusdt,dotusdt,solusdt}_4h.json`,
`escalation_tf_15m.json`, `run_{048,050,053}_generated.json`. All nine carry
`promotion_provenance.status: generic_unratified` and `ratified_by: None`.

Beyond confirming the flag is set (which the dispatch explicitly said is not enough),
**empirically exercised `_resolve_protocol_path` end-to-end** — not just
`_assert_promotion_ratified` in isolation — for every reachable branch, in a real
temp `ROOT` with monkeypatched `campaign_state`/`run_context.yaml`:

- `forced_diagnostic` (names the protocol explicitly): **9/9 raised** `UngatedProtocolError`.
- `protocol_ref_pinned` (names the protocol explicitly): **9/9 raised.**
- B10 `last_escalation` fallback, correctly claimed by the run: **9/9 raised.**
- `replication_diagnostic` (hardcoded to always select `baseline_v1.json` — only
  meaningful for that one file): **raised.**

28/28 branch×file combinations tested, all correctly refused. No path into
`_resolve_protocol_path` hands out any of the nine files without raising. This claim
holds fully.

(Not a bypass of the nine files, and out of the dispatch's scope, but worth flagging
for the record since it surfaced during this check: `promotion_is_generic` is exact
`dict ==` equality against the four abolished numbers. A protocol carrying the same
four thresholds plus one additional harmless key, or the same numbers as floats where
the default uses ints spelled differently in a way that still compares equal, would
not be caught by *this* mechanism — Python's `==` already treats `0 == 0.0`, so type
drift doesn't break it, but an extra key would. This is the same brittle-exact-match
shape already logged as D-7 against G1's product allowlist, one layer over. Not tested
against a live file, since none of the nine actually has this shape — noted for
completeness only.)

---

## 5. Test suite

Ran `strategy-research/tests/` directly (the suite the commit's own "Tests 369 -> 389"
claim refers to — `trading-bot/tests/` is a separate, unrelated suite and was not what
2c8b8d1 touched):

```
389 passed, 3 warnings in 48.38s
```

Matches the claimed count exactly. `trading-bot/results/trades.json` dirtied by this
run (known D4 pattern); reverted with the pre-authorized `git checkout --`. Final tree
state confirmed clean before writing this report.

---

## 6. Summary

**Overall: DO NOT RATIFY.**

The single STOP condition that governs this round fires: **a G6 bypass succeeds** —
five of them, in fact, on live code, not hypothetically. The count (§2) and the
nine-protocol-file guard (§4) both check out cleanly and independently; those parts of
2c8b8d1's remediation are real and should be kept.

What 2c8b8d1 gets right and should be kept:
- **D-5** (verdict count correction to 1, `honest_verdict_count` replacing the
  `completed_rejected` string-match) — independently reproduced by a third method.
- **D-6** (`_find_pass_rule` checking both locations, run_057 re-classified honestly as
  `legacy_not_evaluable` rather than silently unrun) — the nested prose shape was
  verified by direct type-check, not assumed.
- **D-3** (`_assert_promotion_ratified` at every `_resolve_protocol_path` branch) — 28/28
  branch×file combinations empirically confirmed refusing.
- **D-4's queue-writer half** — `_save_queue` validating the whole list, atomically, on
  every call, with no partial write on rejection — empirically confirmed, not just read.

What does not hold, and is why this round cannot ratify:
- **D-4's shape-matcher half.** Nested fields, list-embedded fields, and any top-level
  key not containing the literal English substring "verdict" (`status`, `disposition`,
  `resolution`, `result`, `decision`, `conclusion`, and non-English equivalents) all
  bypass `strict_fields` cleanly, with no `outcome` fallback to catch them.
- **D-4's ref-resolution half has a new hole of its own.** The "belongs to this entry's
  own run" check is a substring match on an *unresolved* path string, defeated by a
  `..`-bearing relative ref that resolves (via the OS, at `open()` time) to a
  completely different, real run's real result. This lets a fabricated entry citing a
  run that never executed borrow a genuine PASS/FAIL from an unrelated hypothesis.

**Carry-forwards, in priority order:**
1. **(blocking, re-opens D-4)** Fix `resolve_evaluation_ref`'s run-membership check to
   operate on the *resolved* path (`path.resolve()`, or reject any ref containing `..`
   outright) before the substring match, not after.
2. **(blocking, re-opens D-4)** Replace the substring-of-"verdict" name marker with
   something that does not depend on the field author choosing an English name
   containing that literal word — e.g., a recursive walk of the entry's full value tree
   (catching nested/listed fields as a side effect), or an explicit allow-list of the
   handful of fields a corrected record is permitted to carry (`outcome`,
   `outcome_reason`, `verdict_status`, `verdict_status_basis`, `verdict_void_reason`,
   `power_verdict`, the provenance/id/run fields) with anything else on a KB/queue
   entry treated as suspect by default — inverting today's opt-in denylist-of-shapes
   into an opt-in allowlist-of-fields.
3. **(non-blocking, new observation)** No file-existence check can distinguish a
   genuine evaluator-produced `pass_rule_evaluation.yaml` from a hand-authored one
   dropped into a real run's `artifacts/`. Not tested (would require a write outside
   this audit's remit); worth a decision on whether this is in-scope for a future
   round or accepted as a standing limitation of filesystem-only provenance.
4. **(carried from a83084b, restated precisely by this round's census)** 58/59 (98.3%)
   of the campaign's runs never passed through the C7 mechanical gate. The campaign's
   "zero confirmed edges" framing should state this denominator explicitly wherever it
   is asserted, rather than implying uniform gate coverage across the archive.
5. **(minor, informational)** `promotion_is_generic`'s exact-dict-equality check is the
   same brittle-match shape as the already-logged D-7 (G1's allowlist); not exploited
   by any of the nine files today, but the same class of fragility.
