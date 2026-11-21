def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(c)
            lr = np.log(c)
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30).std().values
            vol90 = r1.rolling(90, min_periods=60).std().values
            mom28 = pd.Series(c).pct_change(28).values
            for h in (5, 10, 20, 40):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=w, wnum=int(w[1:]), h=h, f=f[i],
                                     fwd=c[i + h] / c[i] - 1, mom=mom28[i],
                                     vr=vol30[i] / vol90[i] if vol90[i] == vol90[i] else np.nan,
                                     vol=vol30[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    d["prod"] = d["f"] / 10 * d["ex"]
    d["sex"] = np.sign(d["f"]) * d["ex"]
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["by_horizon"] = d.groupby("h")["prod"].apply(tt).unstack()
    g = d[d.h == 20].copy()
    out["by_coin"] = g.groupby("coin")["prod"].apply(tt).unstack()
    g["year_grp"] = pd.cut(g["wnum"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
    out["by_wingroup"] = g.groupby("year_grp")["prod"].apply(tt).unstack()
    g["side"] = np.where(g.f > 0, "long", np.where(g.f < 0, "short", "flat"))
    out["by_side_signed_excess"] = g.groupby("side")["sex"].apply(tt).unstack()
    g["fq"] = pd.qcut(g["f"].abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_absforecast_q"] = g.groupby("fq")["sex"].apply(tt).unstack()
    g["vq"] = pd.qcut(g["vr"], 3, labels=["calm", "mid", "volatile"])
    out["by_volratio"] = g.groupby("vq")["sex"].apply(tt).unstack()
    g["msign"] = np.sign(g["mom"])
    out["raw_mom_signed_excess_20"] = tt(g["msign"] * g["ex"]).to_frame().T
    out["raw_mom_by_volratio"] = g.assign(m=g.msign * g.ex).groupby("vq")["m"].apply(tt).unstack()
    out["spearman_mom_fwd_20"] = pd.Series(stats.spearmanr(g["mom"], g["ex"], nan_policy="omit"))
    out["corr_f_mom"] = float(g[["f", "mom"]].corr().iloc[0, 1])
    return out
