import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            vs = pd.Series(df["volume"].values)
            m1 = vs.rolling(30).mean(); m0 = vs.shift(30).rolling(30).mean()
            lvr = np.log(m1 / m0)
            cs = pd.Series(c)
            r30 = cs.pct_change(30); r60 = cs.pct_change(60)
            v5 = np.log(vs.rolling(5).mean() / m1)
            n = len(df)
            for i in range(n):
                f5 = c[i+5]/c[i]-1 if i+5 < n else np.nan
                f10 = c[i+10]/c[i]-1 if i+10 < n else np.nan
                rows.append({"coin": coin, "w": w, "i": i, "inprof": df["regime"].iloc[i] == "unknown",
                             "lvr": lvr.iloc[i], "r30": r30.iloc[i], "r60": r60.iloc[i], "v5": v5.iloc[i],
                             "f5": f5, "f10": f10, "year": pd.Timestamp(df["timestamp"].iloc[i]).year})
    d = pd.DataFrame(rows)
    out = {}
    # drift from grid 5
    g5 = d[d.i % 5 == 0]
    drift5 = g5.groupby("coin")["f5"].mean(); drift10 = d[d.i % 10 == 0].groupby("coin")["f10"].mean()
    d["ex5"] = d["f5"] - d.coin.map(drift5); d["ex10"] = d["f10"] - d.coin.map(drift10)
    p = d[d.inprof & d.lvr.notna() & d.ex5.notna()].copy()
    out["n_inprof_bars_by_coin"] = p.groupby("coin").size()
    res = []
    for off in range(5):
        q = p[p.i % 5 == off]
        s = stats.linregress(q.lvr, q.ex5)
        top = q[q.lvr > q.lvr.quantile(0.8)]
        res.append({"offset": off, "n": len(q), "slope": s.slope, "t": s.slope/s.stderr,
                    "ex_top20_growth": top.ex5.mean(), "n_top": len(top), "ex_rest": q[q.lvr <= q.lvr.quantile(0.8)].ex5.mean()})
    out["grid_offsets_h5"] = pd.DataFrame(res)
    # all bars, quintiles of lvr (overlapping, descriptive)
    p["q"] = pd.qcut(p.lvr, 5, labels=False)
    out["all_bars_lvr_quint"] = p.groupby("q").agg(n=("ex5","size"), lvr=("lvr","mean"), ex5=("ex5","mean"), ex10=("ex10","mean"), down5=("f5", lambda s: (s<0).mean()))
    out["all_bars_lvr_quint_by_coin"] = p.groupby(["coin","q"]).ex5.mean().unstack()
    out["all_bars_lvr_quint_by_year"] = p.groupby(["year","q"]).ex5.mean().unstack()
    # interaction: growth x 30d rise
    p["hiR"] = p.r30 > p.r30.median(); p["hiV"] = p.lvr > p.lvr.median()
    out["growth_x_rise"] = p.groupby(["hiR","hiV"]).agg(n=("ex5","size"), ex5=("ex5","mean"), ex10=("ex10","mean"))
    # product signal on grid offset 0
    q = p[p.i % 5 == 0].copy()
    q["z"] = q.lvr.clip(lower=0) * q.r30.clip(lower=0)
    s = stats.linregress(q.z, q.ex5)
    out["grid0_slope_growth_x_rise"] = pd.Series({"n": len(q), "slope": s.slope, "t": s.slope/s.stderr})
    s = stats.linregress(q.lvr.clip(lower=0), q.ex5)
    out["grid0_slope_growth_pos_only"] = pd.Series({"n": len(q), "slope": s.slope, "t": s.slope/s.stderr})
    # all-bar slope with rough t divided by sqrt(5) for overlap
    s = stats.linregress(p.lvr.clip(lower=0), p.ex5)
    out["allbars_growthpos_slope"] = pd.Series({"n": len(p), "slope": s.slope, "t_naive": s.slope/s.stderr, "t_adj": s.slope/s.stderr/np.sqrt(5)})
    s = stats.linregress(p.v5.fillna(0), p.ex5)
    out["allbars_v5_slope"] = pd.Series({"slope": s.slope, "t_adj": s.slope/s.stderr/np.sqrt(5)})
    return out
