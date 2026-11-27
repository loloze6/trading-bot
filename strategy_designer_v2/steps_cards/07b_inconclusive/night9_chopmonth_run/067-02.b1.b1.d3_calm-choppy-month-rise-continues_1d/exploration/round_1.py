def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [3, 7, 14]
    # coin mean per horizon over all windows
    for coin, wins in bars.items():
        cm = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            cm[h] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 7):
                if df["regime"].iloc[i] != "unknown":
                    continue
                f = df["forecast"].iloc[i]
                if pd.isna(f) or f == 0:
                    continue
                r30 = c[i] / c[i - 30] - 1 if i >= 30 else np.nan
                rec = dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                           f=f, r30=r30)
                for h in H:
                    rec[f"x{h}"] = (c[i + h] / c[i] - 1 - cm[h]) if i + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def slope(g, y="x7", x="f"):
        g = g.dropna(subset=[x, y])
        if len(g) < 10: return pd.Series(dict(n=len(g)))
        s = stats.linregress(g[x], g[y])
        sig = np.sign(g[x])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              long_mean=g.loc[sig > 0, y].mean(), n_long=(sig > 0).sum(),
                              short_mean=g.loc[sig < 0, y].mean(), n_short=(sig < 0).sum(),
                              signed_mean=(sig * g[y]).mean()))
    out["all_h"] = pd.DataFrame({h: slope(d, f"x{h}") for h in H}).T
    out["all_h_raw30"] = pd.DataFrame({h: slope(d, f"x{h}", "r30") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(lambda g: slope(g))
    out["by_window"] = d.groupby("w").apply(lambda g: slope(g))
    out["by_year"] = d.groupby("year").apply(lambda g: slope(g))
    d["fq"] = pd.qcut(d["f"], 6, duplicates="drop")
    out["by_fq"] = d.groupby("fq")[["x3", "x7", "x14"]].agg(["mean", "count"])
    d["rq"] = pd.qcut(d["r30"], 6, duplicates="drop")
    out["by_r30q"] = d.groupby("rq")[["x7", "x14"]].agg(["mean", "count"])
    out["corr_f_r30"] = d[["f", "r30"]].corr().iloc[0, 1]
    return out
