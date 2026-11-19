import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H=240
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].values; f=b["forecast"].fillna(0).values; r=b["regime"].values
            n=len(b)
            yr=pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0,n,H):
                rec={"coin":coin,"w":w,"f":f[i],"reg":r[i],"year":yr[i]}
                for h in (24,120,240,480,720):
                    rec[f"r{h}"]=c[i+h]/c[i]-1 if i+h<n else np.nan
                # 60d return proxy
                rec["r60back"]=c[i]/c[i-1440]-1 if i>=1440 else np.nan
                rows.append(rec)
    g=pd.DataFrame(rows)
    def slope(d,col):
        d=d.dropna(subset=[col])
        if len(d)<10 or d["f"].std()==0: return (np.nan,np.nan,len(d))
        res=stats.linregress(d["f"],d[col]); return (res.slope,res.slope/res.stderr,len(d))
    for h in (24,120,240,480,720):
        g[f"x{h}"]=g[f"r{h}"]-g.groupby("coin")[f"r{h}"].transform("mean")
    out={}
    hz=[]
    for h in (24,120,240,480,720):
        s,t,n=slope(g,f"x{h}"); hz.append({"h":h,"slope":s,"t":t,"n":n})
    out["by_horizon_allgrid"]=pd.DataFrame(hz)
    def tab(key):
        L=[]
        for k,d in g.groupby(key):
            s,t,n=slope(d,"x240"); pos=d[d.f>0]
            L.append({key:k,"slope":s,"t":t,"n":n,"npos":len(pos),"mean_x_pos":pos["x240"].mean(),"mean_x_zero":d[d.f==0]["x240"].mean()})
        return pd.DataFrame(L)
    out["by_regime"]=tab("reg"); out["by_coin"]=tab("coin"); out["by_year"]=tab("year")
    # forecast quintiles among positive
    pos=g[g.f>0].dropna(subset=["x240"]).copy()
    pos["q"]=pd.qcut(pos["f"],4,labels=False)
    out["pos_quartiles"]=pos.groupby("q").agg(fmean=("f","mean"),x=("x240","mean"),n=("x240","size"),raw=("r240","mean"))
    out["slope_pos_only"]=str(slope(pos,"x240"))
    zero=g[(g.f==0)].dropna(subset=["x240"])
    tt=stats.ttest_ind(pos["x240"],zero["x240"],equal_var=False)
    out["pos_minus_zero"]=f"{pos['x240'].mean()-zero['x240'].mean():.4f} t={tt.statistic:.2f} n={len(pos)},{len(zero)}"
    # book
    D=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items(): D.append(d.assign(coin=coin,w=w))
    D=pd.concat(D); bd=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book"]=f"book mean {bd.book_return.mean():.5f} sh {bd.book_return.mean()/bd.book_return.std()*np.sqrt(365):.2f}; hold mean {bd.coin_return.mean():.5f}"
    # allocation stats
    A=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"]; f=b["forecast"]
            A.append({"coin":coin,"meanalloc":a.mean(),"share_short":(a<-1e-6).mean(),"share_long":(a>1e-6).mean(),"share_fpos":(f>0).mean()})
    out["alloc"]=pd.DataFrame(A).groupby("coin").mean()
    return out
