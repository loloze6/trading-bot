import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    grid = []
    dd = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            lr = np.log(c).diff()
            df = pd.DataFrame({"coin":coin,"w":w})
            df["ret72"] = c/c.shift(72)-1
            df["ret24"] = c/c.shift(24)-1
            df["vol72"] = lr.rolling(72).std()*np.sqrt(72)
            df["vol30d"] = lr.rolling(720,min_periods=200).std()*np.sqrt(72)
            df["z72"] = df["ret72"]/df["vol30d"]
            df["fwd72"] = c.shift(-72)/c-1
            df["f"] = b["forecast"].fillna(0).values
            grid.append(df.iloc[::72])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"]=coin; d["w"]=w
            dd.append(d[["coin","w","book_return","coin_return"]])
    G = pd.concat(grid).dropna(subset=["ret72","fwd72"])
    mu = G.groupby("coin")["fwd72"].mean()
    G["x"] = G["fwd72"]-G["coin"].map(mu)
    A = G[G.ret72<=0].copy()
    def summ(g):
        return pd.Series({"n":len(g),"x":g.x.mean(),"t":g.x.mean()/(g.x.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    A["d72"] = pd.qcut(A["ret72"],10,labels=False)
    out["x_by_ret72_decile"] = A.groupby("d72").apply(summ)
    A2 = A.dropna(subset=["z72"]).copy()
    A2["dz"] = pd.qcut(A2["z72"],10,labels=False)
    out["x_by_volscaled_fall_decile"] = A2.groupby("dz").apply(summ)
    A["both"] = (A.ret72<=A.ret72.quantile(0.2)).astype(int)*2 + (A.ret24<=A.ret24.quantile(0.2)).astype(int)
    out["x_by_joint_deep(2=deep72,1=deep24)"] = A.groupby("both").apply(summ)
    # forecast quintiles on grid
    Af = A[A.f>0].copy()
    Af["fq"] = pd.qcut(Af["f"],5,labels=False,duplicates="drop")
    out["x_by_forecast_q"] = Af.groupby("fq").apply(summ)
    # does the effect need a widening vol state
    A["volratio"] = A["vol72"]/A["vol30d"]
    A3 = A.dropna(subset=["volratio"]).copy()
    A3["vq"] = pd.qcut(A3["volratio"],4,labels=False)
    A3["deep"] = A3.ret72<=A3.ret72.quantile(0.2)
    out["x_by_volratio_q_and_deep"] = A3.groupby(["vq","deep"]).apply(summ)
    # by coin, deep cases
    out["x_deep72_by_coin"] = A[A.d72<=1].groupby("coin").apply(summ)
    D = pd.concat(dd).dropna(subset=["book_return"])
    dm = D.groupby(D.index if False else ["w"]).size()
    out["book_daily"] = pd.Series({"mean":D.book_return.mean(),"sd":D.book_return.std(),"coin_mean":D.coin_return.mean(),
        "share_days_neg":(D.book_return<0).mean()})
    return out
