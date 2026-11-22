def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=[6,12,18,36]
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            v=b["volume"].values
            sl=b.get("debug_info.components.streak_loss.last_history_value")
            vf=b.get("debug_info.components.volume_fade.last_history_value")
            sl=sl.values if sl is not None else np.full(len(c),np.nan)
            vf=vf.values if vf is not None else np.full(len(c),np.nan)
            down=np.r_[False,c[1:]<c[:-1]]
            slen=np.zeros(len(c),int)
            for i in range(1,len(c)):
                slen[i]=slen[i-1]+1 if down[i] else 0
            low=None; taken=set()
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(len(c)):
                if f[i]<=0: low=None; continue
                if low is None: low=f[i]
                low=min(low,f[i])
                if f[i]-low>=2:
                    low=f[i]
                    cell=i//18
                    if cell in taken: continue
                    taken.add(cell)
                    r={"coin":coin,"w":w,"year":yr[i],"sl":sl[i],"vf":vf[i],"slen":slen[i],"fc":f[i]}
                    for h in H:
                        r[f"x{h}"]=(c[i+h]/c[i]-1-drift[(coin,h)][0]) if i+h<len(c) else np.nan
                    r["str18"]=r["x18"]/drift[(coin,18)][1] if not np.isnan(r["x18"]) else np.nan
                    rows.append(r)
    d=pd.DataFrame(rows)
    def summ(g,col="x18"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    out["overall_by_h"]=pd.DataFrame({h:summ(d,f"x{h}") for h in H}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    d["slq"]=pd.qcut(d["sl"].rank(method="first"),5,labels=False)
    d["vfq"]=pd.qcut(d["vf"].rank(method="first"),5,labels=False)
    d["fcq"]=pd.qcut(d["fc"].rank(method="first"),5,labels=False)
    out["by_streakloss_q"]=d.groupby("slq").apply(lambda g: pd.concat([summ(g),pd.Series({"sl_med":g.sl.median()})]))
    out["by_volfade_q"]=d.groupby("vfq").apply(lambda g: pd.concat([summ(g),pd.Series({"vf_med":g.vf.median()})]))
    out["by_forecast_q"]=d.groupby("fcq").apply(lambda g: pd.concat([summ(g),summ(g,"x36").add_suffix("_36"),pd.Series({"fc_med":g.fc.median()})]))
    out["by_slen"]=d.assign(sb=d.slen.clip(upper=6)).groupby("sb").apply(summ)
    out["sl_x_vf_mean%"]=d.assign(a=d.sl>d.sl.median(),bq=d.vf>d.vf.median()).groupby(["a","bq"]).apply(summ)
    out["strength_mean"]=d["str18"].mean()
    out["corr_sl_x18_spearman"]=stats.spearmanr(d.sl,d.x18,nan_policy="omit")[0]
    out["corr_vf_x18_spearman"]=stats.spearmanr(d.vf,d.x18,nan_policy="omit")[0]
    return out
