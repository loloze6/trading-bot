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
| `alt 1` / `alt 2` / `alt 3` altitude numbering | §2.1 map | stage 11 block, logic step 5 — **with** the note that the matching `altitude` field is phantom ([F22](FINDINGS.md#f22)) |
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

- **Did not move the five flag-gated artifacts' `Objective:` prose into stage
  blocks**, which the EPIC lists for S4. There is nowhere to move it: those
  artifacts belong to features that are off by default and have no stage block
  ([F21](FINDINGS.md#f21)). Forcing the move would also destroy the evidence
  for [F20](FINDINGS.md#f20). Recorded rather than forced.
- **Did not migrate `file:line` anchors to `file::symbol`.** Recommended, and
  the reason it was deferred is in [`S3_TRIAGE.md`](S3_TRIAGE.md) — two
  automated attempts were reverted. It wants a deliberate pass, not a
  session-end rewrite.
- **Did not hyperlink every glossary term at its point of use.** §6 and the
  §2.2 terms table now cross-reference each other, which covers the reader's
  actual need; per-term anchors for 30+ table rows is available if wanted.
- Fixed no findings. F28 was raised, not corrected.
