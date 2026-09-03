# Shared helper — `_contiguous_segments` (the #50 family guardrail)

**Issue:** #50 family (CUL-15) · **Status:** implemented 2026-09-03 (fork `mac/setup`, patches P1/P2/P3); the pre-registration text below is unchanged
**Written:** 2026-09-03, BEFORE any implementation. Measured on fork tree `d961a3d7`.
**Line numbers:** measured on the pre-patch tree `d961a3d7` (upstream `3578355a` plus fork-only docs). On the shipped tree they do not navigate exactly: `prescreen_signal.py` references sit 18 lines lower above the patches (upstream `c9519775` landed first) and further below them; `episode_significance.py` references shift only by patch 3. Navigate by symbol name.

This document specifies the one small helper that the three remaining #50-family
patches share — GH#64 (turnover proxy), CUL-20/GH#63 (block bootstrap), and
CUL-21/GH#66 (episode significance). It is written first because all three
pre-registrations reference it, and because Dorian's ruling D1 = option (a) was
explicitly *"three separate, independently pre-registered patches sharing a
small `_contiguous_segments(records, expected_step)` helper, over a shared
time-aware series type left for later (not built now)."*

---

## 1. Why a shared helper at all

The #50 root defect is one confusion repeated in five consumers: **index
adjacency is treated as time adjacency.** PR #65 (merged `8a997ba8`) fixed the
first two — the forward-return pairing in `_extract_forecasts` and the Fisher-z
`n_eff` in `_block_adjusted_significance` — and, critically, added a per-record
`"timestamp"` field (`prescreen_signal.py:566`) so the remaining consumers can
each be made time-aware cheaply.

PR #65 already contains the exact primitive, inlined once, inside
`_gap_aware_block_count` (`prescreen_signal.py:629-668`, run-partition loop at
`:660-667`):

```python
run_active = 0
for i, rec in enumerate(records):
    run_active += 1 if active_flags[i] else 0
    is_last = i == len(records) - 1
    breaks = is_last or (records[i + 1]["timestamp"] - rec["timestamp"]) != expected_step
    if breaks:
        total += run_active // block_size
        run_active = 0
```

Rather than copy that loop into three more functions (a sixth, seventh and
eighth place for the same off-by-a-hole bug to be reintroduced), the three
patches factor the run-boundary detection into `_contiguous_segments` and each
consumes it. This is the *"prevent a 7th instance"* guardrail from GH#66's
writeup, obtained without building the heavier shared time-aware series type
(D1b), which would re-touch the record contract PR #65 just stabilized.

---

## 2. Signature and contract

Home: `strategy-research/tools/prescreen_signal.py`, adjacent to
`_gap_aware_block_count`. `episode_significance.py` already imports
`prescreen_signal` (it calls `prescreen_signal._spearman` at
`episode_significance.py:123`), so the episode consumer reaches it as
`prescreen_signal._contiguous_segments` with no new import cycle.

```python
def _contiguous_segments(
    records: list,
    expected_step: "pd.Timedelta | None",
) -> list[tuple[int, int]]:
    """
    Partition `records` (each a dict carrying a "timestamp" key, in bar order)
    into maximal runs of temporally-consecutive bars. Returns a list of
    half-open [start, end) index ranges covering 0..len(records) with no gaps
    and no overlaps: a boundary falls exactly where
    records[i+1]["timestamp"] - records[i]["timestamp"] != expected_step.

    expected_step=None returns [(0, len(records))] — a single segment spanning
    every record — which reproduces the pre-#50 positional behaviour exactly.
    An empty records list returns [].
    """
```

**Contract, pre-registered:**

- **C-H1.** The returned ranges are half-open `[start, end)`, contiguous, and
  exactly cover `[0, len(records))`. `sum(end - start) == len(records)`.
- **C-H2.** A boundary is inserted between `i` and `i+1` **iff**
  `records[i+1]["timestamp"] - records[i]["timestamp"] != expected_step`. The
  comparison is exact `!=` on `pd.Timedelta`, identical to the operator already
  used at `prescreen_signal.py:552` and `:664` — not `>`, so a *backwards* or
  *duplicate* timestamp (delta `<= 0`) is also a boundary. This is deliberate:
  a non-monotone timestamp is as much "not the next bar" as a hole is.
- **C-H3.** `expected_step is None` ⇒ exactly one segment `[(0, n)]`. This is
  the bit-identity lever: every consumer routed through the helper with
  `expected_step=None` computes byte-for-byte what it computes today.
- **C-H4.** The helper reads only `"timestamp"`. It never reads `"forecast"`,
  `"active"`, or `"next_return_bps"`, so it is valid for every record shape the
  three consumers pass, provided `"timestamp"` is present when `expected_step`
  is not None (see the run_protocol caveat in the bootstrap policy).
- **C-H5.** Fail-loud (per `CLAUDE.fork.md` — *"anything feeding decisions
  raises on degenerate inputs"*): if `expected_step` is not None and any record
  lacks a `"timestamp"` key, raise `KeyError`/`ValueError` naming the index —
  never silently fall back to positional. Silent fallback is exactly the class
  of bug this family exists to kill.

---

## 3. How each of the three consumes it

| Consumer | File:line (d961a3d7) | Use of `_contiguous_segments` |
|---|---|---|
| GH#64 `_compute_turnover_proxy` | `prescreen_signal.py:841`, loop `:864-873` | Iterate the segments of each symbol's records; **reset `prev_sign = 0` at each segment start** so a holding that spans a hole is closed and reopened rather than read as "no transition". |
| CUL-20 `_stationary_block_bootstrap_ic_significance` | `prescreen_signal.py:758`, block build `:809-813` | Draw each bootstrap block from **within a single segment** (choose a segment, then a start inside it, wrapping circularly within that segment) instead of over the whole positional series with a global circular wrap. |
| CUL-21 `identify_episodes` | `episode_significance.py:89`, gap test `:107` | Use the segments to convert the episode gap from positional bars to **true elapsed bars**: two consecutive active bars in the same segment keep today's `curr - prev - 1`; across a segment boundary the true bar-gap (from their timestamps) is used against `gap_bars`. |

The episode consumer needs the *magnitude* of a hole, not merely its presence
(it tolerates up to `gap_bars = 48` inactive bars before splitting), so its
pre-registration also states the exact timestamp-to-bars conversion. The other
two need only *presence* of a boundary. All three obtain that boundary from the
same helper, which is the point.

---

## 4. Pinning test for the helper itself

New test module: `strategy-research/tests/test_contiguous_segments.py`.

- **`test_contiguous_segments_none_is_single_span`** — `expected_step=None` on a
  10-record list returns `[(0, 10)]` (C-H3).
- **`test_contiguous_segments_splits_on_hole`** — a synthetic list with one
  known 1-bar hole splits into exactly the two expected ranges; the surrounding
  contiguous records stay in one range each (C-H2).
- **`test_contiguous_segments_cover_is_exact`** — for a randomized gappy list,
  the ranges are contiguous, non-overlapping, and sum to `len(records)` (C-H1).
- **`test_contiguous_segments_nonmonotone_is_boundary`** — a duplicate or
  backwards timestamp inserts a boundary (C-H2, the `!=` not `>` clause).
- **`test_contiguous_segments_missing_timestamp_raises`** — a record with no
  `"timestamp"` and `expected_step` set raises, naming the index (C-H5).

Mutation obligation (per `mutation-test-new-tests` and Dorian's tests-ship-with-
every-change directive): each test must be shown to **bite** — flip the `!=` to
`>`, drop the `is None` short-circuit, and swap half-open for closed ranges;
each mutation must fail at least one test above before the patches build.

---

## 5. What this document does NOT decide

- It does not build the shared time-aware series type (D1b) — explicitly
  deferred by D1a.
- It introduces no behaviour change on its own: until a consumer routes through
  it with a non-None `expected_step`, every output is byte-identical. The three
  behaviour changes are declared in the three consumer policies, each under fork
  rule 4, and each ships only with its consumer.
