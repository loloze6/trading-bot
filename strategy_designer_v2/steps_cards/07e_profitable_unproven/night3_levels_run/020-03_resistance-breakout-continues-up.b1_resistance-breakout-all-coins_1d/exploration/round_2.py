def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H = (5, 10, 20)
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values.astype(float); n = len(cl)
            s = pd.Series(cl)
            hi20 = s.rolling(20).max().shift(1).values
            hi60 = s.rolling(60).max().shift(1).values
            r20 = (s / s.shift(20) - 1).values
            vol = s.pct_change().rolling(20).std().values
            f = b["forecast"].fillna(0).values
            brk = np.r_[False, (f[1:] > 0) & (f[:-1] <= 0)]
            for h in H:
                for i in range(0, n - h, h):
                    rows.append({"coin": c, "win": w, "h": h, "i": i,
                                 "fwd": cl[i+h]/cl[i]-1,
                                 "m20": (cl[i]/hi20[i]-1)/vol[i] if not np.isnan(hi20[i]) and vol[i] > 0 else np.nan,
                                 "nh60": (cl[i] > hi60[i]) if not np.isnan(hi60[i]) else np.nan,
                                 "r20": r20[i], "brk": brk[i]})
    G = pd.DataFrame(rows)
    G["drift"] = G.groupby(["coin","h"])["fwd"].transform("mean")
    G["usual"] = G.groupby(["coin","h"])["fwd"].transform("std")
    G["u"] = G["fwd"] - G["drift"]; G["st"] = G["u"]/G["usual"]
    def summ(g):
        u = g["u"].dropna(); t = u.mean()/(u.std()/np.sqrt(len(u))) if len(u) > 2 else np.nan
        return pd.Series({"u": u.mean(), "t": t, "total": g["fwd"].mean(), "strength": g["st"].mean(), "n": len(u)})
    G["nh20"] = G["m20"] > 0
    out["newhigh20_by_h"] = G.dropna(subset=["m20"]).groupby(["h","nh20"]).apply(summ).round(4)
    out["break_x_newhigh20_by_h"] = G.dropna(subset=["m20"]).groupby(["h","brk","nh20"]).apply(summ).round(4)
    pos = G[(G.m20 > -0.5)].copy()
    pos["m20bin"] = pos.groupby("h")["m20"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["margin_above_20d_high_quartiles"] = pos.groupby(["h","m20bin"]).apply(summ).round(4)
    out["newhigh60_by_h"] = G.dropna(subset=["nh60"]).groupby(["h","nh60"]).apply(summ).round(4)
    nh = G[(G.nh20 == True) & (G.h == 10)].copy()
    nh["year_w"] = nh["win"]
    nh["r20pos"] = nh["r20"] > 0
    out["newhigh20_h10_by_r20sign"] = nh.dropna(subset=["r20"]).groupby("r20pos").apply(summ).round(4)
    # by coin count positive for nh20 h10
    bc = nh.groupby("coin")["u"].mean()
    out["newhigh20_h10_coins_positive"] = pd.Series({"pos": (bc > 0).sum(), "n": len(bc)})
    # by window group
    nh["wnum"] = nh["win"].str[1:].astype(int)
    nh["wgrp"] = pd.cut(nh["wnum"], [0,6,12,18,24], labels=["w1-6","w7-12","w13-18","w19-24"])
    out["newhigh20_h10_by_wgrp"] = nh.groupby("wgrp").apply(summ).round(4)
    return out
