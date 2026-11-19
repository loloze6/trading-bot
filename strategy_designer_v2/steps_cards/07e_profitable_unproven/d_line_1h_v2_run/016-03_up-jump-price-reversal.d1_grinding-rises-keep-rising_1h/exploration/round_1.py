import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    mh = {}
    for c in coins:
        rs = [b["close"].pct_change().dropna() for w, b in bars[c].items()]
        mh[c] = pd.concat(rs).mean()
    rows = []
    for c in coins:
        for w, b in bars[c].items():
            r1 = b["close"].shift(-1)/b["close"]-1
            a = b["postRebalance_current_allocation"].fillna(0)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(pd.DataFrame({"coin":c,"win":w,"yr":yr,"gain":a*r1,"mkt":a*mh[c],"alloc":a}).dropna())
    B = pd.concat(rows)
    tot = B.groupby("coin")[["gain","mkt"]].sum()
    tot["timing"] = tot.gain - tot.mkt
    tot["mean_alloc"] = B.groupby("coin").alloc.mean()
    tot["share_bars_in"] = B.groupby("coin").alloc.apply(lambda s:(s>0).mean())
    out["by_coin_sum_gain"] = tot
    out["total"] = pd.Series({"gain":B.gain.sum(),"mkt":B.mkt.sum(),"timing":B.gain.sum()-B.mkt.sum()})
    out["by_year"] = B.groupby("yr")[["gain","mkt"]].sum().assign(timing=lambda d:d.gain-d.mkt)
    bw = B.groupby("win")[["gain","mkt"]].sum(); bw["timing"]=bw.gain-bw.mkt
    out["by_window"] = bw
    D = []
    for c in coins:
        for w, d in days[c].items():
            D.append(d.assign(coin=c, win=w))
    D = pd.concat(D)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_daily"] = pd.Series({"book_mean":bk.book_return.mean(),"hold_mean":bk.coin_return.mean(),
        "book_sh":bk.book_return.mean()/bk.book_return.std()*np.sqrt(365),
        "corr_book_hold":bk.corr().iloc[0,1],
        "beta":np.polyfit(bk.coin_return,bk.book_return,1)[0]})
    res = []
    for H in [24,72,168]:
        G=[]
        for c in coins:
            for w,b in bars[c].items():
                cl=b["close"].values; f=b["forecast"].values
                n=len(cl)
                for i in range(0,n,H):
                    if i-72<0 or i+H>=n: continue
                    G.append((c,cl[i]/cl[i-72]-1,cl[i+H]/cl[i]-1,f[i]))
        G=pd.DataFrame(G,columns=["coin","past","fwd","fc"])
        G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
        up=G[G.past>0].dropna()
        X=np.column_stack([np.ones(len(up)),up.fc,up.past])
        beta,_,_,_=np.linalg.lstsq(X,up.ex.values,rcond=None)
        resid=up.ex.values-X@beta; s2=resid@resid/(len(up)-3)
        se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        tu=stats.ttest_ind(G[G.past>0].ex,G[G.past<=0].ex,equal_var=False)
        q=pd.qcut(up.fc.rank(method="first"),4,labels=False)
        qm=up.groupby(q).ex.mean()
        res.append({"H":H,"n_up":len(up),"t_fc":beta[1]/se[1],"t_past":beta[2]/se[2],
                    "up_minus_down_ex":G[G.past>0].ex.mean()-G[G.past<=0].ex.mean(),"t_updown":tu.statistic,
                    "fcQ1":qm.iloc[0],"fcQ4":qm.iloc[3],"fc_zero_share":(up.fc==0).mean()})
    out["grid"]=pd.DataFrame(res)
    return out
