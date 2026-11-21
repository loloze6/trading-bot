def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # trades by entry forecast size and side
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            t = t.copy(); t["coin"] = c; t["w"] = w; tr.append(t)
    tr = pd.concat(tr)
    tr["fb"] = pd.cut(tr["entry_forecast"].abs(), [0, 0.5, 2, 5, 10, 20.01])
    out["trades_by_fsize_side"] = tr.groupby(["fb", "side"]).agg(n=("coin", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", "median")).reset_index()
    # bar-level position gain: decomposition
    recs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].astype(float).reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            f = b["forecast"].astype(float).reset_index(drop=True)
            nxt = cl.shift(-1)/cl - 1
            recs.append(pd.DataFrame({"coin": c, "pos": pos, "f": f, "g": pos*nxt,
                                      "turn": pos.diff().abs()}))
    bb = pd.concat(recs).dropna()
    bb["fb"] = pd.cut(bb["f"].abs(), [-0.01, 0.0001, 0.5, 2, 5, 10, 20.01])
    out["bar_gain_by_forecast"] = bb.groupby("fb").agg(n=("g", "size"), gain_bps=("g", lambda x: x.mean()*1e4),
        mean_abs_pos=("pos", lambda x: x.abs().mean()), turn=("turn", "mean"))
    out["total_gain_bps_per_bar"] = bb["g"].mean()*1e4
    out["cost_bps_per_bar_est"] = bb["turn"].mean()*19/2
    # after-fall signal at longer horizons, graded, with window halves
    recs = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].astype(float).reset_index(drop=True)
            r1 = cl.pct_change(); v24 = r1.rolling(24).std()
            va = v24.rolling(720, min_periods=200).mean()
            z = (cl/cl.shift(2)-1)/(va*np.sqrt(2)); vr = v24/va
            z24 = (cl/cl.shift(24)-1)/(va*np.sqrt(24))
            wn = int(w[1:])
            for h in (24, 48, 72):
                idx = np.arange(0, len(cl)-h, h)
                recs.append(pd.DataFrame({"coin": c, "half": "w1-12" if wn <= 12 else "w13-24", "h": h,
                    "z": z.values[idx], "z24": z24.values[idx], "vr": vr.values[idx],
                    "fwd": (cl.shift(-h)/cl-1).values[idx]}))
    df = pd.concat(recs).dropna()
    df = df.join(df.groupby(["coin", "h"])["fwd"].mean().rename("drift"), on=["coin", "h"])
    df["un"] = df["fwd"]-df["drift"]
    def agg(g):
        return pd.Series({"n": len(g), "un_long_bps": g["un"].mean()*1e4, "tot_long_bps": g["fwd"].mean()*1e4,
                          "t": g["un"].mean()/(g["un"].std()/np.sqrt(len(g)))})
    fall = df[(df["vr"] >= 1) & (df["z"] < 0)].copy()
    fall["zb"] = pd.cut(-fall["z"], [0, 1, 2, 3, 5, 100])
    out["fall2h_vrhi_by_z_h"] = fall.groupby(["h", "zb"]).apply(agg).unstack(0)
    f2 = fall[-fall["z"] >= 2]
    out["fall2h_z2_by_half_h"] = f2.groupby(["half", "h"]).apply(agg).unstack(1)
    # 24h fall as situation instead of 2h
    f24 = df[(df["vr"] >= 1) & (df["z24"] < 0)].copy()
    f24["zb"] = pd.cut(-f24["z24"], [0, 1, 2, 3, 100])
    out["fall24h_vrhi_by_z_h"] = f24.groupby(["h", "zb"]).apply(agg).unstack(0)
    rise = df[(df["vr"] >= 1) & (df["z"] >= 2)]
    out["rise2h_z2_by_h_short"] = rise.groupby("h").apply(lambda g: pd.Series({"n": len(g),
        "un_short_bps": -g["un"].mean()*1e4, "t": -g["un"].mean()/(g["un"].std()/np.sqrt(len(g)))}))
    return out
