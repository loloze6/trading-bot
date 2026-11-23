"""Topic 47: the trades' excursions without the entry bar. The engine's diagnostics (trading-bot/backtest/
run_protocol.py, _compute_mae_mfe over bars[entry_idx : exit_idx + 1]) include the entry bar, whose high and low come
before the entry at its close: look-ahead (2026-11-23: a BTC trade entered at the close 43,410 has MFE 8.42 % from that
bar's high 47,066). Here MAE and MFE are taken over the bars after the entry bar up to the exit bar, from the local
OHLC files. Adds mae_clean, mfe_clean to the trade table.  python3 topics/47_review/clean_excursions.py TRADES.csv.gz"""
import sys, pathlib, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
DATA = pathlib.Path(__file__).resolve().parents[4] / "trading-bot" / "local_data"
path = sys.argv[1]
d = pd.read_csv(path, parse_dates=["entry_time"])


class RangeMax:
    def __init__(self, a, fn):
        self.fn = fn; self.t = [a]
        k = 1
        while 2 * k <= len(a):
            p = self.t[-1]; self.t.append(fn(p[:-k], p[k:])); k *= 2
    def q(self, lo, hi):                      # fn over a[lo..hi] inclusive, arrays of indices
        n = hi - lo + 1; j = np.floor(np.log2(np.maximum(n, 1))).astype(int)
        out = np.empty(len(lo))
        for jj in np.unique(j):
            m = j == jj; t = self.t[jj]
            out[m] = self.fn(t[lo[m]], t[hi[m] - (1 << jj) + 1])
        return out


d["mae_clean"] = np.nan; d["mfe_clean"] = np.nan
for (bar, coin), idx in d.groupby(["bar", "symbol"]).groups.items():
    px = pd.read_csv(DATA / f"kraken_{coin}_{bar}.csv", usecols=["timestamp", "high", "low"], parse_dates=["timestamp"]).drop_duplicates("timestamp").set_index("timestamp").sort_index()
    t = d.loc[idx]
    ei = px.index.get_indexer(t.entry_time)
    hb = t.holding_bars.fillna(1).astype(int).to_numpy()
    lo, hi = ei + 1, ei + np.maximum(hb, 1)                       # the bars after the entry bar, up to the exit bar
    ok = (ei >= 0) & (hi < len(px))
    H, L = RangeMax(px.high.to_numpy(float), np.maximum), RangeMax(px.low.to_numpy(float), np.minimum)
    mx = np.full(len(t), np.nan); mn = np.full(len(t), np.nan)
    mx[ok] = H.q(lo[ok], hi[ok]); mn[ok] = L.q(lo[ok], hi[ok])
    # the entry price: the entry bar's close (the engine fills at it, less a small difference)
    entry = pd.read_csv(DATA / f"kraken_{coin}_{bar}.csv", usecols=["timestamp", "close"], parse_dates=["timestamp"]).drop_duplicates("timestamp").set_index("timestamp").sort_index().close.reindex(t.entry_time).to_numpy(float)
    longs = (t.direction == "long").to_numpy()
    fav = np.where(longs, mx / entry - 1, 1 - mn / entry); adv = np.where(longs, 1 - mn / entry, mx / entry - 1)
    d.loc[idx, "mfe_clean"] = np.clip(100 * fav, 0, None); d.loc[idx, "mae_clean"] = np.clip(100 * adv, 0, None)
d.to_csv(path, index=False, float_format="%.5g")
print("trades with clean excursions:", f"{d.mfe_clean.notna().mean():.1%}")
for bar, x in d.groupby("bar"):
    w, l = x[x.win], x[~x.win]
    print(f"{bar}: engine MFE median {x.mfe.median():.2f} %, clean {x.mfe_clean.median():.2f} % | losers once +1 %: engine {100 * (l.mfe >= 1).mean():.0f} %, clean {100 * (l.mfe_clean >= 1).mean():.0f} %; once +2 %: engine {100 * (l.mfe >= 2).mean():.0f} %, clean {100 * (l.mfe_clean >= 2).mean():.0f} %")
    print(f"     winners first 3 % against: engine {100 * (w.mae >= 3).mean():.0f} %, clean {100 * (w.mae_clean >= 3).mean():.0f} %")
