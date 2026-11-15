def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.below_ma.last_history_value"
    rows = []
    mus = {}
    for c, ws in bars.items():
        r = []
        for w, df in ws.items():
            r.append((df["close"].shift(-1)/df["close"]-1).dropna())
        mus[c] = pd.concat(r).mean()
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            d = df[col].values if col in df else np.full(len(df), np.nan)
            alloc = df["postRebalance_current_allocation"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # 20-day change of the distance & 60-day past return
            for h in [1, 5, 10, 20, 40]:
                for i in range(0, len(df)-h, h):
                    if np.isnan(d[i]): continue
                    ret = cl[i+h]/cl[i]-1
                    past = cl[i]/cl[i-60]-1 if i >= 60 else np.nan
                    rows.append(dict(coin=c, win=w, year=yr[i], h=h, d=d[i], alloc=alloc[i],
                                     ex=ret-h*mus[c], past60=past))
    R = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g.mean(); s = g.std()
        return pd.Series(dict(n=n, mean=m, t=m/(s/np.sqrt(n)) if n > 1 else np.nan))
    out = {}
    R["below"] = R["d"] < 0
    out["dist_scale"] = R["d"].describe()
    # short gain = -ex when below
    out["by_h_side"] = R.groupby(["h", "below"])["ex"].apply(summ).unstack()
    B = R[R.below].copy()
    B["sg"] = -B["ex"]
    b10 = B[B.h == 10].copy()
    out["h10_by_coin"] = b10.groupby("coin")["sg"].apply(summ).unstack()
    out["h10_by_year"] = b10.groupby("year")["sg"].apply(summ).unstack()
    b10["dq"] = pd.qcut(b10["d"], 5, labels=False)
    out["h10_by_depth_q(0=deepest)"] = b10.groupby("dq").agg(dmean=("d", "mean")).join(b10.groupby("dq")["sg"].apply(summ).unstack())
    b10["pq"] = pd.qcut(b10["past60"], 3, labels=False)
    out["h10_by_past60_tercile"] = b10.groupby("pq")["sg"].apply(summ).unstack()
    for h in [20, 40]:
        bh = B[B.h == h].copy()
        bh["dq"] = pd.qcut(bh["d"], 3, labels=False)
        out[f"h{h}_by_depth_tercile"] = bh.groupby("dq")["sg"].apply(summ).unstack()
    # alloc-weighted gain (as plan) by coin
    b10["prod"] = -b10["alloc"]*b10["ex"]*-1  # alloc negative; gain = alloc*ex
    b10["prod"] = b10["alloc"]*b10["ex"]
    out["h10_plan_prod_by_coin"] = b10.groupby("coin")["prod"].apply(summ).unstack()
    return out
