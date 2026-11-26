def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    cs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r = cl.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            f = pd.DataFrame({"r":r, "z":r/sd30, "alloc":b["postRebalance_current_allocation"], "reg":b["regime"], "fc":b["forecast"]})
            f["r5z"] = (cl/cl.shift(5)-1)/(sd30*np.sqrt(5))
            f["prev4z"] = (cl.shift(1)/cl.shift(5)-1)/(sd30*np.sqrt(4))
            f["n1"] = cl.shift(-1)/cl-1
            f["coin"]=c; f["wn"]=int(w[1:])
            f["pnl"] = f["alloc"]*f["n1"]
            cs.append(f)
    F = pd.concat(cs, ignore_index=True)
    mu = F.groupby("coin")["n1"].mean()
    F["u1"] = -(F["n1"] - F["coin"].map(mu))
    inp = F["reg"]=="unknown"
    def summ(g):
        x = g["u1"].dropna()
        return pd.Series({"n":len(x), "u1":x.mean(), "t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "pnl_sum":g["pnl"].sum(), "pnl_mean":g["pnl"].mean(), "absalloc":g["alloc"].abs().mean()})
    S = F[inp & (F["r"]>0)].dropna(subset=["n1","z","prev4z"])
    out["sig_by_prev4z"] = S.groupby(pd.qcut(S["prev4z"],5)).apply(summ)
    S["prevdown"] = S["prev4z"]<0
    out["sig_prevdown_x_z"] = S.groupby([S["prevdown"], S["z"]>0.97]).apply(summ)
    # condition alone: in-profile, previous 4 days down, today down (no signal)
    N = F[inp & (F["r"]<=0)].dropna(subset=["n1","prev4z"])
    out["downday_by_prevdown"] = N.groupby(N["prev4z"]<0).apply(summ)
    # pnl in worst losing positions: their z and prev4z
    P = F[F["alloc"].abs()>1e-6].dropna(subset=["pnl"])
    W = P.nsmallest(25,"pnl")
    out["worst_pos_profile"] = pd.Series({"mean_z":W["z"].mean(),"share_z_gt097":(W["z"]>0.97).mean(),
        "share_prev4_up":(W["prev4z"]>0).mean(),"mean_absalloc":W["alloc"].abs().mean(),"pnl_sum":W["pnl"].sum(),
        "all_share_z_gt097":(P["z"]>0.97).mean(),"all_share_prev4_up":(P["prev4z"]>0).mean()})
    out["pos_by_z"] = P.groupby(pd.qcut(P["z"],5)).apply(summ)
    out["pos_by_absalloc"] = P.groupby(pd.qcut(P["alloc"].abs(),4)).apply(summ)
    out["sig_prevdown_by_window"] = S[S["prevdown"]].groupby("wn").apply(summ)
    return out
