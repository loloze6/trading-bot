def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            vol30 = r1.rolling(30).std().values
            vol90 = r1.rolling(90, min_periods=60).std().values
            mom28 = pd.Series(c).pct_change(28).values
            mom7 = pd.Series(c).pct_change(7).values
            for h in (3, 5, 10, 15, 20):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, wnum=int(w[1:]), h=h, f=f[i],
                                     fwd=c[i + h] / c[i] - 1, mom=mom28[i], mom7=mom7[i],
                                     vr=vol30[i] / vol90[i] if vol90[i] == vol90[i] else np.nan))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["usual"] = d.groupby(["coin", "h"])["fwd"].transform("std")
    d["ex"] = d["fwd"] - d["drift"]
    d["prod"] = d["f"] / 10 * d["ex"]
    d["s"] = np.sign(d["f"])
    d["sex"] = d.s * d.ex
    d["stot"] = d.s * d.fwd
    d["str"] = d.sex / d.usual
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    a = d[d.f != 0]
    out["size_by_h"] = a.groupby("h").agg(n=("sex", "size"), unusual=("sex", "mean"), total=("stot", "mean"), strength=("str", "mean"), usual=("usual", "mean"))
    out["prod_t_by_h"] = d.groupby("h")["prod"].apply(tt).unstack()
    out["raw_mom28_sign_by_h"] = d.assign(m=np.sign(d.mom) * d.ex).groupby("h")["m"].apply(tt).unstack()
    for h in (5, 10):
        g = d[d.h == h].copy()
        g["grp"] = pd.cut(g["wnum"], [0, 6, 12, 18, 24], labels=["w1-6", "w7-12", "w13-18", "w19-24"])
        out[f"h{h}_by_wingroup"] = g.groupby("grp")["prod"].apply(tt).unstack()
        out[f"h{h}_by_coin"] = g.groupby("coin")["prod"].apply(tt).unstack()
        g["side"] = np.where(g.f > 0, "long", np.where(g.f < 0, "short", "flat"))
        out[f"h{h}_side_sex"] = g.groupby("side")["sex"].apply(tt).unstack()
        g["fq"] = pd.qcut(g["f"].abs().rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
        out[f"h{h}_absf_q_sex"] = g.groupby("fq")["sex"].apply(tt).unstack()
        gv = g.dropna(subset=["vr"]).copy()
        gv["vq"] = pd.qcut(gv["vr"], 3, labels=["calm", "mid", "volatile"])
        out[f"h{h}_volratio_prod"] = gv.groupby("vq")["prod"].apply(tt).unstack()
    return out
