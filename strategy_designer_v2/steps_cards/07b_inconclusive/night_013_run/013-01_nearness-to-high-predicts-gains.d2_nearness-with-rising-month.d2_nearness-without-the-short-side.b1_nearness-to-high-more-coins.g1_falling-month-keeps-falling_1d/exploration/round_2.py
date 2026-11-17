import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    H=[7,14,21,30]
    allrows={}
    for h in H:
        rows=[]
        for coin,wins in data["bars"].items():
            for w,df in wins.items():
                df=df.reset_index(drop=True)
                c=df["close"].values; n=len(c)
                r30=pd.Series(c).pct_change(30).values
                dep=df["debug_info.components.depth.last_history_value"].values if "debug_info.components.depth.last_history_value" in df else np.full(n,np.nan)
                for i in range(0,n-h,h):
                    rows.append({"coin":coin,"w":w,"year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 "reg":df["regime"].iloc[i],"fc":df["forecast"].iloc[i],"depth":dep[i],
                                 "r30":r30[i],"r":c[i+h]/c[i]-1})
        d=pd.DataFrame(rows)
        d["x"]=d["r"]-d.groupby("coin")["r"].transform("mean")
        allrows[h]=d
    def slope(g,x="fc",y="x"):
        g=g[[x,y]].dropna()
        if len(g)<10 or g[x].std()==0: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        r=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":r.slope,"t":r.slope/r.stderr})
    out["nonoverlap_fc"]=pd.DataFrame({f"h{h}":slope(allrows[h][allrows[h].reg=="mean_reversion"]) for h in H}).T
    out["nonoverlap_depth"]=pd.DataFrame({f"h{h}":slope(allrows[h][allrows[h].reg=="mean_reversion"],x="depth") for h in H}).T
    out["nonoverlap_r30_mr"]=pd.DataFrame({f"h{h}":slope(allrows[h][allrows[h].reg=="mean_reversion"],x="r30") for h in H}).T
    out["nonoverlap_r30_other"]=pd.DataFrame({f"h{h}":slope(allrows[h][allrows[h].reg!="mean_reversion"],x="r30") for h in H}).T
    for h in [14,30]:
        m=allrows[h][allrows[h].reg=="mean_reversion"].copy()
        m["dq"]=pd.qcut(m["depth"].rank(method="first"),5,labels=False)
        out[f"depthq_h{h}"]=m.groupby("dq").agg(n=("x","count"),depth=("depth","mean"),fc=("fc","mean"),x=("x","mean"),sd=("x","std"))
        out[f"year_fc_h{h}"]=m.groupby("year").apply(slope)
        bc=m.groupby("coin").apply(slope)
        out[f"coin_pos_share_h{h}"]=f"{(bc.slope>0).mean():.2f} of {bc.slope.notna().sum()} coins positive; median t {bc.t.median():.2f}"
        m["half"]=np.where(m.year<=2021,"<=2021",">2021")
        out[f"half_fc_h{h}"]=m.groupby("half").apply(slope)
    # bivariate h14: fc and r30
    m=allrows[14][allrows[14].reg=="mean_reversion"][["fc","r30","x"]].dropna()
    X=np.column_stack([np.ones(len(m)),m.fc,m.r30]); b,res,_,_=np.linalg.lstsq(X,m.x,rcond=None)
    e=m.x-X@b; s2=(e**2).sum()/(len(m)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    out["h14_fc_plus_r30"]=pd.DataFrame({"b":b,"t":b/se},index=["const","fc","r30"])
    return out
