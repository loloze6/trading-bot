"""Read-only recomputation of the ratified XS_momentum findings.
No fetcher call; pd.read_csv only. Verifies commit-2 numbers directly."""

import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parents[4] / "trading-bot" / "local_data"
SYMS = [
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
LIQUID12 = [
    "BTC",
    "ETH",
    "XRP",
    "SOL",
    "ADA",
    "ONDO",
    "NEAR",
    "LINK",
    "TAO",
    "AVAX",
    "AAVE",
    "UNI",
]
FLAGGED7 = ["INJ", "DOGE", "ZEC", "SUI", "XMR", "TRX", "LTC"]


def load_close(sym):
    df = pd.read_csv(DATA / f"kraken_{sym}USD_1h.csv", usecols=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df.set_index("timestamp")["close"].sort_index()


closes = {s: load_close(s) for s in SYMS}
# align on union of hourly index
idx = sorted(set().union(*[c.index for c in closes.values()]))
px = pd.DataFrame({s: closes[s].reindex(idx) for s in SYMS})
logret = np.log(px).diff()  # NaN where price missing -> return excluded (no ffill)


def pairwise_corr(cols):
    return logret[cols].corr(method="pearson", min_periods=100)


def mineig(M):
    return float(np.linalg.eigvalsh(M.values)[0])


def rho_bar(M):
    n = M.shape[0]
    off = M.values[~np.eye(n, dtype=bool)]
    return float(np.nanmean(off))


def n_eff(n, rb):
    return n / (1 + (n - 1) * rb)


print("=== RAW pairwise-complete correlation (as-produced method) ===")
for name, cols in [("all-19", SYMS), ("liquid-12", LIQUID12), ("flagged-7", FLAGGED7)]:
    M = pairwise_corr(cols)
    rb = rho_bar(M)
    me = mineig(M)
    print(
        f"{name:10s} n={len(cols):2d} rho_bar={rb:+.4f} n_eff={n_eff(len(cols), rb):.3f} "
        f"minEig={me:+.4f} PSD={me >= -1e-8}"
    )

print("\n=== ALL-19 LISTWISE common window (correction finding 1) ===")
common = logret[SYMS].dropna()
print(
    f"common-window rows={len(common)}  span={common.index.min()} -> {common.index.max()}"
)
Mlw = common.corr()
me = mineig(Mlw)
rb = rho_bar(Mlw)
print(f"all-19 listwise: rho_bar={rb:+.4f} minEig={me:+.4f} PSD={me >= -1e-8}")

print(
    "\n=== DEMEANED (cross-sectionally) correlation, LISTWISE-complete per subset ==="
)


# demean over the subset's members on the common (dropna) window, so the algebraic
# identity holds: ones-vector -> null space => minEig ~ 0, rho_bar near -1/(n-1).
def demeaned_stats_listwise(cols):
    sub = logret[cols].dropna()  # listwise-complete rows for this subset
    dm = sub.sub(sub.mean(axis=1), axis=0)
    M = dm.corr(method="pearson")
    n = len(cols)
    return (
        rho_bar(M),
        mineig(M),
        -1.0 / (n - 1),
        len(sub),
        sub.index.min(),
        sub.index.max(),
    )


for name, cols in [("liquid-12", LIQUID12), ("flagged-7", FLAGGED7)]:
    rb, me, floor, nrows, t0, t1 = demeaned_stats_listwise(cols)
    print(
        f"{name:10s} demeaned rho_bar={rb:+.4f}  floor=-1/(n-1)={floor:+.4f}  "
        f"minEig={me:+.4f}  rows={nrows}  window={t0}->{t1}"
    )

print("\n=== Decorrelation (raw pairwise) internal / cross ===")


def block_mean(rows, cols, exclude_diag):
    M = logret[list(set(rows) | set(cols))].corr(min_periods=100)
    vals = []
    for r in rows:
        for c in cols:
            if exclude_diag and r == c:
                continue
            vals.append(M.loc[r, c])
    return float(np.nanmean(vals))


print(f"liquid-12 internal = {block_mean(LIQUID12, LIQUID12, True):+.4f}")
print(f"flagged-7 internal = {block_mean(FLAGGED7, FLAGGED7, True):+.4f}")
print(f"flagged-7 -> liquid-12 cross = {block_mean(FLAGGED7, LIQUID12, False):+.4f}")

print("\n=== CROSS-SECTION SIZE over time (commit 3 effective start) ===")
avail = px.notna()
# count assets with a valid PRICE per bar; annual snapshot at Jul 1
for yr in range(2013, 2026):
    ts = pd.Timestamp(f"{yr}-07-01 00:00:00")
    if ts in avail.index:
        print(f"{yr}-07-01: {int(avail.loc[ts].sum()):2d} assets present")
# first bar where >= N assets present, for candidate thresholds
count_series = avail.sum(axis=1)
for N in [4, 5, 6, 8, 10, 12]:
    hit = count_series[count_series >= N]
    if len(hit):
        first = hit.index[0]
        bars = int((count_series >= N).sum())
        print(f"first bar with >= {N:2d} assets: {first}  (bars with>=N: {bars})")
