def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; days=data["days"]
    rows=[]; anyday=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); cl=b["close"].values; n=len(b)
            endt=ts+pd.Timedelta(hours=1)
            r48p=pd.Series(cl).pct_change(48).values
            for i in range(48,n):
                pass
            idx=np.where((endt.dt.weekday==4)&(endt.dt.hour==0))[0]
            for i in idx:
                if i<48: continue
                rec={"coin":c,"win":w,"past48":r48p[i],"fc":b["forecast"].iat[i],
                     "alloc":b["postRebalance_current_allocation"].iat[i]}
                for h in (24,48,72,96):
                    rec[f"f{h}"]=cl[i+h]/cl[i]-1 if i+h<n else np.nan
                rec["sat_only"]=cl[i+48]/cl[i+24]-1 if i+48<n else np.nan
                rec["mon_tue"]=cl[i+120]/cl[i+72]-1 if i+120<n else np.nan
                rows.append(rec)
            # any weekday, 00:00 close: past 48 vs next 48, grid every 24h at hour-0 closes
            idx0=np.where(endt.dt.hour==0)[0]
            for i in idx0:
                if i<48 or i+48>=n: continue
                anyday.append({"coin":c,"wd":int(endt.iat[i].weekday()),"past48":r48p[i],"f48":cl[i+48]/cl[i]-1})
    d=pd.DataFrame(rows); a=pd.DataFrame(anyday)
    out={}
    d["pos"]=d["past48"]>0
    out["fri_by_sign"]=d.groupby("pos")[["f24","f48","f72","f96","sat_only","mon_tue","alloc"]].agg(["mean","count"]).T
    d["q"]=pd.qcut(d["past48"],5,labels=False)
    out["fri_by_quintile_past48"]=d.groupby("q")[["past48","f24","sat_only","f48","f96","mon_tue"]].mean()
    out["fri_by_coin_pos"]=d[d.pos].groupby("coin")[["f48","alloc"]].mean()
    # any weekday slope t of next48 on past48
    res={}
    for wd,g in a.dropna().groupby("wd"):
        s=stats.linregress(g["past48"],g["f48"])
        res[wd]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(g),"mean_f48_pos":g[g.past48>0]["f48"].mean(),"mean_f48_neg":g[g.past48<0]["f48"].mean()}
    out["by_weekday_00_slope"]=pd.DataFrame(res).T
    # book exposure
    ex=[];br=[]
    for c in bars:
        for w,b in bars[c].items():
            al=b["postRebalance_current_allocation"].abs()
            ex.append({"coin":c,"share_bars_in":(al>1e-6).mean(),"mean_alloc_in":al[al>1e-6].mean()})
            dd=days[c][w]; br.append(dd[["book_return","coin_return"]])
    out["exposure"]=pd.DataFrame(ex).groupby("coin").mean()
    allb=pd.concat(br)
    out["book_daily"]=pd.Series({"mean":allb.book_return.mean(),"std":allb.book_return.std(),"coin_mean":allb.coin_return.mean(),"n":len(allb)})
    tr=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items(): tr.append(t)
    t=pd.concat(tr)
    out["trades"]=pd.Series({"n":len(t),"mean_pl":t.profit_loss_percent.mean(),"mean_net":t.net_profit_loss_percent.mean(),"mean_dur_h":t.duration_minutes.mean()/60})
    return out
