def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]
    out={}
    ev=[]; g=[]
    for c in bars:
        for w,b in bars[c].items():
            ts=pd.to_datetime(b["timestamp"]); hr=ts.dt.hour.values; yr=ts.dt.year.values
            cl=b["close"].values.astype(float)
            n=len(cl)
            r2=np.full(n,np.nan); r2[:-2]=cl[2:]/cl[:-2]-1
            r24=np.full(n,np.nan); r24[24:]=cl[24:]/cl[:-24]-1
            lr=pd.Series(np.log(cl)).diff()
            vol=lr.rolling(168).std()*np.sqrt(24)
            vs=r24/vol.values
            conc=(lr.abs().rolling(24).max()/lr.abs().rolling(24).sum()).values
            f24=np.full(n,np.nan); f24[:-24]=cl[24:]/cl[:-24]-1
            f72=np.full(n,np.nan); f72[:-72]=cl[72:]/cl[:-72]-1
            vq=vol.rank(pct=True).values
            m=hr==20
            ev.append(pd.DataFrame({"coin":c,"win":w,"yr":yr[m],"vs":vs[m],"r2":r2[m],"vol":vol.values[m]}))
            idx=np.arange(24,n,24)
            g.append(pd.DataFrame({"coin":c,"yr":yr[idx],"vs":vs[idx],"conc":conc[idx],"f24":f24[idx],"f72":f72[idx]}))
    E=pd.concat(ev).dropna()
    def tt(s): return pd.Series({"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))),"n":len(s)})
    out["r2_21_by_year"]=E.groupby("yr")["r2"].apply(tt).unstack()
    out["r2_21_by_coin_all"]=E.groupby("coin")["r2"].apply(tt).unstack()
    wm=E.groupby("win")["r2"].mean(); out["r2_21_share_windows_pos"]=float((wm>0).mean())
    E["absq"]=pd.qcut(E["vs"].abs(),5,labels=False)
    out["r2_21_by_absvs_q"]=E.groupby("absq")["r2"].apply(tt).unstack()
    E["volq"]=pd.qcut(E.groupby("coin")["vol"].rank(pct=True),4,labels=False)
    out["r2_21_by_vol_q"]=E.groupby("volq")["r2"].apply(tt).unstack()
    out["spearman_absvs_r2"]=float(stats.spearmanr(E["vs"].abs(),E["r2"])[0])
    out["spearman_negvs_r2_fallonly"]=float(stats.spearmanr(-E.loc[E.vs<0,"vs"],E.loc[E.vs<0,"r2"])[0])
    out["spearman_vs_r2_riseonly"]=float(stats.spearmanr(E.loc[E.vs>0,"vs"],E.loc[E.vs>0,"r2"])[0])
    G=pd.concat(g).dropna()
    G["cq"]=pd.qcut(G["conc"],3,labels=False)
    for h in ["f24","f72"]:
        out[h+"_by_conc"]=G.groupby("cq")[h].apply(tt).unstack()
        hi=G.loc[G.cq==2,h]; lo=G.loc[G.cq==0,h]
        out[h+"_high_minus_low_conc_welch"]=pd.Series({"diff":hi.mean()-lo.mean(),"t":stats.ttest_ind(hi,lo,equal_var=False)[0]})
    G["sf72"]=np.sign(G["vs"])*G["f72"]
    G["avq"]=pd.qcut(G["vs"].abs(),3,labels=False)
    out["signed_f72_by_absvs_conc"]=G.pivot_table(index="avq",columns="cq",values="sf72",aggfunc="mean")
    out["conc_f24_by_year"]=G.groupby(["yr","cq"])["f24"].mean().unstack()
    # partial: regress f24 on conc controlling vs
    X=np.column_stack([np.ones(len(G)),G["vs"],G["conc"]]); y=G["f24"].values
    bb,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@bb
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-3)); out["ols_f24_vs_conc"]=pd.Series({"b_vs":bb[1],"t_vs":bb[1]/np.sqrt(cov[1,1]),"b_conc":bb[2],"t_conc":bb[2]/np.sqrt(cov[2,2]),"n":len(y)})
    out["f24_by_coin_conc"]=G.groupby(["coin","cq"])["f24"].mean().unstack()
    return out
