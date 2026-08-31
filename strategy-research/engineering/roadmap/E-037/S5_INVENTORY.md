# E-037 S5 — Anchor migration: what happened

Companion to [`S5_ANCHOR_MIGRATION.md`](S5_ANCHOR_MIGRATION.md), which was
written **before** any code ran. This records the result.

**Scope:** `docs/USER_GUIDE.md` and `strategy-research/CLAUDE.md` — the living
documentation. The E-037 records were deliberately excluded: their line numbers
are dated measurements tied to a commit, evidence rather than navigation.

**Result: 104 anchors converted, 0 rejected, 0 partial state.**

| | Before | After |
|---|---|---|
| `file.py:N` (explicit) | 32 | 0 |
| bare `:N` | 72 | 0 |
| `file.py::symbol` | 1 | 105 |

---

## 1. It took three attempts, and the first two were right to fail

The gate refused twice more before this succeeded. That is the story worth
keeping.

| Attempt | Rule for a bare `:N` | Outcome |
|---|---|---|
| 1 (S3) | last `.py` mentioned anywhere in the text | **Wrote before validating.** Mis-attributed anchors, corrupted `FINDINGS.md`. Reverted by hand. |
| 2 (S3) | same, plus refuse-on-doubt | Refused: 47 unresolved. Nothing written — correct. |
| 3 (S5) | most-recent-explicit, scoped to the section | Refused: 23 unresolved. **Scope still leaked inside a block** — stage 10 names `prescreen_signal.py` early, so `:2459` inherited it and resolved to nothing. |
| 4 (S5) | constraint: every file the section names, accept only if exactly one yields a symbol | Refused: 46 unresolved. Both files are long enough that most line numbers resolve in **both**. |
| 5 (S5) | **per-section default supplied by the author, verified by output** | **0 problems, 104 edits.** |

**Why the last one is not "guessing with extra steps."** Four sections — stages
4, 5, 6, 11, 12, 13 — contain bare `:N` anchors and **name no file at all**.
That information was never in the document, so no amount of parsing could
recover it. It had to come from the author. What makes it verifiable rather
than asserted is the second half: every resolution was printed with the 78
characters of prose preceding it, and checked to match. `:2262` →
`determine_post_validation_route` beside *"if neither key is present it raises"*;
`:720` → `_is_degenerate_active_forecast` beside *"detector"*; `:982` →
`_determine_route` beside *"`_determine_route` ("*.

**That those six sections named no file is itself a defect** the migration
fixes: a reader could not have resolved those anchors either.

## 2. Loss check

| Category | Result |
|---|---|
| Amendment codes | **zero lost** |
| Dates | **zero lost** |
| Non-anchor identifiers | **zero lost** |
| Line numbers | **93 removed — the point of the exercise** |
| Symbol identifiers | 54 added |

54 rather than 93 because line numbers collapse: eight separate anchors inside
`run_prescreen` all become `prescreen_signal.py::run_prescreen`. **That is a
real, accepted loss of precision** — a reader now lands on a 400-line function
instead of a line. It is the trade the migration makes deliberately: the
numbered step titles in each block say *what* to look for, and a symbol that
stays correct beats a line number that silently stops being correct. Where
precision mattered most, the surrounding prose already names the function.

## 3. Verification

- `tests/test_doc_anchors.py`: **85 passed.** Every `::symbol` checked against
  the file's real top-level names via `ast` — not a regex, and not "in range".
- Remaining `:N` anchors reported by that test (49 explicit, 91 bare) are all in
  the E-037 records, out of scope by design.
- Full suite: 1313 passed, 4 skipped, 1 failed — `E037-26`, pre-existing.

## 4. One correction found on the way

Resolving `:490` showed it sits inside `ensure_files`'s **docstring**, not a
prompt string. [E037-18](FINDINGS.md#e037-18) and stage 3's block both said
"inside a prompt string". Corrected in both.

The claim is unaffected and slightly strengthened: `library_category` appears
once in `workflow/` and `tools/`, and that one occurrence is a note about a YAML
repair incident — not even an instruction to the model. Nothing enforces the
diversity rule.

## 5. Acceptance (from the pre-written plan)

- [x] `test_doc_anchors.py` green; navigation anchors show **0 by line number**
- [x] every `::symbol` resolves — enforced by test, not inspection
- [x] loss check run; identifier churn itemised above
- [x] no partial state — validated in memory, applied in one pass
- [x] inventory committed, same shape as S2's and S4's
