# Stationary block bootstrap gap-awareness — policy pre-registration (CUL-20 / GH#63)

**Issue:** GH#63 / CUL-20 · **Status:** proposed, awaiting Jeremy + Dorian sign-off
**Written:** 2026-09-03, BEFORE any implementation. Measured on fork tree `d961a3d7`.
**Shared helper:** [`PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md`](PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md).
**Parent policy:** [`PRESCREEN_GAP_POLICY.md`](PRESCREEN_GAP_POLICY.md) §6 scope-limit
note — *"(B) corrects the Fisher-z branch only. The stationary block bootstrap …
still builds blocks positionally and wraps circularly, so a block there can
still straddle a hole. Filed as a follow-up."* This is that follow-up.

This is the most invasive of the three (memo estimate ~15-25 lines) and changes
recorded p-values on the degenerate-active-forecast path, which is the family
the committed production strategy belongs to. It ships **on by default** and is
declared under fork rule 4.

---

## 1. Exact current behaviour (measured, `d961a3d7`)

`_stationary_block_bootstrap_ic_significance`
(`strategy-research/tools/prescreen_signal.py:758-834`) resamples fixed-length
blocks with replacement, per symbol, wrapping circularly at the end of each
symbol's series:

```python
# prescreen_signal.py:805-815 (per-symbol block build; enclosing `for _ in range(n_resamples)` at :803)
for f, ret in symbol_arrays.values():
    n = len(f)
    if n == 0:
        continue
    n_blocks_needed = (n + block_size - 1) // block_size
    for _b in range(n_blocks_needed):
        start = rng.randrange(0, n)
        for k in range(block_size):
            idx = (start + k) % n  # circular wrap -- Politis & Romano (1994)
            rf.append(f[idx])
            rr.append(ret[idx])
```

`symbol_arrays` (built `:783-789`) drops the timestamp — it keeps only `f` and
`ret` lists. `start` is drawn over the whole positional series `[0, n)` and the
block walks `(start + k) % n`, so a block **spans any hole** that falls inside
its `block_size` window, and the circular wrap at the series end stitches the
last bar to the first (a maximal discontinuity). Both corrupt the serial
dependence the block bootstrap exists to preserve. Because the resampled IC
distribution is the null the p-value is read against, spanning gaps distorts
that distribution — **plausibly narrowing it and understating p** (making junk
look significant), same direction as the Fisher-z `n_eff` defect PR #65 fixed.

**Blast radius (CBM graph, `trace_path` inbound `_stationary_block_bootstrap_ic_significance`, depth 4): six distinct function callers.**
Table convention (shared across all three patch docs): one row per distinct
**function** on the inbound trace — direct callers at hop 1, transitive callers
at the hop the graph first reaches them; a *call-site* line is the line inside
the caller that reaches the next hop. Two graph rows are module-level nodes
(`prescreen_signal`, `run_protocol`), not functions, and are omitted.

| Caller | Hop | File:line | Records carry `"timestamp"`? | `expected_step` available? |
|---|---|---|---|---|
| `prescreen_signal.run_prescreen` | 1 (direct) | `prescreen_signal.py:1495` — `_stationary_block_bootstrap_ic_significance(all_records_by_symbol)` | **Yes** (`_extract_forecasts` :566) | **Yes** (`expected_step_by_symbol`, :1320) |
| `prescreen_signal.main` | 2 | `prescreen_signal.py:1764`; via `run_prescreen` (call `:1780`) | inherits | inherits |
| `run_protocol._pooled_ic_with_bootstrap_fallback` | 1 (direct) | `run_protocol.py:765` — `_stationary_block_bootstrap_ic_significance({symbol: records})` | **NO** — records built at `run_protocol.py:757-760` carry only `'forecast'` and `'next_return_bps'` | **No** |
| `run_protocol._build_extended_summary` | 2 | `run_protocol.py:769` (def); calls the fallback at `:792` | inherits (No) | inherits (No) |
| `run_protocol.evaluate_against_decision_rules` | 3 | `run_protocol.py:845` (def); calls `_build_extended_summary` at `:863` | inherits (No) | inherits (No) |
| `run_protocol.main` | 3 | `run_protocol.py:1106` (def); calls `_build_extended_summary` at `:1464` (and `evaluate_against_decision_rules` at `:1472`) | inherits (No) | inherits (No) |

The entire `run_protocol.py` chain (the three transitive callers above all reach
the bootstrap only through `_pooled_ic_with_bootstrap_fallback`) is the
load-bearing constraint: that function builds its records with **no timestamp
column** (`:757-760`), pooling one symbol's `bars.csv` across walk-forward
windows. If the fix required timestamps unconditionally it would `KeyError`
here. Therefore the convention below is `expected_step=None` ⇒
positional behaviour, and that caller passes nothing (keeps today's behaviour,
bit-identically). Whether that caller *should* eventually be made gap-aware
(its records span window boundaries positionally too) is a **separate latent
instance**, logged as an observation, not fixed here.

---

## 2. The convention (stated before any number)

**A bootstrap block never spans a data gap and never wraps across one.** Blocks
are drawn from within a single contiguous segment: pick a segment, pick a start
inside it, and wrap circularly **within that segment only**. A segment shorter
than `block_size` contributes blocks of its own (whole-segment) length rather
than borrowing bars from across a hole. Segments come from
`_contiguous_segments(recs, expected_step)`; the block budget stays
`ceil(n_segment / block_size)` summed over segments so total resampled mass is
comparable to today's.

Pre-committed rationale: a block straddling a 53-hour hole asserts a serial
dependence between bars that were never consecutive — the identical error #50
describes, in the resampling instead of the labelling. The circular wrap at the
series end is the same error at maximum magnitude and is likewise confined
within a segment.

---

## 3. Signature and wiring

- `_stationary_block_bootstrap_ic_significance` gains
  `expected_step_by_symbol: dict | None = None`. **Default None ⇒ one segment
  per symbol ⇒ byte-identical resampling** (same seed, same `rng` draw order over
  the same `[0, n)`), which is the bit-identity lever.
- **Seed/draw-order preservation is load-bearing.** The current code draws
  `n_blocks_needed` starts per symbol in a fixed order from a single seeded
  `random.Random`. The segmented version must preserve the exact draw sequence
  when `expected_step=None` (one segment == whole series) or the "byte-identical"
  claim is false even on gap-free inputs. A test pins the RNG draw order.
- `run_prescreen` (`:1495`) passes `expected_step_by_symbol`.
- `run_protocol.py`'s fallback caller (`:765`) passes nothing → None → unchanged.

Estimated size: ~15-25 lines (memo), the most invasive because the per-symbol
block-build region (`:805-815`, block-construction inner loops `:810-813`) is
rewritten and the per-symbol draw budget re-derived per
segment while holding the RNG sequence stable in the None case.

---

## 4. Pinning tests to be written

New/extended modules:
`strategy-research/tests/test_prescreen_gap_continuity.py` (extend),
`strategy-research/tests/test_significance_methodology_pin.py` (extend),
`strategy-research/tests/test_pooled_ic_bootstrap_fallback.py` (extend).

- **`test_bootstrap_no_expected_step_is_byte_identical`** — with
  `expected_step_by_symbol=None`, the returned dict (pooled_ic, p_value,
  n_bootstrap_valid) is byte-identical to today's on a gappy fixture, same seed
  (the RNG-draw-order gate).
- **`test_bootstrap_block_never_spans_gap`** — instrument the resampler on a
  synthetic two-segment symbol; assert no emitted block contains a
  `(bar_i, bar_j)` pair whose timestamps differ by more than `block_size ×
  expected_step` — i.e. no block crosses the known hole.
- **`test_bootstrap_no_circular_wrap_across_series_end`** — the last-to-first
  wrap only ever occurs within a segment, never between the final segment's end
  and the first segment's start.
- **`test_bootstrap_gapfree_unchanged`** — a gap-free single symbol is
  byte-identical with and without `expected_step` (one segment).
- **`test_pooled_ic_bootstrap_fallback_timestampless_records`** — the
  `run_protocol.py` caller path (records with no `"timestamp"`, `expected_step`
  unset) still runs and returns today's result — the KeyError guard.

Mutation obligation: each must bite. Per PR #65's own hard lesson, **the wiring
inside `run_prescreen` must be exercised end-to-end, not only the function in
isolation** — PR #65 found three mutations of part (B) that survived because the
tests exercised the helpers alone while the mutated lines lived inside
`run_prescreen`. At least one test here drives `run_prescreen` on the degenerate
path so a mutation of the segmented block build is killed at the call site.

Existing tests at risk of re-pinning:
`test_significance_methodology_pin.py`, `test_pooled_ic_bootstrap_fallback.py`,
`test_prescreen_gap_continuity.py`.

---

## 5. Expected effect on existing artifacts (fork rule 4)

- **May change:** `p_value`, `significant`, and `n_bootstrap_valid` from
  `block_bootstrap_all_bars_v1`, **on gappy symbols only**, on the
  degenerate-active-forecast path (`run_prescreen` `:1495`, and the
  `run_protocol` fallback only if it is ever given timestamps + `expected_step`,
  which this patch does not do). Direction expected: p-values **rise** (less
  significant) where gap-spanning blocks were narrowing the null; not
  pre-committed as a threshold.
- **Must NOT change:** any gap-free symbol (one segment ⇒ identical draws);
  the `run_protocol.py:765` fallback result (stays on the None default);
  `run_060`'s kill (USDT majors, 0.00-0.05% gap pairs, died at a cost hurdle
  three orders of magnitude away); trial accounting / DSR N (prescreen rows
  never enter the pool); the backtest path.
- **`forecast_hash`:** unchanged — this patch reads forecasts but does not
  produce them.
- **No lookahead:** resampling reads only recorded (forecast, return, timestamp)
  triples that already exist; timestamps are read solely to decide segment
  membership, never to reference a future bar's value.

---

## 6. Kill criteria

- If `test_bootstrap_no_expected_step_is_byte_identical` fails, the None path
  perturbed the RNG draw order — the byte-identity claim is dead; stop.
- If a gap-free symbol's p_value moves, segmentation mis-fires; stop.
- If the `run_protocol.py` fallback raises `KeyError` on `"timestamp"`, the
  None-default guard is missing; stop — this caller must remain untouched.
- If the change *lowers* a p-value on a gappy symbol (more significant), the
  correction sign is inverted; stop — hidden gaps were inflating significance.
- If making blocks segment-local forces a rewrite of the pooling/seed contract
  beyond ~25 lines, scope has crossed into D1b territory; stop and reconsider.
