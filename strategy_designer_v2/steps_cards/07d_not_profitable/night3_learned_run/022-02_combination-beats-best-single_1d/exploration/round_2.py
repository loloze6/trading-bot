import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    rows=[]; pers=[]
    for coin in data["bars"]:
        for H in [5,20]:
            g_all=[]
            for w,b in data["bars"][coin].items():
                c=b["close"].values
                idx=np.arange(0,len(c)-H,H)
                g_all+=list(c[idx+H]/c[idx]-1)
            drift=np.mean(g_all); sd=np.std(g_all)
            for w,b in data["bars"][coin].items():
                b=b.reset_index(drop=True); c=b["close"]
                r28=c/c.shift(28)-1
                r90=c/c.shift(90)-1
                vol30=np.log(c).diff().rolling(30).std()
                alloc=b["postRebalance_current_allocation"]
                idx=np.arange(0,len(c)-H,H)
                for i in idx:
                    rows.append(dict(coin=coin,H=H,win=w,y=c[i+H]/c[i]-1-drift,tot=c[i+H]/c[i]-1,
                        ys=(c[i+H]/c[i]-1-drift)/sd,r28=r28[i],r90=r90[i],vol30=vol30[i],alloc=alloc[i]))
    C=pd.DataFrame(rows)
    res=[]
    for H in [5,20]:
        g=C[C.H==H].dropna(subset=["r28"]).copy()
        g["q"]=g.groupby("coin")["r28"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
        t=g.groupby("q").agg(unusual=("y","mean"),total=("tot","mean"),strength=("ys","mean"),n=("y","size"))
        t["H"]=H; res.append(t.reset_index())
    out["y_by_r28_quintile_within_coin"]=pd.concat(res)
    # signed momentum size: sign(r28)*y
    sz=[]
    for H in [5,20]:
        g=C[C.H==H].dropna(subset=["r28"])
        s=np.sign(g["r28"])
        u=s*g["y"]; tot=s*g["tot"]; st=s*g["ys"]
        sz.append(dict(H=H,unusual=u.mean(),t=u.mean()/u.std()*np.sqrt(len(u)),total=tot.mean(),strength=st.mean(),n=len(u)))
    out["size_sign_r28"]=pd.DataFrame(sz)
    # book alloc vs coin's 90d trend: did it short rising coins?
    g=C[C.H==5].dropna(subset=["r90"]).copy()
    g["up90"]=g["r90"]>0
    out["alloc_and_y_by_90d_trend"]=g.groupby("up90").agg(mean_alloc=("alloc","mean"),share_short=("alloc",lambda a:(a<0).mean()),
        y=("y","mean"),gain=("alloc",lambda a: (a*g.loc[a.index,"tot"]).mean()),n=("y","size"))
    # vol tercile and momentum strength at 20d
    g=C[C.H==20].dropna(subset=["r28","vol30"]).copy()
    g["vq"]=g.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s,3,labels=False))
    g["m"]=np.sign(g["r28"])*g["y"]
    out["mom20_by_vol_tercile"]=g.groupby("vq").agg(signed_unusual=("m","mean"),n=("m","size"),
        corr=("m",lambda m: stats.pearsonr(g.loc[m.index,"r28"],g.loc[m.index,"y"])[0]))
    return out
