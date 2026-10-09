# Lessons (appended after user corrections)

## 2026-09-18 — Don't propose a control that already exists as a step
Pattern: proposed a "requires new data, yes/no" flag for idea proposals; the operator pointed out E-054's
data-availability gate already does this, per variant, pre-backtest.
Rule: before proposing any new check/flag/score, grep the stage graph (STAGE_CONFIGS, USER_GUIDE §2.1)
and the existing gates; if a step already owns the concern, route to it instead of adding a sibling.

## 2026-09-18 — Component-gap detection belongs where words become config
Pattern: put the "requires new component" outlet at hypothesis design (Step 1); the operator corrected
that feasibility is checked at backtest_specification, where the design is turned into a bot config.
Rule: place a check at the earliest step that has the concrete information the check needs, not the
earliest step conceptually related to it.

## 2026-09-17 — Write for a new joiner
Pattern: first review reply was dense and jargon-heavy; the operator asked for the same content in plain
words.
Rule: default to plain language, short sentences, one idea per sentence; keep file paths and line refs
in the record file, not in the prose the operator reads.

## 2026-09-23 — Built two slices on the legacy verdict vocabulary the target design had retired
- **Pattern:** E-046a 5b-ii-A/B1 made the 5 readers' proposal scores decide refine/kill and fed a per-family circuit breaker. The agreed target (roadmap v26/v27 cards G/I, delivery_plan_v26.md slices 2, 6b, 6c) says: idea status = the grid (validated/refuted/inconclusive), reader scores only RANK the next candidate (decide_next, 6b), refine/pivot/escalate/kill + the circuit breaker are retired (6c), repeats are caught by an exact-match check (slice 8). I framed the 5b S1 question as "who synthesizes the readers into a routing decision", the operator answered the question as framed, and two builds followed. The operator caught it from the downstream questions ("why do we still have escalation?").
- **Rule:** before designing any slice that touches verdicts, routing or "what runs next", re-read the target cards and the delivery plan's LATER slices that retire things, and check the design does not re-create what a later slice deletes. When an S1 finding offers a choice, first ask "does the target design already answer this?" — never pose a question whose framing presupposes retired machinery.

## 2026-10-08 — Open points must be concrete before asking for a decision
- **Pattern:** the open points of #356/#357 were written as abstract rules ("the several-folds rule", "empty-vehicle re-runs"); the operator replied "I do not get the open points, please explain concretely, concisely, simply".
- **Rule:** for each decision, one line each: what happens today with a small example, the options, my recommendation. Gloss every id. Ask only after that.

## 2026-10-08 — Run every test file that imports a touched module before pushing
- **Pattern:** #357's first CI run failed on a guard test (test_e068_5_readers_v3's no-verdict-words check) in a file I had not run; my own docstring tripped it.
- **Rule:** before a push, run the full strategy-research suite (about 5 minutes with -n 4), or at least every test file that imports a changed module (`grep -l`).

## 2026-10-08 — Exercise the real SDK constructor, not only stubs
- **Pattern:** PR-5's wiring was written against claude-agent-sdk 0.2.82, but the installed `mcp` 2.x (allowed by the SDK's open `mcp>=1.23`) made `create_sdk_mcp_server` raise on the first real tool. Only a test that built the server with the real tools caught it.
- **Rule:** when wiring a third-party constructor, at least one test must call it for real with real arguments; pin a transitive dependency when its new major breaks the API the code uses.

## 2026-10-09 — A claim made to justify an option must be checked in the code first
- **Pattern:** asking the operator to choose how to fix the analyst's floor refusal, I argued against "copy `min_events: 1`" because "the floor grades the fold-B confirmation, so a 1-event floor makes it nearly free". I had not opened `tools/fold_confirm.py`; it never reads the floor. The independent review caught it after the operator had chosen.
- **Rule:** every "this would cause X downstream" in an option's pros/cons is grepped and read before it is written (name the file:line in the question). When one turns out false after a decision, say so plainly and re-ask, even if the choice probably stands.

## 2026-10-09 — In a PowerShell chain, a failed read does not stop the publishing step
- **Pattern:** `$b = (Get-Content $p ...).TrimEnd() + ...; WriteAllText($p, $b); gh pr edit 361 --body-file $p` ran on after `Get-Content` failed (the scratch file was gone) and blanked PR #361's description. Restored from the text in context.
- **Rule:** any step that publishes (gh pr edit/create, push) is guarded: `-ErrorAction Stop` on the reads before it, and a size check (`if ((Get-Item $p).Length -gt N) { gh ... }`) on the file it sends; verify the published result afterwards.

## 2026-10-09 — Tests that stub the default value hide identity bugs
- **Pattern:** PR-5's end-to-end stub used `floor: {min_events: 1}`, the only value the tool could produce, and the tests with another floor mocked the claim's hash, so "a claim with a real floor is always refused" reached the paid smoke session.
- **Rule:** an end-to-end test of a model-written block uses a non-default value for every field the model may choose, through the real hashing/checking code, never a mocked hash.

## 2026-10-09 -- The same rule applies to a reason for NOT changing something
- **Pattern:** the same day as the lesson above, I justified leaving `CLAIM_TESTS_TRADE.md` unchanged with "other stages' prompts include it, so editing it breaks their flag-off byte identity". Only the analyst's prompt reads it (`analyst_session.build_prompt`, pinned by `tests/test_e075_pr3_trade_tests.py`). Review round 2 of #367 caught it; the conflicting line was then fixed in the same PR.
- **Rule:** "X reads/uses this file" is a downstream claim like any other: grep the loaders (and the test that pins them) before writing it, whether it argues for a change or against one.

## 2026-10-09 -- A chained edit-then-commit commits the half that worked
- **Pattern:** one PowerShell command ran a Python edit of two files, then `git add` + `git commit`. The Python step stopped on its own assertion after editing nothing in DECISION_LOG, but the commit still ran with the other file and a message saying "D-095 updated". Amended before push.
- **Rule:** never chain an edit and a commit in one command; after an edit, read `git diff --numstat` and match it to the commit message before committing.

## 2026-10-09 -- PowerShell 5.1 traps for PR bodies and deletes
- **Pattern:** a PR body re-saved with `Set-Content -Encoding utf8` started with a BOM, visible at the top of PR #363 (fixed with `gh pr edit`). `Remove-Item -Recurse -Force $var` was blocked by the safety hook as a "system path" (nothing ran).
- **Rule:** write or rewrite PR bodies with the Write tool or Python (`newline='\n'`, no BOM) and check the first byte before publishing; give `Remove-Item` a literal path.

## 2026-10-09 -- A lane's reported counts are claims to measure
- **Pattern:** a build agent reported "205 tests before"; master had 198. The PR body would have carried the wrong baseline.
- **Rule:** before quoting a before/after test count in a PR body, run the file on master (or the base commit) myself.
