import numpy as np, pandas as pd

def explore(data):
    out = {}
    recs = []
    held = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            v = b["volume"].astype(float)
            r1 = cl.pct_change()
            ma = r1.abs().rolling(720, min_periods=240).mean()
            z = r1 / ma
            vr = v / v.rolling(720, min_periods=240).mean()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in [1, 2, 4]:
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(cl), h)
                g = pd.DataFrame({"z": z.iloc[idx].values, "vr": vr.iloc[idx].values,
                                  "f": fwd.iloc[idx].values, "yr": yr.iloc[idx].values})
                g["coin"] = c; g["h"] = h; g["w"] = w
                recs.append(g)
            # book: gain on each bar by hours since position opened
            a = b["postRebalance_current_allocation"].astype(float).fillna(0)
            nxt = cl.shift(-1) / cl - 1
            gain = a * nxt
            opened = (a != 0) & (b["previous_allocation"].astype(float).fillna(0) == 0)
            grp = opened.cumsum()
            age = a.ne(0).groupby(grp).cumsum()
            fc = b["forecast"].astype(float).fillna(0)
            held.append(pd.DataFrame({"age": age, "gain": gain, "inpos": a != 0,
                                      "fc0": fc == 0, "absa": a.abs()}))
    E = pd.concat(recs).dropna()
    dr = E.groupby("h")["f"].mean()
    E["ex_long"] = E["f"] - E["h"].map(dr)
    def summ(g):
        m = g["ex_long"].mean(); s = g["ex_long"].std(); n = len(g)
        return pd.Series({"n": n, "mean_pct": 100*m, "t": m/(s/np.sqrt(n)) if n > 2 else np.nan,
                          "total_pct": 100*g["f"].mean()})
    dn = E[E["z"] < -2].copy()
    dn["zb"] = pd.cut(-dn["z"], [2, 3, 4, 6, 100])
    dn["vb"] = pd.cut(dn["vr"], [0, 0.8, 1.25, 2, 4, 1000])
    out["fall_long_by_h_z_vol"] = dn[dn["vr"] > 2].groupby(["h", "zb"], observed=True).apply(summ)
    hv = dn[(dn["h"] == 2) & (dn["z"] < -3)]
    out["fall_z<-3_h2_by_vol"] = hv.groupby("vb", observed=True).apply(summ)
    hv2 = hv[hv["vr"] > 2]
    out["fall_z<-3_vr>2_h2_by_coin"] = hv2.groupby("coin").apply(summ)
    out["fall_z<-3_vr>2_h2_by_year"] = hv2.groupby("yr").apply(summ)
    H = pd.concat(held)
    Hp = H[H["inpos"]]
    Hp["ageb"] = pd.cut(Hp["age"], [0, 1, 2, 3, 5, 10, 1000])
    out["book_gain_by_hours_held"] = Hp.groupby("ageb", observed=True).agg(
        n=("gain", "size"), mean_gain_pct=("gain", lambda x: 100*x.mean()),
        share_fc_flat=("fc0", "mean"), mean_abs_alloc=("absa", "mean"))
    out["share_bars_in_position"] = float(H["inpos"].mean())
    return out
