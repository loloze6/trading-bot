def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    B=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.copy(); b["coin"]=c; b["w"]=w
            cl=b.close; r=cl.pct_change()
            b["er"]=(cl-cl.shift(30)).abs()/cl.diff().abs().rolling(30).sum()
            b["p7"]=cl/cl.shift(7)-1; b["p30"]=cl/cl.shift(30)-1
            b["vol30"]=r.rolling(30).std()
            b["f7"]=cl.shift(-7)/cl-1
            b["r1"]=cl.shift(-1)/cl-1
            b["pos"]=b.postRebalance_current_allocation.fillna(0)
            b["inreg"]=(b.regime=="mean_reversion")
            # bars since last in-regime bar
            g=(b.inreg).cumsum()
            b["since"]=b.groupby(g).cumcount()
            b.loc[g==0,"since"]=999
            b["gain"]=b.pos*b.r1
            b["i"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            B.append(b)
    B=pd.concat(B).dropna(subset=["r1"])
    B["side"]=np.sign(B.pos)
    B["volq"]=B.groupby("coin").vol30.transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    B["wn"]=B.w.str[1:].astype(int)
    def book(gcol):
        P=B.groupby(["wn","day"])[gcol].mean().reset_index().sort_values(["wn","day"])
        s=P[gcol]; eq=(1+s).cumprod(); dd=(eq/eq.cummax()-1).min()
        yr=eq.iloc[-1]**(365/len(s))-1
        return pd.Series({"sharpe":s.mean()/s.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd)})
    pos=B.pos
    B["g_all"]=B.gain
    B["g_long"]=np.where(B.side>0,B.gain,0)
    B["g_inreg"]=np.where(B.inreg,B.gain,0)
    B["g_since3"]=np.where(B.since<=3,B.gain,0)
    B["g_noshort_hv"]=np.where((B.side<0)&(B.volq==2),0,B.gain)
    B["g_short_inreg_long_all"]=np.where((B.side<0)&(~B.inreg),0,B.gain)
    B["g_long_inreg"]=np.where((B.side>0)&B.inreg,B.gain,0)
    out["variants_no_fees"]=pd.DataFrame({k:book(k) for k in ["g_all","g_long","g_inreg","g_since3","g_noshort_hv","g_short_inreg_long_all","g_long_inreg"]}).T
    # gain by bars since regime ended
    B["sinceb"]=pd.cut(B.since,[-1,0,3,7,14,1000])
    out["gain_by_since_side"]=B[B.side!=0].groupby(["sinceb","side"]).gain.agg(["mean","count"])
    # deepest fall episode: contributions by side and inreg
    P=B.groupby(["wn","day"]).g_all.mean().reset_index().sort_values(["wn","day"]).reset_index(drop=True)
    eq=(1+P.g_all).cumprod(); peak=eq.cummax(); dd=eq/peak-1
    trough=dd.idxmin(); start=(eq[:trough+1]==peak[trough]).iloc[::-1].idxmax()
    ep=P.loc[start:trough,["wn","day"]]
    E=B.merge(ep,on=["wn","day"])
    out["deepest_fall"]=pd.Series({"days":len(ep),"window":ep.wn.iloc[0],"dd":dd.min()})
    out["fall_contrib"]=E.groupby(["side","inreg"]).gain.agg(["sum","count"])
    out["fall_coin_state"]=pd.Series({"coin_r1_mean":E.r1.mean(),"volq_mean":E.volq.mean(),"er_mean":E.er.mean(),"all_volq":B.volq.mean()})
    # condition-alone checks: f7 on non-overlapping grid
    G=B[B.i%7==0].copy()
    drift=G.groupby("coin").f7.mean(); G["ex"]=G.f7-G.coin.map(drift)
    G["sig"]=G.inreg&(B.loc[G.index].forecast if False else True)
    def agg(s):
        s=s.dropna(); return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan,"n":len(s)})
    G["dir30"]=np.sign(G.p30)
    out["grid_inreg_side_volq"]=G[G.inreg].groupby([np.sign(G[G.inreg].forecast),"volq"]).apply(lambda g: agg(np.sign(g.forecast)*g.ex))
    out["grid_outreg_dir30_volq"]=G[~G.inreg].groupby(["dir30","volq"]).apply(lambda g: agg(g.dir30*g.ex))
    return out
