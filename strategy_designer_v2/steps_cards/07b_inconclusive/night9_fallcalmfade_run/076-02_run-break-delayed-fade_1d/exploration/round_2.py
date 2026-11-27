def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[];drifts={}
    for coin,ws in data["bars"].items():
        d={1:[],2:[],3:[]}
        for w,b in ws.items():
            c=b["close"].values
            for h in d:
                idx=np.arange(0,len(c)-h,h); d[h]+=list(c[idx+h]/c[idx]-1)
        drifts[coin]={h:np.mean(v) for h,v in d.items()}
        for w,b in ws.items():
            c=b["close"].values;n=len(c);ts=pd.to_datetime(b["timestamp"]).values
            r=np.r_[np.nan,c[1:]/c[:-1]-1];run=np.zeros(n,int)
            for i in range(1,n):
                if r[i]<0: run[i]=run[i-1]+1 if i>1 and r[i-1]<0 else 1
            f=b["forecast"].values;seen=set()
            for i in range(2,n-3):
                if r[i]>0 and run[i-1]>=1:
                    cell=i//3
                    if cell in seen: continue
                    seen.add(cell)
                    rows.append(dict(coin=coin,w=w,day=str(ts[i])[:10],year=str(ts[i])[:4],k=run[i-1],
                        wf=abs(f[i]) if not np.isnan(f[i]) else np.nan,
                        r1=c[i+1]/c[i]-1,r23=c[i+3]/c[i+1]-1,r13=c[i+3]/c[i]-1))
    df=pd.DataFrame(rows)
    for col,h in [("r1",1),("r23",2),("r13",3)]:
        df["x"+col]=-(df[col]-df.coin.map(lambda c:drifts[c][h]))
    def wsumm(g,wcol):
        g=g.dropna(subset=[wcol]);g=g[g[wcol]>0]
        out={"n":len(g),"days":g.day.nunique()}
        for col in ["xr1","xr23","xr13"]:
            W=g[wcol];m=(g[col]*W).sum()/W.sum()
            dd=((g[col]-m)*W).groupby(g.day).sum();D=len(dd)
            se=np.sqrt((dd**2).sum()*D/(D-1))/W.sum()
            out[col]=round(m*100,3);out["t_"+col]=round(m/se,2)
        return pd.Series(out)
    df["kw"]=df.k.clip(upper=4)
    res={"weighted_by_forecast":wsumm(df,"wf").to_frame().T,
         "weighted_by_runlen":wsumm(df,"kw").to_frame().T,
         "k_ge2_unweighted":wsumm(df[df.k>=2].assign(one=1.0),"one").to_frame().T,
         "by_year_fw":df.groupby("year").apply(lambda g:wsumm(g,"wf")),
         "by_coin_fw":df.groupby("coin").apply(lambda g:wsumm(g,"wf"))}
    for col in ["xr1","xr13"]:
        for yr,g in df.groupby("year"):
            s=stats.linregress(g.k.clip(upper=10),g[col])
            res[f"slope_{col}_{yr}"]=f"{s.slope*100:.3f}%/day t {s.slope/s.stderr:.2f} n {len(g)}"
    return res
