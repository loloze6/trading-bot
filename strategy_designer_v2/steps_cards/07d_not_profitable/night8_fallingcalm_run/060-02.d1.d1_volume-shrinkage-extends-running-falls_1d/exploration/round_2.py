def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []; pnl = []
    drift = {}
    for c in bars:
        for h in [5, 10]:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs)
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            ret5p = cl / cl.shift(5) - 1
            n = len(b)
            al = b["postRebalance_current_allocation"].fillna(0)
            r1n = cl.shift(-1) / cl - 1
            fc = b["forecast"]
            fcb = pd.cut(fc, [-100, -10, -3, -1e-9, 1e-9, 100], labels=["strong", "mid", "weak", "zero", "pos"])
            # bar gain by forecast bucket at entry of state, and by last5
            p = pd.DataFrame({"g": al * r1n, "fcb": fcb, "last5": np.where(ret5p < 0, "fell5", "rose5"),
                              "inpos": al != 0, "regime": b["regime"], "w": w, "coin": c,
                              "chg": (b["postRebalance_current_allocation"].fillna(0) - b["previous_allocation"].fillna(0)).abs()})
            pnl.append(p)
            for h in [5, 10]:
                for i in range(0, n - h, h):
                    if b["regime"].iat[i] != "trending": continue
                    rows.append(dict(h=h, coin=c, w=w, fc=fc.iat[i], last5="fell5" if ret5p.iat[i] < 0 else "rose5",
                                     yr=pd.Timestamp(b["timestamp"].iat[i]).year,
                                     su=-(cl.iat[i + h] / cl.iat[i] - 1 - drift[(c, h)]),
                                     tot=-(cl.iat[i + h] / cl.iat[i] - 1)))
    g = pd.DataFrame(rows)
    g["strength"] = np.where(g.fc <= -10, "strong", np.where(g.fc < 0, "midweak", "zero"))
    def s(df):
        x = df["su"]; y = df["tot"]
        return pd.Series({"n": len(x), "unusual": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan, "total": y.mean()})
    out["h_strength_last5"] = g.groupby(["h", "strength", "last5"]).apply(s)
    out["strong_by_year_h10"] = g[(g.h == 10) & (g.strength == "strong")].groupby("yr").apply(s)
    out["strong_by_year_h5"] = g[(g.h == 5) & (g.strength == "strong")].groupby("yr").apply(s)
    P = pd.concat(pnl)
    P = P[P.inpos]
    out["bar_gain_by_fcb"] = P.groupby("fcb", observed=True)["g"].agg(["count", "mean", "sum"])
    out["bar_gain_by_fcb_last5"] = P.groupby(["fcb", "last5"], observed=True)["g"].agg(["count", "mean", "sum"])
    out["bar_gain_by_regime"] = P.groupby("regime")["g"].agg(["count", "mean", "sum"])
    out["bar_gain_by_window"] = P.groupby("w")["g"].agg(["count", "mean", "sum"])
    out["turnover_by_fcb"] = P.groupby("fcb", observed=True)["chg"].mean()
    return out
