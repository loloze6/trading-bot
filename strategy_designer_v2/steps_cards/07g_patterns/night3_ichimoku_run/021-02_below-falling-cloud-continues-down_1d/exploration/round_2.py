import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    d=[]; g=[]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df=df.reset_index(drop=True)
            c=df["close"].astype(float); hi=df["high"].astype(float); lo=df["low"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std().shift(1)
            ts=pd.to_datetime(df["timestamp"])
            d.append(pd.DataFrame(dict(coin=coin,w=w,yr=ts.dt.year,wd=ts.dt.weekday,r=r,zz=r/sd,nxt=r.shift(-1))))
            n=len(c)
            H=hi.rolling(26).max(); L=lo.rolling(26).min(); rp=(c-L)/(H-L)
            p26=c/c.shift(26)-1; p52=c/c.shift(52)-1
            ma=c/c.rolling(52).mean()-1
            for h in (7,26):
                for t in range(0,n-h,h):
                    g.append(dict(coin=coin,w=w,yr=ts.iloc[t].year,h=h,fwd=c.iloc[t+h]/c.iloc[t]-1,
                                  rp=rp.iloc[t],p26=p26.iloc[t],p52=p52.iloc[t],ma=ma.iloc[t]))
    d=pd.concat(d,ignore_index=True)
    # weekday per coin: Sat and Fri minus others
    rows=[]
    for coin,s in d.dropna(subset=["r"]).groupby("coin"):
        for wd in (4,5):
            a=s[s.wd==wd]["r"]; b=s[s.wd!=wd]["r"]
            rows.append(dict(coin=coin,wd=wd,diff_bps=(a.mean()-b.mean())*1e4,t=stats.ttest_ind(a,b,equal_var=False)[0],n=len(a)))
    out["weekday_by_coin"]=pd.DataFrame(rows)
    s=d.dropna(subset=["r"])
    sat=s.assign(sat=(s.wd==5)).groupby(["yr","sat"])["r"].mean().unstack()*1e4
    out["sat_vs_rest_by_year_bps"]=sat
    # market-day level (avg across coins) to remove cross-coin correlation: by weekday per window/day index
    # rebound after big drops per coin
    rows=[]
    for coin,s2 in d.dropna(subset=["zz","nxt"]).groupby("coin"):
        a=s2[s2.zz<=-2]["nxt"]; b=s2[s2.zz>-2]["nxt"]
        rows.append(dict(coin=coin,n=len(a),diff_bps=(a.mean()-b.mean())*1e4,t=stats.ttest_ind(a,b,equal_var=False)[0]))
    s2=d.dropna(subset=["zz","nxt"])
    out["slope_nxt_on_negz_bycoin"]=pd.DataFrame(rows)
    a=s2[s2.zz<=-2]; out["drop_rebound_by_year_bps"]=a.groupby("yr")["nxt"].agg(["mean","count"]).assign(mean=lambda x:x["mean"]*1e4)
    g=pd.DataFrame(g)
    g["ex"]=g["fwd"]-g.groupby(["coin","h"])["fwd"].transform("mean")
    g["z"]=g["ex"]/g.groupby(["coin","h"])["fwd"].transform("std")
    rows=[]
    for h in (7,26):
        for f in ["rp","p26","p52","ma"]:
            for coin,s3 in g[g.h==h].dropna(subset=[f]).groupby("coin"):
                sl=stats.linregress((s3[f]-s3[f].mean())/s3[f].std(),s3["z"])
                rows.append(dict(h=h,f=f,coin=coin,n=len(s3),slope=sl.slope,t=sl.slope/sl.stderr))
    pc=pd.DataFrame(rows)
    out["slopes_summary"]=pc.groupby(["h","f"]).agg(mean_slope=("slope","mean"),mean_t=("t","mean"),pos=("slope",lambda v:(v>0).sum()),n=("n","sum"))
    # p26 at 26d: quintiles pooled, ex mean in %
    s4=g[(g.h==26)].dropna(subset=["p26"]).copy()
    s4["q"]=s4.groupby("coin")["p26"].transform(lambda v:pd.qcut(v,4,labels=False))
    out["h26_by_p26_quartile"]=s4.groupby("q").agg(ex_pct=("ex",lambda v:v.mean()*100),z=("z","mean"),n=("z","size"))
    out["h26_p26_slope_by_year"]=s4.groupby("yr").apply(lambda x: pd.Series(dict(n=len(x),corr=np.corrcoef(x.p26,x.z)[0,1] if len(x)>3 else np.nan)))
    s5=g[(g.h==7)].dropna(subset=["rp"]).copy()
    s5["q"]=s5.groupby("coin")["rp"].transform(lambda v:pd.qcut(v,4,labels=False))
    out["h7_by_rp_quartile"]=s5.groupby("q").agg(ex_pct=("ex",lambda v:v.mean()*100),z=("z","mean"),n=("z","size"))
    out["h7_rp_corr_by_year"]=s5.groupby("yr").apply(lambda x: pd.Series(dict(n=len(x),corr=np.corrcoef(x.rp,x.z)[0,1] if len(x)>3 else np.nan)))
    out["usual_move_pct"]=g.groupby("h")["fwd"].std()*100
    return out
