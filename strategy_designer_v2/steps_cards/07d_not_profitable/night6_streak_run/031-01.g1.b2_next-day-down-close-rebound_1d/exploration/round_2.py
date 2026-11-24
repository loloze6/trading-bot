def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    recs = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r = cl.pct_change()
            vol60 = r.rolling(60).std()
            nxt = cl.shift(-1)/cl-1
            f = pd.DataFrame({"coin":c,"wn":int(w[1:]),"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "nxt":nxt,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"].astype(float),
                "prev":b["previous_allocation"].astype(float),
                "ret20":cl/cl.shift(20)-1,"volratio":r.rolling(20).std()/vol60,
                "vr5":r.rolling(5).std()/vol60})
            recs.append(f)
    F = pd.concat(recs).dropna(subset=["nxt"])
    drift = F.groupby("coin")["nxt"].mean()
    F["ex"] = F["nxt"]-F["coin"].map(drift)
    F["sig"] = F["fc"]>0
    cost = 0.0019/2
    def book(mask, name):
        a = F["alloc"].where(mask, 0.0)
        G = F[["coin","wn","day"]].copy()
        G["a"] = a.values
        G = G.sort_values(["coin","wn","day"])
        G["pa"] = G.groupby(["coin","wn"])["a"].shift(1).fillna(0)
        G["g"] = G["a"]*F.loc[G.index,"nxt"].values if False else 0
        return G
    res = {}
    variants = {"all": F["sig"]|(~F["sig"]),
                "vr>1": F["volratio"]>1.0, "vr>1.2": F["volratio"]>1.2,
                "ret20>=0": F["ret20"]>=0, "vr>1_or_ret20>=0": (F["volratio"]>1.0)|(F["ret20"]>=0)}
    F2 = F.reset_index(drop=True)
    for k, m in variants.items():
        m = m.reset_index(drop=True).fillna(False)
        a = F2["alloc"].where(m, 0.0)
        pa = a.groupby([F2["coin"],F2["wn"]]).shift(1).fillna(0)
        g = a*F2["nxt"] - (a-pa).abs()*cost
        T = pd.DataFrame({"wn":F2["wn"],"day":F2["day"],"g":g}).groupby(["wn","day"])["g"].mean().sort_index()
        v = (1+T).cumprod(); ddn = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(T))-1
        res[k] = {"sharpe":T.mean()/T.std()*np.sqrt(365),"yearly":yr,"maxdd":ddn,"calmar":yr/abs(ddn),
                  "share_in":(a.abs()>1e-6).mean()}
    out["books"] = pd.DataFrame(res).T
    def tt(x):
        x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    S = F[F["sig"]].copy()
    S["vrq"] = pd.qcut(S["volratio"],4,labels=False)
    S["fh"] = S.groupby("vrq")["fc"].transform(lambda x: x>x.median())
    out["sig_vrq_by_fc_half"] = S.groupby(["vrq","fh"]).apply(lambda g: tt(g["ex"])).unstack()
    N = F[~F["sig"]].copy()
    N["vrq"] = pd.cut(N["volratio"], [0]+list(S.groupby("vrq")["volratio"].max().values[:-1])+[99], labels=False)
    out["nosig_by_same_vr_bins"] = N.groupby("vrq").apply(lambda g: tt(g["ex"]))
    S["year"] = S["day"].dt.year
    out["sig_vr>1_by_year"] = S[S["volratio"]>1].groupby("year").apply(lambda g: tt(g["ex"]))
    out["sig_vr<=1_by_year"] = S[S["volratio"]<=1].groupby("year").apply(lambda g: tt(g["ex"]))
    out["sig_vr>1_by_coin"] = S[S["volratio"]>1].groupby("coin").apply(lambda g: tt(g["ex"]))
    return out
