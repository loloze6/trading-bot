import numpy as np, pandas as pd
from scipy import stats
def explore(data):
    out={}
    res={}
    for k in [1,4,12,24,48]:
        xs=[];ys=[]
        for c,ws in data["bars"].items():
            for w,b in ws.items():
                cl=b["close"].values
                lr=np.log(cl)
                r1=pd.Series(np.diff(lr,prepend=np.nan))
                vol=r1.rolling(24*max(1,k//24) if k<24 else k).std()
                vol=r1.rolling(max(24,k)).std()
                past=pd.Series(lr).diff(k)/(vol*np.sqrt(k))
                fut=pd.Series(cl).shift(-k)/pd.Series(cl)-1
                idx=np.arange(0,len(b),k)
                x=past.values[idx]; y=fut.values[idx]
                m=~(np.isnan(x)|np.isnan(y))
                xs.append(x[m]); ys.append(y[m])
        x=np.concatenate(xs); y=np.concatenate(ys)
        y=y-y.mean()
        sl=stats.linregress(-x,y)
        q=pd.qcut(np.abs(x),5,labels=False)
        sg=-np.sign(x)*y*1e4
        res[k]={"n":len(x),"slope_bps_per_unit":sl.slope*1e4,"t":sl.slope/sl.stderr,
                "signed_bps_all":sg.mean(),"signed_bps_topq":sg[q==4].mean(),"signed_bps_q0":sg[q==0].mean(),
                "signed_bps_per_hour_topq":sg[q==4].mean()/k}
    out["vol-scaled past k-h return vs next k-h (reversal sign)"]=pd.DataFrame(res).T
    # book daily
    dd=[]
    for c,ws in data["days"].items():
        for w,t in ws.items():
            dd.append(t.assign(coin=c,w=w))
    d=pd.concat(dd)
    br=d.groupby(["w","day"]).book_return.mean().dropna()
    cr=d.groupby(["w","day"]).coin_return.mean().dropna()
    out["daily"]=pd.Series({"book_mean":br.mean(),"book_sharpe":br.mean()/br.std()*np.sqrt(365),"hold_mean":cr.mean(),"hold_sharpe":cr.mean()/cr.std()*np.sqrt(365),"days":len(br)})
    return out
