def explore(data):
    import numpy as np, pandas as pd
    H=[6,12,18,36]
    drift={}
    for coin,ws in data["bars"].items():
        for h in H:
            rs=[]
            for w,b in ws.items():
                c=b["close"].values
                idx=np.arange(0,len(c)-h,h)
                rs+=list(c[idx+h]/c[idx]-1)
            drift[(coin,h)]=(np.mean(rs),np.std(rs))
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values
            sl=b["debug_info.components.streak_loss.last_history_value"].values
            vf=b["debug_info.components.volume_fade.last_history_value"].values
            down=np.r_[False,c[1:]<c[:-1]]
            slen=np.zeros(len(c),int)
            for i in range(1,len(c)):
                slen[i]=slen[i-1]+1 if down[i] else 0
            low=None; taken=set()
            for i in range(len(c)):
                if f[i]<=0: low=None; continue
                if low is None: low=f[i]
                low=min(low,f[i])
                if f[i]-low>=2:
                    low=f[i]; cell=i//18
                    if cell in taken: continue
                    taken.add(cell)
                    r={"coin":coin,"sl":sl[i],"vf":vf[i],"slen":slen[i],
                       "tr30":(c[i]/c[i-180]-1) if i>=180 else np.nan,
                       "tr7":(c[i]/c[i-42]-1) if i>=42 else np.nan}
                    for h in H:
                        r[f"x{h}"]=(c[i+h]/c[i]-1-drift[(coin,h)][0]) if i+h<len(c) else np.nan
                    rows.append(r)
    d=pd.DataFrame(rows)
    def summ(g,col="x18"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    d["tr30s"]=np.where(d.tr30.isna(),"na",np.where(d.tr30>0,"up30","down30"))
    d["tr7s"]=np.where(d.tr7.isna(),"na",np.where(d.tr7>0,"up7","down7"))
    out["by_trend30"]=d.groupby("tr30s").apply(summ)
    out["by_trend7"]=d.groupby("tr7s").apply(summ)
    d["slq"]=pd.qcut(d["sl"].rank(method="first"),5,labels=False)
    out["trend30_x_slq"]=d[d.tr30s!="na"].groupby(["tr30s","slq"]).apply(summ)
    d["sld"]=pd.qcut(d["sl"].rank(method="first"),10,labels=False)
    out["top_sl_deciles_by_h"]=pd.concat({h:d[d.sld>=8].groupby("sld").apply(lambda g: summ(g,f"x{h}")) for h in H})
    d["t30q"]=pd.qcut(d["tr30"].rank(method="first"),5,labels=False)
    out["by_tr30_q"]=d.dropna(subset=["tr30"]).groupby("t30q").apply(lambda g: pd.concat([summ(g),pd.Series({"tr30_med%":100*g.tr30.median()})]))
    out["slen_by_slq"]=d.groupby("slq").slen.mean()
    return out
