def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        allr=[]
        for w,b in wins.items():
            allr.append(pd.Series(b["close"].values).pct_change().dropna())
        mu=pd.concat(allr).mean()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]); wd=ts.dt.weekday.values
            c=b["close"].values; n=len(c)
            f=b["forecast"].fillna(0).values
            r1d=pd.Series(c).pct_change()
            sd=r1d.rolling(60,min_periods=20).std().values
            r1d=r1d.values
            for t in range(n):
                if wd[t]!=6 or t+3>=n or np.isnan(sd[t]): continue
                d={"coin":coin,"w":w,"f":f[t],"z":r1d[t]/sd[t]}
                for k in (1,2,3):
                    d[f"d{k}"]=c[t+k]/c[t+k-1]-1-mu
                d["r3"]=c[t+3]/c[t]-1-3*mu
                d["r3z"]=d["r3"]/sd[t]
                rows.append(d)
    df=pd.DataFrame(rows)
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out={}
    fall=df[df.z<0].copy(); rise=df[df.z>0].copy()
    out["fall_by_day"]=pd.DataFrame({k:tt(fall[k]) for k in ("d1","d2","d3","r3")})
    out["rise_by_day"]=pd.DataFrame({k:tt(rise[k]) for k in ("d1","d2","d3","r3")})
    df["zq"]=pd.qcut(df.z,6)
    out["r3_by_weekend_z_sextile"]=df.groupby("zq")[["r3","r3z","d1","d2","d3"]].mean()
    out["corr_z_r3z"]=float(np.corrcoef(df.z,df.r3z)[0,1])
    out["n_cases"]=len(df)
    # book: daily returns, deepest fall
    D=pd.concat([dd.assign(coin=c,w=w) for c,ws in data["days"].items() for w,dd in ws.items()])
    D["wd"]=pd.to_datetime(D["day"]).dt.weekday
    D["y"]=pd.to_datetime(D["day"]).dt.year
    out["book_by_year"]=D.groupby("y")[["book_return","coin_return"]].mean()
    mon=D[D.wd==0]
    out["monday_book_nonzero"]=tt(mon.book_return[mon.book_return.abs()>1e-9])
    return out
