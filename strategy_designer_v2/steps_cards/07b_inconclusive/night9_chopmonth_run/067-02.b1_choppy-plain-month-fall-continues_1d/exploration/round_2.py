def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=7
    rows=[]; drift={}
    for coin,ws in data["bars"].items():
        allr=[]
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; n=len(c)
            ts=pd.to_datetime(df["timestamp"])
            r30=pd.Series(c).pct_change(30).values
            r60=pd.Series(c).pct_change(60).values
            f=df["forecast"].values
            for i in range(0,n-H,H):
                fr=c[i+H]/c[i]-1; allr.append(fr)
                rows.append(dict(coin=coin,w=w,day=ts[i].normalize(),f=f[i],r30=r30[i],r60=r60[i],fr=fr,
                    fr10=(c[i+10]/c[i]-1) if i+10<n else np.nan,fr5=(c[i+5]/c[i]-1) if i+5<n else np.nan))
        drift[coin]=np.mean(allr)
    d=pd.DataFrame(rows)
    d["ex"]=d["fr"]-d["coin"].map(drift)
    def ct(x,day):
        x=pd.Series(x).reset_index(drop=True); day=pd.Series(day).reset_index(drop=True)
        g=pd.DataFrame({"x":x-x.mean(),"d":day}).groupby("d").x.sum()
        D=len(g); se=np.sqrt((g**2).sum()*D/(D-1))/len(x)
        return pd.Series(dict(n=len(x),mean=x.mean(),t=x.mean()/se,days=D))
    out={}
    s=d[d.f<0].copy(); s["sx"]=-s.ex
    s["sxw"]=(-s.f/10)*s.sx   # correctly signed weighted short gain
    out["weighted_short_gain_correct_sign"]=ct(s.sxw,s.day)
    out["plain_depth_weighted"]=ct(-s.r30.clip(upper=0)*10*s.sx,s.day)
    out["deep_r30_lt_-0.1"]=ct(s[s.r30<-0.1].sx,s[s.r30<-0.1].day)
    out["shallow_r30_ge_-0.1"]=ct(s[s.r30>=-0.1].sx,s[s.r30>=-0.1].day)
    out["spearman_depth_sx"]=pd.Series(dict(r30_vs_sx=stats.spearmanr(-s.r30,s.sx)[0],f_vs_sx=stats.spearmanr(-s.f,s.sx)[0],
        r30_vs_f=stats.spearmanr(s.r30,s.f)[0]))
    out["by_half_window_split"]=s.assign(g=s.w.str[1:].astype(int)<=12).groupby("g").sx.agg(["size","mean"])
    s["deep"]=s.r30<-0.1
    out["deep_by_window"]=s[s.deep].groupby("w").sx.agg(["size","mean"])
    out["coin_drift_7d_mean"]=pd.Series(drift).mean()
    return out
