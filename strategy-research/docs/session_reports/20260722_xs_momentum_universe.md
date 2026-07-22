# Phase 2 Track A close-out: n_eff measurement and XS_momentum universe selection

**Auditor/measurer:** Claude Opus 4.8 (recon/measurement, read-only)
**Date:** 2026-07-22
**Mode:** READ-ONLY. All 19 Kraken cache CSVs loaded by direct `pd.read_csv` only —
no `CcxtFetcher`/`get_data()` call was made, per the standing write-on-read guard from
commit `446885b`. Cache-file mtimes verified byte-identical before and after this
session (normalized `stat` diff, zero changes). Two config files updated per the
brief's unblock procedure (`coin_universe.yaml`, `campaign_data_policy.yaml`); this
report is the third file. `research_brief_XS_momentum.md`'s `market_universe`
frontmatter and `campaign_queue.yaml`'s `blocked_on_P2` status are **not** touched —
that ratification is the director's, not mine.

---

## 0. Precondition manifest — PASS

```
$ git log --oneline -1
446885b Phase 2 Track A: settle Kraken symbol convention (standard-base) + 15-pair scale-up
$ git status --porcelain
(empty)
```

Brief re-read in full (`strategy-research/briefs/research_brief_XS_momentum.md`) before
starting; its unblock procedure is what "done" means for this dispatch.

---

## 1. Panel shape — all 19 ingested Kraken pairs

Loaded directly (`pd.read_csv`, no fetcher). Sorted by listing date. `within-life
missing %` = missing bars / expected hourly bars over each pair's own observed span.

| sym | rows | first | last | within-life missing % |
|---|---:|---|---|---:|
| BTC | 96,381 | 2013-10-06 21:00 | 2025-12-31 23:00 | 10.14 |
| LTC | 84,563 | 2013-10-24 13:00 | 2025-12-31 23:00 | 20.85 |
| ETH | 87,690 | 2015-08-07 14:00 | 2025-12-31 23:00 | 3.83 |
| ZEC | 76,449 | 2016-10-29 00:00 | 2025-12-31 23:00 | 4.94 |
| XMR | 77,317 | 2017-01-02 19:00 | 2025-12-31 23:00 | 1.94 |
| XRP | 75,440 | 2017-05-18 15:00 | 2025-12-31 23:00 | 0.19 |
| ADA | 63,291 | 2018-09-28 13:00 | 2025-12-31 23:00 | 0.54 |
| LINK | 54,430 | 2019-09-25 14:00 | 2025-12-31 23:00 | 0.94 |
| DOGE | 50,232 | 2019-12-19 18:00 | 2025-12-31 23:00 | 5.05 |
| TRX | 50,331 | 2020-03-05 14:00 | 2025-12-31 23:00 | 1.42 |
| UNI | 45,507 | 2020-10-15 13:00 | 2025-12-31 23:00 | 0.39 |
| AAVE | 44,001 | 2020-12-15 14:00 | 2025-12-31 23:00 | 0.49 |
| SOL | 39,743 | 2021-06-17 15:00 | 2025-12-31 23:00 | 0.15 |
| INJ | 36,298 | 2021-08-10 15:00 | 2025-12-31 23:00 | 5.73 |
| AVAX | 35,285 | 2021-12-21 15:00 | 2025-12-31 23:00 | 0.08 |
| NEAR | 30,775 | 2022-06-16 14:00 | 2025-12-31 23:00 | 0.94 |
| SUI | 22,522 | 2023-05-03 12:00 | 2025-12-31 23:00 | 3.60 |
| ONDO | 15,089 | 2024-04-11 14:00 | 2025-12-31 23:00 | 0.11 |
| TAO | 13,159 | 2024-07-01 00:00 | 2025-12-31 23:00 | 0.13 |

BTC's and LTC's full-history figures (10.14%, 20.85%) are inflated by the 2013–2015
illiquid era (per the 2026-07-22 ingest audit, 97.5% of BTC's gaps sit in 2013–2015);
their 2017-restricted rates are 0.11% and 1.38% respectively, matching ledger G2's
own table exactly — this measurement independently reproduces those figures rather
than trusting them.

**Every pair terminates at exactly 2025-12-31 23:00.** No instrument's archive reaches
into the frozen `holdout_range` (2026-01-01 → 2026-06-30). Recorded as a hard
prerequisite in `campaign_data_policy.yaml` (see §7 below), not merely a footnote.

---

## 2. Ragged-panel correlation method — chosen, justified, and its trap

**Method: pairwise-complete Pearson correlation of 1h log returns.** Each pair `(i,j)`
uses the full intersection of `i`'s and `j`'s own available timestamps — every
instrument's complete listing-to-present history participates in every comparison it's
part of; no instrument is truncated to SUI's 2023-05-03 start.

**Why not listwise-complete:** the dispatch's own framing is correct — restricting to
rows where all 19 pairs have data collapses the window to 2023-05-03 onward, discarding
BTC's, ETH's, LTC's, ZEC's, XMR's, and XRP's entire pre-2023 history. That is not
defensible for a measurement whose whole point is characterizing a decade-plus panel.

**The trap, found and not silently worked around:** the resulting full 19×19 matrix is
**non-positive-semidefinite**:

```
Eigenvalues of the 19x19 pairwise-complete correlation matrix:
  min=-0.222963  max=10.880275
  PSD (min_eig >= -1e-8): False
  1 negative eigenvalue
```

This is one of the dispatch's explicit STOP conditions ("correlation matrix non-PSD
under your chosen method"). Before treating it as a hard stop, I checked whether it was
a single-pair artifact — dropping any one of the 19 symbols and rechecking:

```
drop BTC  -> min_eig=-0.0456  still non-PSD
drop ETH  -> min_eig=-0.0202  still non-PSD
... (all 19 leave-one-out drops remain non-PSD)
```

**No single symbol removal fixes it — this is structural**, not a flaky short-history
pair contaminating the set. The offending eigenvector loads heavily on ETH, BTC, LTC,
AVAX, DOGE, SOL, ZEC, TRX — a mix of very-long-history and very-short-history
instruments compared over highly non-overlapping windows, the classic ragged-panel
pathology: pairwise correlations estimated over different, non-nested time slices are
each individually valid bilateral statistics but need not compose into one internally
consistent 19-dimensional joint structure.

**Resolution, not a workaround:** I checked PSD for the actual decision-relevant
submatrices separately, and both are clean:

```
ALL-19       n=19  min_eig=-0.222963  PSD=False
LIQUID-12    n=12  min_eig=+0.033471  PSD=True
FLAGGED-7    n= 7  min_eig=+0.274530  PSD=True
```

I also tested whether a hand-picked hybrid could route around the problem — adding just
the three best-gap-rate flagged pairs (LTC, TRX, XMR) to liquid-12:

```
liquid-12 + LTC/TRX/XMR (n=15): min_eig=-0.1360  STILL non-PSD
all-19 minus worst-4-gap-rate pairs (DOGE/INJ/ZEC/SUI) (n=15): min_eig=-0.1360  STILL non-PSD
```

Both re-break PSD. **No blend across the liquid-12/flagged-7 boundary that I tested
stays PSD** — the inconsistency is tied to specific long-vs-short-history pairings
(LTC is a repeat offender in the eigenvector loadings), not simply "the flagged-7 are
bad." Under my chosen method, **neither the full-19 single joint matrix nor an
arbitrary hybrid is defensible as one coherent multivariate structure.** The two clean
building blocks are liquid-12 and flagged-7, each individually.

**What this means for the numbers below:** the all-19 row is reported for completeness
per the dispatch's explicit request ("at minimum: all-19..."), but it should be read as
a directional average over 171 individually-valid bilateral correlations, not as
summarizing one coherent 19-asset joint distribution. The liquid-12 and flagged-7 rows
rest on genuinely PSD-valid matrices and are the numbers I'd actually trust for a
decision.

---

## 3. ρ̄ and n_eff_symbols per candidate universe

`n_eff_symbols = n / (1 + (n-1)·ρ̄)` (A8.6). Brief's bar: "materially above ≈1.10."

| universe | n | ρ̄ | n_eff_symbols | PSD |
|---|---:|---:|---:|---|
| **all-19** | 19 | +0.5419 | 1.767 | **NO** (structural, see §2) |
| **liquid-12** | 12 | +0.6165 | 1.542 | yes |
| **flagged-7** | 7 | +0.4386 | 1.928 | yes |

All three clear "materially above 1.10" by a wide margin — this was never in question.
The interesting result is the *ordering*: **flagged-7 alone has the highest n_eff of
the three**, because it is the least internally correlated block (ρ̄=0.44 vs liquid-12's
0.62). That result feeds directly into the trade-off question below.

---

## 4. Decorrelation trade-off — does the flagged-7 carry something the liquid-12 lacks?

Each flagged pair's mean correlation to the liquid-12 block (pairwise-complete, same
method):

| pair | mean corr to liquid-12 | min | max |
|---|---:|---:|---:|
| SUI | +0.5931 | +0.532 | +0.636 |
| LTC | +0.5782 | +0.398 | +0.699 |
| TRX | +0.4848 | +0.321 | +0.576 |
| INJ | +0.5145 | +0.427 | +0.568 |
| DOGE | +0.4988 | +0.346 | +0.671 |
| ZEC | +0.4577 | +0.314 | +0.580 |
| XMR | +0.4366 | +0.225 | +0.564 |

```
liquid-12 intra-block rho_bar        = +0.6165
flagged-7 intra-block rho_bar        = +0.4386
flagged-7 -> liquid-12 cross rho_bar = +0.5091
```

**Answer, with numbers: yes, the flagged-7 carry real decorrelation the liquid-12 core
lacks.** Both of the flagged-7's correlation figures (0.4386 internal, 0.5091 cross to
liquid-12) sit below liquid-12's own internal 0.6165. This is not "more of the same
asset with worse data" — it is measurably lower co-movement, in both directions. A
cross-sectional momentum signal's edge comes specifically from dispersion across
instruments; correlation is the enemy of that dispersion. Excluding the flagged-7
because of their data quality means deliberately keeping the *most* mutually-correlated
12 of the 19 available instruments — the opposite of what the signal wants.

---

## 5. Gap rate → cost input mapping (per Phase 1's cost_model.yaml convention)

**No defensible bps mapping exists without fabricating a new constant, and I am not
inventing one.** Reasoning:

- `cost_model.yaml`'s existing per-symbol `spread_estimate_bps` / `slippage_estimate_bps`
  values are not derived from any formula — they are stated, sourced assumptions
  (Binance's published fee schedule for the fee component; qualitative liquidity
  judgment for spread/slippage, explicitly flagged where unvalidated, e.g. the
  `maker.adverse_selection_bps` block: *"UNVALIDATED ASSUMPTION — no order-book data
  exists to calibrate this"*). There is no existing `gap_rate → bps` conversion
  anywhere in the file to extend, and constructing one (e.g. `spread_bps = base + k ×
  gap_pct`) requires picking `k` with nothing to calibrate it against —
  `config/available_feeds.yaml` already documents that no order-book feed is available,
  which is exactly the data this constant would need.
- Kraken perp's cost block (`cost_model.yaml` `perp:` section) is a single flat tier
  (5 bps taker, no per-symbol breakdown) sourced from Kraken's own published fee
  schedule — again nothing to key a per-pair adjustment off.

**What is defensible, and is what I recorded** (in `campaign_data_policy.yaml`, see
§7): the measured 2017+ within-life missing-% figures, presented as an **ordinal risk
flag** — which pairs warrant a manual conservative markup or a real spread check before
carrying weight in a live signal, not a computed cost number. This mirrors the existing
file's own pattern of separating confirmed values from flagged unvalidated ones rather
than inventing precision that doesn't exist. `INJ` (5.73%) and `DOGE` (5.05%) are the
two pairs I'd flag most strongly for that manual check before either carries real
weight in a backtest.

---

## 6. Config updates made (brief unblock items 2–3)

### `coin_universe.yaml`

- Flipped `data_cached: false → true` for the 7 pre-existing entries now verified:
  SOL, AVAX, UNI, AAVE, LINK, XRP, DOGE.
- Added a new `altcoin_l1_verified_kraken` category for the 10 coins with no prior
  entry: ADA, SUI, ZEC, XMR, LTC, ONDO, NEAR, TAO, TRX, INJ — all `data_cached: true`.
- Every touched/added entry gets `exchange: kraken` + `cache_key: kraken_<BASE>USD_1h`
  and a notes field with row count, verified span, and within-life missing % — flagging
  the file's `default_exchange: binance` header does **not** apply to these entries
  (this file previously only ever recorded Binance-verified data; that convention would
  otherwise mislead a future reader into assuming Binance provenance).
- DOGE, SUI, ZEC, XMR, LTC, TRX, INJ notes explicitly carry the "FLAGGED" marker
  matching §4/§5 above.

### `campaign_data_policy.yaml`

- New `kraken_breadth_19pair` block mirroring the `backward_extension` convention:
  per-pair `availability` date ranges (verified, not assumed), the
  `within_life_missing_pct_2017plus` table, the liquid-12/flagged-7 partition, and the
  `data_manager.py:768` reachability caveat from the 2026-07-22 ingest audit.
- **Holdout treatment, explicitly recorded**: none of the 19 pairs reach into
  `holdout_range`; `holdout_evaluation` for any XS_momentum hypothesis on this
  instrument set is blocked until a live top-up backfills 2026-01-01 → present per
  pair. Walk-forward search is unaffected — the archive's 2025-12-31 cutoff aligns with
  the existing `walk_forward_extension` end date.
- `status: measured_not_walk_forward_eligible` — deliberately not `walk_forward_eligible`
  like the P1b block, since that clearance is the market_universe ratification call,
  not implied by a measurement entry.
- A comment block documenting that `campaign_config.yaml`'s `symbol_correlation` block
  (still BTC/ETH-only, ρ=0.82) is now superseded/insufficient per the brief's own
  framing, with the headline ρ̄/n_eff numbers recorded for whoever ratifies the
  `market_universe` next. `campaign_config.yaml` itself is **not** edited — out of this
  dispatch's two-file write scope, and updating the campaign's canonical
  `symbol_correlation` block for a specific chosen universe is a decision that should
  follow universe ratification, not precede it.

`research_brief_XS_momentum.md` frontmatter and `campaign_queue.yaml`'s
`blocked_on_P2` status: untouched, as instructed.

---

## 7. Recommended universe

**Recommend `liquid-12`** (BTC, ETH, XRP, SOL, ADA, ONDO, NEAR, LINK, TAO, AVAX, AAVE,
UNI) as the universe to ratify into the brief's `market_universe`, with flagged-7 held
as a documented follow-on extension candidate rather than folded in immediately.

**Rationale:**
- Clears the brief's own bar decisively: n_eff=1.542, well above the ≈1.10 floor that
  motivated P2 in the first place.
- Rests on a genuinely PSD correlation matrix — a mathematically coherent 12-instrument
  joint structure, not a directional approximation over an inconsistent one.
- Best aggregate data quality: every member is at or below 0.94% within-life missing
  (2017+), versus flagged-7's 1.4%–5.7% range. For a signal that ranks instruments by
  relative return, a gap in one instrument's series directly corrupts that bar's
  cross-sectional rank — this is a bigger risk for a ranking signal specifically than
  for a single-instrument strategy, where a gap just means a skipped bar.
- No hybrid blend I tested (liquid-12 + best-3-of-flagged-7) recovers PSD, so there is
  no clean "best of both" middle ground available under this method — it's liquid-12
  clean, or a broader set that carries the acknowledged non-PSD caveat.

**Single strongest counterargument:** §4's numbers cut directly against this
recommendation. Flagged-7 is the *least* correlated block available (ρ̄=0.44 internal,
0.51 cross to liquid-12, both below liquid-12's own 0.62 internal figure) — meaning
liquid-12 is, by construction, the *most mutually redundant* 12 of the 19 verified
instruments. A cross-sectional momentum test is explicitly a test of whether ranking
across dispersion produces edge; deliberately excluding the instruments carrying the
most dispersion because their price series have more gaps could bias the eventual test
toward finding no edge even where one exists — the exclusion criterion (data
completeness) is not orthogonal to the phenomenon being tested (return dispersion). If
that concern outweighs the data-quality risk, the honest alternative is all-19 with the
non-PSD caveat carried forward explicitly into the eventual `symbol_correlation` record,
or a targeted per-pair sanity check (§5) on INJ/DOGE specifically to see if their gap
rate reflects genuine illiquidity risk or is otherwise tolerable, before deciding
whether to admit the full flagged-7 rather than defaulting them out.

---
---

# DIRECTOR CORRECTION (ratified 2026-07-22) — layered on top; original text above is preserved verbatim

Everything above §0–§7 is the measurement session's **as-produced** output and is left
unedited on purpose. This appendix records what the director overturned, why, and on
what evidence. Where a §-numbered conclusion above conflicts with a finding here, **this
appendix governs.** All four findings below were established by direct recomputation on
the same ingested Kraken CSVs (`_verify_xs_neff.py`, this directory; read-only,
`pd.read_csv` only, no fetcher).

## Recomputation, independently reproduced

| quantity | as-produced (§) | ratified recompute | agree? |
|---|---|---|---|
| all-19 pairwise-complete minEig | −0.2230 (§2, "non-PSD, structural") | −0.0545 | non-PSD *under this estimator*, yes |
| **all-19 LISTWISE common-window minEig** | not computed | **+0.1575 → PSD** | overturns "structural" |
| liquid-12 raw ρ̄ / flagged-7 raw ρ̄ | +0.6165 / +0.4386 (§3) | +0.6193 / +0.4558 | yes (method-noise) |
| liquid-12 demeaned ρ̄ (listwise) | not computed | **−0.0800** (floor −0.0909, minEig 0.0000) | new |
| flagged-7 demeaned ρ̄ (listwise) | not computed | **−0.1588** (floor −0.1667, minEig 0.0000) | new |

## Finding 1 — the non-PSD result is an ESTIMATOR ARTIFACT, not structural. §2 RETRACTED.

§2 concluded the all-19 matrix is non-PSD "structurally" because leave-one-out never
recovered PSD. That conclusion is retracted. The all-19 correlation matrix computed on a
**listwise common window** (every bar where all 19 pairs are present, 2024-07-01 →
2025-12-31, 12,966 rows) has **minEig = +0.1575 — PSD.** Pairwise-deletion on ragged
windows is a *known* generator of non-PSD matrices: each bilateral correlation is
estimated over a different, non-nested time slice, so the 171 valid pairwise statistics
need not compose into one PSD 19×19 object. The leave-one-out test in §2 could not have
detected this, because **every one of its 19 subsets was still estimated by
pairwise-deletion** — it varied the asset set but never the estimator, so it could only
ever find "still non-PSD." The §2 claim "No blend across the liquid-12/flagged-7 boundary
stays PSD" (and §7's reliance on it) is likewise retracted: it too is an artifact of the
estimator, not a property of the asset set.

## Finding 2 — raw n_eff is NOT the decision statistic for a dollar-neutral book.

§3 quotes raw `n_eff_symbols` per universe against the brief's ≈1.10 bar. For a
**dollar-neutral long/short** cross-sectional book this is the wrong statistic. Raw ρ̄ /
raw n_eff measure **directional (market-factor) concentration** — precisely the component
a dollar-neutral long-top/short-bottom book does *not* hold, because the common factor
cancels in the long−short spread. The brief's ≈1.10 blocker was sound **for n=2**, where
the cross-section is degenerate and there is nothing but the common factor. Carrying that
same raw-n_eff bar to n=12 or n=19 misapplies it: it measures the exposure the strategy
is constructed to cancel. This does not retract §3's arithmetic (the raw figures are
fine); it retracts using them as the go/no-go breadth statistic.

## Finding 3 — demeaned ρ̄ sits at the orthogonality floor: real idiosyncratic dispersion exists.

The decision-relevant statistic is the correlation of **cross-sectionally demeaned**
returns (each bar's cross-sectional mean subtracted — the neutral book's actual
exposure). Measured listwise per subset:

```
liquid-12  demeaned rho_bar = -0.0800   floor -1/(n-1) = -0.0909   minEig = 0.0000
flagged-7  demeaned rho_bar = -0.1588   floor -1/(n-1) = -0.1667   minEig = 0.0000
```

Both sit **just above the orthogonality floor** −1/(n−1): once the common factor is
removed, the residuals are close to mutually orthogonal — i.e. genuine idiosyncratic
dispersion exists to rank on. This is the affirmative breadth result the brief's power
check actually needed.

Two guardrails, ratified:
- **Do NOT quote a demeaned n_eff.** As ρ̄ → −1/(n−1) the denominator `1+(n−1)ρ̄` → 0 and
  n_eff explodes to meaningless values (100–149). Cross-sectional breadth is properly
  read as ≈ **n−1 rank bets, conditional on dollar-neutrality**, not as an n_eff figure.
- **minEig = 0 on the demeaned matrices is EXPECTED, not a defect.** Demeaning puts the
  ones-vector in the null space by construction; a zero eigenvalue is the signature that
  the demeaning was done correctly, not a non-PSD failure.

## Finding 4 — ratified universe: ALL 19 ingested Kraken pairs. §7's liquid-12 recommendation OVERTURNED.

§7 recommended liquid-12 and defaulted the flagged-7 out on gap rate. Overturned. The
ratified `market_universe` is **all 19 ingested Kraken pairs.** §4's own numbers (which
§7 flagged as its single strongest counterargument) are decisive here and are confirmed
on recompute: the flagged-7 carry **real decorrelation** — 0.456 internal / 0.519 cross
to the liquid core, versus 0.619 within the core. Excluding them on gap rate would strip
out exactly the return dispersion a cross-sectional signal exists to detect; the exclusion
criterion (data completeness) is not orthogonal to the phenomenon under test (dispersion).
The gap rate remains a legitimate **ordinal risk flag** (§5's refusal to fabricate a
gap-rate → bps mapping stands and is *not* overturned) — but an ordinal flag is not
grounds to drop instruments from the ranked set. INJ/DOGE stay in, flagged.

## Net effect on the brief

`market_universe` = the 19. Raw and demeaned ρ̄ recorded in the brief frontmatter. Queue
status flipped `blocked_on_P2 → ready`. The run's effective start is determined
empirically in the follow-on run commit (cross-section-size curve → minimum-viable-n
threshold), not assumed here.
