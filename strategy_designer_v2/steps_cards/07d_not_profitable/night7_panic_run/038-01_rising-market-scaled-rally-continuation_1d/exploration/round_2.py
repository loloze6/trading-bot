import numpy as np, pandas as pd

def explore(data):
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    recs = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            f = pd.DataFrame({"coin": c, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "fc": b["forecast"].fillna(0), "rising": b["regime"] != "chop",
                              "alloc": b["postRebalance_current_allocation"].fillna(0)})
            f["nxt"] = cl.shift(-1)/cl - 1
            f["fh20"] = cl/cl.rolling(20).max() - 1
            f["r20"] = cl/cl.shift(20) - 1
            f["fwd3"] = cl.shift(-3)/cl - 1
            f["dalloc"] = f["alloc"].diff().abs().fillna(f["alloc"].abs())
            recs.append(f)
    A = pd.concat(recs, ignore_index=True)
    A["entry_fh20"] = np.nan
    # condition state carried from entry: a position opened when fh20 was deep keeps that tag until flat
    def tag(g):
        held = g["alloc"] > 0
        start = held & ~held.shift(1, fill_value=False)
        grp = start.cumsum()
        efh = g["fh20"].where(start).groupby(grp).transform("first")
        efc = g["fc"].where(start).groupby(grp).transform("first")
        er20 = g["r20"].where(start).groupby(grp).transform("first")
        return pd.DataFrame({"efh": efh.where(held), "efc": efc.where(held), "er20": er20.where(held)}, index=g.index)
    T = A.groupby(["coin","win"], group_keys=False).apply(tag)
    A = A.join(T)
    A["gain"] = A["alloc"]*A["nxt"].fillna(0)
    nwins = sorted(A.win.unique(), key=lambda s: int(s[1:]))
    def book(mask_keep, scale=None):
        g = A["gain"].where(mask_keep, 0.0)
        al = A["alloc"].where(mask_keep, 0.0)
        if scale is not None:
            g = g*scale; al = al*scale
        dal = al.groupby([A.coin, A.win]).diff().abs().fillna(al.abs())
        net = g - dal*0.00095
        D = pd.DataFrame({"win": A.win, "day": A.day, "net": net}).groupby(["win","day"])["net"].mean().reset_index()
        D["wn"] = D.win.str[1:].astype(int); D = D.sort_values(["wn","day"])
        v = (1+D.net).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(v)) - 1
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr/abs(dd), "sharpe": D.net.mean()/D.net.std()*np.sqrt(365),
                          "inpos": (al > 0).mean()})
    allk = pd.Series(True, index=A.index)
    res = {"as_tested": book(allk),
           "entry_fh20_gt_-0.10": book(~(A.efh < -0.10)),
           "entry_fh20_gt_-0.05": book(~(A.efh < -0.05)),
           "entry_r20_gt_0": book(~(A.er20 < 0)),
           "entry_fc_ge_10": book(~(A.efc < 10)),
           "now_fh20_gt_-0.10": book(~(A.fh20 < -0.10)),
           "entry_fc_ge_10_and_fh20": book(~(A.efc < 10) & ~(A.efh < -0.10)),
           "entry_fh20_and_r20": book(~(A.efh < -0.10) & ~(A.er20 < 0))}
    out["books"] = pd.DataFrame(res).T
    # in-position gain by entry condition
    P = A[A.alloc > 0].copy()
    P["fh_bin"] = pd.cut(P.efh, [-1, -0.10, -0.05, 0.001])
    out["gain_by_entry_fh20"] = P.groupby("fh_bin").agg(n=("gain","size"), mean=("gain","mean"), sum=("gain","sum"))
    P["fc_bin"] = pd.cut(P.efc, [0, 10, 15, 20.01])
    out["gain_by_entry_fc"] = P.groupby("fc_bin").agg(n=("gain","size"), mean=("gain","mean"), sum=("gain","sum"))
    # interaction check on grid: rising bars, fh20 deep, with vs without signal; fh20 shallow with vs without
    G = A.groupby(["coin","win"], group_keys=False).apply(lambda g: g.iloc[::3]).dropna(subset=["fwd3","fh20"])
    dr = G.groupby("coin")["fwd3"].mean(); G["ex"] = G.fwd3 - G.coin.map(dr)
    R = G[G.rising].copy()
    R["deep"] = R.fh20 < -0.10; R["sig"] = R.fc > 0; R["strong"] = R.fc >= 10
    def s(x): return pd.Series({"n": len(x), "ex": x.ex.mean(), "t": x.ex.mean()/(x.ex.std()/np.sqrt(len(x)))})
    out["deep_x_sig"] = R.groupby(["deep","sig"]).apply(s)
    out["deep_x_strong"] = R[R.sig].groupby(["deep","strong"]).apply(s)
    out["slope_shallow_only"] = pd.Series(np.polyfit(R[~R.deep].fc, R[~R.deep].ex, 1)[0], index=["slope"])
    # deepest fall w16-w17: what was held
    F = A[A.win.isin(["w16","w17"]) & (A.alloc > 0)]
    out["w16_17_held_by_entry_fh"] = F.groupby(pd.cut(F.efh, [-1,-0.10,-0.05,0.001])).agg(n=("gain","size"), sum=("gain","sum"))
    return out
