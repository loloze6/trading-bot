def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins=list(bars.keys())
    B=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            b["ret1"]=cl.shift(-1)/cl-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["gain"]=b["pos"]*b["ret1"]
            ch=cl.diff().abs()
            b["er"]=(cl-cl.shift(30)).abs()/ch.rolling(30).sum()
            b["r7"]=cl/cl.shift(7)-1; b["r30"]=cl/cl.shift(30)-1
            b["vol30"]=r.rolling(30).std()
            b["z30"]=b["r30"]/(b["vol30"]*np.sqrt(30))
            b["fwd7"]=cl.shift(-7)/cl-1
            b["coin"]=c; b["w"]=w; b["i"]=np.arange(len(b))
            b["chop"]=(b["regime"]=="chop")
            b["dpos"]=b["pos"].diff().abs().fillna(b["pos"].abs())
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    drift=B[B["i"]%7==0].groupby("coin")["fwd7"].mean()
    B["fwd7a"]=B["fwd7"]-B["coin"].map(drift)
    B["day"]=pd.to_datetime(B["timestamp"]).dt.floor("D")
    wins=sorted(B["w"].unique(),key=lambda s:int(s[1:]))
    q75=B["z30"].abs().quantile(0.75)
    def tt(x): return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    G=B[(B["i"]%7==0)].dropna(subset=["fwd7a","er","r7","r30","z30"]).copy()
    G["sig"]=np.sign(G["r7"])*G["fwd7a"]
    G["aligned_chop"]=(G["er"]<=0.3)&(np.sign(G["r7"])==np.sign(G["r30"]))
    G["z30top"]=G["z30"].abs()>q75
    out["grid_aligned_x_z30top"]=G.groupby(["aligned_chop","z30top"])["sig"].apply(tt).unstack()
    A=G[G["aligned_chop"]].copy()
    A["z30q"]=pd.qcut(A["z30"].abs(),3,labels=False)
    out["aligned_cases_by_absz30_tercile"]=A.groupby("z30q")["sig"].apply(tt).unstack()
    A["side"]=np.where(A["r7"]>0,"long","short")
    out["aligned_cases_by_side_z30top"]=A.groupby(["side","z30top"])["sig"].apply(tt).unstack()
    held=B["pos"].abs()>1e-6
    def calmar(mask):
        g=B.copy(); g["gg"]=np.where(mask,g["gain"],0.0); g["gg"]=g["gg"].fillna(0)
        g["fee"]=np.where(mask,g["dpos"]*0.0019/2,0.0)
        g["gg"]=g["gg"]-g["fee"]
        d=g.groupby(["w","day"])["gg"].mean().reset_index()
        d["wo"]=d["w"].map({w:i for i,w in enumerate(wins)}); d=d.sort_values(["wo","day"])
        v=(1+d["gg"]).cumprod(); dd=v/v.cummax()-1
        yr=v.iloc[-1]**(365/len(d))-1
        tr=dd.idxmin(); worst_w=d.loc[tr,"w"]
        return pd.Series({"yearly":yr,"mdd":dd.min(),"calmar":yr/abs(dd.min()),"sharpe":d["gg"].mean()/d["gg"].std()*np.sqrt(365),"trough_w":int(worst_w[1:])})
    res={"all":calmar(held),
         "chop_now":calmar(held&B["chop"]),
         "chop_now_z30notTop":calmar(held&B["chop"]&(B["z30"].abs()<=q75)),
         "drop_short_offchop":calmar(held&~(~B["chop"]&(B["pos"]<0))),
         "notTop_any":calmar(held&(B["z30"].abs()<=q75))}
    out["variants_approx_fees"]=pd.DataFrame(res).T
    H=B[held].dropna(subset=["gain","z30"]).copy()
    H["top"]=H["z30"].abs()>q75; H["side"]=np.where(H["pos"]>0,"long","short")
    out["held_gain_by_top_side"]=H.groupby(["top","side"])["gain"].agg(["mean","sum","count"])
    return out
