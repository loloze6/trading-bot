import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d=df.sort_values("timestamp").reset_index(drop=True)
            c=d["close"].astype(float)
            r=c.pct_change()
            vol=r.pow(2).shift(1).rolling(60,min_periods=20).mean().pow(0.5)
            ts=pd.to_datetime(d["timestamp"])
            g=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(d)),"r":r,"z":r/vol,"vol":vol,
                            "f2":c.shift(-2)/c-1,"f3":c.shift(-3)/c-1,"wd":ts.dt.weekday,"year":ts.dt.year,
                            "p7":c.shift(1)/c.shift(8)-1,"p14":c.shift(1)/c.shift(15)-1,"p30":c.shift(1)/c.shift(31)-1})
            rows.append(g)
    A=pd.concat(rows,ignore_index=True)
    out={}
    for h in [2,3]:
        m=A[A.pos%h==0].groupby("coin")[f"f{h}"].mean()
        A[f"ex{h}"]=A[f"f{h}"]-A["coin"].map(m)
    G=A[A.pos%2==0].dropna(subset=["z","ex2","p7"]).copy()
    def reg(g,x,y="ex2"):
        g=g.dropna(subset=[x,y])
        if len(g)<30: return pd.Series({"n":len(g),"slope":np.nan,"t":np.nan})
        l=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope":l.slope,"t":l.slope/l.stderr})
    # counter-trend signed move: z * -sign(prior trend), positive when move goes against trend
    for L in ["p7","p14","p30"]:
        G["ct_"+L]=-G.z*np.sign(G[L])
    out["ct_slope_by_lookback"]=pd.DataFrame({L:reg(G,"ct_"+L) for L in ["p7","p14","p30"]}).T
    out["plain_signed_z_slope"]=reg(G,"z")
    G["ctq"]=pd.qcut(G.ct_p7,5,labels=False)
    out["ct7_quintiles"]=G.groupby("ctq").apply(lambda g: pd.Series({"n":len(g),"mean_ct":g.ct_p7.mean(),"mean_ex2":g.ex2.mean(),"t":g.ex2.mean()/(g.ex2.std()/np.sqrt(len(g)))}))
    out["ct7_by_year"]=G.groupby("year").apply(lambda g: reg(g,"ct_p7"))
    out["ct7_by_coin"]=G.groupby("coin").apply(lambda g: reg(g,"ct_p7"))
    out["ct7_by_wd"]=G.groupby("wd").apply(lambda g: reg(g,"ct_p7"))
    G3=A[A.pos%3==0].dropna(subset=["z","ex3","p7"]).copy(); G3["ct"]=-G3.z*np.sign(G3.p7)
    out["ct7_h3"]=reg(G3,"ct","ex3")
    # does ct survive with abs z (tested idea) in same regression
    X=G.dropna(subset=["ct_p7"]); Xm=np.column_stack([np.ones(len(X)),X.ct_p7,X.z.abs()])
    b,res,_,_=np.linalg.lstsq(Xm,X.ex2.values,rcond=None); e=X.ex2.values-Xm@b
    s2=e@e/(len(X)-3); se=np.sqrt(np.diag(s2*np.linalg.inv(Xm.T@Xm)))
    out["joint_ct_absz"]=pd.DataFrame({"b":b,"t":b/se},index=["const","ct7","absz"])
    # book around its largest days
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df.copy().reset_index(drop=True); x["nxt"]=x.book_return.shift(-1); x["prv"]=x.book_return.shift(1); D.append(x)
    D=pd.concat(D).dropna(subset=["book_return"])
    D["bq"]=pd.qcut(D.book_return.rank(method="first"),10,labels=False)
    out["book_next_by_decile"]=D.groupby("bq")[["book_return","prv","nxt"]].mean()
    return out
