def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; coins=list(bars.keys())
    R=[]
    for c in coins:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); cl=b.close; hi=b.high; lo=b.low
            rng24=hi.rolling(6).max()/lo.rolling(6).min()-1
            df=pd.DataFrame({"coin":c,"wn":int(w[1:]),"f":b.forecast,
                "alloc":b.postRebalance_current_allocation,"nxt":cl.shift(-1)/cl-1,
                "fall24":cl/cl.shift(6)-1,"rm":rng24/rng24.rolling(180).mean(),
                "past7":cl/cl.shift(42)-1,"past3":cl/cl.shift(18)-1,
                "ret6":cl.shift(-6)/cl-1,
                "fee":(b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value,
                "bars_since_pos_f":None})
            # bars since forecast was last >= 1
            strong=(b.forecast>=1).values
            since=np.full(len(b),np.nan); last=-10**9
            for i in range(len(b)):
                if strong[i]: last=i
                since[i]=i-last if last>-10**9 else np.nan
            df["since"]=since
            R.append(df)
    A=pd.concat(R,ignore_index=True)
    A["gain"]=A.alloc*A.nxt
    drift=A.groupby("coin").nxt.transform("mean")
    A["mkt"]=A.alloc*drift; A["timing"]=A.gain-A.mkt
    inm=A[A.alloc.abs()>0].copy()
    inm["fb"]=pd.cut(inm.f,[-1,0,0.1,1,5,20.1],labels=["f=0","0-0.1","0.1-1","1-5","5-20"])
    g=inm.groupby("fb",observed=True).agg(bars=("gain","size"),alloc=("alloc","mean"),
        gain_sum=("gain","sum"),mkt_sum=("mkt","sum"),timing_sum=("timing","sum"),fee_sum=("fee","sum"),
        gain_sd=("gain","std"))
    g["t_gain"]=g.gain_sum/g.bars/(g.gain_sd/np.sqrt(g.bars))
    out["inmarket_by_forecast_bucket"]=g.round(4)
    inm["sb"]=pd.cut(inm.since,[-1,0,6,12,24,60,10**6],labels=["0","1-6","7-12","13-24","25-60",">60"])
    g2=inm.groupby("sb",observed=True).agg(bars=("gain","size"),alloc=("alloc","mean"),gain_sum=("gain","sum"),timing_sum=("timing","sum"),fee_sum=("fee","sum"))
    out["inmarket_by_bars_since_strong"]=g2.round(4)
    out["total_fee_sum"]=float(A.fee.sum()); out["total_gain_sum"]=float(A.gain.sum())
    # deepest fall w16 and w12-14: what held
    for nm,ws in [("w16",[16]),("w12_14",[12,13,14])]:
        S=A[A.wn.isin(ws)]
        out["fall_"+nm]=pd.DataFrame({"gain_sum":[S.gain.sum()],"timing_sum":[S.timing.sum()],
            "mean_alloc":[S.alloc.mean()],"share_in":[(S.alloc>0).mean()],
            "gain_when_f>=1":[S[S.f>=1].gain.sum()],"gain_when_0<f<1":[S[(S.f>0)&(S.f<1)].gain.sum()],
            "gain_when_f=0":[S[S.f<=0].gain.sum()]}).round(4)
    # 6-bar grid: strong cases split by past3 (the 3-day return before) and fall continuing
    G=A[(A.f>=1)].dropna(subset=["ret6","past3","rm","fall24"]).copy()
    G=G.groupby(["coin","wn"]).apply(lambda x:x.iloc[::6]).reset_index(drop=True)
    d6=A.dropna(subset=["ret6"]).groupby("coin").apply(lambda x:x.ret6.iloc[::6].mean())
    G["ex"]=G.ret6-G.coin.map(d6)
    def q(col,k=4):
        G["g"]=pd.qcut(G[col],k,labels=False,duplicates="drop")
        r=G.groupby("g").agg(n=("ex","size"),lo=(col,"min"),hi=(col,"max"),mean_ex=("ex","mean"),sd=("ex","std"))
        r["t"]=r.mean_ex/(r.sd/np.sqrt(r.n)); return r.drop(columns="sd").round(5)
    out["strong_by_past7"]=q("past7"); out["strong_by_rm"]=q("rm"); out["strong_by_fall24"]=q("fall24")
    return out
