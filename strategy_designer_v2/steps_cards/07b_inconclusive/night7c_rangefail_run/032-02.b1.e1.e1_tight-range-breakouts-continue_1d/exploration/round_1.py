import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 20
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = (np.mean(allr), np.std(allr, ddof=1))
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ar = np.abs(pd.Series(c).pct_change()).values
            fc = df["forecast"].values
            reg = df["regime"].values
            raw = df.get("debug_info.components.tight.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            for s in range(0, n, H):
                for i in range(s, min(s + H, n)):
                    if reg[i] == "trending" and fc[i] > 0:
                        if i + H >= n:
                            break
                        r = c[i + H] / c[i] - 1
                        d = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                                 fc=fc[i], raw=raw[i], ret=r, unus=r - drift[coin][0],
                                 strength=(r - drift[coin][0]) / drift[coin][1],
                                 r10=c[i + 10] / c[i] - 1 - drift[coin][0] / 2,
                                 r5=c[i + 5] / c[i] - 1 - drift[coin][0] / 4)
                        if i >= 60:
                            p = c[i - 60:i]
                            d["dist"] = c[i] / p.max() - 1
                            d["rng"] = (p.max() - p.min()) / p.mean()
                            d["mad"] = np.nanmean(ar[i - 59:i + 1])
                            d["W"] = d["rng"] / d["mad"]
                            d["ret60"] = c[i] / c[i - 60] - 1
                        if i >= 20:
                            d["ret20"] = c[i] / c[i - 20] - 1
                        rows.append(d)
                        break
    X = pd.DataFrame(rows)
    out = {}
    out["n_cases"] = len(X)
    def summ(g):
        return pd.Series({"n": len(g), "unus_mean": g.unus.mean(),
                          "t": g.unus.mean() / (g.unus.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "hit": (g.ret > 0).mean(), "unus10": g.r10.mean(), "unus5": g.r5.mean()})
    out["by_coin"] = X.groupby("coin").apply(summ)
    out["by_year"] = X.groupby("year").apply(summ)
    out["by_window"] = X.groupby("w").apply(summ)
    corrs = {}
    for f in ["fc", "raw", "dist", "rng", "W", "ret60", "ret20", "mad"]:
        sub = X[[f, "unus"]].dropna()
        if len(sub) > 10:
            r, p = stats.spearmanr(sub[f], sub["unus"])
            sl = stats.linregress(sub[f], sub["unus"])
            corrs[f] = {"n": len(sub), "spearman": r, "slope_t": sl.slope / sl.stderr}
    out["feature_vs_unus"] = pd.DataFrame(corrs).T
    for f in ["fc", "W", "dist", "ret60", "mad"]:
        sub = X.dropna(subset=[f])
        if len(sub) > 20:
            sub = sub.assign(q=pd.qcut(sub[f].rank(method="first"), 3, labels=["lo", "mid", "hi"]))
            out["tercile_" + f] = sub.groupby("q").apply(summ)
    out["feature_missing_share_W"] = X["W"].isna().mean()
    return out
