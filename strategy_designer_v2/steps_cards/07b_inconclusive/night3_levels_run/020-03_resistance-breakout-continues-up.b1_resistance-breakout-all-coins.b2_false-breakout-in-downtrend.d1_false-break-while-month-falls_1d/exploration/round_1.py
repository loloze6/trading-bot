def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; base = []
    for coin, ws in bars.items():
        # drift: mean daily return over all windows
        rets = []
        for w, b in ws.items():
            rets.append(b["close"].pct_change().dropna())
        drift = pd.concat(rets).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            r30 = pd.Series(c).pct_change(30).values
            fc = b["forecast"].fillna(0).values
            reg = b["regime"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            seen = set()
            for t in range(n):
                cell = t // 10
                ok = reg[t] == "mean_reversion" and fc[t] <= -2
                if ok and cell not in seen and t + 20 < n + 10:
                    if t + 10 >= n: continue
                    seen.add(cell)
                    d = {"coin": coin, "win": w, "year": yr[t], "r30": r30[t], "fc": fc[t]}
                    for h in [1, 3, 5, 10, 20]:
                        d[f"x{h}"] = (-(c[t+h]/c[t]-1) + drift*h) if t+h < n else np.nan
                    # cut version
                    cut = 10
                    for k in range(1, 11):
                        if not np.isnan(r30[t+k]) and r30[t+k] >= 0:
                            cut = k; break
                    d["xcut"] = -(c[t+cut]/c[t]-1) + drift*cut
                    d["cut"] = cut
                    d["ret5pre"] = c[t]/c[t-5]-1 if t >= 5 else np.nan
                    rows.append(d)
            # baseline grid on all bars with r30<0
            for t in range(0, n-10, 10):
                if not np.isnan(r30[t]) and r30[t] < 0:
                    base.append({"r30": r30[t], "x10": -(c[t+10]/c[t]-1) + drift*10,
                                 "brk": reg[t] == "mean_reversion"})
    df = pd.DataFrame(rows); bs = pd.DataFrame(base)
    def summ(g, col):
        s = g[col].dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "median": s.median(),
                          "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan,
                          "hit": (s > 0).mean()})
    out = {}
    out["horizons"] = pd.DataFrame({h: summ(df, h) for h in ["x1","x3","x5","x10","x20","xcut"]}).T
    out["by_coin"] = df.groupby("coin").apply(lambda g: summ(g, "xcut"))
    out["by_year"] = df.groupby("year").apply(lambda g: summ(g, "xcut"))
    df["depth_q"] = pd.qcut(df["r30"], 3, labels=["deep","mid","shallow"])
    out["by_depth_cut"] = df.groupby("depth_q").apply(lambda g: summ(g, "xcut"))
    out["by_depth_x20"] = df.groupby("depth_q").apply(lambda g: summ(g, "x20"))
    out["depth_r30_range"] = df.groupby("depth_q")["r30"].agg(["min","max","mean"])
    df["pre5_q"] = pd.qcut(df["ret5pre"], 3, labels=["low","mid","high"])
    out["by_pre5"] = df.groupby("pre5_q").apply(lambda g: summ(g, "xcut"))
    out["cut_dist"] = df["cut"].value_counts().sort_index()
    bs["depth_q"] = pd.qcut(bs["r30"], 3, labels=["deep","mid","shallow"])
    out["baseline_neg_month_x10"] = bs.groupby("depth_q").apply(lambda g: summ(g, "x10"))
    out["baseline_all"] = summ(bs, "x10")
    out["spearman_r30_xcut"] = str(stats.spearmanr(df["r30"], df["xcut"]))
    return out
