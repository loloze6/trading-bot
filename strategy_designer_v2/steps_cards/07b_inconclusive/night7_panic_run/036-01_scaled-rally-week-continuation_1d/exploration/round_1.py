def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hs = [1, 3, 7, 14]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std().values
            r3 = pd.Series(c).pct_change(3).values
            r60 = pd.Series(c).pct_change(60).values
            sd = r.rolling(30).std()
            # agitation proxy within window: 30d sd vs its expanding median in window
            agi = (sd > sd.expanding(30).median()).values
            fc = df["forecast"].astype(float).values
            for t in range(0, n, 7):
                d = {"coin": coin, "w": w, "t": t, "fc": fc[t],
                     "z": r3[t] / (sd30[t] * np.sqrt(3)) if sd30[t] and not np.isnan(sd30[t]) else np.nan,
                     "r60": r60[t], "agi": agi[t], "day": t}
                for h in hs:
                    d[f"f{h}"] = c[t + h] / c[t] - 1 if t + h < n else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    # drift per coin, h=7 grid (all grid rows), other h approx scaled
    out = {}
    for h in hs:
        dr = D.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D["coin"].map(dr)
    D["zq"] = pd.qcut(D["z"], 5, labels=False, duplicates="drop")
    g = D.groupby("zq").agg(n=("u7", "count"), zmean=("z", "mean"),
                           u1=("u1", "mean"), u3=("u3", "mean"), u7=("u7", "mean"), u14=("u14", "mean"))
    out["by scaled-3d quintile (all grid bars)"] = g
    def tstat(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    cs = D[D["fc"] > 0]
    out["cases fc>0: n, u-means, t"] = pd.DataFrame({
        "n": [cs[f"u{h}"].count() for h in hs],
        "mean": [cs[f"u{h}"].mean() for h in hs],
        "t": [tstat(cs[f"u{h}"]) for h in hs]}, index=hs)
    out["cases by coin u7"] = cs.groupby("coin")["u7"].agg(["count", "mean", tstat])
    out["cases by window u7"] = cs.groupby("w")["u7"].agg(["count", "mean", tstat])
    cs = cs.copy()
    cs["trend"] = pd.cut(cs["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["cases by trend x agi u7"] = cs.groupby(["trend", "agi"])["u7"].agg(["count", "mean", tstat])
    cs["fq"] = pd.qcut(cs["fc"], 4, labels=False, duplicates="drop")
    out["cases by forecast quartile"] = cs.groupby("fq").agg(n=("u7", "count"), fc=("fc", "mean"),
                                                             u3=("u3", "mean"), u7=("u7", "mean"), u14=("u14", "mean"))
    D["trend"] = pd.cut(D["r60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    out["corr z vs u7 by trend (all grid)"] = D.groupby("trend").apply(
        lambda x: pd.Series({"n": x[["z", "u7"]].dropna().shape[0],
                             "spearman": stats.spearmanr(x["z"], x["u7"], nan_policy="omit")[0]}))
    return out
