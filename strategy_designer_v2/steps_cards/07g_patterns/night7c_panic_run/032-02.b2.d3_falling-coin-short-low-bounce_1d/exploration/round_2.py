import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"]
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["r1"]=c.shift(-1)/c-1
            d["prev1"]=c/c.shift(1)-1
            lr=np.log(c).diff()
            d["vol20"]=lr.rolling(20).std()
            d["z1"]=d["prev1"]/lr.shift(1).rolling(60,min_periods=20).std()
            d["ret30"]=c/c.shift(30)-1
            d["alloc"]=b["postRebalance_current_allocation"]
            d["volq"]=np.nan
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["r1"].mean(); D["x1"]=D["r1"]-D["coin"].map(mu)
    D["day"]=D["ts"].dt.floor("D")
    D["volq"]=D.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    def tstat(s,col="x1"):
        s=s.dropna(subset=[col]); n=len(s)
        if n<5: return (n,np.nan,np.nan)
        m=s[col].mean(); gd=(s[col]-m).groupby(s["day"]).sum()
        return (n,m,m/(np.sqrt((gd**2).sum())/n))
    res={}
    S=D.dropna(subset=["z1","x1"]).copy()
    S["zq"]=pd.qcut(S["z1"],10,labels=False)
    out=[]
    for k,s in S.groupby("zq"): out.append((k,)+tstat(s)+(s.z1.mean(),))
    res["by_z1_decile"]=pd.DataFrame(out,columns=["zdec","n","mean_x1","t","mean_z"])
    # slope of x1 on z1 per coin, clustered-ish via OLS t
    out=[]
    for coin,s in S.groupby("coin"):
        r=stats.linregress(s.z1,s.x1); out.append((coin,len(s),r.slope,r.slope/r.stderr))
    res["slope_x1_on_z1_by_coin"]=pd.DataFrame(out,columns=["coin","n","slope","t"])
    out=[]
    for w,s in S.groupby("w"):
        r=stats.linregress(s.z1,s.x1); out.append((w,len(s),r.slope,r.slope/r.stderr))
    res["slope_by_window"]=pd.DataFrame(out,columns=["w","n","slope","t"])
    out=[]
    for (vq,fall),s in S.groupby(["volq",S.ret30<0]):
        r=stats.linregress(s.z1,s.x1); out.append((vq,fall,len(s),r.slope,r.slope/r.stderr))
    res["slope_by_volterc_and_falling30"]=pd.DataFrame(out,columns=["volq","fall30","n","slope","t"])
    # bottom z decile split by ret30 sign
    low=S[S.zq==0]
    out=[]
    for f,s in low.groupby(low.ret30<0): out.append((f,)+tstat(s))
    res["lowest_z_decile_by_fall30"]=pd.DataFrame(out,columns=["fall30","n","mean_x1","t"])
    # book: largest gain/loss days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; dd.append(x)
    DD=pd.concat(dd,ignore_index=True).dropna(subset=["book_return"])
    act=DD[DD.book_return!=0]
    res["book_active_days"]=pd.Series({"n":len(act),"mean":act.book_return.mean(),
        "top5pct_share_of_sum":act.book_return.nlargest(max(1,len(act)//20)).sum()/act.book_return.sum(),
        "worst5pct_sum":act.book_return.nsmallest(max(1,len(act)//20)).sum()})
    return res
