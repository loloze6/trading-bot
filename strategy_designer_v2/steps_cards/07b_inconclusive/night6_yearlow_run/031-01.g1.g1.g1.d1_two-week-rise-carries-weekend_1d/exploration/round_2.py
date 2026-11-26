def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin, wins in data["bars"].items():
        g2=[]
        for w,b in wins.items():
            c=b["close"].values
            g2+= [c[i+2]/c[i]-1 for i in range(0,len(c)-2,2)]
        drift=np.mean(g2)
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"])
            c=b["close"]
            lr=np.log(c).diff()
            r14=np.log(c/c.shift(14))/(lr.rolling(20).std()*np.sqrt(14))
            f2=c.shift(-2)/c-1
            d=pd.DataFrame({"coin":coin,"day":ts.dt.floor("D"),"wd":ts.dt.weekday,
                            "r14":r14,"fc":b["forecast"],"ex":f2-drift,"pos":np.arange(len(b))})
            rows.append(d)
    d=pd.concat(rows).dropna(subset=["ex","r14"])
    def cl(x,col):
        x=x.dropna(subset=[col,"ex"])
        X=np.column_stack([np.ones(len(x)),x[col].values]); y=x["ex"].values
        XtXi=np.linalg.inv(X.T@X); b=XtXi@X.T@y; e=y-X@b
        S=np.zeros((2,2))
        for _,idx in x.groupby("day").indices.items():
            s=X[idx].T@e[idx]; S+=np.outer(s,s)
        G=x["day"].nunique(); n=len(x)
        V=XtXi@S@XtXi*G/(G-1)*(n-1)/(n-2)
        return pd.Series({"slope":b[1],"t_clust":b[1]/np.sqrt(V[1,1]),"n":n,"days":G})
    out={}
    fr=d[d.wd==4]
    out["friday_fc>0_on_forecast"]=cl(fr[fr.fc>0],"fc")
    out["friday_fc>0_on_raw_r14"]=cl(fr[fr.fc>0],"r14")
    out["friday_all_on_raw_r14"]=cl(fr,"r14")
    fr2=fr.copy(); fr2["r14p"]=fr2["r14"].clip(lower=0)
    out["friday_all_on_r14_clipped0"]=cl(fr2,"r14p")
    wk={}
    for wd,x in d.groupby("wd"):
        x=x[x.pos%2==0]
        wk[wd]=cl(x,"r14")
    out["by_weekday_raw_r14_all_days_grid2"]=pd.DataFrame(wk).T
    out["corr_fc_r14_friday_fc>0"]=float(fr[fr.fc>0][["fc","r14"]].corr().iloc[0,1])
    return out
