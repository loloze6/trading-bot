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
            z=r/vol
            vrel=d["volume"].astype(float)/d["volume"].astype(float).shift(1).rolling(30,min_periods=10).mean()
            f2=c.shift(-2)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(d["timestamp"])
            g=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(d)),"r":r,"z":z,"vol":vol,"vrel":vrel,
                            "f2":f2,"f1":f1,"wd":ts.dt.weekday,"year":ts.dt.year,
                            "r7":c/c.shift(7)-1})
            rows.append(g)
    A=pd.concat(rows,ignore_index=True)
    m2=A[A.pos%2==0].groupby("coin")["f2"].mean()
    A["ex2"]=A["f2"]-A["coin"].map(m2)
    G=A[(A.pos%2==0)].dropna(subset=["z","ex2"]).copy()
    out={}
    G["zb"]=pd.cut(G.z,[-np.inf,-2,-1,-0.5,0,0.5,1,2,np.inf])
    def summ(gr):
        return pd.Series({"n":len(gr),"mean_ex2":gr.ex2.mean(),"t":gr.ex2.mean()/(gr.ex2.std()/np.sqrt(len(gr)))})
    out["by_signed_z"]=G.groupby("zb",observed=True).apply(summ)
    G["absz_q"]=pd.qcut(G.z.abs(),5,labels=False)
    G["side"]=np.sign(G.z)
    out["absz_q_by_side"]=G.groupby(["side","absz_q"]).apply(summ)
    # weekday of move, large abs moves
    G["big"]=G.z.abs()>1.5
    out["wd_big_side"]=G[G.big].groupby(["wd","side"]).apply(summ)
    # vol regime: vol quintile within coin
    G["volq"]=G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=False))
    out["absz_by_volq_slope"]=G.groupby("volq").apply(lambda g: pd.Series(dict(zip(["slope","t","n"],[stats.linregress(g.z.abs(),g.ex2).slope, stats.linregress(g.z.abs(),g.ex2).slope/stats.linregress(g.z.abs(),g.ex2).stderr,len(g)]))))
    # signed z slope by 7d trend
    G["tr"]=np.sign(G.r7)
    out["signedz_by_trend"]=G.dropna(subset=["r7"]).groupby(["tr","side"]).apply(lambda g: pd.Series({"n":len(g),"slope_absz":stats.linregress(g.z.abs(),g.ex2).slope,"t":stats.linregress(g.z.abs(),g.ex2).slope/stats.linregress(g.z.abs(),g.ex2).stderr}))
    # volume relative
    H=G.dropna(subset=["vrel"]).copy()
    H["vq"]=pd.qcut(H.vrel,3,labels=False)
    out["big_by_volume"]=H[H.big].groupby(["vq","side"]).apply(summ)
    out["by_year_slope"]=G.groupby("year").apply(lambda g: pd.Series({"n":len(g),"slope":stats.linregress(g.z.abs(),g.ex2).slope,"t":stats.linregress(g.z.abs(),g.ex2).slope/stats.linregress(g.z.abs(),g.ex2).stderr}))
    # book by weekday
    D=[]
    for coin,wins in data["days"].items():
        for w,df in wins.items():
            x=df.copy(); x["wd"]=pd.to_datetime(x["day"]).dt.weekday; D.append(x)
    D=pd.concat(D)
    out["book_coin_by_wd"]=D.groupby("wd")[["book_return","coin_return"]].mean()
    return out
