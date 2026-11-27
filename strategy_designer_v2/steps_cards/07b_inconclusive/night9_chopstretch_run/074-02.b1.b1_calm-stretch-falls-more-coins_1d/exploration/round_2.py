import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin, ws in data["bars"].items():
        allr={h:[] for h in (5,10)}
        for w, b in ws.items():
            c=b["close"].values
            for h in allr:
                idx=np.arange(0,len(c)-h,h)
                allr[h]+=list(c[idx+h]/c[idx]-1)
        dr={h:np.mean(v) for h,v in allr.items()}; sd={h:np.std(v,ddof=1) for h,v in allr.items()}
        for w, b in ws.items():
            b=b.reset_index(drop=True); c=b["close"].values; n=len(b)
            cs=pd.Series(c); r=cs.pct_change(); sma=cs.rolling(20).mean(); s20=r.rolling(20).std()
            st=(((cs-sma)/sma)/s20).values
            tr60=(cs/cs.shift(60)-1).values
            r5p=(cs/cs.shift(5)-1).values
            fs=(-b["forecast"].clip(upper=0)).values
            reg=b["regime"].values
            low=np.inf; last_bet=-10**9
            bets=[]
            for i in range(n):
                if reg[i]!="unknown" or fs[i]<=0:
                    low=min(low,0.0) if np.isfinite(low) else 0.0
                    low=0.0; continue
                if not np.isfinite(low): low=fs[i]
                if fs[i]-low>=2:
                    bets.append(i); low=fs[i]
                else:
                    low=min(low,fs[i])
            seen=set()
            for i in bets:
                cell=i//5
                if cell in seen: continue
                seen.add(cell)
                d={"coin":coin,"w":w,"day":str(b.loc[i,"timestamp"])[:10],"f":fs[i],"st":st[i],"tr60":tr60[i],"r5p":r5p[i]}
                for h in (5,10):
                    if i+h<n:
                        d[f"u{h}"]=-(c[i+h]/c[i]-1-dr[h])
                rows.append(d)
    df=pd.DataFrame(rows)
    def tt(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out={}
    def dct(col):
        g=df.dropna(subset=[col]).groupby("day")[col].sum()
        dd=df.dropna(subset=[col]).groupby("day").size()
        m=g.sum()/dd.sum()
        dev=df.dropna(subset=[col]).assign(dv=lambda x:x[col]-m).groupby("day")["dv"].sum()
        G=len(dev); se=np.sqrt((dev**2).sum()*G/(G-1))/dd.sum()
        return pd.Series({"cases":dd.sum(),"days":G,"mean%":100*m,"t_day":m/se})
    out["main_like"]=pd.DataFrame({h:dct(f"u{h}") for h in ("5","10") if False} or {c_:dct(c_) for c_ in ("u5","u10")}).T
    med=df["f"].median()
    df["deep"]=np.where(df["f"]>med,"deep","shallow")
    out["median_split"]=df.groupby("deep")[["u5","u10"]].mean()*100
    df["fq"]=pd.qcut(df["f"].rank(method="first"),5,labels=False)
    out["f_quintile"]=df.groupby("fq").agg(f=("f","mean"),st=("st","mean"),n=("u5","count"),u5=("u5",lambda x:100*x.mean()),u10=("u10",lambda x:100*x.mean()))
    df["trend"]=pd.cut(df["tr60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["trend_split"]=df.groupby(["trend","deep"]).agg(n=("u5","count"),u5=("u5",lambda x:100*x.mean()),u10=("u10",lambda x:100*x.mean()))
    out["trend_main"]=df.groupby("trend")["u5"].apply(tt).unstack()
    out["corr_f_u5_by_trend"]=df.groupby("trend").apply(lambda x:x[["f","u5"]].corr().iloc[0,1])
    df["y"]=df["day"].str[:4]
    out["year_split"]=df.groupby(["y","deep"])["u5"].mean().unstack()*100
    return out
