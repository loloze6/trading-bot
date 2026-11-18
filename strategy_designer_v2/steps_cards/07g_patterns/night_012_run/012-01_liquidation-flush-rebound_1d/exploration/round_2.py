def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            vol=r.rolling(20).std().shift(1)
            z=r/vol
            vr=b["volume"]/b["volume"].rolling(30).mean().shift(1)
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            wick=(np.minimum(b["open"],c)-b["low"])/rng
            yr=pd.to_datetime(b["timestamp"]).dt.year
            for h in (1,2,3,5):
                fwd=c.shift(-h)/c-1
                grid=(np.arange(len(b))%h==0)
                rows.append(pd.DataFrame({"coin":coin,"w":w,"wn":int(w[1:]),"h":h,"z":z,"vr":vr,"wick":wick,"fwd":fwd,"grid":grid,"yr":yr,"vol":vol}))
    D=pd.concat(rows,ignore_index=True)
    D=D[D.grid].dropna(subset=["fwd","z","vr"])
    D["ex"]=D["fwd"]-D.groupby(["coin","h"])["fwd"].transform("mean")
    D["exv"]=D["ex"]/D["vol"]
    out={}
    def summ(g):
        n=len(g); return pd.Series({"n":n,"mean_ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(n)) if n>2 else np.nan})
    F=D[D.z<=-1].copy()
    F["lvr"]=np.log(F.vr)
    sp={}
    for h in (1,2,3,5):
        g=F[F.h==h]
        sp[h]={"rho_vr":stats.spearmanr(g.vr,g.ex)[0],"p_vr":stats.spearmanr(g.vr,g.ex)[1],
               "rho_wick":stats.spearmanr(g.wick,g.ex)[0],"p_wick":stats.spearmanr(g.wick,g.ex)[1],
               "rho_zvr":stats.spearmanr(-g.z*g.vr,g.ex)[0],"p_zvr":stats.spearmanr(-g.z*g.vr,g.ex)[1],"n":len(g)}
    out["falls_spearman"]=pd.DataFrame(sp).T
    # all bars: vr effect regardless of sign (is it volume or the fall?)
    D["vrb"]=pd.cut(D.vr,[0,1,2,4,np.inf])
    D["sgn"]=np.where(D.z<=-1,"fall",np.where(D.z>=1,"rise","mid"))
    out["h3_by_sign_vr"]=D[D.h==3].groupby(["sgn","vrb"],observed=True).apply(summ).unstack(0)
    F3=F[F.h==3].copy(); F3["hv"]=F3.vr>=2
    out["h3_falls_vr2_by_coin"]=F3.groupby(["coin","hv"]).apply(summ).unstack(1)
    out["h3_falls_vr2_by_year"]=F3.groupby(["yr","hv"]).apply(summ).unstack(1)
    out["h3_falls_vr2_by_windowthird"]=F3.groupby([pd.cut(F3.wn,[0,8,16,24]),"hv"],observed=True).apply(summ).unstack(1)
    F3["zb"]=pd.cut(F3.z,[-np.inf,-2.5,-1.5,-1])
    out["h3_falls_z_by_vr"]=F3.groupby(["zb","hv"],observed=True).apply(summ).unstack(1)
    # regression on falls: ex ~ log vr + z + wick
    g=F3.dropna(subset=["wick"])
    X=np.column_stack([np.ones(len(g)),np.log(g.vr),g.z,g.wick]); y=g.ex.values
    beta,res,_,_=np.linalg.lstsq(X,y,rcond=None); e=y-X@beta
    cov=np.linalg.inv(X.T@X)*(e@e/(len(y)-4))
    out["reg_h3_falls"]=pd.DataFrame({"beta":beta,"t":beta/np.sqrt(np.diag(cov))},index=["c","logvr","z","wick"])
    return out
