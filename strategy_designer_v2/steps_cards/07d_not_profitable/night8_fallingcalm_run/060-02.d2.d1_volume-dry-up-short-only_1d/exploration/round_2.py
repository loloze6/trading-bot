def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    wins = sorted(data["bars"][coins[0]].keys(), key=lambda w:int(w[1:]))
    rows=[]
    for c in coins:
        for w in wins:
            d=data["days"][c].get(w)
            if d is None: continue
            t=d[["day","book_return","coin_return"]].copy(); t["coin"]=c; t["w"]=w
            rows.append(t)
    D=pd.concat(rows)
    B=D.groupby(["w","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    B["wn"]=B.w.str[1:].astype(int); B=B.sort_values(["wn","day"]).dropna(subset=["br"]).reset_index(drop=True)
    B["year"]=pd.to_datetime(B.day).dt.year
    v=(1+B.br).cumprod(); peak=v.cummax(); dd=v/peak-1
    B["dd"]=dd.values
    i=int(np.argmin(dd.values)); pk=int(np.argmax(v.values[:i+1]))
    out["deepest fall"]=pd.Series({"depth":dd.values[i],"days_long":i-pk,"peak_window":B.w.values[pk],"trough_window":B.w.values[i],"coin_mean_ret_in_fall":B.cr.values[pk+1:i+1].sum()})
    falldays=set(zip(B.w.values[pk+1:i+1],B.day.values[pk+1:i+1]))
    out["by window"]=B.groupby("w").agg(book_sum=("br","sum"),coin_sum=("cr","sum"),min_dd=("dd","min")).reindex(wins)
    # contributions by coin in deepest fall
    Df=D[[ (a,b) in falldays for a,b in zip(D.w,D.day)]]
    out["fall by coin (sum book_return/6)"]=(Df.groupby("coin").book_return.sum()/6)
    # cases and non-signal bars in regime
    cs=[]; ns=[]; held=[]
    for c in coins:
        drs=[]
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            cl=b.close.values
            for k in range(0,len(cl)-5,5): drs.append(cl[k+5]/cl[k]-1)
        drift=np.mean(drs)
        for w in wins:
            b=data["bars"][c].get(w)
            if b is None: continue
            b=b.reset_index(drop=True)
            cl=b.close; r1=cl.pct_change(); vol=b.volume
            vr=np.log(vol.rolling(30).mean()/vol.shift(30).rolling(30).mean())
            ret10=cl/cl.shift(10)-1; ret3=cl/cl.shift(3)-1
            v10=r1.rolling(10).std(); v60=r1.rolling(60).std()
            vrel=v10/v60
            f=b.forecast.values; n=len(b); reg=b.regime.values
            alloc=b.postRebalance_current_allocation
            g=(cl.shift(-1)/cl-1)*alloc
            held.append(pd.DataFrame({"g":g,"alloc":alloc,"vrel":vrel,"ret10":ret10,"w":w,"coin":c,"day":b.timestamp.astype(str).str[:10]}))
            for k in range(0,n-5,5):
                hit=False
                for j in range(k,min(k+5,n-5)):
                    if f[j]<=-2:
                        r5=cl[j+5]/cl[j]-1
                        cs.append(dict(coin=c,w=w,u=drift-r5,tot=-r5,f=f[j],ret10=ret10[j],ret3=ret3[j],r1=r1[j],vrel=vrel[j],vr=vr[j]))
                        hit=True; break
                if not hit and reg[k]=="mean_reversion":
                    r5=cl[k+5]/cl[k]-1
                    ns.append(dict(u=drift-r5,vr=vr[k],vrel=vrel[k],ret10=ret10[k]))
    C=pd.DataFrame(cs); N=pd.DataFrame(ns)
    def tt(s): return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    out["cases"]=pd.Series({"n":len(C),"mean_u":C.u.mean(),"t":tt(C.u),"mean_total":C.tot.mean()})
    out["regime bars no signal"]=pd.Series({"n":len(N),"mean_u":N.u.mean(),"t":tt(N.u),"vr_ge0_n":(N.vr>=0).sum(),"vr_ge0_u":N.u[N.vr>=0].mean()})
    def tab(X,col,q=3):
        x=X.dropna(subset=[col]).copy(); x["b"]=pd.qcut(x[col],q,labels=False,duplicates="drop")
        return x.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),mean_u=("u","mean"),n=("u","size"),t=("u",tt))
    out["cases by ret10"]=tab(C,"ret10"); out["cases by ret3"]=tab(C,"ret3"); out["cases by r1"]=tab(C,"r1")
    out["cases by vrel(10d/60d vol)"]=tab(C,"vrel"); out["cases by forecast"]=tab(C,"f")
    out["nosignal by vrel"]=tab(N,"vrel"); out["nosignal by ret10"]=tab(N,"ret10")
    out["cases by coin"]=C.groupby("coin").u.agg(["mean","size"])
    out["cases by window"]=C.groupby("w").u.agg(["mean","size"]).reindex(wins)
    H=pd.concat(held); H=H[H.alloc.abs()>1e-9].dropna(subset=["g"])
    H["fall"]=[(a,b) in falldays for a,b in zip(H.w,H.day)]
    out["held in fall vs not"]=H.groupby("fall").agg(mean_g=("g","mean"),n=("g","size"),vrel=("vrel","mean"),ret10=("ret10","mean"),absalloc=("alloc",lambda s:s.abs().mean()))
    H["vb"]=pd.qcut(H.vrel,3,labels=False)
    out["held gain by vrel"]=H.groupby("vb").agg(lo=("vrel","min"),mean_g=("g","mean"),sd=("g","std"),n=("g","size"))
    H["rb"]=pd.qcut(H.ret10,3,labels=False)
    out["held gain by ret10"]=H.groupby("rb").agg(lo=("ret10","min"),mean_g=("g","mean"),sd=("g","std"),n=("g","size"))
    return out
