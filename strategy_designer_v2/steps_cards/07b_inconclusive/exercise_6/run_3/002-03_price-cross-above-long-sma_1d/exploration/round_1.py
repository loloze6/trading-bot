import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    blk = []
    for coin, ws in bars.items():
        rets = []
        for w, df in ws.items():
            c = df["close"].values
            rets.append(c[1:]/c[:-1]-1)
        mu = np.nanmean(np.concatenate(rets))
        for w, df in ws.items():
            c = df["close"].values; f = df["forecast"].values
            a = df["postRebalance_current_allocation"].values
            n = len(c); yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [5,10,20,40,60]:
                for i in range(0, n-h, h):
                    rows.append((coin, w, yr[i], h, f[i], a[i], c[i+h]/c[i]-1 - h*mu))
            # block measure
            for s in range(0, n, 20):
                v=[]; nz=False
                for i in range(s, min(s+20,n)):
                    if i+20 < n:
                        v.append(a[i]*(c[i+20]/c[i]-1-20*mu)); nz |= a[i]!=0
                if v: blk.append((coin, w, yr[s], sum(v), nz))
    R = pd.DataFrame(rows, columns=["coin","w","yr","h","f","a","ex"])
    B = pd.DataFrame(blk, columns=["coin","w","yr","s","nz"])
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "hit":(x>0).mean()})
    R["fb"] = pd.cut(R["f"], [-0.01,0.0001,5,10,15,20.1], labels=["0","0-5","5-10","10-15","15-20"])
    out = {}
    out["by_h_fbucket"] = R.groupby(["h","fb"])["ex"].apply(tt).unstack()
    R20 = R[R.h==20]
    out["h20_active_by_coin"] = R20[R20.f>0].groupby("coin")["ex"].apply(tt).unstack()
    out["h20_active_by_year"] = R20[R20.f>0].groupby("yr")["ex"].apply(tt).unstack()
    out["h20_flat_by_year"] = R20[R20.f==0].groupby("yr")["ex"].apply(tt).unstack()
    out["block_by_coin"] = B.groupby("coin")["s"].apply(tt).unstack()
    out["block_by_year"] = B.groupby("yr")["s"].apply(tt).unstack()
    out["block_all"] = tt(B["s"]).to_frame().T
    # active vs flat welch by horizon
    res=[]
    for h in [5,10,20,40,60]:
        x=R[(R.h==h)&(R.f>0)]["ex"]; y=R[(R.h==h)&(R.f==0)]["ex"]
        res.append((h,len(x),x.mean(),len(y),y.mean(),stats.ttest_ind(x,y,equal_var=False).statistic, stats.spearmanr(R[(R.h==h)&(R.f>0)]["f"],x).correlation))
    out["active_vs_flat"] = pd.DataFrame(res, columns=["h","n_act","m_act","n_flat","m_flat","welch_t","spearman_f_ex_active"])
    return out
