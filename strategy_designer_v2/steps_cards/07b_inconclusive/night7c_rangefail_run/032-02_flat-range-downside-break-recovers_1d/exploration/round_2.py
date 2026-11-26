def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 2 else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            ch = (c - c.shift(60)).abs()
            vol = c.diff().abs().rolling(60).sum()
            er = (ch / vol).rolling(5).mean()
            plow = df["low"].shift(1).rolling(60).min()
            phigh = df["high"].shift(1).rolling(60).max()
            dlow = c / plow - 1
            dhigh = c / phigh - 1
            r20 = c / c.shift(20) - 1
            r5 = c / c.shift(5) - 1
            vr = df["volume"] / df["volume"].shift(1).rolling(20).mean()
            for h in H:
                for side, cond, dep in [("down", dlow < 0, -dlow), ("up", dhigh > 0, dhigh)]:
                    cells = {}
                    for i in np.where(cond.fillna(False).values)[0]:
                        cell = i // h
                        if cell in cells or i + h >= len(c):
                            continue
                        cells[cell] = i
                    for cell, i in cells.items():
                        r = c.iloc[i + h] / c.iloc[i] - 1
                        sgn = 1 if side == "up" else 1
                        rows.append(dict(coin=coin, w=w, h=h, side=side, day=str(df["timestamp"].iloc[i])[:10],
                                         ex=r - drift[(coin, h)], tot=r, st=(r - drift[(coin, h)]) / usual[(coin, h)],
                                         er=er.iloc[i], dep=dep.iloc[i], r20=r20.iloc[i], r5=r5.iloc[i], vr=vr.iloc[i],
                                         year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)

    def tclus(g):
        dev = g.groupby("day")["ex"].apply(lambda x: (x - g["ex"].mean()).sum())
        G = len(dev)
        if G < 3: return np.nan
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(g)
        return g["ex"].mean() / se

    def summ(g):
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean_ex=g["ex"].mean(), t=tclus(g),
                              strength=g["st"].mean(), mean_tot=g["tot"].mean(), hit=(g["tot"] > 0).mean()))

    out = {}
    flat = R[R.er <= 0.3]
    out["flat_by_side_h"] = flat.groupby(["side", "h"]).apply(summ)
    u = flat[flat.side == "up"].copy()
    for h in [5, 10, 20]:
        g = u[u.h == h].copy()
        g["dq"] = pd.qcut(g["dep"], 3, labels=["small", "mid", "large"], duplicates="drop")
        out[f"flat_up_{h}_by_dist"] = g.groupby("dq").apply(summ)
        sl = stats.linregress(g["dep"], g["ex"])
        out[f"flat_up_{h}_slope_ex_on_dist"] = f"slope {sl.slope:.3f} t {sl.slope/sl.stderr:.2f} n {len(g)}"
    g = u[u.h == 10]
    out["flat_up_10_by_year"] = g.groupby("year").apply(summ)
    out["flat_up_10_by_coin"] = g.groupby("coin").apply(summ)
    allu = R[(R.side == "up") & (R.h == 10)]
    out["all_up_10_by_year"] = allu.groupby("year").apply(summ)
    d = flat[(flat.side == "down") & (flat.h == 10)].copy()
    d["r20q"] = pd.qcut(d["r20"], 3, labels=["fell", "mid", "rose"], duplicates="drop")
    out["flat_down_10_by_r20"] = d.groupby("r20q").apply(summ)
    d["vrq"] = pd.qcut(d["vr"], 2, labels=["lowvol", "highvol"], duplicates="drop")
    out["flat_down_10_by_volratio"] = d.groupby("vrq").apply(summ)
    d1 = flat[(flat.side == "down") & (flat.h == 1)].copy()
    d1["dq"] = pd.qcut(d1["dep"], 3, labels=["small", "mid", "large"], duplicates="drop")
    out["flat_down_1_by_dist"] = d1.groupby("dq").apply(summ)
    return out
