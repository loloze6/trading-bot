def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            c=b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        drift=pd.concat(allr).mean() if allr else 0
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float).values
            r=pd.Series(c).pct_change()
            sd=r.rolling(30).std()
            n=len(c)
            fc=b["forecast"].astype(float).values
            for i in np.where(fc<0)[0]:
                d={"coin":coin,"w":w,"day":str(b["timestamp"].iloc[i])[:10],
                   "year":str(b["timestamp"].iloc[i])[:4],
                   "fc":-float(fc[i]),
                   "today_z":r.iloc[i]/sd.iloc[i] if sd.iloc[i]>0 else np.nan,
                   "f4":(c[i-1]/c[i-5]-1)/sd.iloc[i] if i>=5 and sd.iloc[i]>0 else np.nan}
                for h in [1,2,3,5]:
                    d[f"u{h}"]= -(c[i+h]/c[i]-1-drift*h) if i+h<n else np.nan
                d["tot1"]= -(c[i+1]/c[i]-1) if i+1<n else np.nan
                rows.append(d)
    df=pd.DataFrame(rows)
    def stat(g,col="u1"):
        x=g.dropna(subset=[col])
        G=x["day"].nunique()
        if G<3 or len(x)<3: return pd.Series({"n":len(x),"days":G,"mean":x[col].mean(),"t":np.nan})
        m=x[col].mean(); dev=(x[col]-m).groupby(x["day"]).sum()
        se=np.sqrt((dev**2).sum()*G/(G-1))/len(x)
        return pd.Series({"n":len(x),"days":G,"mean":m,"t":m/se})
    out={}
    out["all_by_h"]=pd.DataFrame({c:stat(df,c) for c in ["u1","u2","u3","u5","tot1"]}).T
    out["by_coin"]=df.groupby("coin").apply(stat)
    out["by_year"]=df.groupby("year").apply(stat)
    out["by_window"]=df.groupby("w").apply(stat)
    df["fcq"]=pd.qcut(df["fc"].rank(method="first"),4,labels=["q1low","q2","q3","q4high"])
    out["by_fc_q"]=df.groupby("fcq").apply(stat)
    out["by_fc_q_u3"]=df.groupby("fcq").apply(lambda g:stat(g,"u3"))
    d2=df.dropna(subset=["today_z"])
    d2["tq"]=pd.qcut(d2["today_z"].rank(method="first"),4,labels=["t1small","t2","t3","t4big"])
    out["by_today_q"]=d2.groupby("tq").apply(stat)
    d3=df.dropna(subset=["f4"])
    d3["f4q"]=pd.qcut(d3["f4"].rank(method="first"),4,labels=["deep","d2","d3","shallow"])
    out["by_f4_q"]=d3.groupby("f4q").apply(stat)
    out["by_f4_q_u3"]=d3.groupby("f4q").apply(lambda g:stat(g,"u3"))
    out["corr_fc_u1"]=float(df[["fc","u1"]].corr().iloc[0,1])
    out["corr_f4_u1"]=float(d3[["f4","u1"]].corr().iloc[0,1])
    nday=df.groupby("day")["coin"].transform("size")
    df["crowd"]=np.where(nday>=3,"many","few")
    out["by_crowd"]=df.groupby("crowd").apply(stat)
    out["n_cases"]=len(df)
    return out
