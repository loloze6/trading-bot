import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    H=72
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float); n=len(c)
            lr=np.diff(np.log(c),prepend=np.nan)
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            fc=df["forecast"].values
            for t in range(0,n,H):
                if t<H: continue
                r=lr[t-H+1:t+1]
                if np.isnan(r).any(): continue
                net=r.sum()
                up=np.sort(r)[::-1][:3]; dn=np.sort(r)[:3]
                sh_up=(net-up[up>0].sum())/net if net>0 else np.nan
                sh_dn=(net-dn[dn<0].sum())/net if net<0 else np.nan
                rec={"coin":coin,"w":int(w[1:]),"yr":yr[t],"past":np.exp(net)-1,"shu":sh_up,"shd":sh_dn,"fc":fc[t]}
                for h in (24,72,144):
                    rec[f"f{h}"]=c[t+h]/c[t]-1 if t+h<n else np.nan
                rows.append(rec)
    d=pd.DataFrame(rows)
    out={}
    def tb(x,col,sc,f):
        x=x.dropna(subset=[sc,f])
        if len(x)<30: return (len(x),np.nan,np.nan,np.nan)
        q=x[sc].rank(method="first")
        k=len(x)//3
        lo=x[f][q<=k]; hi=x[f][q>len(x)-k]
        t=stats.ttest_ind(hi,lo,equal_var=False).statistic
        rho=stats.spearmanr(x[sc],x[f]).correlation
        return (len(x),hi.mean()-lo.mean(),t,rho)
    up=d[d.past>0]; dn=d[d.past<0]
    res={}
    for f in ("f24","f72","f144"):
        res[("up_shu_raw",f)]=tb(up,None,"shu",f)
        res[("up_fc",f)]=tb(up[up.fc>0],None,"fc",f)
        res[("dn_shd_raw",f)]=tb(dn,None,"shd",f)
        res[("up_past_size",f)]=tb(up,None,"past",f)
    out["overall"]=pd.DataFrame(res,index=["n","hi-lo","t","rho"]).T
    g={}
    for coin,x in up.groupby("coin"): g["coin "+coin]=tb(x,None,"shu","f72")
    for y,x in up.groupby("yr"): g["yr %d"%y]=tb(x,None,"shu","f72")
    up2=up.copy(); up2["psz"]=pd.qcut(up2.past,3,labels=["small","mid","big"])
    for s,x in up2.groupby("psz"): g["pastsize "+s]=tb(x,None,"shu","f72")
    out["up_groups_f72"]=pd.DataFrame(g,index=["n","hi-lo","t","rho"]).T
    g={}
    for coin,x in dn.groupby("coin"): g["coin "+coin]=tb(x,None,"shd","f72")
    for y,x in dn.groupby("yr"): g["yr %d"%y]=tb(x,None,"shd","f72")
    out["dn_groups_f72"]=pd.DataFrame(g,index=["n","hi-lo","t","rho"]).T
    out["hold_mean_f72"]=d.f72.mean()
    out["corr_shu_fc"]=up[up.fc>0][["shu","fc"]].corr(method="spearman").iloc[0,1]
    return out
