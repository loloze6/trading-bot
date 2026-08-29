"""
P4 daily-panel breadth measurement (task 2 of the P4_ts_trend reactivation
package, operator ruling 2026-08-22).

Read-only. Computes correlation-adjusted effective breadth (n_eff) of the
19-pair Kraken DAILY panel now cached at trading-bot/local_data/kraken_*USD_1d.csv
(landed 2026-08-07, commit 8cff3f24), and separately for the 17-pair
non-BTC/ETH primary universe the parent SMA(100)-daily reactivation rule uses
(BTC/ETH are contaminated for this family -- measured under it on Binance in
runs 053-057; kraken_BTCUSD/kraken_ETHUSD are the same assets on a different
venue, not an untouched sample -- see the pass_rule draft in this directory).

Methodology deliberately mirrors
strategy-research/engineering/sessions/session_reports/_verify_xs_neff.py
(the script that produced the ratified 1h prior: rho_bar=+0.5419, n_eff=1.767
for the same 19-symbol universe on 1h bars) so the two numbers are comparable
apples-to-apples: same symbol set, same formula, same "as-produced" pairwise
-complete Pearson correlation on log returns, same n_eff = n/(1+(n-1)*rho_bar)
A8.6 formula. Only the bar interval (1d vs 1h) and the resulting source files
differ.

Why not power_check.py: that tool computes n_eff_symbols from a SINGLE
pre-supplied rho scalar (campaign_config.yaml's symbol_correlation.
btc_eth_return_correlation_1h, a 2-symbol BTC/ETH constant) -- it has no
facility to compute a pairwise correlation MATRIX over an arbitrary N-symbol
panel from raw price data. Bending it to do so would mean rewriting its core
loop, which is more invasive than a fresh ~80-line script reusing its
n_eff formula (the one piece that does fit).

No holdout data touched: every source file's own last row is 2025-12-31 or
earlier -- entirely before the sealed boundary (campaign_data_policy.yaml's
holdout_range) -- this reads the DAILY caches whose generation script logs
2013-10-06 through end-of-2025, not the sealed local_data/holdout_sealed/
directory, which is never opened here.
"""

import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parents[3] / ".." / "trading-bot" / "local_data"
DATA = DATA.resolve()

# All 19 Kraken USD daily pairs landed 2026-08-07 (commit 8cff3f24).
SYMS_19 = [
    "BTC",
    "ETH",
    "XRP",
    "SOL",
    "ADA",
    "SUI",
    "ZEC",
    "DOGE",
    "XMR",
    "LTC",
    "ONDO",
    "NEAR",
    "LINK",
    "TAO",
    "AVAX",
    "TRX",
    "AAVE",
    "INJ",
    "UNI",
]
# Primary universe for the P4 parent-rule pass_rule: BTC/ETH excluded as an
# ASSET-level contamination (operator ruling) -- measured under this family on
# Binance in runs 053-057; Kraken BTC/ETH are the same assets, different venue.
SYMS_17 = [s for s in SYMS_19 if s not in ("BTC", "ETH")]


def load_close(sym: str) -> pd.Series:
    df = pd.read_csv(DATA / f"kraken_{sym}USD_1d.csv", usecols=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.set_index("timestamp")["close"].sort_index()


def rho_bar(M: pd.DataFrame) -> float:
    n = M.shape[0]
    off = M.values[~np.eye(n, dtype=bool)]
    return float(np.nanmean(off))


def mineig(M: pd.DataFrame) -> float:
    return float(np.linalg.eigvalsh(M.values)[0])


def n_eff(n: int, rb: float) -> float:
    return n / (1 + (n - 1) * rb)


def main():
    closes = {s: load_close(s) for s in SYMS_19}
    idx = sorted(set().union(*[c.index for c in closes.values()]))
    px = pd.DataFrame({s: closes[s].reindex(idx) for s in SYMS_19})
    logret = np.log(px).diff()  # NaN where price missing -- no ffill, no lookahead

    print(f"DATA dir: {DATA}")
    print(f"Union daily index: {len(idx)} rows, {idx[0]} -> {idx[-1]}")
    print()

    print("=== RAW pairwise-complete correlation (as-produced method, matches _verify_xs_neff.py's 1h methodology) ===")
    for name, cols in [("all-19", SYMS_19), ("primary-17-nobtceth", SYMS_17)]:
        M = logret[cols].corr(method="pearson", min_periods=100)
        rb = rho_bar(M)
        me = mineig(M)
        ne = n_eff(len(cols), rb)
        print(f"{name:22s} n={len(cols):2d} rho_bar={rb:+.4f} n_eff={ne:.3f} minEig={me:+.4f} PSD={me >= -1e-8}")

    print()
    print(
        "=== LISTWISE common-window (all-19) correlation, for comparison "
        "(this is what changes if short-history symbols like TAO/ONDO are "
        "allowed to set the window) ==="
    )
    for name, cols in [("all-19", SYMS_19), ("primary-17-nobtceth", SYMS_17)]:
        common = logret[cols].dropna()
        Mlw = common.corr()
        rb = rho_bar(Mlw)
        me = mineig(Mlw)
        ne = n_eff(len(cols), rb)
        print(
            f"{name:22s} rows={len(common):4d} window={common.index.min()} -> "
            f"{common.index.max()}  rho_bar={rb:+.4f} n_eff={ne:.3f} minEig={me:+.4f}"
        )

    print()
    print(
        "=== Per-symbol history length (rows, first date) -- context for the "
        "pairwise-complete vs listwise divergence above ==="
    )
    for s in SYMS_19:
        c = closes[s]
        print(f"  {s:6s} rows={len(c):5d} first={c.index.min().date()} last={c.index.max().date()}")

    print()
    print("=== 1h prior (reference, from _verify_xs_neff.py / ratified XS_momentum findings, NOT recomputed here) ===")
    print("  all-19  1h: rho_bar=+0.5419  n_eff=1.767  (quoted, not measured by this script)")


if __name__ == "__main__":
    main()
