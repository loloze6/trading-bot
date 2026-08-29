# Prescreen forward-return continuity — policy pre-registration

**Issue:** #50 (raised by Dorian) · **Status:** proposed, awaiting Jeremy + Dorian sign-off
**Written:** 2026-08-29, BEFORE any implementation, because the remedy changes
every prescreen IC already recorded and therefore cannot be chosen after seeing
the result it produces.

---

## 1. The decision, in one paragraph

`prescreen_signal._extract_forecasts` pairs each bar with the *next row in the
CSV* and calls the difference a one-bar return. It never checks that the next
row is one bar later. The caches contain real holes, so on gappy symbols a
fraction of the "1-bar returns" driving the kill/refine/backtest decision are
actually multi-hour or multi-day returns wearing a one-bar label.

**We adopt: (A) skip the pair across a gap, and (B) make the effective sample
size gap-aware.** We reject re-warmed segmentation and cache repair, and — see
§5 — we drop the per-symbol admission gate that was part of the original
proposal, because measuring it showed it does not bind.

---

## 2. Evidence

All numbers below are reproduced by `tools/cache_gap_census.py`, committed
alongside this document, so they can be re-checked rather than trusted:

```bash
../.venv/bin/python tools/cache_gap_census.py
```

Independently re-derived on this machine before being accepted. Issue #50's
figures reproduce exactly; the census here covers 38 symbol×window
combinations rather than #50's 40, the difference being two `BTCUSDT` rows
whose cache is untracked and absent from this clone.

| symbol (worst) | window | gap pairs | % of pairs | worst gap | median run |
|---|---|---|---|---|---|
| kraken_SUIUSD | train | 549 | **10.93%** | 8 h | **3 bars** |
| kraken_INJUSD | train | 1472 | 7.84% | 15 h | 4 bars |
| kraken_ZECUSD | train | 2100 | 4.22% | **53 h** | 6 bars |
| kraken_DOGEUSD | train | 1314 | 4.02% | 24 h | 2 bars |
| kraken_BTCUSD | train | 12 | 0.02% | 24 h | — |

**36 of 38** combinations contain at least one gap. The split is the headline:
BTC majors are contaminated at 2–5 pairs in 10,000 (noise); SUIUSD-class
symbols at roughly **1 pair in 9** (not noise). This matters now because both
candidate next lanes — funding carry and 19-pair breadth — are multi-symbol by
construction and draw on exactly the altcoin caches where the defect is
material.

Deliberate non-claim, carried over from #50 and confirmed here: this is a
**wrong-horizon** defect, not a magnitude effect. Gap-spanning returns are
comparable to or smaller than contiguous ones (SUIUSD median |ret| 48.5 vs 57.0
bps; ZECUSD 46.0 vs 54.7). The damage is an unlabeled, inconsistent horizon —
not systematically large moves.

---

## 3. The defect has three parts, and they need separating

#50 describes the first. The other two were found while scoping this policy.

**(i) The labelled return is wrong.** `closes[i+1] - closes[i]` across a hole
scores a 53-hour move as one hour. Feeds `ic_all_bars`/`ic_active_bars`, the
bootstrap p-value, the sigma behind the cost hurdle, and hence `_determine_route`.

**(ii) The effective sample size is overstated.**
`_block_adjusted_significance` (`prescreen_signal.py:568`) computes
`n_eff = n_active_bars // block_size` with no gap awareness, so it counts
bootstrap blocks that cannot be placed — a block spanning a hole is the very
defect under discussion. Since `z = IC * sqrt(n_eff - 3)`, an overstated `n_eff`
inflates significance directly:

| symbol | window | nominal n_eff | gap-aware n_eff | z inflated by |
|---|---|---|---|---|
| kraken_SUIUSD | train | 204 | 73 | **1.67×** |
| kraken_INJUSD | train | 777 | 426 | 1.35× |
| kraken_ZECUSD | train | 2070 | 1404 | 1.21× |
| kraken_NEARUSD | train | 547 | 431 | 1.13× |

Real but bounded: ≤1.1× on 33 of 38 combinations. Still, 1.67× is enough to
move a marginal p-value across a threshold, in the direction that makes junk
look significant. Fixing it costs nothing — the run-length structure is already
computed to do (A).

**(iii) The forecast side is contaminated too, and we are not fixing it.** Bars
are fed sequentially into `strategy.update()`, so rolling indicators are
computed straight across a hole. (A) and (B) address the return and the
significance; neither touches this. See §4 for why we accept it.

---

## 4. Options considered

| Option | Verdict |
|---|---|
| **1. Raise on any gap** | **Rejected.** 36/38 combinations are gappy; this breaks nearly every 1h prescreen. |
| **2. Skip the gap-spanning pair** | **ADOPTED as (A).** Minimal and correct for defect (i). |
| **3. Segment + re-warm per segment** | **Rejected.** The only option that fixes defect (iii), and it is unaffordable exactly where it is needed: at the ~120-bar warmup it destroys **91%** of SUIUSD train (median run 3 bars), 78% of INJUSD train, 65% of ZECUSD train. Its *bootstrap* half is salvaged as (B) without the re-warm. |
| **4. Repair the caches upstream** | **Rejected for now.** Cleanest end state but largest scope, requires refetching from Kraken and re-hashing every cache, and would invalidate every data SHA. Reasonable later; not a prerequisite for the next lane. |

**Accepted residual (iii).** Indicator staleness across a hole degrades
smoothly — an EMA spanning an 8-hour hole is a slightly stale EMA — whereas a
mislabeled horizon is a categorical error. Fixing the smooth one costs 91% of
the sample on the symbol that needs it most. We take the categorical fix, and
**disclose the residual in the prescreen artifact** rather than pretending (A)
resolves it.

---

## 5. What we dropped, and why — the admission gate

The original proposal added a per-symbol admission gate refusing a
symbol×timeframe when too little clean contiguous sample survived. To keep it
honest the threshold was derived only from constants that already exist
(`episode_significance._MIN_N_EPISODES = 8`, `block_size = 24`) rather than
chosen after seeing the census.

**Simulated before implementing, it admits 38 of 38 — at both floors.**

> **Corrected 2026-08-29 (Dorian, #50 R2).** This section first reported that
> the ≥30 floor "stops exactly one: SUIUSD train." That number was computed
> under the **re-warm** sample model — option 3's model, the one §4 *rejects* —
> while the policy adopts the no-re-warm model. Under the model actually
> adopted, SUIUSD train has 73 placeable blocks, not 17, and passes both floors.
> Dorian could not reproduce the original claim because he reconstructed it
> against the adopted model; he was right, and the error was ours. The
> simulation now ships in the census tool under **both** models so the
> discrepancy is visible rather than re-derivable only by argument.

| model | floor 8 | floor 30 |
|---|---|---|
| no-re-warm (**adopted**) | admits all 38 | admits all 38 |
| re-warm (rejected, §4) | admits all 38 | stops 1 — SUIUSD train |

Reproduce with `tools/cache_gap_census.py` (see `--gate-floor`).

The correction strengthens the conclusion rather than weakening it: under the
model we actually use, the gate rejects **nothing at either floor**. We are not
raising the floor to make it bite — choosing a threshold because the principled
one failed to reject anything is exactly the threshold-fitting this document
exists to prevent. Per `CLAUDE.fork.md` — *"prefer the cheapest control that
works … do not add guards to guards"* — the gate is dropped.

---

## 6. Specification

**(A) Continuity-checked pairing.** In `_extract_forecasts`, emit a record only
when `timestamp[i+1] - timestamp[i]` equals the timeframe step. Skipped pairs
are counted, never silently dropped, and surfaced in the prescreen artifact as
`gap_skipped_pairs` and `gap_skipped_pct`.

**(B) Gap-aware effective sample size.** `n_eff` becomes the number of blocks
that fit *within* contiguous runs — `sum(records_in_run // block_size)` — rather
than `total // block_size`. No re-warm, no sample loss beyond (A).

**Fail-loud, not flattering.** A symbol whose post-(A) record count is zero
raises, rather than routing on an empty series.

**Off-by-default is NOT appropriate here.** The current behaviour is wrong, not
merely a different option, so this ships on by default — which makes the
declaration below mandatory.

---

## 7. Consequence — this invalidates prior prescreen numbers

Every recorded prescreen IC, p-value, sigma and route on a gappy symbol changes.
Under `CLAUDE.fork.md` rule 4 this is a loud declaration, not a silent
improvement:

- Prior prescreen ICs on gappy symbols are **not comparable** to post-change ones.
- Affected artifacts stay in place; they are not retro-corrected. The graveyard
  is the knowledge.
- run_060's kill stands regardless: it ran on USDT majors (0.00–0.05% gap
  pairs) and died at a cost hurdle of 0.153 against a required 2.0 — three
  orders of magnitude from anything this could move.
- Trial accounting is untouched, confirming #50: prescreen rows are hardcoded
  `statistic_valid="neither"` and never enter the DSR pool. N does not change.
- Backtest-path metrics are untouched. This is prescreen-only.

---

## 8. Related residual — the lexical window filter

Found while reviewing #45. `_load_ohlcv` filters rows to the window with a
**string** comparison performed *before* the parse guard:

```python
ts_date = ts[:10]
if ts_date < start or ts_date >= end:   # lexical
    continue
```

A row with a malformed timestamp sorts unpredictably and is dropped without
ever reaching #45's new counter — verified: `'garbage'`, `''` and `'NaN'` all
skip silently. Same dropped-interior-row consequence #45 exists to prevent.
(A) must parse timestamps anyway, so this is closed in the same change: a row
whose timestamp does not parse is counted and raised on, exactly as #45 treats
an unparseable close.

Also folded in, per #50's closing note: `float("NaN")` and `float("inf")` parse
successfully and would survive #45's guard. Non-finite OHLC values are rejected
by the same check.

---

## 9. Pre-registered acceptance criteria

Fixed before implementation:

1. Bit-identity on a gap-free symbol: a prescreen over `AVAXUSDT`/`SOLUSDT`
   valid (0 gap pairs) is **byte-identical** before and after. If it moves, (A)
   is wrong.
2. `gap_skipped_pairs` equals the census count for that symbol×window exactly.
3. **(revised — Dorian, #50 R1)** Gap-aware `n_eff` is validated against a
   synthetic series with a known gap structure *and* a known active-bar
   pattern, **not** against the census's `gapaware` column. The original
   criterion was unmeetable: the real statistic at `prescreen_signal.py:568` is

   ```python
   n_eff = max(n_active_bars // max(block_size, 1), len(ic_values))
   ```

   — computed over **active** bars (a strategy-dependent subset), whereas the
   census counts **total rows**. The two are only equal when every bar is
   active, so the census column validates (B) *only* in that degenerate case,
   which the test states explicitly rather than assuming.

   On the `len(ic_values)` floor Dorian flags as able to "silently undo (B)":
   confirmed structurally, but measured inert today — both call sites
   (`prescreen_signal.py:1195` and `episode_significance.py:207`) pass
   `[ic_active]`, a **single-element** list, so the floor is at most 1 and can
   bite only when the gap-aware count would be 0. It is a real latent hazard
   for any future caller passing a longer list, so (B) applies gap-awareness to
   the block term **before** the floor is taken, and a test pins that ordering.
4. A synthetic series with one known hole scores the gap-spanning pair as
   skipped, and the surrounding contiguous pairs unchanged.
5. A malformed-timestamp row raises, naming file and count (§8).
6. Both suites green; `trading-bot` unchanged (prescreen is not on its path).

Criteria 2 and 3 are the load-bearing ones: they pin the implementation against
an independent reimplementation of the same quantity, which is how run_060's
`CandleBuilder` bug surfaced.
