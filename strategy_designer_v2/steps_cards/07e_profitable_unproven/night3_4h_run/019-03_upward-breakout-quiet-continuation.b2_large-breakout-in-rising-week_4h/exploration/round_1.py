def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; trades=data["trades"]
    out={}
    rows=[];case_rows=[]
    for c in bars:
        # coin drift per bar and per h
        allr=[]
        for w,b in bars[c].items():
            allr.append(b["close"].pct_change().dropna())
        mu=pd.concat(allr).mean()
        drift={}
        for h in (6,18,36,72):
            v=[]
            for w,b in bars[c].items():
                cl=b["close"].values
                idx=np.arange(0,len(cl)-h,h)
                v+=list(cl[idx+h]/cl[idx]-1)
            drift[h]=np.mean(v)
        for w,b in bars[c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            r=np.append(cl[1:]/cl[:-1]-1,np.nan)
            a=b["postRebalance_current_allocation"].fillna(0).values
            g=a*r; m=a*mu
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            r42=pd.Series(cl).pct_change(42).values
            for i in range(len(b)-1):
                pass
            df=pd.DataFrame({"g":g[:-1],"m":m[:-1],"yr":yr[:-1],"in":(a[:-1]!=0)})
            s=df.groupby("yr")[["g","m"]].sum()
            for y,rr in s.iterrows():
                rows.append((c,w,y,rr.g,rr.m,df["in"].mean()))
            f=b["forecast"].fillna(0).values
            prev=np.append(0,f[:-1])
            ent=(f>0)&(prev<=0)
            for h in (6,18,36,72):
                seen=set()
                for i in np.where(ent)[0]:
                    cell=i//18
                    if cell in seen or i+h>=len(cl): continue
                    seen.add(cell)
                    case_rows.append((c,w,yr[i],h,cl[i+h]/cl[i]-1-drift[h],f[i],r42[i]))
            # regime-only grid: 18-bar from grid bars with r42>0 vs <=0
            for i in range(0,len(cl)-18,18):
                if np.isnan(r42[i]): continue
                case_rows.append((c,w,yr[i],-18 if r42[i]>0 else -180,cl[i+18]/cl[i]-1-drift[18],f[i],r42[i]))
    R=pd.DataFrame(rows,columns=["c","w","yr","g","m","inshare"])
    out["by_coin"]=R.groupby("c")[["g","m"]].sum().assign(timing=lambda d:d.g-d.m)
    out["by_year"]=R.groupby("yr")[["g","m"]].sum().assign(timing=lambda d:d.g-d.m)
    W=R.groupby("w")[["g","m"]].sum(); W["timing"]=W.g-W.m
    out["by_window"]=W
    out["in_market_share"]=R.inshare.mean()
    C=pd.DataFrame(case_rows,columns=["c","w","yr","h","u","f","r42"])
    def summ(d):
        return pd.Series({"n":len(d),"mean":d.u.mean(),"t":d.u.mean()/(d.u.std()/np.sqrt(len(d))) if len(d)>2 else np.nan})
    out["entries_by_h"]=C.groupby("h").apply(summ)
    e18=C[C.h==18].copy()
    e18["fbin"]=pd.qcut(e18.f.rank(method="first"),4,labels=False)
    e18["rbin"]=pd.qcut(e18.r42.rank(method="first"),4,labels=False)
    out["e18_by_forecast_q"]=e18.groupby("fbin").apply(summ).join(e18.groupby("fbin").f.mean())
    out["e18_by_r42_q"]=e18.groupby("rbin").apply(summ).join(e18.groupby("rbin").r42.mean())
    out["e18_by_coin"]=e18.groupby("c").apply(summ)
    out["e18_by_year"]=e18.groupby("yr").apply(summ)
    g=C[C.h==-18].copy()
    g["rbin"]=pd.qcut(g.r42.rank(method="first"),4,labels=False)
    out["grid_r42pos_by_q"]=g.groupby("rbin").apply(summ).join(g.groupby("rbin").r42.mean())
    gf=g.copy(); gf["brk"]=gf.f>0
    out["grid_r42pos_break_vs_not"]=gf.groupby("brk").apply(summ)
    # trades
    T=pd.concat([t.assign(c=c) for c in trades for t in trades[c].values()])
    p=T.net_profit_loss_percent.sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(T),"sum_net":p.sum(),"top10_sum":p.head(10).sum(),"top50_sum":p.head(50).sum(),"win_share":(p>0).mean(),"mean_dur_h":T.duration_minutes.mean()/60})
    return out
