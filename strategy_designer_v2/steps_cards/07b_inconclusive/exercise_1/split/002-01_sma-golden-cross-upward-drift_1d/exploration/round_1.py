def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            raw = b["debug_info.components.sma_cross.last_history_value"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(0, n - 10, 10):
                r = c[i+10]/c[i]-1
                past = c[i]/c[i-30]-1 if i >= 30 else np.nan
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, f=f[i], raw=raw[i], r=r, past30=past))
    d = pd.DataFrame(rows)
    d["ex"] = d["r"] - d.groupby("coin")["r"].transform("mean")
    d["pos"] = d["f"] > 0
    out = {}
    def reg(g):
        if len(g) < 10 or g["f"].std() == 0:
            return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope/s.stderr, npos=g["pos"].sum(),
                              ex_pos=g.loc[g.pos,"ex"].mean(), ex_zero=g.loc[~g.pos,"ex"].mean(), sd_ex=g["ex"].std()))
    out["overall"] = reg(d).to_frame().T
    out["by_coin"] = d.groupby("coin").apply(reg)
    out["by_year"] = d.groupby("year").apply(reg)
    d["fb"] = pd.cut(d["f"], [-0.1, 0, 5, 10, 15, 20.1], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["by_fbucket"] = d.groupby("fb").agg(n=("ex","size"), mean_ex=("ex","mean"), med_ex=("ex","median"),
                                            sd=("ex","std"), hit=("r", lambda x: (x>0).mean()))
    d["rawq"] = pd.qcut(d["raw"], 5, duplicates="drop")
    out["by_raw_spread_q"] = d.groupby("rawq").agg(n=("ex","size"), mean_ex=("ex","mean"), sd=("ex","std"),
                                                    hit=("r", lambda x: (x>0).mean()))
    # raw spread as continuous predictor (both sides)
    s = stats.linregress(d["raw"].fillna(0), d["ex"])
    out["raw_spread_reg"] = pd.Series(dict(slope=s.slope, t=s.slope/s.stderr))
    # condition on past 30d momentum among forecast>0
    dd = d.dropna(subset=["past30"]).copy()
    dd["mom"] = np.where(dd["past30"] > 0, "up30", "down30")
    out["pos_x_mom"] = dd.groupby(["pos","mom"]).agg(n=("ex","size"), mean_ex=("ex","mean"), sd=("ex","std"),
                                                     t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    # fresh cross: forecast>0 now but previous block 0
    d["prevpos"] = d.groupby(["coin","win"])["pos"].shift(1)
    d["fresh"] = d["pos"] & (d["prevpos"] == False)
    out["fresh_vs_old"] = d[d.pos].groupby("fresh").agg(n=("ex","size"), mean_ex=("ex","mean"),
                                                       t=("ex", lambda x: x.mean()/x.std()*np.sqrt(len(x))))
    return out
