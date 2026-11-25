def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            nxt = c.shift(-1)/c - 1
            rng = (h-l)
            loc = ((h-c)/rng).where(rng>0)
            r30 = c/c.shift(30)-1
            r1 = c/c.shift(1)-1
            alloc = b["postRebalance_current_allocation"].fillna(0)
            df = pd.DataFrame({"coin":coin,"w":w,"day":b["timestamp"].dt.floor("D"),"nxt":nxt,"loc":loc,"r30":r30,"r1":r1,
                               "alloc":alloc,"reg":b["regime"],"gain":alloc*nxt})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["ex"] = D["nxt"] - D["coin"].map(drift)
    D["wn"]=D.w.str[1:].astype(int)
    out = {}
    # book proxy: daily mean over coins of gain; find drawdown periods
    def book(g_col, df):
        x = df.copy(); x["g"]=x[g_col].fillna(0)
        # cost on change of position
        x = x.sort_values(["coin","wn","day"])
        x["ch"]=x.groupby(["coin","w"])[g_col.replace("gain","pos")].diff().abs().fillna(0) if False else 0
        Bd = x.groupby(["wn","day"])["g"].mean().reset_index().sort_values(["wn","day"])
        return Bd
    # positions under variants (use actual alloc magnitude as size where held)
    reg = D.reg=="mean_reversion"
    size = D.alloc.abs()
    D["inR"]=reg & D.r30.notna() & D["loc"].notna()
    variants = {
        "actual": D.alloc,
        "nearlow_only": np.where(D.inR & (D["loc"]>2/3), D.alloc.where(D.alloc>0, 0), 0),
        "r30neg_only": np.where(D.inR & (D.r30<0), D.alloc, 0),
        "r1neg_only": np.where(D.inR & (D.r1<0), D.alloc, 0),
        "r1neg_nearlow": np.where(D.inR & (D.r1<0) & (D["loc"]>0.5), D.alloc, 0),
    }
    res = {}
    for k, pos in variants.items():
        x = D[["coin","w","wn","day","nxt"]].copy(); x["pos"]=pos
        x = x.sort_values(["coin","wn","day"])
        x["ch"]=x.groupby(["coin","w"])["pos"].diff().abs().fillna(x["pos"].abs())
        x["g"]=(x.pos*x.nxt).fillna(0) - x.ch*0.0095
        Bd = x.groupby(["wn","day"])["g"].mean().sort_index()
        v=(1+Bd).cumprod(); dd=(v/v.cummax()-1).min()
        yrs=len(Bd)/365; yr=v.iloc[-1]**(1/yrs)-1
        res[k]={"mean_d":Bd.mean(),"sharpe":Bd.mean()/Bd.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd),"inpos":(x.pos!=0).mean()}
    out["variants_proxy"]=pd.DataFrame(res).T
    # drawdown episodes of actual book proxy: where held during worst 10% book days
    x=D.copy(); Bd=x.groupby(["wn","day"])["gain"].mean()
    worst = Bd[Bd<=Bd.quantile(0.05)].index
    W = x.set_index(["wn","day"]).loc[worst].reset_index()
    W = W[W.alloc>0]
    W["locg"]=pd.cut(W["loc"],[-0.01,1/3,2/3,1.01],labels=["nearhigh","mid","nearlow"])
    W["r1s"]=np.where(W.r1<0,"r1neg","r1pos"); W["r30s"]=np.where(W.r30<0,"r30neg","r30pos")
    out["worst5pct_held_by_loc_r1"]=W.groupby(["locg","r1s"]).agg(n=("gain","size"),sum_gain=("gain","sum"),mean_alloc=("alloc","mean"))
    out["worst5pct_held_by_r30"]=W.groupby("r30s").agg(n=("gain","size"),sum_gain=("gain","sum"))
    # condition alone check: r1neg in regime, loc low vs not
    R=D[D.inR].dropna(subset=["nxt"])
    R["locg"]=pd.cut(R["loc"],[-0.01,1/3,2/3,1.01],labels=["nearhigh","mid","nearlow"])
    R["r1s"]=np.where(R.r1<0,"r1neg","r1pos")
    def s(g): return pd.Series({"n":len(g),"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))),"mean_nxt":g.nxt.mean()})
    out["regime_r1_x_loc"]=R.groupby(["r1s","locg"]).apply(s)
    out["regime_r1_alone"]=R.groupby("r1s").apply(s)
    # grading of nearlow among r1neg: graded by loc and by r1 depth
    N=R[R.r1<0].copy(); N["r1q"]=pd.qcut(N.r1,3,labels=["deep","midneg","shallow"])
    out["r1neg_by_depth_x_loc"]=N.groupby(["r1q","locg"]).apply(s)
    # per window, nearlow & r1neg excess
    out["r1neg_nearlow_by_window"]=R[(R.r1<0)&(R.locg=="nearlow")].groupby("wn").apply(s)
    return out
