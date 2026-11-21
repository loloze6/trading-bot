def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    ev=[]; drops=[]
    for coin, wins in data["bars"].items():
        g=[];g6=[]
        r1=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H); g+=list(c[idx+H]/c[idx]-1)
            idx6=np.arange(0,len(c)-6,6); g6+=list(c[idx6+6]/c[idx6]-1)
            r1.append(b["close"].pct_change())
        if len(g)<10: continue
        drift=np.nanmean(g); sd=np.nanstd(g); drift6=np.nanmean(g6); sd6=np.nanstd(g6)
        r1=pd.concat(r1); d1=r1.mean(); s1=r1.std()
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]
            rng=(hi-lo)/c; m180=rng.rolling(180).mean()
            phi=hi.shift(1).rolling(12).max(); plo=lo.shift(1).rolling(12).min()
            narrow=m180/((phi-plo)/c.shift(1))
            r180=c/c.shift(180)-1
            fwd=c.shift(-H)/c-1; fwd6=c.shift(-6)/c-1
            n=len(b); cell=np.arange(n)//H; cell6=np.arange(n)//6
            wn=int(w[1:])
            df=pd.DataFrame({"cell":cell,"narrow":narrow,"r180":r180,"fwd":fwd,"dn":c<plo,"up":c>phi})
            df=df[df.fwd.notna()&df.narrow.notna()&df.r180.notna()]
            for side in ["dn","up"]:
                e=df[df[side]].groupby("cell").head(1).copy()
                s=1 if side=="up" else -1
                e["side"]=side; e["coin"]=coin; e["half"]="early" if wn<=12 else "late"; e["w"]=w
                e["u"]=(e.fwd-drift)*s*100; e["tot"]=e.fwd*s*100; e["uz"]=(e.fwd-drift)*s/sd
                ev.append(e[["side","coin","half","w","narrow","r180","u","tot","uz"]])
            z0=(c.pct_change()-d1)/s1
            dd=pd.DataFrame({"cell":cell6,"z0":z0,"f6":fwd6,"f18":fwd,"r180":r180})
            dd=dd[(dd.z0<=-2)&dd.f6.notna()].groupby("cell").head(1).copy()
            dd["u6"]=(dd.f6-drift6)*100; dd["u18"]=(dd.f18-drift)*100; dd["half"]="early" if wn<=12 else "late"
            drops.append(dd)
    E=pd.concat(ev); D=pd.concat(drops)
    out={}
    def agg(x,col="u"):
        return pd.Series({"n":len(x),"u_pct":x[col].mean(),"tot_pct":x.tot.mean() if "tot" in x else np.nan,"t":x[col].mean()/x[col].std()*np.sqrt(len(x))})
    E["agree"]=np.where(((E.side=="dn")&(E.r180<0))|((E.side=="up")&(E.r180>0)),"with30d","against30d")
    out["by_agreement_half"]=E.groupby(["agree","half"]).apply(agg)
    out["by_agreement"]=E.groupby(["agree"]).apply(agg)
    A=E[(E.side=="dn")&(E.r180<0)].copy()
    A["nq"]=pd.qcut(A.narrow,5,labels=False)
    out["dn_neg_narrow_quint"]=A.groupby("nq").apply(agg)
    out["dn_neg_narrow_quint_half"]=A.groupby(["half","nq"]).apply(agg)
    rho=[];
    for h,x in A.groupby("half"):
        r,p=stats.spearmanr(x.narrow,x.uz); rho.append((h,r,p,len(x)))
    r,p=stats.spearmanr(A.narrow,A.uz); rho.append(("all",r,p,len(A)))
    out["dn_neg_spearman"]=pd.DataFrame(rho,columns=["half","rho","p","n"])
    top=A[A.nq==4]
    pc=top.groupby("coin").u.mean()
    out["dn_neg_narrowest_coins_pos_share"]=pd.Series({"coins":len(pc),"pos":(pc>0).sum()})
    U=E[(E.side=="up")&(E.r180>0)].copy(); U["nq"]=pd.qcut(U.narrow,5,labels=False)
    out["up_pos_narrow_quint"]=U.groupby("nq").apply(agg)
    # against trend graded by narrowness (reversal)
    X=E[E.agree=="against30d"].copy(); X["nq"]=pd.qcut(X.narrow,5,labels=False)
    out["against_narrow_quint"]=X.groupby("nq").apply(agg)
    D["zb"]=pd.cut(D.z0,[-99,-4,-3,-2])
    D["reg"]=np.where(D.r180<0,"neg","pos")
    def ad(x):
        return pd.Series({"n":len(x),"u6":x.u6.mean(),"t6":x.u6.mean()/x.u6.std()*np.sqrt(len(x)),
                          "u18":x.u18.mean(),"t18":x.u18.mean()/x.u18.std()*np.sqrt(x.u18.notna().sum())})
    out["drop_rebound_z"]=D.groupby("zb").apply(ad)
    out["drop_rebound_z_half"]=D.groupby(["half","zb"]).apply(ad)
    out["drop_rebound_reg"]=D.groupby(["reg","zb"]).apply(ad)
    return out
