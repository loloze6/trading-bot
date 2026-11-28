import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    coinmean = {}
    for coin, wins in bars.items():
        allg = {h: [] for h in (1, 3, 5, 10)}
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std().shift(1)
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            f["prof"] = (b["regime"] != "chop").values
            f["r1z"] = (r / sd30).values
            f["r3z"] = (c.pct_change(3) / (sd30 * np.sqrt(3))).values
            f["r10z"] = (c.pct_change(10) / (sd30 * np.sqrt(10))).values
            f["clv"] = ((c - lo) / (hi - lo).replace(0, np.nan)).values
            f["rangez"] = (((hi - lo) / c.shift(1)) / sd30).values
            f["dhigh20z"] = ((c / hi.rolling(20, min_periods=10).max() - 1) / sd30).values
            f["volr"] = (v / v.rolling(20, min_periods=10).mean().shift(1)).values
            f["sd30"] = sd30.values
            dn = (r < 0).astype(int); up = (r > 0).astype(int)
            rd = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            ru = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            f["runsign"] = (ru - rd).values
            f["wd"] = pd.to_datetime(b["timestamp"]).dt.weekday.values
            f["alloc"] = b["postRebalance_current_allocation"].astype(float).values
            for h in (1, 3, 5, 10):
                fr = c.shift(-h) / c - 1
                f[f"fr{h}"] = fr.values
                g = fr.iloc[::h].dropna()
                allg[h] += list(g.values)
            rows.append(f)
        coinmean[coin] = {h: np.mean(allg[h]) for h in allg}
    F = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 5, 10):
        F[f"ex{h}"] = F[f"fr{h}"] - F["coin"].map(lambda k: coinmean[k][h])
    P = F[F["prof"]]
    out = {}
    out["profile share of bars by coin"] = F.groupby("coin")["prof"].mean()
    feats = ["r1z", "r3z", "r10z", "clv", "rangez", "dhigh20z", "volr", "sd30", "runsign"]
    summ = []
    for h in (1, 5, 10):
        G = P[P["pos"] % h == 0]
        for ft in feats:
            d = G[[ft, f"ex{h}"]].dropna()
            if len(d) < 30: continue
            sl = stats.linregress(d[ft], d[f"ex{h}"])
            q = pd.qcut(d[ft].rank(method="first"), 5, labels=False)
            m = d.groupby(q)[f"ex{h}"].mean()
            summ.append({"h": h, "feat": ft, "n": len(d), "slope_t": sl.slope / sl.stderr,
                         "q1": m.iloc[0], "q3": m.iloc[2], "q5": m.iloc[4],
                         "q5_t": stats.ttest_1samp(d[f"ex{h}"][q == 4], 0).statistic,
                         "q1_t": stats.ttest_1samp(d[f"ex{h}"][q == 0], 0).statistic})
    out["profile features vs forward excess"] = pd.DataFrame(summ).round(4)
    G5 = P[P["pos"] % 5 == 0]
    out["profile all grid ex5"] = pd.Series({"n": G5["ex5"].count(), "mean": G5["ex5"].mean(),
                                             "t": stats.ttest_1samp(G5["ex5"].dropna(), 0).statistic})
    G1 = P.dropna(subset=["ex1"])
    out["weekday ex1 in profile"] = G1.groupby("wd")["ex1"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["runsign ex5 in profile"] = G5.groupby(G5["runsign"].clip(-4, 4))["ex5"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["coin ex5 in profile"] = G5.groupby("coin")["ex5"].agg(["count", "mean"])
    out["window-year-ish ex5"] = G5.groupby("win")["ex5"].agg(["count", "mean"])
    return out
