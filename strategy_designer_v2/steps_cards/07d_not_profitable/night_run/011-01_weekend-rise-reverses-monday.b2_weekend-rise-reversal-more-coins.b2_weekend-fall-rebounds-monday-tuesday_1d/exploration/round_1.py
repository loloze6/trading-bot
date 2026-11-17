def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; dayrows=[]
    # coin mean daily return over all windows
    for coin, wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            c=b["close"].values; allr.append(pd.Series(c).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); wd=ts.dt.weekday.values
            c=b["close"].values; n=len(c)
            f=b["forecast"].fillna(0).values
            pos=b["postRebalance_current_allocation"].fillna(0).values
            r1d=pd.Series(c).pct_change().values
            for t in range(n):
                if wd[t]!=6: continue
                d={"coin":coin,"w":w,"f":f[t],"pos":pos[t],"wkend":r1d[t],"mu":mu}
                for h in (1,2,3,5):
                    d[f"r{h}"]=c[t+h]/c[t]-1-h*mu if t+h<n else np.nan
                d["tr20"]=c[t]/c[t-20]-1 if t>=20 else np.nan
                d["tr60"]=c[t]/c[t-60]-1 if t>=60 else np.nan
                d["vol"]=pd.Series(r1d[max(1,t-29):t+1]).std()
                d["fri_sat"]=c[t]/c[t-2]-1 if t>=2 else np.nan
                rows.append(d)
        for w,dd in data["days"][coin].items():
            x=dd.copy(); x["coin"]=coin; x["w"]=w; dayrows.append(x)
    df=pd.DataFrame(rows); act=df[df.f>0].copy()
    out={}
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out["active_excess_by_h"]=pd.DataFrame({f"r{h}":tt(act[f"r{h}"]) for h in (1,2,3,5)})
    out["inactive_sundays_by_h"]=pd.DataFrame({f"r{h}":tt(df[df.f<=0][f"r{h}"]) for h in (1,2,3,5)})
    act["fq"]=pd.qcut(act.f,3,labels=["lo","mid","hi"])
    out["by_forecast_tercile"]=act.groupby("fq")[["r1","r2","r3","pos","wkend"]].mean()
    act["trend"]=np.where(act.tr20>0,"up20","down20")
    g=act.groupby("trend")
    out["by_trend20"]=pd.concat([g["r1"].apply(lambda s:tt(s)).unstack(), g["r2"].mean().rename("r2")],axis=1)
    act["trend60"]=np.where(act.tr60>0,"up60","down60")
    g=act.groupby("trend60")
    out["by_trend60"]=pd.concat([g["r1"].apply(lambda s:tt(s)).unstack(), g["r2"].mean().rename("r2")],axis=1)
    act["fs"]=np.where(act.fri_sat<0,"2d_down","2d_up")
    out["by_fri_sat"]=act.groupby("fs")["r2"].apply(lambda s:tt(s)).unstack()
    D=pd.concat(dayrows); D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"]=D.groupby("wd")[["book_return","coin_return"]].mean()
    out["share_days_nonzero_book"]=float((D.book_return.abs()>1e-9).mean())
    out["mean_pos_active"]=float(act.pos.mean())
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=pd.Series({"n":len(tr),"pl_gross":tr.profit_loss_percent.mean(),"pl_net":tr.net_profit_loss_percent.mean(),"dur_h":tr.duration_minutes.mean()/60})
    out["by_year_r2"]=act.assign(y=pd.to_datetime(act.index.map(lambda i:0)) if False else 0).groupby("coin")["r2"].mean()
    return out
