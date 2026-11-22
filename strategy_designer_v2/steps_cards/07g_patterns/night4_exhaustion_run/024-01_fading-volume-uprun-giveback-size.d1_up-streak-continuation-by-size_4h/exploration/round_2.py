def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; bars=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change(); um=r.abs().rolling(180,min_periods=60).mean()
            sgn=np.sign(r).fillna(0).values
            L=np.zeros(len(b))
            for i in range(1,len(b)):
                L[i]=L[i-1]+sgn[i] if (sgn[i]!=0 and sgn[i]==sgn[i-1]) else sgn[i]
            k=np.abs(L).astype(int)
            sgain=np.array([c.iloc[i]/c.iloc[i-k[i]]-1 if k[i]>0 and i-k[i]>=0 else 0.0 for i in range(len(b))])
            # volume fade over streak: mean vol of last half of streak vs first half; simpler: vol last 2 vs streak-start-prior 6
            vf=np.log(v.rolling(2).mean()/v.rolling(6).mean())
            r42=(c/c.shift(42)-1)/(um*np.sqrt(42))
            ts=pd.to_datetime(b["timestamp"]); yr=ts.dt.year
            for i in range(0,len(b)-18,18):
                rows.append(dict(coin=coin,w=w,yr=yr.iloc[i],f18=c.iloc[i+18]/c.iloc[i]-1,
                   f6=c.iloc[i+6]/c.iloc[i]-1,L=L[i],sg=sgain[i]/um.iloc[i] if um.iloc[i]>0 else np.nan,
                   vf=vf.iloc[i],r42=r42.iloc[i],r1=r.iloc[i]/um.iloc[i] if um.iloc[i]>0 else np.nan))
            bb=pd.DataFrame(dict(coin=coin,w=w,yr=yr,hour=ts.dt.hour,wd=ts.dt.weekday,rn=r.shift(-1),r1s=r/um,
                r6n=(c.shift(-6)/c-1)))
            bb.loc[bb.index%6!=0,"r6n"]=np.nan
            bars.append(bb)
    G=pd.DataFrame(rows); B=pd.concat(bars)
    sd=G.groupby("coin")["f18"].transform("std")
    G["exz"]=(G.f18-G.groupby("coin")["f18"].transform("mean"))/sd
    G["ex6"]=(G.f6-G.groupby("coin")["f6"].transform("mean"))/G.groupby("coin")["f6"].transform("std")
    out={}
    # r42 momentum robustness
    d=G.dropna(subset=["r42"]).copy()
    out["r42_corr_by_year"]=d.groupby("yr").apply(lambda x: pd.Series(dict(n=len(x),slope_t=stats.linregress(x.r42,x.exz).slope/stats.linregress(x.r42,x.exz).stderr))).round(2)
    out["r42_corr_by_coin"]=d.groupby("coin").apply(lambda x: pd.Series(dict(n=len(x),corr=np.corrcoef(x.r42,x.exz)[0,1],t=stats.linregress(x.r42,x.exz).slope/stats.linregress(x.r42,x.exz).stderr))).round(3)
    lr=stats.linregress(d.r42,d.exz); out["r42_pooled_slope_t"]=round(lr.slope/lr.stderr,2)
    # down streaks with fading volume, graded
    dn=G[(G.L<=-2)].dropna(subset=["vf","sg"]).copy()
    dn["fade"]=-dn.vf  # positive = fading
    dn["score"]=(-dn.sg)*dn.fade
    for col in ["fade","sg","score"]:
        lr=stats.linregress(dn[col],dn.exz); out["down_slope_t_"+col]=round(lr.slope/lr.stderr,2)
    lo=dn[dn.fade<=dn.fade.median()].exz; hi=dn[dn.fade>dn.fade.median()].exz
    out["down_fade_minus_rising"]=pd.Series(dict(diff=hi.mean()-lo.mean(),t=stats.ttest_ind(hi,lo,equal_var=False)[0],n=len(dn))).round(3)
    out["down_fade_by_year"]=dn.assign(h=(dn.fade>dn.fade.median()).astype(int)).groupby(["yr","h"])["exz"].mean().unstack().round(3)
    out["down_fade_by_coin"]=dn.assign(h=(dn.fade>dn.fade.median()).astype(int)).groupby(["coin","h"])["exz"].mean().unstack().round(3)
    up=G[(G.L>=2)].dropna(subset=["vf"]).copy()
    lo=up[up.vf<=up.vf.median()].exz; hi=up[up.vf>up.vf.median()].exz
    out["up_rising_minus_fading"]=pd.Series(dict(diff=hi.mean()-lo.mean(),t=stats.ttest_ind(hi,lo,equal_var=False)[0],n=len(up))).round(3)
    # large single-bar drop rebound over next day, non-overlapping 6-bar grid
    Bg=B.dropna(subset=["r6n","r1s"]).copy()
    Bg["z6"]=Bg.groupby("coin")["r6n"].transform(lambda x:(x-x.mean())/x.std())
    Bg["bq"]=pd.cut(Bg.r1s,[-99,-3,-2,-1,1,2,3,99])
    t=Bg.groupby("bq")["z6"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); out["after_1bar_next1day"]=t[["mean","count","t"]].round(3)
    neg=Bg[Bg.r1s<0]; lr=stats.linregress(neg.r1s,neg.z6); out["drop_size_slope_t_1day"]=round(lr.slope/lr.stderr,2)
    out["bigdrop_by_coin"]=Bg[Bg.r1s<=-2].groupby("coin")["z6"].agg(["mean","count"]).round(3)
    out["bigdrop_by_year"]=Bg[Bg.r1s<=-2].groupby("yr")["z6"].agg(["mean","count"]).round(3)
    # hour effect robustness
    B["z"]=B.groupby("coin")["rn"].transform(lambda x:(x-x.mean())/x.std())
    out["hour_by_coin"]=B.groupby(["coin","hour"])["z"].mean().unstack().round(3)
    out["hour_by_year"]=B.groupby(["yr","hour"])["z"].mean().unstack().round(3)
    return out
