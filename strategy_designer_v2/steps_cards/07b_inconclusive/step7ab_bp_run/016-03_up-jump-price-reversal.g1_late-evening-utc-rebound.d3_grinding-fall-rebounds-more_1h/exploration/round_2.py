def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [24, 48, 96, 168]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            hr = np.full(n, np.nan); hr[1:] = c[1:] / c[:-1] - 1
            loss = np.where(hr < 0, -hr, 0.0)
            L = pd.Series(loss)
            sumL = L.rolling(24).sum().values
            maxL = L.rolling(24).max().values
            S = 1 - maxL / np.where(sumL > 0, sumL, np.nan)
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            vol24 = pd.Series(hr).rolling(24).std().values
            vol720 = pd.Series(hr).rolling(720, min_periods=200).std().values
            for i in range(0, n, 48):
                d = {"coin": coin, "f": f[i], "S": S[i], "r24": r24[i], "v24": vol24[i], "v720": vol720[i]}
                for h in H:
                    d["fw%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    for h in H:
        g["ex%d" % h] = g["fw%d" % h] - g.groupby("coin")["fw%d" % h].transform("mean")
    pos = g[(g.r24 < 0)].dropna(subset=["S", "v24", "ex48"]).copy()
    pos["depth"] = -pos.r24 / (pos.v24 * np.sqrt(24))
    def st(s, x, y):
        s = s[[x, y]].dropna()
        r = stats.linregress(s[x], s[y]); return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    out["pos_rawS_by_h"] = pd.DataFrame({h: st(pos, "S", "ex%d" % h) for h in H}).T
    out["pos_f_by_h"] = pd.DataFrame({h: st(pos[pos.f > 0], "f", "ex%d" % h) for h in H}).T
    out["pos_depth_by_h"] = pd.DataFrame({h: st(pos, "depth", "ex%d" % h) for h in H}).T
    pos["dq"] = pd.qcut(pos.depth, 3, labels=["shallow", "mid", "deep"])
    pos["Sh"] = pos.S > pos.groupby("dq")["S"].transform("median")
    res = {}
    for dq, s in pos.groupby("dq"):
        for h in [48, 168]:
            a = s[s.Sh]["ex%d" % h].dropna(); b = s[~s.Sh]["ex%d" % h].dropna()
            res[(dq, h)] = {"grind": a.mean(), "jump": b.mean(), "diff": a.mean() - b.mean(), "t": stats.ttest_ind(a, b, equal_var=False).statistic, "n": len(a) + len(b)}
    out["grind_minus_jump_by_depth"] = pd.DataFrame(res).T
    pos["dq5"] = pd.qcut(pos.depth, 5, labels=False)
    out["depth_quint"] = pos.groupby("dq5").agg(n=("ex48", "size"), depth=("depth", "mean"), S=("S", "mean"), ex24=("ex24", "mean"), ex48=("ex48", "mean"), ex168=("ex168", "mean"))
    pos["Sq"] = pd.qcut(pos.S, 5, labels=False)
    out["rawS_quint"] = pos.groupby("Sq").agg(n=("ex48", "size"), S=("S", "mean"), depth=("depth", "mean"), ex24=("ex24", "mean"), ex48=("ex48", "mean"), ex168=("ex168", "mean"))
    out["corr_f_S"] = float(pos[pos.f > 0][["f", "S"]].corr().iloc[0, 1])
    pos["volreg"] = np.where(pos.v24 > pos.v720, "hotter", "calmer")
    out["S_by_volreg"] = pos.groupby("volreg").apply(lambda s: st(s, "S", "ex48"))
    return out
