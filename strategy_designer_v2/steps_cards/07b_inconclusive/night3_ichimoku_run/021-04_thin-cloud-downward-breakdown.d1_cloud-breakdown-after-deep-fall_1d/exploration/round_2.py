def explore(data):
    import numpy as np, pandas as pd
    H=26
    bars=data["bars"]
    drift={}
    for c,ws in bars.items():
        r=[]
        for w,df in ws.items():
            cl=df["close"].values
            idx=np.arange(0,len(cl)-H,H)
            r+=list(cl[idx+H]/cl[idx]-1)
        drift[c]=np.mean(r)
    rows=[]
    for c,ws in bars.items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            cl=df["close"].values; hi=df["high"].values; lo=df["low"].values
            f=df["forecast"].fillna(0).values
            n=len(cl); ts=pd.to_datetime(df["timestamp"])
            s=pd.Series(cl); H_=pd.Series(hi); L_=pd.Series(lo)
            ten=(H_.rolling(9).max()+L_.rolling(9).min())/2
            kij=(H_.rolling(26).max()+L_.rolling(26).min())/2
            sa=((ten+kij)/2).shift(26); sb=((H_.rolling(52).max()+L_.rolling(52).min())/2).shift(26)
            thick=((sa-sb).abs()/s).values
            sbslope=(sb/sb.shift(10)-1).values
            kslope=(kij/kij.shift(10)-1).values
            lr=np.log(s).diff()
            vol20=lr.rolling(20).std().values
            ret10=(s/s.shift(10)-1).values
            used=set()
            for i in range(n):
                if f[i]<0:
                    cell=i//H
                    if cell in used: continue
                    used.add(cell)
                    rec={"coin":c,"year":ts[i].year,"pos":i,
                         "since_start":cl[i]/cl[0]-1,"thick":thick[i],"sbslope":sbslope[i],
                         "kslope":kslope[i],"vol20":vol20[i],"ret10":ret10[i],
                         "ret26":cl[i]/cl[i-26]-1 if i>=26 else np.nan}
                    for h in [10,26,52]:
                        if i+h<n: rec[f"un{h}"]=-(cl[i+h]/cl[i]-1-drift[c]*h/H)
                    rows.append(rec)
    d=pd.DataFrame(rows)
    def summ(g,col="un26"):
        x=g[col].dropna()
        return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,"hit":(x>0).mean()})
    out={}
    def split(var,q=3):
        dd=d.dropna(subset=[var]).copy()
        dd["g"]=pd.qcut(dd[var],q,duplicates="drop")
        return pd.concat({h:dd.groupby("g").apply(lambda g:summ(g,f"un{h}")) for h in ["26","52"]},axis=1)
    for v in ["since_start","thick","sbslope","kslope","vol20","ret10","pos"]:
        out[v]=split(v)
    out["corr_un26"]=d[["since_start","thick","sbslope","kslope","vol20","ret10","ret26","un26"]].corr()["un26"]
    out["by_year_52"]=d.groupby("year").apply(lambda g:summ(g,"un52"))
    out["ex2018"]=summ(d[d.year!=2018])
    return out
