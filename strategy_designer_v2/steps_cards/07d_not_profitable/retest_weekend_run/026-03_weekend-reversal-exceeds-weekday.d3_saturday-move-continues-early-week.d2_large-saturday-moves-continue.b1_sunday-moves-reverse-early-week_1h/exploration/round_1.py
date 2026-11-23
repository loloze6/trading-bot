def explore(data):
    import numpy as np, pandas as pd
    rows=[]; trades=[]
    H=[24,48,72,120]
    for coin,ws in data["bars"].items():
        drift={}
        for h in H:
            rr=[]
            for w,b in ws.items():
                c=b["close"].values.astype(float)
                idx=np.arange(0,len(c)-h,h)
                rr.append(c[idx+h]/c[idx]-1)
            drift[h]=np.nanmean(np.concatenate(rr))
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])+pd.Timedelta(hours=1)
            c=b["close"].values.astype(float); n=len(c)
            r24=pd.Series(c).pct_change(24)
            scale=r24.abs().rolling(720,min_periods=200).mean()
            z=(r24/scale).values
            r720=pd.Series(c).pct_change(720).values
            vol=pd.Series(c).pct_change().rolling(720,min_periods=200).std().values
            fc=b["forecast"].values
            alloc=b["postRebalance_current_allocation"].values
            hrs=ts.dt.hour.values; wds=ts.dt.weekday.values; yrs=ts.dt.year.values
            for i in np.where(hrs==0)[0]:
                if np.isnan(z[i]): continue
                d={"coin":coin,"w":w,"wd":wds[i],"year":yrs[i],"z":z[i],
                   "fc":fc[i],"alloc":alloc[i],"tr30":r720[i],"vol":vol[i]}
                for h in H:
                    d[f"r{h}"]=c[i+h]/c[i]-1-drift[h] if i+h<n else np.nan
                rows.append(d)
        for w,t in data["trades"][coin].items():
            t=t.copy(); t["coin"]=coin; trades.append(t)
    df=pd.DataFrame(rows)
    df["vq"]=df.groupby("coin")["vol"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    out={}
    def summ(g,h=48):
        x=(-np.sign(g["z"])*g[f"r{h}"]).dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["by_weekday_h48"]=df.groupby("wd").apply(summ)
    mon=df[df.wd==0].copy()
    mon["zq"]=pd.qcut(mon["z"].abs(),5,labels=False)
    out["mon_by_absz_quint"]=mon.groupby("zq").apply(lambda g: pd.concat([summ(g),pd.Series({"absz":g.z.abs().mean()})]))
    out["mon_by_horizon"]=pd.DataFrame({h:summ(mon,h) for h in H}).T
    mon["side"]=np.where(mon.z>0,"short_after_rise","long_after_fall")
    out["mon_by_side"]=mon.groupby("side").apply(summ)
    out["mon_by_year"]=mon.groupby("year").apply(summ)
    out["mon_by_coin"]=mon.groupby("coin").apply(summ)
    mon["trend"]=np.where(np.sign(mon.tr30)==np.sign(mon.z),"move_with_30d_trend","move_against_30d_trend")
    out["mon_by_trend"]=mon.groupby("trend").apply(summ)
    out["mon_by_volterc"]=mon.groupby("vq").apply(summ)
    oth=df[df.wd.isin([1,2,3,4,5])].copy()
    oth["trend"]=np.where(np.sign(oth.tr30)==np.sign(oth.z),"with","against")
    out["other_days_by_trend"]=oth.groupby("trend").apply(summ)
    out["mon_abs_alloc_mean"]=float(mon["alloc"].abs().mean())
    T=pd.concat(trades)
    T["fq"]=pd.qcut(T["entry_forecast"].abs(),4,labels=False,duplicates="drop")
    agg=dict(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_h=("duration_minutes",lambda s:s.mean()/60))
    out["trades_by_absforecast"]=T.groupby("fq").agg(absf=("entry_forecast",lambda s:s.abs().mean()),**agg)
    out["trades_by_side"]=T.groupby("side").agg(**agg)
    return out
