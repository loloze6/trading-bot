import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    H=72
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            c=df["close"].values.astype(float); n=len(c)
            lr=np.diff(np.log(c),prepend=np.nan)
            fc=df["forecast"].values
            for t in range(0,n,H):
                if t<H: continue
                r=lr[t-H+1:t+1]
                if np.isnan(r).any(): continue
                net=r.sum()
                if net<=0: continue
                up=np.sort(r)[::-1][:3]
                sh=(net-up[up>0].sum())/net
                vol=np.std(r)
                rec={"coin":coin,"w":w,"past":np.exp(net)-1,"shu":sh,"fc":fc[t],"vol":vol,
                     "nup":(r>0).mean(),
                     "f72":c[t+H]/c[t]-1 if t+H<n else np.nan}
                rows.append(rec)
    d=pd.DataFrame(rows).dropna(subset=["f72"])
    out={}
    def tb(x,sc,f="f72"):
        x=x.dropna(subset=[sc,f])
        q=x[sc].rank(method="first"); k=len(x)//3
        lo=x[f][q<=k]; hi=x[f][q>len(x)-k]
        return pd.Series({"n":len(x),"hi_mean":hi.mean(),"lo_mean":lo.mean(),"hi-lo":hi.mean()-lo.mean(),
                          "t":stats.ttest_ind(hi,lo,equal_var=False).statistic})
    g={}
    g["all_risen_shu"]=tb(d,"shu")
    g["fc>0_shu"]=tb(d[d.fc>0],"shu")
    g["fc==0_shu"]=tb(d[d.fc<=0],"shu")
    g["all_risen_fc"]=tb(d,"fc")
    g["all_risen_nup"]=tb(d,"nup")
    g["all_risen_negvol"]=tb(d.assign(nv=-d.vol),"nv")
    out["splits"]=pd.DataFrame(g).T
    # OLS f72 ~ shu + past + vol
    X=np.column_stack([np.ones(len(d)),d.shu,d.past,d.vol]); y=d.f72.values
    b,_,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@b
    cov=np.linalg.inv(X.T@X)*(e@e)/(len(y)-X.shape[1])
    out["ols_shu_past_vol"]=pd.DataFrame({"b":b,"t":b/np.sqrt(np.diag(cov))},index=["c","shu","past","vol"])
    # share terciles means
    d["shq"]=pd.qcut(d.shu.rank(method="first"),3,labels=["lo","mid","hi"])
    out["by_share_tercile"]=d.groupby("shq").agg(n=("f72","size"),mean=("f72","mean"),shu=("shu","mean"),past=("past","mean"),vol=("vol","mean"))
    out["corr"]=d[["shu","past","vol","nup","fc"]].corr(method="spearman")
    out["share_fc_pos"]=(d.fc>0).mean()
    # window halves: w1-12 vs w13-24
    d["half"]=np.where(d.w.str[1:].astype(int)<=12,"w1-12","w13-24")
    out["halves"]=pd.DataFrame({h:tb(x,"shu") for h,x in d.groupby("half")}).T
    return out
