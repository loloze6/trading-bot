# Lessons

Patterns that produced a correction, and the rule adopted to prevent a repeat.
Newest last. Each entry states what happened, why the reasoning failed, and the rule.

> **File created 2026-07-26.** The standing operating rules call for this file; it had
> not been created before now, so it starts with the two entries below rather than with
> the full history of prior corrections. Earlier lessons live in
> `strategy-research/PIPELINE_IMPROVEMENTS_20260712_v4.md` (the ledger) and in
> `strategy-research/engineering/sessions/SESSION_LOG.md`.

---

## L-2026-07-26-A — Scope a guard by the policy's own unit, not by where the thing happens to sit

**What happened.** The frozen holdout is defined as a DATE RANGE:
`holdout_range: ["2026-01-01", "2026-06-30"]`
(`strategy-research/config/campaign_data_policy.yaml:18`). Every mechanical guard built
for it was scoped to a DIRECTORY NAME instead — `**/holdout_sealed/`,
`trading-bot/local_data/*/`, and the 2026-07-24 quarantine that physically moved the
Kraken Q1 tranche into `holdout_sealed/`. Those guards worked, and the reachability
re-check that confirmed them was genuine.

They also missed the leak entirely. Seven loose CSVs at `trading-bot/local_data/` root —
`BTCUSDT_1h`, `ETHUSDT_1h`, `BTCUSDT_1d`, `ETHUSDT_1d`, `fear_greed_daily`,
`BTCUSDT_funding_8h`, `ETHUSDT_funding_8h` — carry between 78 and 4,344 rows each inside
the protected range, in the default un-prefixed Binance cache slot every fetcher consumer
reads. Three of them were committed and published from `ac27791` (2026-06-12) onward,
while `local_data/README.md` told collaborators not to obtain 2026 H1 data. Nothing was
evaded: the directory guards were simply answering a different question than the policy
asks.

**Why the reasoning failed.** "Protected data lives under `holdout_sealed/`" was treated
as equivalent to "protected data is 2026 H1". It never was. The first is a claim about
LOCATION, the second about CONTENT, and the two coincide only for as long as nobody
writes protected content anywhere else. A cache fetcher topping up BTCUSDT to the present
day does exactly that, silently, as a side effect of doing its normal job — no policy
violation is required, only a default `end_date`.

**Same class as the G6 name-enumeration failure, reached from the opposite direction.**
G6 failed three times because it enumerated FORBIDDEN NAMES over an unbounded set of
possible names (`strategy-research/tools/record_schema.py:5-26`); the fix was deny-by-
default over a closed set of PERMITTED fields. Here the enumeration is of PERMITTED
LOCATIONS over an unbounded set of possible locations. Both are the same mistake: the
guard is expressed in a vocabulary — names, paths — that is not the vocabulary the policy
is written in. A guard stated in the wrong unit can be perfectly enforced and still not
enforce the rule.

**RULE.** When a policy protects something by a property (a date range, a value bound, a
provenance class), the guard must test THAT PROPERTY. If the available mechanism cannot
express it — `.gitignore` cannot ask "does this CSV contain a row after 2026-01-01" —
then say so at the guard site, name what the mechanism does and does not catch, and file
the residual gap as open. Do not let a location-scoped or name-scoped proxy be recorded,
or believed, as coverage of the real rule. Concretely for this campaign: any new guard
for `holdout_range` is scoped by TIMESTAMP, and a check that reads the last timestamp of
every cache CSV before publication is the missing control — **not built as of
2026-07-26**, filed open, not closed by the name enumeration now in `.gitignore`.

---

## L-2026-07-26-B — Re-baseline a dispatch drafted before its predecessor's commit lands

**What happened, twice.** A dispatch is drafted while a sibling writer still has an
uncommitted change in flight, so its precondition manifest names the HEAD visible at
drafting time. The writer commits; HEAD moves; the manifest now fails on a commit that is
not merely acceptable but is the exact state the dispatch was meant to build on, and the
reader STOPs. The failure mode is not a wrong baseline — it is a STALE one, and it looks
identical to a genuine premise failure at the moment it fires, which is why it costs a
full round trip every time.

This was recorded once already, in the parallel-dispatch context (a read-only sibling
baselined at pre-write HEAD stopping once the writer sibling committed), with the remedy
stated as: baseline at the writer's produced commit, or set relay order, or make the
manifest tolerant. It then recurred. A remedy that is written down but has no carrier in
the artifact it governs is not a remedy; it is a hope that the next author remembers.

**Why "just baseline it correctly" is not sufficient.** At drafting time the writer's
commit hash does not exist yet, so the correct value is genuinely unavailable to the
author. Any rule that requires knowing it in advance will keep failing. The rule has to
survive the hash being unknown.

**RULE.** Every dispatch header carries an explicit **RE-BASELINE marker** stating the
manifest's relationship to pending work — one of:

- `RE-BASELINE: none — no writer in flight; manifest HEAD is final.`
- `RE-BASELINE: required — manifest HEAD <X> predates <writer>'s pending commit.
  Re-baseline at that commit's hash before dispatching; do not dispatch against <X>.`
- `RE-BASELINE: tolerant — accept HEAD <X> OR any descendant of <X> whose only
  additional commits are <writer>'s. Verify by ancestry, not equality.`

The marker is mandatory and explicit even when the answer is "none", for the same reason
the schema exemption in `record_schema.py:131-148` is named rather than left implicit: an
unexamined default is how the previous rounds failed. A dispatch whose header lacks the
marker is malformed, and the reader should say so instead of guessing which case applies.

---

## L-2026-07-26-C — Empty tool output is not evidence until cwd and search scope are stated

**What happened, three times.** W2, then W3, then W4 (this session) each drew a conclusion
from a search that returned nothing, when the search had not actually run over the
intended files. W4's instance is the cleanest specimen because the exit code was still on
screen: a scan of 2,914 untracked CSVs for holdout-range rows was piped through
`xargs -0 rg -l ...`, and it printed `FILES WITH 2026+ DATED ROWS: 0`. That zero was
produced by `xargs: rg: No such file or directory` — ripgrep is not on the Git Bash PATH
in this environment — and the command exited 127. Re-run with `grep -E`, the same scan
over the same list returned **4 files**, all of them genuine holdout leaks. The "clean"
result and the "contaminated" result differed only in whether the binary existed.

**Why the reasoning failed.** A search has two independent failure modes that render an
identical empty result: *the thing is not there*, and *the search never looked*. Only the
first is evidence. The second is produced by a missing binary (exit 127), a cwd that is
not the repo root, a glob that matched no files, a path list built against a different
tree, or a filter applied before the data. Nothing in the output distinguishes them —
`0 results` renders the same either way — so the reader supplies the interpretation, and
the convenient interpretation is the one that lets the task proceed. This is the same
error class as L-2026-07-26-A: a claim about LOCATION or MECHANISM ("I ran a scan") was
substituted for a claim about CONTENT ("the files are clean"), and the two coincide only
while the mechanism is actually working.

**Why "be careful" is not sufficient.** All three instances involved an operator already
trying to be rigorous. The failure is not inattention; it is that an empty result is
*self-certifying* by default — it arrives looking like an answer, with no field that says
"and here is the number of files I opened." Any remedy that depends on remembering to feel
suspicious will fail on the run where the result is what you expected anyway.

**RULE.** A negative search result may not be cited as evidence — in a report, a gate, or
a decision to proceed — unless the same message states all three:

1. **cwd**, verified in the same command (`pwd` or `git rev-parse --show-toplevel`), not
   assumed from an earlier call. Bash tool cwd does not persist the way it appears to.
2. **Scope actually covered** — the file count the search consumed, not the count it was
   meant to consume. `files scanned: N` where N is measured, e.g. `wc -l` of the input
   list, plus the tool's exit code. Exit 127/126 or any nonzero from the search leg voids
   the result outright.
3. **A positive control** — the pattern demonstrated matching a fixture that must match,
   run in the same invocation. A pattern that matches nothing anywhere is
   indistinguishable from a clean tree.

Corollary for gates whose failure is permanent (publication, commit, holdout): the
positive control is mandatory, not optional. W4's gate found real 2026 bars only because
the pattern was first proven against a synthetic `2026-01-01` row and a `2025-12-31` row
that must NOT match. Absent that step, a typo'd regex would have certified the leak clean
and the commit would have been unrecoverable.

---

## L-2026-07-27-A — A canary's "own return" vs "next return" framing must be checked against the harness's OWN trade timing, not just the audit's timing

**What happened.** Building the aux-feed causality canary for dispatch W8, the first
version defined the HONEST fixture as `canary[T] = (close[T+1]-close[T])/close[T]`
(labelled "bar T's own forward return, already realized by delivery time") and the
CONTROL fixture as that value shifted one bar further out. Run through the real
merge/strategy/execution path, the "honest" fixture produced a 14.76x blowup and the
"control" produced a flat ~6.6% — exactly backwards from what the test was designed to
show. The error: `close[T+1]` requires bar `T+1`'s own close, which does not exist until
bar `T+1` itself completes — so the "honest" fixture was already the leak, not the safe
case. The actual honest quantity is `own_ret[T] = (close[T]-close[T-1])/close[T-1]`
(bar T's OWN return, using only information available by the time bar T is delivered);
`(close[T+1]-close[T])/close[T]` is genuinely "that bar's NEXT return" and is exactly the
thing a canary is supposed to prove the pipeline cannot profit from.

**Why the reasoning failed.** The audit correctly established WHEN a bar is delivered
(after its own window closes). It is easy to then reason only about delivery time and
forget that the TEST HARNESS itself has its own trade-timing model: in this codebase, a
strategy's decision made in response to bar T's data is filled at `close[T]` and marked
to market at `close[T+1]` on the next call — meaning the harness inherently pays out
`(close[T+1]-close[T])/close[T]` for whatever position is opened at bar T, regardless of
which synthetic feature is under test. A feature is only "honest" if it is uncorrelated
with THAT specific quantity by construction; checking the audit's delivery-time argument
alone is necessary but not sufficient; it is also not sufficient to just plant "a
plausible-sounding future value" and trust the label without deriving, index by index,
which close prices it requires and when those become known.

**RULE.** When building a canary/positive-control pair for a look-ahead test: (1) name
the exact real-world quantity in closed form (e.g. `(close[T+1]-close[T])/close[T]`), (2)
state explicitly which raw inputs it requires and the earliest index at which each of
those inputs is known, (3) separately trace what the TEST HARNESS's own execution timing
actually pays out for a decision at row T (not just what the production system would),
and (4) only then assign "honest" vs "leaky" labels. Run both fixtures before trusting
either assertion — a canary that has never been observed to fail on its own control is not
yet known to be sensitive, and one whose "honest" case fails on the first run is telling
you the labels are wrong, not that the pipeline is broken.

---

## L-2026-09-05-A — A declarative control artifact with no reader is not a control

**What happened.** A recurring pattern, five separate instances found in one pass
(2026-08-24): a schema, a threshold, or a config field gets written — `workflow_artifacts/schemas/*.json`,
`workflow/stages.yaml`'s `conditions` field, `promotion_audit.schema.json`'s
declared fields, `campaign_state.yaml` bookkeeping — and treated from then on as
though writing it were the same as enforcing it. It never was. Confirmed
independently and separately for the schema case: no code under `workflow/` or
`tools/` ever loads `workflow_artifacts/schemas/*.json` — the only hits are
source comments (see `strategy-research/CLAUDE.md`'s own corrected preamble,
and E-037 finding E037-09). A schema that nothing reads cannot reject a bad
artifact; it can only look, to a human skimming the repo, like a rule that
exists.

**Why the reasoning failed.** Declaring the shape of a rule and building the
seam that checks it against real values are two different acts of work, and
the first one is far cheaper — a JSON Schema file or a YAML field can be
written in minutes, wiring a validator into the actual read/write path takes
longer and touches more code. When both acts produce an artifact that *looks*
like "the control exists" (a file under `schemas/`, a `conditions:` key in a
config), the cheap act gets mistaken for the expensive one having happened.
This is the same class as L-2026-07-26-A (a guard scoped to the wrong unit):
here the guard isn't scoped wrong, it simply was never built, but the
declaration alone is convincing enough to be filed as done.

**RULE.** A control (schema, threshold, validation rule) is not "in place"
until you can point at the specific code line that reads the declared
artifact and rejects a value that violates it. If asked "is X validated" or
"is X enforced," grep for a reader before answering yes — a file existing
under a name like `schemas/` or a field existing in a YAML config is not
evidence of enforcement, only of intent. Where enforcement genuinely doesn't
exist yet, say so explicitly at the point of use rather than letting the
artifact's mere existence stand in for it (this is now stated as a standing
rule in `strategy-research/CLAUDE.md`: "Schemas are declared but not
enforced").
