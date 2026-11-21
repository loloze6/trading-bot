def explore(data):
    import numpy as np, pandas as pd
    H=240
    out={}
    rows=[]
    for coin,ws in data["bars"].items():
        recs=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            r24=c/c.shift(24)-1
            mav=r24.abs().rolling(720,min_periods=500).mean()
            z=r24/mav
            r720=c/c.shift(720)-1
            r240p=c/c.shift(240)-1
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(c),H)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z.values[idx],"r720":r720.values[idx],
                            "r240p":r240p.values[idx],"mav":mav.values[idx],
                            "fwd":fwd.values[idx],"year":ts.dt.year.values[idx],
                            "wd":ts.dt.weekday.values[idx],
                            "fc":b["forecast"].astype(float).values[idx],
                            "alloc":b["postRebalance_current_allocation"].astype(float).values[idx]})
            recs.append(d)
        d=pd.concat(recs,ignore_index=True)
        drift=d["fwd"].mean(); sd=d["fwd"].std()
        d["unu"]=d["fwd"]-drift
        d["str"]=d["unu"]/sd
        for col in ["r720","r240p","mav","z"]:
            d[col+"_rk"]=d[col].rank(pct=True)
        rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D[D["fwd"].notna()].reset_index(drop=True)
    def summ(g):
        x=g["unu"].dropna(); n=len(x)
        return pd.Series({"n":n,"mean_unu":x.mean(),
            "t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"strength":g["str"].mean()})
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err: "+str(e)[:80]
    safe("by_z24",lambda: D.dropna(subset=["z"]).assign(zb=lambda x: pd.cut(x["z"],[-np.inf,-3,-2,-1,0,1,2,3,np.inf]).astype(str)).groupby("zb").apply(summ))
    safe("big_z_by_prior",lambda: D[(D["z"].abs()>2)&D["r720"].notna()].assign(
        s=lambda x: np.where(x["z"]>0,"up24","down24"),p=lambda x: np.where(x["r720"]>0,"r30up","r30down")).groupby(["s","p"]).apply(summ))
    safe("by_r30d_quintile",lambda: D.dropna(subset=["r720"]).assign(q=lambda x:(x["r720_rk"]*5).clip(upper=4.999).astype(int)).groupby("q").apply(summ))
    safe("by_r10d_quintile",lambda: D.dropna(subset=["r240p"]).assign(q=lambda x:(x["r240p_rk"]*5).clip(upper=4.999).astype(int)).groupby("q").apply(summ))
    safe("by_vol_tercile",lambda: D.dropna(subset=["mav"]).assign(q=lambda x:(x["mav_rk"]*3).clip(upper=2.999).astype(int)).groupby("q").apply(summ))
    safe("vol_x_r30",lambda: D.dropna(subset=["mav","r720"]).assign(v=lambda x:(x["mav_rk"]*3).clip(upper=2.999).astype(int),
        p=lambda x:(x["r720_rk"]*3).clip(upper=2.999).astype(int)).groupby(["v","p"]).apply(summ))
    safe("by_year",lambda: D.groupby("year").apply(summ))
    safe("by_coin",lambda: D.groupby("coin").apply(summ))
    safe("by_weekday",lambda: D.groupby("wd").apply(summ))
    safe("in_vs_flat",lambda: D.assign(s=lambda x: np.where(x["alloc"].abs()>1e-6,"in","flat")).groupby("s").apply(summ))
    # book
    def book():
        dl=[]
        for coin,ws in data["days"].items():
            for w,dd in ws.items():
                x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; dl.append(x)
        DD=pd.concat(dl,ignore_index=True).dropna()
        day=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
        day["year"]=pd.to_datetime(day["day"]).dt.year
        return day
    try:
        day=book()
        out["book_by_year"]=day.groupby("year").agg(n=("book_return","size"),book_mean=("book_return","mean"),
            book_sd=("book_return","std"),coin_mean=("coin_return","mean"))
        out["book_by_window"]=day.groupby("w").agg(book_sum=("book_return","sum"),coin_sum=("coin_return","sum"),worst=("book_return","min"))
        q=day["book_return"].quantile([0.01,0.99])
        out["book_tail"]=pd.Series({"q01":q.iloc[0],"q99":q.iloc[1],
            "share_gain_top1pct":day.loc[day["book_return"]>=q.iloc[1],"book_return"].sum()/day["book_return"].sum(),
            "coin_mean_on_worst1pct":day.loc[day["book_return"]<=q.iloc[0],"coin_return"].mean()})
    except Exception as e: out["book"]="err: "+str(e)[:80]
    try:
        tl=[]
        for coin,ws in data["trades"].items():
            for w,t in ws.items():
                if len(t): x=t.copy(); x["coin"]=coin; tl.append(x)
        T=pd.concat(tl,ignore_index=True)
        T["fq"]=(T["entry_forecast"].rank(pct=True)*4).clip(upper=3.999).astype(int)
        out["trades_by_fc_quartile"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),
            fc=("entry_forecast","mean"),pnl=("net_profit_loss_percent","mean"),
            med=("net_profit_loss_percent","median"),days=("duration_minutes",lambda s:s.mean()/1440))
        T["h6"]=pd.to_datetime(T["entry_time"]).dt.hour//6
        out["trades_by_entry_6h"]=T.groupby("h6")["net_profit_loss_percent"].agg(["size","mean","median"])
        out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["size","mean","median"])
    except Exception as e: out["trades"]="err: "+str(e)[:80]
    return out
