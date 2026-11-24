def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            b["nxt"] = c.shift(-1)/c - 1
            b["sd30"] = r.rolling(30, min_periods=20).std()
            b["z"] = r/b["sd30"]
            b["tr60"] = c/c.shift(60)-1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["prev"] = b["previous_allocation"].fillna(0)
            b["coin"]=coin; b["win"]=w; b["i"]=np.arange(len(b))
            rows.append(b[["coin","win","i","nxt","sd30","z","tr60","forecast","pos","prev"]])
    B = pd.concat(rows, ignore_index=True)
    B["wn"]=B["win"].str[1:].astype(int)
    drift = B.groupby("coin")["nxt"].mean(); B["ex"]=B["nxt"]-B["coin"].map(drift)
    med = B.groupby("coin")["sd30"].median()
    B["agit"]=np.where(B["sd30"]>B["coin"].map(med),"agit","calm")
    B["trend"]=pd.cut(B["tr60"],[-np.inf,-0.10,0.10,np.inf],labels=["fall","chop","rise"]).astype(str)
    B["sig"]=B["forecast"]>0
    cost=0.0019/2
    def book(mask):
        p = B["pos"].where(mask,0.0)
        pp = p.groupby([B.coin,B.win]).shift(1).fillna(0)
        g = p*B["nxt"].fillna(0) - (p-pp).abs()*cost
        d = pd.DataFrame({"wn":B.wn,"i":B.i,"g":g}).groupby(["wn","i"])["g"].mean().sort_index()
        eq=(1+d).cumprod(); dd=(eq/eq.cummax()-1).min()
        yrs=len(d)/365; yr=eq.iloc[-1]**(1/yrs)-1
        held=(p.abs()>0).mean()
        return pd.Series({"yearly%":yr*100,"maxdd%":dd*100,"calmar":yr/abs(dd),"sharpe":d.mean()/d.std()*np.sqrt(365),"held share":held})
    ok = B["tr60"].notna()
    out["approx books (cost on changes)"] = pd.DataFrame({
        "all": book(pd.Series(True,index=B.index)),
        "agitated only": book(B.agit=="agit"),
        "fall agitated only": book((B.agit=="agit")&(B.trend=="fall")),
        "not fall calm": book(~((B.agit=="calm")&(B.trend=="fall"))),
        "agit or rise calm": book((B.agit=="agit")|((B.trend=="rise")&(B.agit=="calm"))),
    }).T
    def st(x):
        x=x.dropna(); n=len(x); return pd.Series({"n":n,"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    S=B[B.sig]
    out["agit: sig by z"]=S[S.agit=="agit"].groupby(pd.cut(S["z"],[-np.inf,-2,-1,-0.5,0]))["ex"].apply(st).unstack()
    out["calm: sig by z"]=S[S.agit=="calm"].groupby(pd.cut(S["z"],[-np.inf,-2,-1,-0.5,0]))["ex"].apply(st).unstack()
    out["agit sig ex by window"]=S[S.agit=="agit"].groupby("wn")["ex"].apply(st).unstack()
    out["calm sig ex by window"]=S[S.agit=="calm"].groupby("wn")["ex"].apply(st).unstack()
    # day-clustered t for agit signal
    for lab in ["agit","calm"]:
        x=S[S.agit==lab].groupby(["wn","i"])["ex"].sum()
        out[f"{lab} sig ex day-clustered t (n days)"]=f"t {x.mean()/(x.std()/np.sqrt(len(x))):.2f}, days {len(x)}"
    # contribution to losses on worst book days
    p=B["pos"]; g=p*B["nxt"]
    dg=pd.DataFrame({"wn":B.wn,"i":B.i,"g":g,"agit":B.agit,"trend":B.trend})
    day=dg.groupby(["wn","i"])["g"].sum()
    worst=day.nsmallest(int(len(day)*0.05)).index
    W=dg.set_index(["wn","i"]).loc[worst]
    out["worst 5% book days: summed gain% by profile"]=W.groupby(["trend","agit"])["g"].agg(lambda x:x.sum()*100)
    return out
