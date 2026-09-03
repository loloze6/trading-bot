# Episode significance gap-awareness — policy pre-registration (CUL-21 / GH#66)

**Issue:** GH#66 / CUL-21 · **Status:** implemented 2026-09-03 (fork `mac/setup`, patches P1/P2/P3); the pre-registration text below is unchanged
**Written:** 2026-09-03, BEFORE any implementation. Measured on fork tree `d961a3d7`.
**Line numbers:** measured on the pre-patch tree `d961a3d7` (upstream `3578355a` plus fork-only docs). On the shipped tree they do not navigate exactly: `prescreen_signal.py` references sit 18 lines lower above the patches (upstream `c9519775` landed first) and further below them; `episode_significance.py` references shift only by patch 3. Navigate by symbol name.
**Shared helper:** [`PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md`](PRESCREEN_GAP_CONTIGUOUS_SEGMENTS.md).
**Parent policy:** [`PRESCREEN_GAP_POLICY.md`](PRESCREEN_GAP_POLICY.md) — this is
the fifth consumer of the #50 root defect, named in GH#64's "same family" list.

`n_episodes` is the headline sample-and-bootstrap unit of the A8.5.1a
significance path. This patch changes it on gappy symbols, ships **on by
default**, and is declared under fork rule 4.

---

## 1. Exact current behaviour (measured, `d961a3d7`)

`identify_episodes` (`strategy-research/tools/episode_significance.py:89-115`)
splits the active-bar sequence into episodes using a **positional** gap:

```python
# episode_significance.py:101-114
active_idx = [i for i, r in enumerate(records) if r.get("active")]
...
current = [active_idx[0]]
for prev, curr in zip(active_idx, active_idx[1:]):
    gap = curr - prev - 1                      # :107  positional bar count
    era_break = era_of is not None and era_of(prev) != era_of(curr)
    if gap <= gap_bars and not era_break:
        current.append(curr)
    else:
        episodes.append(current)
        current = [curr]
episodes.append(current)
```

`gap = curr - prev - 1` (`:107`) counts **list positions** between two active
bars, i.e. the number of recorded inactive bars between them. It never counts
bars that are *missing from the record list because of a data hole*. So two
active bars separated by a 53-hour hole but by only, say, 3 recorded inactive
bars read `gap = 3 <= gap_bars (48)` → they are kept in the **same episode**
that should have split. Episodes that should split **merge** → `n_episodes` is
**understated**. Because the A8.5.1a path gates on
`n_episodes < min_n_episodes` (`_MIN_N_EPISODES = 8`, `episode_significance.py:80`)
and bootstraps over episodes, an understated count both (a) can wrongly clear or
fail the `min_n_episodes` gate and (b) shrinks the resampling unit count.

Constants (measured): `_DEFAULT_GAP_BARS = 48` (`:78`),
`_MIN_N_EPISODES = 8` (`:80`).

**Blast radius (CBM graph, `trace_path` inbound `identify_episodes`, depth 4): four distinct function callers.**
Table convention (shared across all three patch docs): one row per distinct
**function** on the inbound trace — direct callers at hop 1, transitive callers
at the hop the graph first reaches them; a *call-site* line is the line inside
the caller that reaches the next hop. One graph row is a module-level node
(`prescreen_signal`), not a function, and is omitted.

| Caller | Hop | File:line | Records carry `"timestamp"`? |
|---|---|---|---|
| `episode_significance.compute_a851a_significance` | 1 (direct) | `episode_significance.py:244` — `identify_episodes(records, gap_bars=gap_bars, era_of=era_of)` | Yes when called from `run_prescreen` |
| `episode_significance.per_era_report` | 1 (direct) | `episode_significance.py:270` | Yes (same records) |
| `prescreen_signal.run_prescreen` | 2 | `prescreen_signal.py:1476` passes `all_records`; via `compute_a851a_significance` | **Yes** — `all_records` carry `"timestamp"` (`prescreen_signal.py:566`) and `run_prescreen` reads `_records[i]["timestamp"]` at `:1474` for `_era_of` |
| `prescreen_signal.main` | 3 | `prescreen_signal.py:1764`; via `run_prescreen` (call `:1780`) | inherits |

`run_prescreen` builds `all_records` as a **single pooled list across symbols**
and the `_era_of` closure already keys on `(symbol, era_id)` so, *when eras are
configured*, episodes already split at symbol boundaries. When `eras` is empty
(`era_of=None`), nothing closes an episode at a symbol boundary either — a
pre-existing pooled-symbols concern noted below, orthogonal to the gap defect.

`all_records` is one timeframe per prescreen run (block_size derived once), so a
single scalar `expected_step` is valid for every record in the list.

---

## 2. The convention (stated before any number)

**An episode gap is measured in true elapsed bars, not list positions.** Two
consecutive active bars belong to the same episode only when the real number of
bars between them (from their timestamps) is `<= gap_bars` *and* no era break
intervenes. A data hole between them adds its missing bars to the gap, so a hole
large enough pushes the gap past `gap_bars` and splits the episode — which is
the correct behaviour a positional count silently defeats.

The true bar-gap is obtained through the shared helper's notion of segments:

- If `prev` and `curr` fall in the **same** contiguous segment, no hole
  intervenes and `curr - prev - 1` already equals the true bar-gap — behaviour
  unchanged (this is what preserves gap-free bit-identity).
- If they fall in **different** segments, a hole intervenes; the true bar-gap is
  `round((records[curr]["timestamp"] - records[prev]["timestamp"]) / expected_step) - 1`,
  compared against `gap_bars`.

Pre-committed rationale: `n_episodes` is the sample floor the whole A8.5.1a
verdict rests on (`min_n_episodes`, and the bootstrap's resampling unit). A
count inflated by merged episodes is the optimistic direction — more apparent
independent evidence than exists. We correct toward **fewer, honestly-separated**
episodes.

---

## 3. Signature and wiring

- `identify_episodes` gains `expected_step: "pd.Timedelta | None" = None`.
  **Default None ⇒ one segment ⇒ `gap = curr - prev - 1` for every pair ⇒
  byte-identical to today** (helper contract C-H3). This is the bit-identity
  lever. (Note: the parent `PRESCREEN_GAP_POLICY.md` §9.3 discusses a
  single-element `[ic_active]` floor; the real call on `d961a3d7` is
  `episode_significance.py:232-233` — the parent's `es:207`/`ps:1195` line refs
  are stale on this tree, and PR #65 (`8a997ba8`) never touched
  `episode_significance.py`. That floor sits on the dense-fallback branch
  (`:230-242`), which returns before `identify_episodes` (`:244`) is ever
  reached, so it is orthogonal to this patch.)
- `compute_a851a_significance` (`:200`) and `per_era_report` (`:265`) each gain
  `expected_step` and thread it into `identify_episodes`.
- `run_prescreen` (`:1476`) passes the scalar `expected_step` (all records share
  one timeframe).
- Records with no `"timestamp"` while `expected_step` is set: fail loud (helper
  C-H5). All three current callers supply timestamped records, so no caller
  needs the None fallback except by explicit choice.

Estimated size: ~8-12 lines (memo).

---

## 4. Pinning tests to be written

Module: `strategy-research/tests/test_a851a_episode_bootstrap.py` (extend);
integration coverage in `strategy-research/tests/test_a851a_prescreen_integration.py`
(exists — confirmed **3 passed** in the main repo on `d961a3d7`).

- **`test_identify_episodes_none_is_positional`** — with `expected_step=None`,
  episode partitioning is byte-identical to today on a gappy fixture (the
  bit-identity gate).
- **`test_identify_episodes_hole_splits_merged_episode`** — a synthetic list
  where two active bars are 3 recorded-bars apart but a known hole makes the
  true gap exceed `gap_bars`: they split with `expected_step` set, merge without
  it. `n_episodes` differs by exactly one.
- **`test_identify_episodes_same_segment_unchanged`** — two active bars in the
  same contiguous segment partition identically with and without
  `expected_step` (the bit-identity gate).
- **`test_identify_episodes_era_and_gap_compose`** — an era break and a data
  gap on the same pair still produce exactly one split (no double-count).
- **`test_a851a_min_n_episodes_gate_moves_with_gap`** — end-to-end through
  `compute_a851a_significance`: a fixture whose gap-aware `n_episodes` crosses
  `min_n_episodes` selects a different `method` branch than the positional count
  did (drives the wiring, per PR #65's isolation lesson).

Mutation obligation: each must bite — reverting `:107` to the positional
`curr - prev - 1` under a non-None `expected_step` must fail
`test_identify_episodes_hole_splits_merged_episode`.

Existing tests at risk of re-pinning:
`test_a851a_episode_bootstrap.py`, `test_a851a_prescreen_integration.py`,
`test_significance_methodology_pin.py`.

---

## 5. Expected effect on existing artifacts (fork rule 4)

> **Direction corrected — see §8.** The "n_episodes down" claim below is
> backwards; the fix raises n_episodes (or leaves it equal). Text kept verbatim.

- **May change:** `n_episodes`, and through it the A8.5.1a `method` selection
  (`block_*_dense_fallback` vs `episode_bootstrap_*` vs
  `episode_bootstrap_insufficient_n`), `p_value`, `significant`, and CI —
  **on gappy symbols only**. Direction: `n_episodes` down (or equal). Prior
  artifacts on gappy symbols are not retro-corrected.
- **Must NOT change:** any gap-free symbol (one segment ⇒ positional gap ⇒
  identical); the dense-fallback branch (`episode_significance.py:230-242`),
  which returns before `identify_episodes` (`:244`) and so is untouched by this
  patch; every output when `expected_step` is left at the default `None`;
  trial accounting / DSR N (prescreen rows never enter the pool); the backtest
  path.
- **`forecast_hash`:** unchanged — episodes are derived from forecasts, not part
  of the hash input.
- **No lookahead:** the gap is computed from timestamps of bars `prev` and
  `curr` that already exist in the record list; no future value is read — only
  the *distance* between two already-recorded bars.

---

## 6. Kill criteria

> **Third bullet corrected — see §8.** "raises n_episodes ⇒ sign inverted" is
> backwards; the correct kill criterion is n_episodes must never FALL. Kept verbatim.

- If `test_identify_episodes_none_is_positional` fails, the default path is not
  bit-identical — stop and re-derive.
- If a gap-free symbol's `n_episodes` moves, segmentation mis-fires on non-gaps
  — stop.
- If the change ever *raises* `n_episodes` on a gappy symbol (more apparent
  independent samples), the correction sign is inverted — stop; hidden gaps were
  merging, not splitting.
- If threading `expected_step` through `compute_a851a_significance` /
  `per_era_report` demands changes to the record contract or the dense-fallback
  path, scope has crept past the ~8-12-line patch — stop and reconsider against
  D1b.

---

## 7. Out-of-scope note (logged, not fixed here)

When `eras` is empty, `run_prescreen` pools `all_records` across symbols and
nothing closes an episode at a **symbol** boundary — a pooled active bar of
symbol A can merge with the first active bar of symbol B. This is a distinct
issue from the time-gap defect (it is a symbol-boundary defect) and is not
addressed by this patch. Recorded as an observation for triage.

---

## 8. Pre-registration correction (2026-09-03, before any market data)

**§5 and §6 above stated the episode-count direction backwards. This section
corrects it; the original text is left in place per the amendment protocol
(git history keeps it either way).**

**(a) Original wording, verbatim.** §5: *"Direction: `n_episodes` down (or
equal)."* §6: *"If the change ever raises `n_episodes` on a gappy symbol (more
apparent independent samples), the correction sign is inverted — stop; hidden
gaps were merging, not splitting."*

**(b) Mechanism.** For every consecutive active pair, the true elapsed-bar gap
is `positional_gap + missing_hole_bars`, so `true_gap >= positional_gap`
**always**. The split test is `gap > gap_bars`; making every gap larger (or
equal) can only flip a pair from *merge* to *split*, never the reverse. So the
gap-aware split set is a **superset** of the positional one, and `n_episodes` is
**monotonic non-decreasing**: it can only **rise or stay equal**, never fall.
(§1 already says this correctly — positional *merges* → *understates* → the fix
*splits* → *more* episodes. §5/§6 simply contradicted §1.)

**(c) Executed synthetic proof** (`identify_episodes`, 3 active bars, a 10-bar
data hole after index 1, `gap_bars=2`, `expected_step=1h`):

```
positional (expected_step=None): n_episodes = 1   [[0, 1, 2]]
gap-aware  (expected_step=1h):   n_episodes = 2   [[0, 1], [2]]
gap-aware > positional
```

**(d) Corrected direction and kill criterion.** Declared direction: `n_episodes`
**up (or equal)** on a gappy symbol. Kill criterion: **`n_episodes` must never
FALL** on a gappy symbol (the monotonic property); if it ever falls, the sign is
inverted — stop. Pinned by `test_identify_episodes_n_episodes_never_falls_on_gappy`
(randomized gappy fixture) plus the 1→2 split above.

**(e) LOUD flag — this is the LESS conservative direction for the sample-floor
gate.** `_MIN_N_EPISODES = 8` gates the A8.5.1a path on `n_episodes <
min_n_episodes`. More episodes makes it **easier** to clear that floor (a
symbol that would have read "insufficient sample" can now reach the bootstrap).
That is the correct statistical direction — the hole genuinely produces more
*independent* episodes — but it is the direction that admits **more** signals to
significance testing, not fewer, so it must be declared, not buried. This is a
**mechanism correction discovered on synthetic input**, not a threshold moved
after seeing market data: no market data was touched, and the pre-registered
thresholds (`gap_bars=48`, `min_n_episodes=8`) are unchanged.
