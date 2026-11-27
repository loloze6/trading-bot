import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; drift={}
    for coin, ws in data["bars"].items():
        allr={h:[] for h in (1,3,5,10)}
        for w, b in ws.items():
            c=b["close"].values
            for h in allr:
                idx=np.arange(0,len(c)-h,h)
                allr[h]+=list(c[idx+h]/c[idx]-1)
        dr={h:np.mean(v) for h,v in allr.items()}; sd={h:np.std(v,ddof=1) for h,v in allr.items()}
        for w, b in ws.items():
            b=b.reset_index(drop=True); c=b["close"]
            r=c.pct_change(); sma=c.rolling(20).mean(); s20=r.rolling(20).std()
            stretch=((c-sma)/sma)/s20
            tr60=c/c.shift(60)-1
            n=len(b)
            for i in range(0,n-5,5):
                f=b.loc[i,"forecast"]
                if not (b.loc[i,"regime"]=="unknown" and f<0): continue
                d={"coin":coin,"w":w,"year":pd.Timestamp(b.loc[i,"timestamp"]).year,"f":abs(f),"st":stretch[i],"tr60":tr60[i],"day":b.loc[i,"timestamp"]}
                for h in (1,3,5,10):
                    if i+h<n:
                        d[f"u{h}"]=-(c[i+h]/c[i]-1-dr[h]); d[f"z{h}"]=d[f"u{h}"]/sd[h]
                rows.append(d)
    df=pd.DataFrame(rows)
    out={}
    def tt(x): x=x.dropna(); return pd.Series({"n":len(x),"mean%":100*x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["by_horizon"]=pd.DataFrame({h:tt(df[f"u{h}"]) for h in (1,3,5,10)}).T
    df["fq"]=pd.qcut(df["f"],5,labels=False,duplicates="drop")
    out["by_forecast_quintile_u5"]=df.groupby("fq")["u5"].apply(tt).unstack()
    df["sq"]=pd.qcut(df["st"],5,labels=False,duplicates="drop")
    out["by_raw_stretch_quintile_u5"]=df.groupby("sq").agg(st=("st","mean"),n=("u5","count"),m=("u5",lambda x:100*x.mean()),m10=("u10",lambda x:100*x.mean()))
    out["by_coin_u5"]=df.groupby("coin")["u5"].apply(tt).unstack()
    out["by_year_u5"]=df.groupby("year")["u5"].apply(tt).unstack()
    df["trend"]=pd.cut(df["tr60"],[-9,-0.1,0.1,99],labels=["falling","choppy","rising"])
    out["by_trend_u5"]=df.groupby("trend")["u5"].apply(tt).unstack()
    out["by_trend_u10"]=df.groupby("trend")["u10"].apply(tt).unstack()
    out["corr_f_u5"]=float(df[["f","u5"]].corr().iloc[0,1])
    out["corr_st_u5"]=float(df[["st","u5"]].corr().iloc[0,1])
    return out
