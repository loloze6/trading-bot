def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b.close; r=np.log(cl).diff()
            pos=b.postRebalance_current_allocation.fillna(0)
            nxt=cl.shift(-1)/cl-1
            r7=cl/cl.shift(7)-1; r30=cl/cl.shift(30)-1
            er=(np.log(cl)-np.log(cl.shift(30))).abs()/r.abs().rolling(30).sum()
            vol=r.rolling(30).std()
            vol90=r.rolling(90,min_periods=60).std()
            f7=cl.shift(-7)/cl-1
            rows.append(pd.DataFrame({"coin":c,"w":w,"pos":pos,"gain":pos*nxt,"nxt":nxt,"fc":b.forecast,"r7":r7,"r30":r30,
                "er":er,"vol":vol,"vrat":vol/vol90,"f7":f7,"i":np.arange(len(b)),"grid":(np.arange(len(b))%7==0)}))
    B=pd.concat(rows,ignore_index=True)
    B["side"]=np.sign(B.pos)
    q=B.loc[B.pos!=0,"vol"].quantile([1/3,2/3]).values
    vq=B.loc[B.pos!=0,"vrat"].quantile([1/3,2/3]).values
    B["vhi"]=B.vol>q[1]; B["vrhi"]=B.vrat>vq[1]
    def stats(g):
        B2=B.assign(g=g)
        ws=sorted(B2.w.unique(),key=lambda s:int(s[1:]))
        d=[]
        for w in ws:
            x=B2[B2.w==w].groupby("i").g.mean(); d.append(x.dropna())
        d=pd.concat(d,ignore_index=True)
        v=(1+d).cumprod(); mdd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(d))-1
        return pd.Series({"sharpe":d.mean()/d.std()*np.sqrt(365),"yearly":yr,"mdd":mdd,"calmar":yr/-mdd,"inpos":(g!=0).mean()})
    res={}
    res["variants"]=pd.DataFrame({
        "base":stats(B.gain),
        "long_only":stats(np.where(B.side>0,B.gain,0)),
        "short_only":stats(np.where(B.side<0,B.gain,0)),
        "no_hi_vol":stats(np.where(~B.vhi,B.gain,0)),
        "no_hi_vrat":stats(np.where(~B.vrhi,B.gain,0)),
        "long_no_hivol":stats(np.where((B.side>0)&~B.vhi,B.gain,0)),
        "short_no_hivol":stats(np.where((B.side<0)&~B.vhi,B.gain,0)),
    }).T
    # condition checks on grid: f7 in direction of r7
    G=B[B.grid & B.f7.notna() & B.r7.notna() & B.r30.notna() & B.er.notna()].copy()
    drift=G.groupby("coin").f7.transform("mean")
    G["sgn"]=np.sign(G.r7); G["dirmove"]=G.sgn*(G.f7-drift)
    G["sig"]=G.fc!=0
    G["up"]=G.r7>0
    G["chop_agree"]=(G.er<=0.3)&(np.sign(G.r7)==np.sign(G.r30))
    G["vhi"]=G.vol>q[1]
    def tt(s): return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    res["dir_by_sig_up"]=G.groupby(["sig","up"]).dirmove.apply(tt).unstack()
    res["dir_by_sig_vhi"]=G.groupby(["sig","vhi"]).dirmove.apply(tt).unstack()
    res["dir_by_chop_up_nosig"]=G[~G.sig].groupby(["chop_agree","up"]).dirmove.apply(tt).unstack()
    # raw (not drift-removed) f7 for up/down outside signal: drift of up-weeks
    res["raw_f7_up_nosig"]=G[~G.sig].groupby("up").f7.apply(tt).unstack()
    # trade-level: losing short trades, the market's 7-day moves
    res["gain_side_x_vhi"]=B[B.pos!=0].groupby(["side","vhi"]).gain.agg(["count","mean","sum"])
    res["vhi_by_window_share"]=B[B.pos!=0].groupby("w").vhi.mean()
    return res
