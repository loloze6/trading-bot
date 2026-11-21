import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    res=[]
    for h in [1,4,12,24,72]:
        P=[];F=[];V=[]
        for c,ws in data["bars"].items():
            for w,b in ws.items():
                cl=b["close"].astype(float).values
                lr=np.diff(np.log(cl))
                idx=np.arange(h,len(cl)-h,h)
                past=cl[idx]/cl[idx-h]-1; fut=cl[idx+h]/cl[idx]-1
                sd=pd.Series(np.r_[np.nan,lr]).rolling(720,min_periods=200).std().values[idx]*np.sqrt(h)
                P.append(past);F.append(fut);V.append(sd)
        p=np.concatenate(P);f=np.concatenate(F);v=np.concatenate(V)
        m=np.isfinite(p)&np.isfinite(f)&np.isfinite(v)
        p,f,v=p[m],f[m],v[m]
        z=p/v; g=-np.sign(p)*f
        q=pd.qcut(np.abs(z),5,labels=False)
        for k in range(5):
            s=g[q==k]
            res.append({"h":h,"absz_q":k,"n":len(s),"fade_gain_bp":1e4*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
        hv=v>np.median(v)
        for lab,mm in [("hivol",hv),("lovol",~hv)]:
            s=g[mm&(q>=3)]
            res.append({"h":h,"absz_q":lab+"_top2q","n":len(s),"fade_gain_bp":1e4*s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out["fade_by_horizon_size"]=pd.DataFrame(res)
    # hour of day: next-hour fade gain by UTC hour
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            cl=b["close"].astype(float)
            r=cl.pct_change(); nx=cl.shift(-1)/cl-1
            hr=pd.to_datetime(b["timestamp"]).dt.hour+1  # hour at bar close
            rows.append(pd.DataFrame({"hr":hr%24,"g":-np.sign(r)*nx}))
    H=pd.concat(rows).dropna()
    gh=H.groupby("hr").g
    out["fade1h_by_close_hour"]=pd.DataFrame({"bp":1e4*gh.mean(),"t":gh.mean()/(gh.std()/np.sqrt(gh.size()))})
    return out
