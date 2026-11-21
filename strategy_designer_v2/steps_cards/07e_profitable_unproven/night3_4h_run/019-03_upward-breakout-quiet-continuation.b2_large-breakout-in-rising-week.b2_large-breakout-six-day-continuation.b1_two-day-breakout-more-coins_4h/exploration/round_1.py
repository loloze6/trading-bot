import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = [6, 12, 36, 72]
    # coin drift per horizon (non-overlapping) and mean bar return
    drift = {}; barmean = {}
    for c in bars:
        d = {}
        allr = []
        for h in H + [1]:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.append(cl[idx + h] / cl[idx] - 1)
            rs = np.concatenate(rs)
            d[h] = (rs.mean(), rs.std())
        drift[c] = d
    cases = []
    coin_rows = []
    win_rows = []
    for c in bars:
        mb = drift[c][1][0]
        tot_gain = 0; mkt = 0; nb = 0
        for w, b in bars[c].items():
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(cl)
            f = b["forecast"].fillna(0).values
            a = b["postRebalance_current_allocation"].fillna(0).values
            r1 = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            g = a * r1
            tot_gain += np.nansum(g[:-1]); mkt += np.sum(a[:-1]) * mb; nb += n - 1
            win_rows.append({"w": w, "gain": np.nansum(g[:-1]), "mkt": np.sum(a[:-1]) * mb, "bars": n - 1})
            ser = pd.Series(hi).shift(1).rolling(12).max().values
            rng = pd.Series(hi - lo).rolling(180, min_periods=45).mean().values
            raw = (cl - ser) / rng
            r7 = pd.Series(cl).pct_change(42).values
            vol30 = pd.Series(r1).shift(1).rolling(180, min_periods=45).std().values
            prevf = np.r_[0, f[:-1]]
            entry = (f > 0) & (prevf <= 0)
            seen = set()
            for t in np.where(entry)[0]:
                cell = t // 36
                if cell in seen: continue
                seen.add(cell)
                row = {"coin": c, "w": w, "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                       "raw": raw[t], "r7": r7[t], "f": f[t], "vol": vol30[t], "hour": pd.Timestamp(b["timestamp"].iloc[t]).hour}
                for h in H:
                    if t + h < n:
                        row["u%d" % h] = cl[t + h] / cl[t] - 1 - drift[c][h][0]
                        row["s%d" % h] = row["u%d" % h] / drift[c][h][1]
                cases.append(row)
        coin_rows.append({"coin": c, "gain_per_bar_bps": 1e4 * tot_gain / nb, "mkt_bps": 1e4 * mkt / nb})
    cs = pd.DataFrame(cases)
    out = {}
    out["coins"] = pd.DataFrame(coin_rows).set_index("coin").round(3)
    wr = pd.DataFrame(win_rows).groupby("w")[["gain", "mkt", "bars"]].sum()
    wr["gain_bps"] = 1e4 * wr.gain / wr.bars; wr["mkt_bps"] = 1e4 * wr.mkt / wr.bars
    out["windows"] = wr[["gain_bps", "mkt_bps"]].round(2)
    out["forecast_at_entry"] = cs["f"].describe().round(2)
    def tab(key, q=5):
        cs2 = cs.dropna(subset=[key])
        cs2 = cs2.assign(b=pd.qcut(cs2[key], q, labels=False, duplicates="drop"))
        res = cs2.groupby("b").agg(n=("u36", "count"), key_med=(key, "median"),
            u6=("u6", "mean"), u12=("u12", "mean"), u36=("u36", "mean"), u72=("u72", "mean"), s36=("s36", "mean"))
        return res.round(4)
    out["by_raw_break"] = tab("raw")
    out["by_r7"] = tab("r7")
    out["by_vol"] = tab("vol")
    out["by_year"] = cs.groupby("year")[["u6", "u36", "u72"]].agg(["mean", "count"]).round(4)
    t = {}
    for h in H:
        x = cs["u%d" % h].dropna(); t[h] = (x.mean(), x.mean() / (x.std() / np.sqrt(len(x))), len(x))
    out["horizons"] = pd.DataFrame(t, index=["mean", "t", "n"]).T.round(4)
    # trades concentration
    tr = pd.concat([d for c in data["trades"] for d in data["trades"][c].values()])
    p = tr["net_profit_loss_percent"].dropna().sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10": p.head(10).sum(), "top5pct": p.head(max(1, len(p)//20)).sum(), "win_share": (p > 0).mean(), "median": p.median()}).round(3)
    return out
