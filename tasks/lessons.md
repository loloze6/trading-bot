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

## 2026-10-10 -- A rule that needs a third exception is a design signal: step back to the objective
- **Pattern:** the analyst's prose-number rule got an exception per smoke (#368, #370, #371) and I proposed a further batch (signed values, event-study offsets, hour buckets). The operator asked for a step back: the rule raised 71 of 94 errors over smokes 2-6 while protecting the least load-bearing output; it became mask-and-list (D-096).
- **Rule:** before adding another exception to a check, tally what it refused in the live records and trace what its output feeds; if the protected output is not load-bearing, change the mechanism, not the whitelist.

## 2026-10-10 -- Compute a share before stating it
- **Pattern:** I told the operator a one-turn retry was "about 60%" of each lens's real cost and wrote it in the E-069 doc; computed from the tokens it was about 35%.
- **Rule:** a percentage, ratio or total goes into a message or a doc only after it is computed from the records in this session, with the inputs named.

## 2026-10-10 -- Attributions and names in docs are checked like code claims
- **Pattern:** the E-069 doc said the analyst cap was "$1.50 until D-097's PR, #371" (it was #371 alone; D-097 is #373), and D-098 named `claim_tests._check_spec` (it is `check_spec`). The fact-check and a grep caught them.
- **Rule:** every "changed in PR #N / decided in D-NNN / function X" in a doc is checked with `git log` / `gh pr view` / grep before the commit.

## 2026-10-10 -- Say what a test cannot distinguish, not that its result is "automatic"
- **Pattern:** I called "long-held trades lose more" near-automatic; the operator challenged it: it may mean the exit is too late. The accurate statement: the test cannot tell "exit too late" from "losers stay open longer", and the test that could does not exist yet (CUL-425).
- **Rule:** when refusing or criticising a claim, name the two explanations its test cannot separate and the test that would; keep a legitimate idea alive as a backlog item.

## 2026-10-10 -- A finding about one strategy must carry the strategy
- **Pattern:** the operator spotted that "long trades lose more" recorded without context would read as a market fact for every later run; the memory view showed only the source run id.
- **Rule:** any recorded finding whose truth depends on how a strategy enters or exits carries that strategy (code-written components, the idea id) wherever later stages read it.

## 2026-10-10 -- A template the model copies is code: test that it parses
- **Pattern:** the analyst skill's answer template (`statement: >  one sentence ...`) was invalid YAML; Haiku copied it twice in the pilot and was refused twice.
- **Rule:** every example block a model is told to copy (YAML/JSON templates in skills and prompts) is parsed by a test.

## 2026-10-10 -- Reviewer roles: Fable for direction, Sonnet for code
- **Pattern:** the operator stopped a Fable code review: Fable is reserved for strategic review of the direction; code reviews and fact-checks cost less with a Sonnet reviewer, one round, one PR where asked.
- **Rule:** PR reviews and doc fact-checks go to a Sonnet reviewer; the persistent Fable agent is used only for step-backs and next-step advice; every reviewer claim is still verified (the Fable advice "rank_ic with a complement baseline" was impossible: `claim_tests.check_spec` refuses any baseline for rank_ic).

## 2026-10-10 -- "The fold has data" was checked at listing dates only
- **Pattern:** I told the operator fold B had data for the pilot runs from the Layer-1 check (listing dates); the data gate then graded every BTC variant `refine` (Kraken's 2018-01 outage, runs of 5-40 missing bars) and run_076 paused.
- **Rule:** before a child is minted on a fold, scan the fold's blocks for the child's coins at the data gate's own rule (any missing run longer than the engine's ignore tier, 3 bars) and say which check was run.

## 2026-10-10 -- An id plan stated before reading every collision rule
- **Pattern:** I said setting the held entry to `superseded` would free its proposal id; decide-next refuses an id three ways (a queue entry's `proposal_ref` names it, the queue id exists, the brief file exists), whatever the status.
- **Rule:** before proposing how to reuse or free an id, read the candidate checks (`decide_next._candidate`) and the pool filter (`decide`'s `named` set) and list every rule that applies.

## 2026-10-10 -- Mechanisms described from memory, files scripted from a guess
- **Pattern:** I wrote "the engine flattens at a gap" (it has three tiers: ignore, block new entries, flatten at the warmup); I scripted against `confirmations.yaml`'s `fold_confirmations` (the list is `looks`); I planned the campaign steps on the main checkout without checking it held the analyst code (143 commits behind).
- **Rule:** read the code before describing a mechanism to the operator; open a file before scripting against its keys; check that the checkout that will run a plan contains the code the plan needs (`git merge-base --is-ancestor`).

## 2026-10-10 -- Cost share read from an unweighted per-trade ratio; a brief drafted against the wrong flag set
- **Pattern:** my first read of cost drag used the per-trade mean (`realized_edge_to_cost_ratio`), which gave run_079 a positive edge of 1.69x cost while its account lost money in every window: the larger positions lose. Separately, the lane-1 basket idea collides with the operator's live `variant_loop` flag (one coin per variant), found only by reading the variant code.
- **Rule:** measure cost drag at portfolio weight (net % of account per trade) and cross-check its sign against the account's result before reporting; before drafting a brief, read the operator's live flag set and check the brief's shape (coins per variant, components, sizing) against the code paths those flags select.

## 2026-10-11 -- A flag's effect stated from one call site
- **Pattern:** I told the operator "with the variant loop off, every variant runs the whole coin list" after reading the coin-context branch only (`run_phase1_research.py:2839`); protocol_execution's loop-off path backtests only the base config (`_single_column_untested_kw`, and the flag register says so). The operator then built a plan on it.
- **Rule:** before stating what a flag does, read its register entry and every branch on it in the stage that consumes the result (here protocol_execution), not just the first `if` that mentions it.

## 2026-10-11 -- A figure from a memory note written into a decision row
- **Pattern:** D-102's first draft carried "24 merged PRs (17 analyst checker) against 5 real runs" and "0 of 10 ideas validated" from my step-back memory note, unre-measured; the Sonnet fact-check could not source them, and a GitHub search for PRs merged 2026-10-08..2026-10-10 returns 41 (the note's window is not recorded).
- **Rule:** a number goes into a committed decision only with its source (a file, a command and its date); a memory-note figure is re-measured first or left out.

## 2026-10-11/12 -- A brief named a component without checking the hard rules and the stage's allowlist
- **Pattern:** the v1 lane-1 brief specified `SmaTrendLongOnlyComponent` (on/off, refused as a forecast source by D-051) and the `vol_target` op (not in the design guide the config-writing stage is limited to). Neither I nor the fact-check checked either; run_080 was rewritten by 1b and voided.
- **Rule:** before a brief is registered, check every component and op it names against the decision log's hard rules (D-051 and the like) and the authoring skill's allowlist (the guide's op table, the catalogue).

## 2026-10-11/12 -- A guideline routed around a prompt file without checking the stage accepts that route
- **Pattern:** "edit no SKILL or catalogue file, the brief names the op" kept prompts byte-identical, but the config-writing stage accepts only ops the guide lists, so the brief's op was unusable by that route.
- **Rule:** a guideline that routes around a prompt file must first check, in the stage's skill and code, that the stage accepts input by that route.

## 2026-10-11/12 -- A warm-up claim checked on the test windows only
- **Pattern:** the v2 briefs said every coin's warm-up fits the 2 x required_bars prefetch; XRP's two missing days sat inside four sma100/sma200 prefetch spans, so the launcher's readiness assert would have stopped them (found by the fact-check).
- **Rule:** before claiming warm-up is covered, replay the launcher's readiness probe on the cached rows of every coin x window x lookback prefetch span, not just the test windows.

## 2026-10-11/12 -- Pushed review fixes to a PR that was already merged
- **Pattern:** #385 was merged with its first commit while I pushed the XRP fix to its branch; I then told the operator it was "ready to merge". The fix needed a new PR (#386).
- **Rule:** run `gh pr view <n> --json state` before every push to a PR branch and before calling a PR ready.

## 2026-10-11/12 -- A gate that trusts the model's own report
- **Pattern:** the deviation gate (D-104) reads the deviations 1b declares; 1b rewrote the config silently (run_081) and the gate passed it (CUL-429).
- **Rule:** when a check guards a model's output, compare the output itself (here the forecast replay, D-106), not the model's account of it.

## 2026-10-11/12 -- Backslashes in a heredoc broke code twice more
- **Pattern:** a `\n` inside a Python-in-bash heredoc became a real newline in an f-string and in a test, and a replacement with backslashes failed its anchor; same family as the 2026-10-05 lesson.
- **Rule (reinforced):** any text with a backslash (code, regex, Windows paths) goes through the Write or Edit tool, never a heredoc.

## 2026-10-11/12 -- Disk at 0 bytes discovered by a failed command
- **Pattern:** a `sed | cut` failed with "No space left on device" mid-session; 40 merged worktrees (about 550 MB each) had accumulated.
- **Rule:** check free space before any run or worktree creation, and remove merged worktrees (junction-safe) at the end of each session.

## 2026-10-12 -- A data-gate probe called with the wrong venue symbol names
- **Pattern:** I called `check_price_window` with `BTCUSDT`; on Kraken the generated protocol names `BTCUSD`, so every window "declined" and every fetch went to the network. A result of "all decline" for coins whose caches I had just read was a probe bug, not data.
- **Rule:** call a gate or fetch helper with the symbol names the generated protocol uses for that venue (`_generated_protocol_venue_keys`, or a past run's `protocol_result.yaml` results), and treat a uniform failure as a probe bug until a cache read confirms it.

## 2026-10-12 -- A gate check rewrote cache files
- **Pattern:** the data gate's fetch (`DataManager.fetch_historical_data`, localStorage on) re-saved five daily caches in my worktree (float re-formatting, after a failed network fill of 2018-01-12). Run against the operator's checkout, it would have edited their files.
- **Rule:** run gate or fetch checks only in a worktree, on copies of the operator's caches; `git checkout -- trading-bot/local_data` afterwards and check `git status` before committing.

## 2026-10-12 -- A prescribed weighting used without checking its range
- **Pattern:** the lot weight net_portfolio_return_pct / realized_return was given; 4 lots got a negative weight (net after fees, realized before). The figures still matched, but the engine-exact weight differs by up to 13%.
- **Rule:** before reporting a weighted figure, print the weight's min / median / max over all records and compare with the exact formula from the code; report both when they differ.

## 2026-10-12 -- Files written with CRLF next to LF siblings
- **Pattern:** the Write tool produced CRLF briefs; the first diff against the LF sibling showed every line changed.
- **Rule:** after writing a file that has siblings, compare `grep -c $'\r'` with a sibling's committed bytes and normalise before diffing or committing.

## 2026-10-12 (continued) -- Backslashes in a heredoc broke code again (sixth and seventh time)
- **Pattern:** a `\n` inside a Python-in-bash heredoc became a real newline, once in a test file and once in a mutation script; an em dash in a command-line string broke a match the same session.
- **Rule (reinforced):** any text with a backslash or a non-ASCII character goes through the Write or Edit tool into a script file; never a heredoc or a `-c` string.

## 2026-10-12 (continued) -- An LLM step told to copy a config verbatim is not a copy
- **Pattern:** 1b dropped or moved the brief's first clip in 4 of 5 attempts while told to build exactly the given JSON; one rewrite (run_085) passed as `exact` and cost a trial.
- **Rule:** when exactness is the requirement, write it by code (D-110) and check the result against the source by replay (D-109).

## 2026-10-12 (continued) -- A new path modelled on an existing one without reading the next stage
- **Pattern:** composition mode's 1b writes no block manifest; a normal run's backtest_specification requires one (the advisor caught it before the build).
- **Rule:** before modelling a new path on an existing one, read what the next stage requires from it.

## 2026-10-12 (continued) -- A brief re-run checked at registration and the repeat gate only
- **Pattern:** I said the SMA 50 re-run would pass after checking `register` and the step-5a repeat check; step 1a declared the brief exhausted because `brief_hypothesis_ids` counts the void run_085's card (run_087).
- **Rule:** before re-running a brief, check what step 1a requires (its `already_produced` context, tried ideas, the knowledge base), not only registration and the repeat check.

## 2026-10-12 (continued) -- Model drift moved from stage to stage
- **Pattern:** after 1b was written by code, step 2 (also a model) named no variant `base` and the run paused (run_088).
- **Rule:** when a brief must run exactly, list every model stage between the brief and the backtest and decide each one up front.

## 2026-10-12 (continued) -- A field's effect stated without checking a run where it was set
- **Pattern:** I told the operator run_088's `symbol: BTCUSDT` on its base would test BTC only; with the variant loop off the key is ignored, and run_084 carries the same key and backtested 3 coins x 6 windows (advisor's correction).
- **Rule:** before stating what a field does, find a finished run where it was set and read what that run did (here `protocol_result.yaml`).

## 2026-10-12 (continued) -- A run record nearly edited to fit a new rule
- **Pattern:** I proposed adding the exact manifest to run_086's frozen `research_brief.yaml`; the advisor ruled it out (editing a run record) and retired the run instead.
- **Rule:** never change a run's frozen artifacts to fit a rule made after it launched; retire the run or start a new one.

## 2026-10-12 (continued, part 3) -- A pre-registered rule read a number the fold's shape made not evaluable
- **Pattern:** D-108's continue rule read the whole-test Sharpe. On fold B's interleaved blocks the chain counted 611 planned gap days, so the Sharpe was NOT_EVALUABLE on all three runs; nobody had run the rule's inputs on the fold's shape before pre-registering it.
- **Rule:** before pre-registering a rule, run its every input once on the fold's real shape (a dry computation on synthetic data shaped like the fold).

## 2026-10-12 (continued, part 3) -- A registry write followed a grid verdict that was not the pre-registered rule
- **Pattern:** run_089 was registered automatically because the grid validated it under step 1a's generic criteria (the lot-based ratio, D-107's artefact), before D-108's own rule was read. My earlier read-only registry-route check (reported in chat to the operator, this session) had said it "won't reliably happen".
- **Rule:** when a brief carries its own decision rule, list every automatic write that a different verdict can trigger (registry, memory, queue) before the run, and say which one fires first.

## 2026-10-12 (continued, part 3) -- Backslashes in a heredoc, eighth and ninth time
- **Pattern:** a script written through a shell heredoc turned `\n` inside Python strings into real newlines (fold_b_figures.py). Ninth time, while fixing these very notes: a Windows path in a heredoc Python string lost `\f` to a form feed (caught by grep, repaired before merge).
- **Rule:** write any file or replacement text that contains a backslash with the Write or Edit tool, never through a heredoc; after any scripted text edit, scan the file for control characters.

## 2026-10-13 -- Re-measure counts and line numbers from the direction
- **Pattern:** the direction's citation count (11) and two line numbers (run_protocol :1130, template :165) were wrong against current master (75 lines; :1178, :175); "nothing loads the file except the include" was also false (gate registry). Separately, one pytest call mixing strategy-research and trading-bot test files fails at collection (clashing `_cache_guard` modules), and a worktree shows 9 failures that also fail on clean master.
- **Rule:** re-run the count and re-read each line on the current tip before acting on a number from a brief; run the two test roots in separate pytest calls from their own directory; before blaming a change for failures, rerun them on stashed/pristine master in the same worktree.


## 2026-10-13 -- A rule entered the system through a bundled design, not through the operator
- **Pattern:** D-085's fold "lineage" (avoid every fold any ancestor used, fixed order A-B-C, "exhausted" after three) was built as if decided; the operator had only answered "fixed folds rather than a random draw" (decision D1). The rest came bundled with the review's design. Same session: refold was first built with options and a step-1a pass the operator never asked for, and the first answer to "decide-next queues nothing" named a field instead of asking what "nothing" meant.
- **Rule:** a control is added only when the operator asks for it (or a hard rule or card requires it); an operator-run command beats an automated gate. When a design arrives bundled with an operator answer, list which parts the operator actually decided before building them.

## 2026-10-13/14 -- Backslashes in a heredoc, tenth and eleventh time; a junction removal that silently failed
- **Pattern:** a `\n` in a heredoc Python string became a real newline (test_d119_d120.py, 10th); a test patch with `\\n` inside a quoted heredoc was mangled (11th); a heredoc that itself contained `'''` broke the shell parse (nothing ran). Separately, `cmd //c "rmdir <absolute path>\venv"` from Git Bash printed "path not found" twice and removed nothing.
- **Rule:** every script and every patch goes through the Write tool, then runs with python; never a shell heredoc for code. Remove a worktree's venv junction with PowerShell `(Get-Item -LiteralPath <path> -Force).Delete()`, check the shared venv's python.exe still exists, and only then `git worktree remove`.

## 2026-10-14 -- A run beyond a ruled exit point is a recorded fact
- **Pattern:** run_091 (SMA 50 on fold D) was launched as the refold vision test; Fable's exit point allowed lane 1 only one fold-C batch, so the run used fold D for this idea beyond the ruling. It was nearly reported only as a test.
- **Rule:** a run that goes beyond a ruled exit point is recorded as such in the next D-row, even when the operator launched it (what it used, which ruling it went past).

## 2026-10-14 -- Read the ruling's verbatim text before building
- **Pattern:** three requirements of ruling 2 almost slipped because the work started from a summary: the numbers had to come from scripts under the epic folder, the fragility condition had to be stated before the run, and the exact wording of the registry item. All three were in the operator's text, recovered from the session transcript.
- **Rule:** before each ruling item, re-read the item's verbatim text (transcript or brief), not a summary of it; quote the requirements it lists in the PR.

## 2026-10-14 -- An instruction's own numbers and tool inputs are checked before "exact commands" are promised
- **Pattern:** the ruling said to build run_084's block with `build_block` (cited at :212) and to retire "seven" held entries. On the live files `build_block` was at :288 and refuses run_084's stored entry (a `refuted` grid; its cell loop requires PASS), and the operator's queue held 12 `__more` entries. Also, `tests/test_feature_flag_register.py` already failed on the operator's own files (`folds` on in config, off in the register). All four surfaced only because the commands were run against copies of the real files first.
- **Rule:** before handing the operator an exact command, run it (read-only or on a scratch copy of the real files) and report any gap between the instruction and what the files hold - a line number, a count, a status - as a finding with a recommendation, never silently adjusted.

## 2026-10-14/15 -- Bar size taken from a proxy field, not the manifest (advisory session, its own words)
- **Pattern:** "I split a sample into daily and hourly using the effective sample size, which is small for hourly bars too, and wrote wrong figures into a PR."
- **Rule:** "take the bar size from the manifest's timeframe, and read a field's definition before grouping by it."

## 2026-10-14/15 -- Merged before review and CI had finished (advisory session, its own words)
- **Pattern:** "#428 was merged before its review and CI had finished. Both came back clean."
- **Rule:** "the order should be review, then CI, then merge."

## 2026-10-14/15 -- Stated what a writer would write before reading the writer (advisory session, its own words)
- **Pattern:** "I said the resume would add trial rows before reading the ledger's duplicate guard (run_phase1_research.py:13282)."
- **Rule:** "read the writer before stating what it will write."

## 2026-10-15 -- A session closed without its SESSION_LOG entry loses its lessons
- **Pattern:** the overnight advisory listed three lessons and a session entry "when you ask for the session log"; the session was closed before the ask; nothing reached disk until the direction session recovered the words from the operator's paste.
- **Rule:** the entry and the lessons are written before a session is closed, not on request; the closing message is the entry.

## 2026-10-15 -- A card rule quoted from memory acquired a trigger it does not have
- **Pattern:** "card J" was restated as "tests: none AND a missing piece means park"; the card's text keys on a missing component at step 5a per variant and never mentions claim status.
- **Rule:** before building or escalating a rule "as the card says", paste the card's sentence verbatim next to the proposed rule.

## 2026-10-15 -- A decision was posed for a fix already open as a PR, and restated against a stale master
- **Pattern:** the item-3 report asked "fix A or A and B" while PR #433 already carried fix A; the direction session restated the choice, and its state line named a master head (e0bc59cf) two merges old.
- **Rule:** before posing or restating a decision, fetch and read the open PR list and the master head against it; a fix in flight is a merge question, not a design question.
