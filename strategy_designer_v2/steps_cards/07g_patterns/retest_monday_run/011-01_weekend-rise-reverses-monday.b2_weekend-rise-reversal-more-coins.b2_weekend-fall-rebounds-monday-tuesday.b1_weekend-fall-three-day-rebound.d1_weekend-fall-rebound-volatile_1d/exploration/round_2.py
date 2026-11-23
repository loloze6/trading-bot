import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        g3=[]
        for w, b in wins.items():
            c=b["close"].values
            n=min(len(c[0::3]),len(c[3::3]))
            g3+=list(c[3::3][:n]/c[0::3][:n]-1)
        m3=np.mean(g3)
        for w, b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["date"]=ts.dt.floor("D").values
            b["wd"]=ts.dt.weekday.values; b["year"]=ts.dt.year.values
            c=b["close"]
            b["r1"]=c/c.shift(1)-1
            b["vol20"]=b["r1"].rolling(20).std()
            b["z"]=b["r1"]/b["vol20"]
            b["vr"]=b["volume"]/b["volume"].rolling(20).mean().shift(1)
            b["vr2"]=(b["volume"]+b["volume"].shift(1))/(2*b["volume"].rolling(20).mean().shift(2))
            b["f3"]=c.shift(-3)/c-1
            b["x3"]=b["f3"]-m3
            b["x3s"]=b["x3"]/(b["vol20"]*np.sqrt(3))
            b["f1"]=c.shift(-1)/c-1
            b["coin"]=coin; b["win"]=w
            rows.append(b[["coin","win","date","wd","year","r1","z","vr","vr2","f1","x3","x3s"]])
    D=pd.concat(rows).dropna(subset=["z","x3"])
    out={}
    # clustered by date: per-date cross-coin mean, then t over dates
    res=[]
    for d,g in D.groupby("wd"):
        dm=g.groupby("date").agg(f1=("f1","mean"),x3=("x3","mean"))
        # per-date slope proxy: mean of z*x3s per date
        g=g.assign(p=g.z*g.x3s)
        pm=g.groupby("date")["p"].mean()
        fall=g[g.z<-1].groupby("date")["x3"].mean()
        res.append([d,len(dm),dm.f1.mean(),stats.ttest_1samp(dm.f1,0).statistic,pm.mean(),stats.ttest_1samp(pm,0).statistic,fall.mean(),stats.ttest_1samp(fall,0).statistic,len(fall)])
    out["clustered_by_date"]=pd.DataFrame(res,columns=["wd","dates","f1","f1_t","z_x3s","zx_t","fall_x3","fall_t","fall_dates"])
    # Friday bar: graded slope by year and continuous, Thursday/Friday grades
    F=D[D.wd==4]
    res=[]
    for y,g in F.groupby("year"):
        s=stats.linregress(g.z,g.x3s); res.append([y,len(g),s.slope,s.slope/s.stderr])
    out["friday_slope_by_year"]=pd.DataFrame(res,columns=["year","n","slope","t"])
    Fq=F.groupby(pd.qcut(F.z,5,labels=False))["x3"].agg(["mean","count"])
    out["friday_z_quintile_x3"]=Fq
    # Sunday: graded z x volume interaction, continuous
    S=D[(D.wd==6)].dropna(subset=["vr2"])
    S=S.assign(lv=np.log(S.vr2))
    X=np.column_stack([np.ones(len(S)),S.z,S.lv,S.z*S.lv])
    beta,res_,_,_=np.linalg.lstsq(X,S.x3s.values,rcond=None)
    e=S.x3s.values-X@beta; s2=e@e/(len(S)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["sunday_z_vol_interaction"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z","logvr2","z*logvr2"])
    # same for weekday bars (Mon-Thu) for comparison
    W=D[D.wd.isin([0,1,2,3])].dropna(subset=["vr"])
    W=W.assign(lv=np.log(W.vr))
    X=np.column_stack([np.ones(len(W)),W.z,W.lv,W.z*W.lv])
    beta,_,_,_=np.linalg.lstsq(X,W.x3s.values,rcond=None)
    e=W.x3s.values-X@beta; s2=e@e/(len(W)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["weekday_z_vol_interaction"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z","logvr","z*logvr"])
    # Sunday clustered: per-date z*x3s for low-volume half vs high
    S["lowv"]=S.lv<S.groupby("coin").lv.transform("median")
    res=[]
    for k,g in S.groupby("lowv"):
        pm=(g.z*g.x3s).groupby(g.date).mean()
        res.append([k,len(pm),pm.mean(),stats.ttest_1samp(pm,0).statistic])
    out["sunday_lowvol_clustered"]=pd.DataFrame(res,columns=["lowvol","dates","z_x3s","t"])
    # Friday-close-to-Monday-close continuation by volume
    F2=F.dropna(subset=["vr"]); F2=F2.assign(lv=np.log(F2.vr))
    X=np.column_stack([np.ones(len(F2)),F2.z,F2.lv,F2.z*F2.lv])
    beta,_,_,_=np.linalg.lstsq(X,F2.x3s.values,rcond=None)
    e=F2.x3s.values-X@beta; s2=e@e/(len(F2)-4); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["friday_z_vol_interaction"]=pd.DataFrame({"beta":beta,"t":beta/se},index=["c","z","logvr","z*logvr"])
    # book: worst window chain drawdown per window
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            dd.append(d.assign(coin=coin,win=w))
    DD=pd.concat(dd).dropna(subset=["book_return"])
    B=DD.groupby(["win","day"]).book_return.mean().reset_index()
    res=[]
    for w,g in B.groupby("win"):
        v=(1+g.book_return).cumprod(); mdd=(v/v.cummax()-1).min()
        res.append([w,len(g),g.book_return.sum(),mdd])
    out["book_by_window"]=pd.DataFrame(res,columns=["win","days","sum_ret","maxdd"]).sort_values("maxdd").head(12)
    return out
