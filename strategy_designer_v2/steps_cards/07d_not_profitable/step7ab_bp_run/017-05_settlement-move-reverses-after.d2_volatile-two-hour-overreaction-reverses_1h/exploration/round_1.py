def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book per coin
    rows = []
    for c in data["days"]:
        br = pd.concat([d["book_return"] for d in data["days"][c].values()]).dropna()
        tr = pd.concat(list(data["trades"][c].values()))
        rows.append({"coin": c, "book_mean_bps": br.mean()*1e4, "sharpe": br.mean()/br.std()*np.sqrt(365),
                     "ntrades": len(tr), "gross_mean_pct": tr["profit_loss_percent"].mean(),
                     "net_mean_pct": tr["net_profit_loss_percent"].mean(),
                     "dur_h_med": tr["duration_minutes"].median()/60})
    out["book_by_coin"] = pd.DataFrame(rows)
    # recompute signal from prices
    recs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].astype(float).reset_index(drop=True)
            r1 = cl.pct_change()
            v24 = r1.rolling(24).std()
            va = v24.rolling(720, min_periods=200).mean()
            z = (cl/cl.shift(2)-1)/(va*np.sqrt(2))
            vr = v24/va
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            for h in (8, 24, 48):
                idx = np.arange(0, len(cl)-h, h)
                fwd = (cl.shift(-h)/cl - 1).values[idx]
                recs.append(pd.DataFrame({"coin": c, "w": w, "h": h, "z": z.values[idx], "vr": vr.values[idx],
                                          "fwd": fwd, "hour": ts.dt.hour.values[idx]}))
    df = pd.concat(recs).dropna()
    drift = df.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["un"] = (df["fwd"]-df["drift"])*(-np.sign(df["z"]))
    df["tot"] = df["fwd"]*(-np.sign(df["z"]))
    df["zb"] = pd.cut(df["z"].abs(), [0, 1, 2, 3, 4, 6, 100])
    df["vrb"] = pd.cut(df["vr"], [0, 0.8, 1.0, 1.3, 1.7, 2.5, 100])
    def agg(g):
        return pd.Series({"n": len(g), "un_bps": g["un"].mean()*1e4,
                          "t": g["un"].mean()/(g["un"].std()/np.sqrt(len(g)))})
    hi = df[df["vr"] >= 1]
    out["vrhigh_by_zbin_h"] = hi.groupby(["h", "zb"]).apply(agg).unstack(0)
    big = df[df["z"].abs() >= 2]
    out["z2plus_by_vrbin_h"] = big.groupby(["h", "vrb"]).apply(agg).unstack(0)
    out["vrhigh_z2_by_coin_h"] = hi[hi["z"].abs() >= 2].groupby(["coin", "h"]).apply(agg).unstack(1)
    # direction of z
    hi2 = hi[hi["z"].abs() >= 2].copy()
    hi2["dir"] = np.where(hi2["z"] > 0, "after_rise", "after_fall")
    out["vrhigh_z2_by_dir_h"] = hi2.groupby(["dir", "h"]).apply(agg).unstack(1)
    return out
