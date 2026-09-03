# Turnover proxy gap-awareness — policy pre-registration (GH#64)

**Issue:** GH#64 / CUL-15 · **Status:** implemented 2026-09-03 (fork `mac/setup`, patches P1/P2/P3); the pre-registration text below is unchanged
**Written:** 2026-09-03, BEFORE any implementation. Measured on fork tree `d961a3d7`.
**Line numbers:** measured on the pre-patch tree `d961a3d7` (upstream `3578355a` plus fork-only docs). On the shipped tree they do not navigate exactly: `prescreen_signal.py` references sit 18 lines lower above the patches (upstream `c9519775` landed first) and further below them; `episode_significance.py` references shift only by patch 3. Navigate by symbol name.
**Shared helper:** [`PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md`](PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md).
**Parent policy:** [`PRESCREEN_GAP_POLICY.md`](PRESCREEN_GAP_POLICY.md) §7 already
declares this movement; that declaration is the reason this must be pre-registered.

This ships **on by default** and changes recorded `avg_holding_bars` /
`edge_to_cost_ratio` on gappy symbols, which reaches a route verdict. It is a
research-integrity change, not plumbing, so — exactly like #50 — the convention
is fixed here before the post-fix numbers are looked at.

---

## 1. Exact current behaviour (measured, `d961a3d7`)

`_compute_turnover_proxy` (`strategy-research/tools/prescreen_signal.py:841-881`)
counts a "trade open" as an activity transition. The loop, per symbol:

```python
# prescreen_signal.py:865-873 (inner loop; outer `for recs` at :864)
prev_sign = 0  # 0 = flat; tracks the actual PRIOR bar's state, flat included
for r in recs:
    curr_sign = 1 if r["forecast"] > _ACTIVE_THRESHOLD else (
               -1 if r["forecast"] < -_ACTIVE_THRESHOLD else 0)
    if curr_sign != 0:
        total_active += 1
        if curr_sign != prev_sign:
            total_opens += 1
    prev_sign = curr_sign
```

`prev_sign` is carried from one record to the **next record in the list**, with
no check that the two records are one bar apart in time. On a gappy symbol, an
active holding whose sign is unchanged across a real data hole reads as "no
transition" (`curr_sign == prev_sign`) → `total_opens` is **undercounted** →
`avg_holding_bars = total_active / implied_trades` is **inflated** →
`edge_to_cost_ratio` (which divides edge by a per-trade cost hurdle built on
holding period) rises, so the strategy looks **cheaper to trade than it is**.

**Blast radius (CBM graph, `trace_path` inbound `_compute_turnover_proxy`, depth 4).**
Table convention (shared across all three patch docs): one row per distinct
**function** on the inbound trace — direct callers at hop 1, transitive callers
at the hop the graph first reaches them; a *call-site* line is the line inside
the caller that reaches the next hop.

| Caller | Hop | File:line |
|---|---|---|
| `prescreen_signal.run_prescreen` | 1 (direct) | call site `prescreen_signal.py:1509` — `_compute_turnover_proxy(all_records_by_symbol)` |
| `prescreen_signal.main` | 2 | `prescreen_signal.py:1764`; reaches it via `run_prescreen` (call `:1780`) |

No caller outside `prescreen_signal.py`. The records dict `all_records_by_symbol` is built
in `run_prescreen` from `_extract_forecasts`, whose records carry `"timestamp"`
(`:566`), and `run_prescreen` already holds `expected_step_by_symbol`
(built `:1320-1321`).

Recorded magnitude, from PR #65's own measurement (kraken_ZECUSD valid):
`edge_to_cost_ratio` 0.2316 → 0.2209, `avg_holding_bars` 21.35 → 21.6 — but
those were the *incidental* move from #50(A) removing gap-spanning pairs. The
residual this patch targets is that the surviving records are still treated as
one contiguous series; the post-patch numbers are **not yet measured** and are
not pre-committed here (that would be threshold-fitting).

---

## 2. The convention (stated before any number)

**A holding period ends at a data gap.** When two temporally non-adjacent
records carry the same active sign, that is a close of the old holding and an
open of a new one — not a continuation. Concretely: reset `prev_sign = 0` at the
start of each contiguous segment, so the first active bar of every segment is an
open. Segments come from `_contiguous_segments(recs, expected_step)`.

Rationale, pre-committed: a 53-hour hole (kraken_ZECUSD worst) between two
long bars is not one 53-hour hold; the position was, in reality, closable and
re-openable across that hole. Counting it as one hold understates turnover and
therefore cost, in the direction that flatters the strategy. We correct in the
direction that makes the cost hurdle **harder**, never easier.

---

## 3. Signature and wiring

- `_compute_turnover_proxy` gains a second parameter:
  `expected_step_by_symbol: dict | None = None`. **Default None ⇒ single
  segment per symbol ⇒ byte-identical to today** (helper contract C-H3). This is
  the bit-identity lever and mirrors PR #65's `expected_step=None` convention.
- `run_prescreen` (`:1509`) passes its existing `expected_step_by_symbol`.
- `main`'s indirect path inherits `run_prescreen`'s behaviour; no separate wiring.

Estimated size: ~5 lines (the memo's estimate), plus the shared helper call.

---

## 4. Pinning tests to be written

Module: `strategy-research/tests/test_turnover_proxy.py` (exists — extend it).

- **`test_turnover_proxy_gap_forces_reopen`** — a synthetic single-symbol
  record list with one known hole between two same-sign active bars yields
  `implied_trades` one higher (and `avg_holding_bars` correspondingly lower)
  with `expected_step` set than with `expected_step=None`.
- **`test_turnover_proxy_no_expected_step_is_byte_identical`** — with
  `expected_step_by_symbol=None`, output equals today's on a gappy fixture
  (bit-identity gate).
- **`test_turnover_proxy_gapfree_unchanged`** — on a gap-free fixture, output is
  identical with and without `expected_step` (a gap-free series has one
  segment).
- **`test_turnover_proxy_sign_flip_across_gap`** — a sign flip that also spans a
  gap is still one open (not two): the gap-close and the flip-open coincide on
  the same bar, matching the same-bar-flip semantics documented at
  `prescreen_signal.py:843-849`.

Each test must be shown to bite (mutation): removing the per-segment
`prev_sign` reset must fail `test_turnover_proxy_gap_forces_reopen`.

Existing tests at risk of re-pinning (re-verify, declare any intended move):
`test_turnover_proxy.py`, `test_significance_methodology_pin.py`.

---

## 5. Expected effect on existing artifacts (fork rule 4)

- **May change:** `avg_holding_bars`, `implied_trades_estimated`,
  `edge_to_cost_ratio`, and hence the cost-hurdle branch of `_determine_route` —
  **only on gappy symbols**. Direction: `avg_holding_bars` down (or equal),
  cost hurdle up. Prior prescreen artifacts on gappy symbols are **not
  retro-corrected**; the graveyard is the knowledge.
- **Must NOT change:** any gap-free symbol×window (one segment ⇒ identical);
  `active_bars_total` (the active-bar count is gap-independent — only the *open*
  count moves); anything on the backtest path (`run_bot` and the backtester
  never call this); trial accounting / DSR N (prescreen rows are hardcoded
  `statistic_valid="neither"` and never enter the DSR pool, confirmed #50/PR#65).
- **`forecast_hash`:** unchanged by this patch — it is derived from forecasts,
  not from the turnover summary. (PR #65 already moved it via #50(A); this patch
  does not touch forecasts.)
- **No lookahead:** the turnover proxy reads only each bar's own forecast sign
  and the timestamp deltas between recorded bars; it makes no forward reference.

---

## 6. Kill criteria

- If `test_turnover_proxy_no_expected_step_is_byte_identical` fails, the default
  path is not bit-identical — the patch is wrong, stop and re-derive.
- If a gap-free symbol's `avg_holding_bars` moves at all, segmentation is
  mis-triggering on non-gaps — stop.
- If the change ever *lowers* a cost hurdle (makes a strategy look cheaper), the
  sign of the correction is inverted — stop; the whole point is that hidden
  gaps were flattering cost.
- If wiring `expected_step_by_symbol` requires touching the record contract or
  any non-gappy output, scope has crept past the ~5-line patch — stop and
  reconsider against D1b.
