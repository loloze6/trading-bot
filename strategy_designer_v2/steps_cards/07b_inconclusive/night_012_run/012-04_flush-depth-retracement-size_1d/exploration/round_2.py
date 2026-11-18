def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    h = 3
    coin_mean = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - h, h)
            rs.extend(cl[idx + h] / cl[idx] - 1)
        coin_mean[c] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            o, hi, lo, cl, v = [df[k].values.astype(float) for k in ["open", "high", "low", "close", "volume"]]
            r = pd.Series(cl).pct_change()
            z = (r / r.rolling(20).std().shift(1)).values
            vr = v / pd.Series(v).shift(1).rolling(20).median().values
            fc = df["forecast"].values.astype(float); reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"]); n = len(df)
            last = -999
            for t in range(1, n - h):
                if np.isnan(z[t]) or z[t] > -2: continue
                if t - last <= h: continue
                last = t
                rows.append(dict(coin=c, win=w, year=ts.iloc[t].year, z=z[t], ret1=cl[t]/cl[t-1]-1,
                                 drop=(o[t]-lo[t])/o[t], vr=vr[t],
                                 flush=(reg[t]=="mean_reversion" and fc[t]>0), fc=fc[t],
                                 x3=cl[t+h]/cl[t]-1-coin_mean[c]))
    d = pd.DataFrame(rows).dropna(subset=["x3","ret1","z"])
    out = {}
    fl = d[d.flush]
    out["flush_fc_share_at_cap"] = float((fl.fc >= 19.99).mean())
    out["flush_fc_distinct_std"] = float(fl.fc.std())
    def s(g, x):
        if len(g) < 5: return dict(n=len(g))
        lr = stats.linregress(g[x], g.x3)
        return dict(n=len(g), slope_t=lr.slope/lr.stderr, spearman=stats.spearmanr(g[x], g.x3)[0], mean=g.x3.mean())
    for x in ["ret1", "z", "drop"]:
        out[f"all_{x}"] = pd.DataFrame([s(d, x)])
        q = d.x3.quantile([0.01, 0.99]); dt = d[(d.x3 > q.iloc[0]) & (d.x3 < q.iloc[1])]
        out[f"all_{x}_trim"] = pd.DataFrame([s(dt, x)])
    out["ret1_by_coin"] = pd.DataFrame({c: s(g, "ret1") for c, g in d.groupby("coin")}).T
    out["ret1_by_year"] = pd.DataFrame({y: s(g, "ret1") for y, g in d.groupby("year")}).T
    d["q"] = pd.qcut(d.ret1.rank(method="first"), 5, labels=False)
    out["ret1_quintile"] = d.groupby("q").agg(ret1=("ret1","mean"), x3=("x3","mean"), n=("x3","count"))
    out["ret1_flush_vs_not"] = pd.DataFrame({"flush": s(fl, "ret1"), "notflush": s(d[~d.flush], "ret1")}).T
    return out
