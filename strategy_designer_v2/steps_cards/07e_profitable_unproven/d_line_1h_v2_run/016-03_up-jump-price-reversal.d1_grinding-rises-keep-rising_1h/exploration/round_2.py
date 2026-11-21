import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; trades = data["trades"]
    coins = list(bars.keys())
    G=[]
    for c in coins:
        for w,b in bars[c].items():
            cl=b["close"].values; f=b["forecast"].values
            hr=np.log(b["close"]).diff().values
            n=len(cl)
            for i in range(0,n,72):
                if i-720<0 or i+72>=n: continue
                past=cl[i]/cl[i-72]-1
                h=hr[i-71:i+1]
                g=h[h>0]; top3=np.sort(g)[-3:].sum() if len(g)>0 else np.nan
                net=np.log(cl[i]/cl[i-72])
                share_up_hours=(h>0).mean()
                G.append((c,w,past,cl[i]/cl[i-720]-1,cl[i+72]/cl[i]-1,f[i],top3/net if net>0 else np.nan,share_up_hours,np.nanstd(h)))
    G=pd.DataFrame(G,columns=["coin","win","past","past30","fwd","fc","top3share","upfrac","vol"])
    G["ex"]=G.fwd-G.groupby("coin").fwd.transform("mean")
    q=pd.qcut(G.past.rank(method="first"),5,labels=False)
    out["fwd_by_past72_quintile"]=G.groupby(q).agg(n=("ex","size"),ex=("ex","mean"),past=("past","mean"))
    t=lambda s:s.mean()/(s.std()/np.sqrt(len(s)))
    out["past_quintile_t"]=G.groupby(q).ex.apply(t)
    up=G[G.past>0].dropna(subset=["fc"])
    up["trend"]=np.where(up.past30>0,"30d_up","30d_down")
    rows=[]
    for k,s in up.groupby("trend"):
        X=np.column_stack([np.ones(len(s)),s.fc,s.past]);b,_,_,_=np.linalg.lstsq(X,s.ex.values,rcond=None)
        r=s.ex.values-X@b;se=np.sqrt(np.diag(r@r/(len(s)-3)*np.linalg.inv(X.T@X)))
        rows.append({"trend":k,"n":len(s),"t_fc":b[1]/se[1],"mean_ex":s.ex.mean(),"t_mean":t(s.ex),"corr_fc_ex":s[["fc","ex"]].corr().iloc[0,1]})
    out["grind_by_30d_trend"]=pd.DataFrame(rows)
    # upfrac (share of up hours) graded, all grid
    q2=pd.qcut(G.upfrac.rank(method="first"),5,labels=False)
    out["fwd_by_upfrac_quintile_all"]=G.groupby(q2).agg(n=("ex","size"),ex=("ex","mean"),upfrac=("upfrac","mean"),t=("ex",t))
    # 30-day return graded
    q3=pd.qcut(G.past30.rank(method="first"),5,labels=False)
    out["fwd_by_past30d_quintile"]=G.groupby(q3).agg(n=("ex","size"),ex=("ex","mean"),past30=("past30","mean"),t=("ex",t))
    pc=[]
    for c,s in up.groupby("coin"):
        pc.append({"coin":c,"n":len(s),"corr_fc_ex":s[["fc","ex"]].corr().iloc[0,1],"t_up_ex":t(s.ex)})
    out["per_coin_up"]=pd.DataFrame(pc)
    T=pd.concat([d.assign(coin=c) for c in coins for w,d in trades[c].items()])
    p=T.net_profit_loss_percent.dropna().sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(p),"sum":p.sum(),"top10_sum":p.head(10).sum(),"top5pct_sum":p.head(int(len(p)*0.05)).sum(),"win_rate":(p>0).mean(),"mean_dur_h":T.duration_minutes.mean()/60})
    return out
