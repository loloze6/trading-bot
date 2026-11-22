import numpy as np, pandas as pd

def explore(data):
    out = {}
    # trades: gross vs net
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t):
                d = t[["profit_loss_percent","net_profit_loss_percent","duration_minutes"]].copy()
                d["coin"] = c
                tr.append(d)
    tr = pd.concat(tr)
    out["trades_by_coin"] = tr.groupby("coin").agg(n=("profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"),
        dur_h=("duration_minutes", lambda x: x.mean()/60))
    # book daily by coin
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            x = d[["book_return","coin_return"]].copy(); x["coin"] = c; dd.append(x)
    dd = pd.concat(dd)
    out["book_daily_by_coin"] = dd.groupby("coin").agg(book=("book_return","mean"), coin=("coin_return","mean"))
    # event study: z-scored hourly rise, by volume ratio and horizon
    H = [2, 6, 12, 24]
    recs = []
    drift = {h: [] for h in H}
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].astype(float).reset_index(drop=True)
            v = b["volume"].astype(float).reset_index(drop=True)
            r1 = cl.pct_change()
            ma = r1.abs().rolling(720, min_periods=240).mean()
            z = r1 / ma
            vr = v / v.rolling(720, min_periods=240).mean()
            for h in H:
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(cl), h)
                g = pd.DataFrame({"z": z.iloc[idx].values, "vr": vr.iloc[idx].values,
                                  "f": fwd.iloc[idx].values})
                g["coin"] = c; g["h"] = h
                drift[h].append(g["f"].dropna())
                recs.append(g)
    E = pd.concat(recs).dropna()
    dr = {h: pd.concat(drift[h]).mean() for h in H}
    sd = {h: pd.concat(drift[h]).std() for h in H}
    E["ex_short"] = -(E["f"] - E["h"].map(dr))
    E["zb"] = pd.cut(E["z"], [1, 2, 3, 4, 6, 100])
    E["vb"] = pd.cut(E["vr"], [0, 0.8, 1.25, 2, 4, 1000])
    up = E[E["z"] > 1]
    def summ(g):
        m = g["ex_short"].mean(); s = g["ex_short"].std(); n = len(g)
        return pd.Series({"n": n, "mean_pct": 100*m, "t": m/(s/np.sqrt(n)) if n > 2 else np.nan})
    out["quietvol_by_z_h"] = up[up["vb"].astype(str) == "(0.8, 1.25]"].groupby(["h","zb"], observed=True).apply(summ)
    out["up_by_vol_h_z>3"] = up[up["z"] > 3].groupby(["h","vb"], observed=True).apply(summ)
    dn = E[E["z"] < -3].copy(); dn["vb"] = pd.cut(dn["vr"], [0,0.8,1.25,2,4,1000])
    out["down_z<-3_by_vol_h_short"] = dn.groupby(["h","vb"], observed=True).apply(summ)
    out["usual_move_pct"] = pd.Series({h: 100*sd[h] for h in H})
    return out
