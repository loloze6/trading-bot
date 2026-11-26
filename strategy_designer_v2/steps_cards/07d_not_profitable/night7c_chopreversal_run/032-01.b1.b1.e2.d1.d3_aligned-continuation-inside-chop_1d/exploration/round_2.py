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
            b["vol30"]=r.rolling(30).std(); b["vol7"]=r.rolling(7).std()
            b["vr"]=b["vol7"]/b["vol30"]
            b["fwd7"]=cl.shift(-7)/cl-1
            b["coin"]=c; b["w"]=w; b["i"]=np.arange(len(b))
            b["chop"]=(b["regime"]=="chop")
            B.append(b)
    B=pd.concat(B,ignore_index=True)
    drift=B[B["i"]%7==0].groupby("coin")["fwd7"].mean()
    B["fwd7a"]=B["fwd7"]-B["coin"].map(drift)
    B["day"]=pd.to_datetime(B["timestamp"]).dt.floor("D")
    wins=sorted(B["w"].unique(),key=lambda s:int(s[1:]))
    def calmar(mask,name):
        g=B.copy(); g["gg"]=np.where(mask,g["gain"],0.0); g["gg"]=g["gg"].fillna(0)
        d=g.groupby(["w","day"])["gg"].mean().reset_index()
        d["wo"]=d["w"].map({w:i for i,w in enumerate(wins)}); d=d.sort_values(["wo","day"])
        v=(1+d["gg"]).cumprod(); mdd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return pd.Series({"yearly":yr,"mdd":mdd,"calmar":yr/abs(mdd),"sharpe":d["gg"].mean()/d["gg"].std()*np.sqrt(365),"share_in":float(np.mean(mask))})
    held=B["pos"].abs()>1e-6
    med=B["vr"].median()
    res={"all":calmar(held,"all"),
         "chop_now":calmar(held&B["chop"],"c"),
         "chop_now_long":calmar(held&B["chop"]&(B["pos"]>0),"c"),
         "drop_short_offchop":calmar(held&~(~B["chop"]&(B["pos"]<0)),"c"),
         "chop_now_vr_low":calmar(held&B["chop"]&(B["vr"]<=med),"c"),
         "chop_now_er_le_.2":calmar(held&B["chop"]&(B["er"]<=0.2),"c"),
         "chop_now_absr30_notTop":calmar(held&B["chop"]&(B["r30"].abs()<=B["r30"].abs().quantile(0.75)),"c")}
    out["variants_before_fees"]=pd.DataFrame(res).T
    # per-window for chop_now vs all
    g=B.copy(); g["a"]=np.where(held,g["gain"],0); g["c"]=np.where(held&g["chop"],g["gain"],0)
    out["per_window_sum"]=g.groupby("w")[["a","c"]].sum().loc[wins]
    # condition-alone checks on grid: aligned chop sign(r7)*fwd7a
    G=B[(B["i"]%7==0)].dropna(subset=["fwd7a","er","r7","r30"]).copy()
    G["s"]=np.sign(G["r7"]); G["sig"]=G["s"]*G["fwd7a"]
    G["aligned_chop"]=(G["er"]<=0.3)&(np.sign(G["r7"])==np.sign(G["r30"]))
    def tt(x): return pd.Series({"mean":x.mean(),"n":len(x),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    G["vrlow"]=G["vr"]<=med
    out["grid_aligned_x_vr"]=G.groupby(["aligned_chop","vrlow"])["sig"].apply(tt).unstack()
    # plain (unsigned) forward return when vr low, no signal vs signal
    out["grid_raw_fwd7a_by_vr"]=G.groupby(["aligned_chop","vrlow"])["fwd7a"].apply(tt).unstack()
    # chop persistence: fwd7 signed for aligned chop cases where chop ends within next 7 vs stays
    B["chop_next7"]=B.groupby(["coin","w"])["chop"].transform(lambda s: s[::-1].rolling(7,min_periods=1).min()[::-1].shift(-1))
    G2=B[(B["i"]%7==0)&B["chop"]].dropna(subset=["fwd7a","chop_next7"]).copy()
    G2["sig"]=np.sign(G2["r7"])*G2["fwd7a"]
    out["grid_chop_stays"]=G2.groupby("chop_next7")["sig"].apply(tt).unstack()
    # offchop held gain by side and whether er rose above .3 (trend) vs sign misalignment
    H=B[held&~B["chop"]].dropna(subset=["gain"]).copy()
    H["why"]=np.where(H["er"]>0.3,"trend","misaligned")
    H["side"]=np.where(H["pos"]>0,"long","short")
    out["offchop_gain"]=H.groupby(["why","side"])["gain"].agg(["mean","sum","count"])
    return out
