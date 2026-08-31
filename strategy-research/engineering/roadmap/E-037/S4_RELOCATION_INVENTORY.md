# E-037 S4 — Relocation inventory

**S4 is the first stage of this epic that removes anything.** S1–S3 were
additive, so the loss check passed by construction and proved little. Here it
had to actually work.

**Range:** `1b56559c` → this commit · **File:** `strategy-research/docs/USER_GUIDE.md`
**Size:** 2169 → 2208 lines · **+121 / −82**

---

## 1. Method — verify before deleting, not after

For each thing removed, the fact was proven present in its destination
**first**, and only then cut. Running that check before touching anything found
**seven facts that were not yet relocated** and would have been lost:

| Fact | Was in | Relocated to (before any deletion) |
|---|---|---|
| `evidence_type` declared from `available_feeds.yaml` | §2.2 table, stage 2 | stage 2 block, logic step 2 |
| route to `feed_wishlist.yaml` when a feed is missing | §2.2 table, stage 2 | stage 2 block, logic step 2 |
| `Impr 04` / Improvement 04 indicator lookup | §2.2 table, stage 2 | stage 2 block, logic step 2 |
| "5 named diagnostic rules" | §2.2 table, stage 11 | stage 11 block, logic step 4 |
| Bailey & López de Prado attribution for the DSR | §2.2 table, stage 13 | stage 13 block, gate 1 |
| `alt 1` / `alt 2` / `alt 3` altitude numbering | §2.1 map | stage 11 block, logic step 5 — **with** the note that the matching `altitude` field is phantom ([E037-22](FINDINGS.md#e037-22)) |
| pre-registered `expected_range` | §2.1 map | stage 13 block, gate 4 |

That is the whole argument for the checklist. Seven facts, all real, none of
them noticed by reading.

---

## 2. What was removed

### 2.1 Stage Map — annotations stripped, steps kept

The ASCII diagram carried flow **and** commentary: engine tags, gate
conditions, amendment codes, and per-node notes. Per the EPIC it is now steps
and links only. Every annotation removed was a **second copy** of what the
stage block says:

| Removed from the map | Now read in |
|---|---|
| `(reads indicator_library.yaml, available_feeds.yaml)` | stage 2 input table |
| `(diversity check: ≥2 library categories or data_requirements)` | stage 3, logic step 2 |
| `A8.6 power check (deterministic, pre-build)` | stage 4, logic step 2 |
| `refine (≤2x)` | stage 4, routes table (`max_refinements`, default 2) |
| `A8.6 pre-flight`, `active-bar IC, cost_check (A8.1: both required)`, `Records trial … (A6.2)` | stage 7, logic steps 0, 5, 8, 9, 14 |
| `(auto-triggered before verdict if report stale)` | stage 9, logic step 1 |
| `DSR gate + single-use enforcement`, `pre-registered expected_range required` | stage 13, gates 1, 2, 4 |

**Kept, not removed:** the **Ungated-only standing policy** paragraph. It is a
campaign policy rather than a step, so it survives verbatim below the map with
a label saying so.

### 2.2 Stage Objectives — paragraphs → one line each

Thirteen Objective cells, several of them 250–430 characters of prose, became
one plain-language line each answering *why the stage exists* — the original
request. Each row now links to its block.

Before compressing, every backticked identifier and amendment code in all 13
cells was checked against the blocks: **zero missing**. The load-bearing prose
was checked separately; six phrases matched only conceptually and are recorded
as `Verbatim? = no` below.

---

## 3. Token decreases, each explained

No amendment code and no number fell to zero. Eight codes dropped in *count*
because the map or table carried a duplicate:

| Code | Before | After | Occurrences in the stage blocks |
|---|---|---|---|
| A1.1 | 2 | 1 | 1 |
| A1.3 | 2 | 1 | 1 |
| A2.2 | 8 | 6 | 2 |
| A3.4 | 4 | 3 | 1 |
| A6.1 | 3 | 2 | 2 |
| A6.2 | 4 | 2 | 2 |
| A8.1 | 6 | 4 | 3 |
| A8.6 | 18 | 14 | 11 |

Every one still appears in the block for the stage it governs. The decrease is
the duplicate being removed, which is what "simplify the map" means.

### Two identifiers reached zero — both reworded, neither lost

| Token | Status |
|---|---|
| `` `available_feeds.yaml` `` | Present 3× as `` `config/available_feeds.yaml` `` — the path form, which is more precise. |
| `` `passes_deflated_threshold=False` `` | Present 2× as `passes_deflated_threshold is False` — Python's actual comparison, which is what the code does. |

### `Verbatim? = no` — six phrases reworded rather than moved intact

| Original phrasing | Now reads | Why not verbatim |
|---|---|---|
| "decide if implementation is possible in current framework" | "Decide whether the blockers … can actually be fixed inside the current engine" | plainer; same claim |
| "A8.1: both IC significance AND cost_check.pass required" | "both IC significance **and** `cost_check.pass` are required" | formatting only |
| "auto-triggered before verdict when … absent or stale" | "Runs: … before the verdict" + a 30-day staleness step | split into a fact and a mechanism |
| "decides trustworthy / needs_retune / unusable" | "Decide whether the detector is trustworthy, needs a retune, or is unusable" | prose; the literal enum stays in §3 |
| "retune acceptance criteria may never include PnL or Sharpe" | the firewall's actual forbidden-term list, which raises | replaced a rule statement with the enforcement that implements it |
| "terminal reject before holdout runs" | "reject before the seal is touched" | plainer; same ordering claim |

All six are the plain-language rewrite that was explicitly asked for. Each was
verified present in concept before the original was cut.

---

## 4. Landing criteria (S1 §4.5)

- [x] Relocation inventory committed, every removal has a destination
- [x] Mechanical residue check run; zero codes and zero numbers to zero, two
      identifiers reworded and accounted for
- [x] Anchors re-verified — `tests/test_doc_anchors.py` passes
- [ ] **Reviewed by someone other than the author** — outstanding, as for S2

---

## 5. What S4 did not do

- **Dropped: moving the five flag-gated artifacts' `Objective:` prose into
  stage blocks**, which the EPIC lists for S4.

  **Reviewed 2026-08-31 at Jérémy's challenge, and the original reasoning did
  not hold.** It claimed there was "nowhere to move it". That was wrong — those
  artifacts attach to real stages: `variant_selection.yaml` and
  `variants_not_pursued.yaml` are written just after stage 6, and
  `exclusion_digest.yaml` / `schedulability.yaml` are campaign-level. It also
  claimed moving the prose would destroy [E037-20](FINDINGS.md#e037-20)'s
  evidence; it would not, because that evidence is now recorded in
  `FINDINGS.md` with counts and does not depend on the guide staying as it is.

  **Dropped anyway, for the honest reason:** the value is low. It would
  relocate design prose for machinery that **does not run** — all six
  orchestrator flags are off ([E037-21](FINDINGS.md#e037-21)) — into blocks for
  stages that never invoke it. §3 now flags those five entries as flag-gated,
  which is what a reader actually needs. If a flag is ever turned on, that is
  the moment to write the stage-block text, against behaviour someone can
  observe rather than infer.

  Recorded this way rather than silently deleted, because "parked for good
  reasons" and "dropped after the reasons turned out to be weak" are different
  states and the second is the true one.
- **Deferred by decision, not dropped: migrating `file:line` anchors to
  `file::symbol`.** Two automated attempts were reverted (see
  [`S3_TRIAGE.md`](S3_TRIAGE.md)); it needs a deliberate pass with the
  per-block resolution rule. **Scheduled 2026-08-31 as its own task, to run
  before Jérémy's review** — see [`S5_ANCHOR_MIGRATION.md`](S5_ANCHOR_MIGRATION.md).
- ✅ **Done 2026-08-31: glossary terms are hyperlinked at their point of use.**
  Parked in error — the EPIC asked for it by name. Taken literally it is
  unworkable: 46 terms across **613** occurrences, "Run" alone appearing 131
  times, which would be unreadable. Implemented to the intent instead — *a
  reader should know a definition exists* — as **first use per section**: 46
  HTML anchors in the glossary and **74** links in the body, about one per 32
  lines. `tests/test_user_guide_toc.py` now validates those anchors too.
- Fixed no findings. E037-28 was raised, not corrected.
