def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {h: {} for h in H}
    for coin, wins in bars.items():
        grid = {h: [] for h in H}
        grid_fa = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values; hi = df["high"].values
            n = len(df)
            low30 = pd.Series(lo).rolling(30, min_periods=30).min().shift(1).values
            infa = (df["regime"] != "chop").values
            for h in H:
                for i in range(0, n - h, h):
                    r = c[i + h] / c[i] - 1
                    grid[h].append(r)
                    if infa[i]:
                        grid_fa[h].append(r)
            for i in range(n):
                if np.isnan(low30[i]): continue
                if lo[i] < low30[i] <= c[i]:
                    rng = hi[i] - lo[i]
                    rec = (c[i] - low30[i]) / rng if rng > 0 else np.nan
                    pierce = (low30[i] - lo[i]) / low30[i]
                    d = dict(coin=coin, w=w, i=i, fa=bool(infa[i]), rec=rec, pierce=pierce,
                             day=str(df["timestamp"].iloc[i])[:10],
                             year=str(df["timestamp"].iloc[i])[:4])
                    for h in H:
                        d[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                    rows.append(d)
        for h in H:
            drift[h][coin] = (np.mean(grid[h]), np.mean(grid_fa[h]) if grid_fa[h] else np.nan, np.std(grid[h]))
    ev = pd.DataFrame(rows)
    for h in H:
        ev[f"x{h}"] = ev[f"r{h}"] - ev["coin"].map(lambda k: drift[h][k][0])
        ev[f"s{h}"] = ev[f"x{h}"] / ev["coin"].map(lambda k: drift[h][k][2])
    def summ(g):
        out = {"n": len(g), "days": g["day"].nunique()}
        for h in H:
            x = g[f"x{h}"].dropna()
            out[f"mx{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["str5"] = g["s5"].mean()
        return pd.Series(out)
    res = {}
    res["by_profile"] = ev.groupby("fa").apply(summ)
    res["all"] = summ(ev).to_frame().T
    fa = ev[ev.fa]
    res["fa_by_coin"] = fa.groupby("coin").apply(summ)
    res["fa_by_year"] = fa.groupby("year").apply(summ)
    ev["recq"] = pd.qcut(ev["rec"], 3, labels=["lowrec", "mid", "highrec"])
    res["all_by_rec"] = ev.groupby("recq").apply(summ)
    res["fa_by_rec"] = fa.assign(recq=pd.qcut(fa["rec"], 2, labels=["low", "high"])).groupby("recq").apply(summ)
    ev["pq"] = pd.qcut(ev["pierce"], 3, labels=["shallow", "mid", "deep"])
    res["all_by_pierce"] = ev.groupby("pq").apply(summ)
    res["corr_rec_x5_all"] = float(ev[["rec", "x5"]].dropna().corr().iloc[0, 1])
    res["corr_rec_x5_fa"] = float(fa[["rec", "x5"]].dropna().corr().iloc[0, 1])
    res["drift5"] = pd.DataFrame(drift[5], index=["mean_all", "mean_fa", "sd"]).T
    return res
