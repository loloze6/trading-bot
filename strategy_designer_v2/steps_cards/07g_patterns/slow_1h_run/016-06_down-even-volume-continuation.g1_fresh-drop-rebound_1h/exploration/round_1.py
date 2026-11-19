import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # 1. book vs holding daily, by coin; fee drag; gross position gain
    rows = []
    for c in bars:
        br=[];cr=[];fee=[];gross=[];alloc=[];ntr=0
        for w,df in bars[c].items():
            d = days[c][w]
            br.append(d["book_return"].dropna()); cr.append(d["coin_return"].dropna())
            f = (df["total_portfolio_value"]-df["postRebalance_total_value"])/df["total_portfolio_value"]
            fee.append(f.sum()); 
            r = df["close"].shift(-1)/df["close"]-1
            gross.append((df["postRebalance_current_allocation"]*r).sum())
            alloc.append(df["postRebalance_current_allocation"].abs().mean())
            ntr += len(data["trades"][c][w])
        br=pd.concat(br); cr=pd.concat(cr); nd=len(br)
        rows.append({"coin":c,"book_mean":br.mean(),"hold_mean":cr.mean(),
                     "fee_per_day":np.sum(fee)/nd,"gross_per_day":np.sum(gross)/nd,
                     "mean_abs_alloc":np.mean(alloc),"trades_per_day":ntr/nd})
    out["book_by_coin"]=pd.DataFrame(rows).set_index("coin")
    # grid analysis
    g=[]
    for c in bars:
        for w,df in bars[c].items():
            cl=df["close"].values; v=df["volume"].values; n=len(cl)
            hr=np.r_[np.nan, cl[1:]/cl[:-1]-1]
            for i in range(0,n,72):
                if i<72 or i+72>=n: continue
                r72=cl[i]/cl[i-72]-1; r24=cl[i]/cl[i-24]-1
                h=hr[i-71:i+1]
                ab=np.abs(h); jump=np.nanmax(ab)/np.nansum(ab)
                eff=abs(r72)/np.nansum(ab)
                vv=v[i-71:i+1]; vconc=np.nanmax(vv)/np.nansum(vv) if np.nansum(vv)>0 else np.nan
                vol=np.nanstd(h)
                fwd=cl[i+72]/cl[i]-1; fwd24=cl[i+24]/cl[i]-1
                g.append((c,w,r72,r24,jump,eff,vconc,vol,fwd,fwd24,
                          pd.Timestamp(df["timestamp"].iloc[i]).hour))
    G=pd.DataFrame(g,columns=["coin","w","r72","r24","jump","eff","vconc","vol","fwd","fwd24","hour"])
    G["ex"]=G["fwd"]-G.groupby("coin")["fwd"].transform("mean")
    G["sgn"]=np.sign(G["r72"])
    def qtab(col,sub,name):
        s=sub.copy(); s["q"]=s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
        t=s.groupby("q")["ex"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        out[name]=t.drop(columns="std")
        sl=stats.linregress(s[col].dropna(), s.loc[s[col].notna(),"ex"]); out[name+"_slope_t"]=float(sl.slope/sl.stderr)
    qtab("r24",G[G.r72<0],"down: r24 quintile")
    qtab("r24",G[G.r72>=0],"up: r24 quintile")
    qtab("r72",G,"all: r72 quintile")
    # signed move continuation x shape: ex*sign(r72) by jump quintile
    G["cont"]=G["ex"]*G["sgn"]
    for col in ["jump","eff","vconc","vol"]:
        s=G.copy(); s["q"]=s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
        t=s.groupby("q")["cont"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
        out["continuation by "+col]=t.drop(columns="std")
    out["n_grid"]=len(G)
    return out
