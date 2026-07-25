# Lessons

Patterns that produced a correction, and the rule adopted to prevent a repeat.
Newest last. Each entry states what happened, why the reasoning failed, and the rule.

> **File created 2026-07-26.** The standing operating rules call for this file; it had
> not been created before now, so it starts with the two entries below rather than with
> the full history of prior corrections. Earlier lessons live in
> `strategy-research/PIPELINE_IMPROVEMENTS_20260712_v4.md` (the ledger) and in
> `strategy-research/SESSION_LOG.md`.

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
