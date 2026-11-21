import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out={}
    recs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; lo=b["low"]
            r1=c.pct_change()
            f=pd.DataFrame({"c":c,
                "ret20":c/c.shift(20)-1,"ret60":c/c.shift(60)-1,
                "abv20lo":c/lo.shift(1).rolling(20).min()-1,
                "abv60lo":c/lo.shift(1).rolling(60).min()-1,
                "vol20":r1.rolling(20).std(),"ret1":r1,
                "wd":pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr":pd.to_datetime(b["timestamp"]).dt.year,
                "pos":np.arange(len(b))})
            for H in [1,5,10,20]:
                f[f"fwd{H}"]=c.shift(-H)/c-1
            f["coin"]=coin; f["w"]=w
            recs.append(f)
    d=pd.concat(recs)
    # drift & sd per coin per H on grid
    for H in [5,10,20]:
        g=d[d.pos%H==0].dropna(subset=[f"fwd{H}"])
        st=g.groupby("coin")[f"fwd{H}"].agg(["mean","std"])
        res={}
        for col in ["ret20","ret60","abv20lo","abv60lo"]:
            x=g.dropna(subset=[col]).copy()
            x["z"]=x.groupby("coin")[col].transform(lambda s:(s-s.mean())/s.std())
            x["y"]=(x[f"fwd{H}"]-x.coin.map(st["mean"]))/x.coin.map(st["std"])
            sl=stats.linregress(x["z"],x["y"])
            row={"slope":sl.slope,"t":sl.slope/sl.stderr,"n":len(x)}
            for cn,xx in x.groupby("coin"):
                s2=stats.linregress(xx["z"],xx["y"]); row[cn[:3]]=round(s2.slope/s2.stderr,2)
            x["half"]=np.where(x.yr<=2021,"early","late")
            for hh,xx in x.groupby("half"):
                s2=stats.linregress(xx["z"],xx["y"]); row[hh]=round(s2.slope/s2.stderr,2)
            res[col]=row
        out[f"mom_H{H}"]=pd.DataFrame(res).T
    # weekday on 1-day returns, by coin and half
    x=d.dropna(subset=["fwd1"]).copy()
    x["dayret"]=x["ret1"]
    x=x.dropna(subset=["dayret"])
    x["half"]=np.where(x.yr<=2021,"early","late")
    t=x.groupby(["wd"])["dayret"].agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"]))
    out["weekday_dayret"]=t
    out["weekday_by_half"]=x.groupby(["wd","half"])["dayret"].mean().unstack()
    out["weekday_by_coin"]=x.groupby(["wd","coin"])["dayret"].mean().unstack()
    # large daily moves: next 5 days by size of the day's move (z)
    x["z1"]=x["ret1"]/x["vol20"]
    x=x.dropna(subset=["z1","fwd5"])
    x["zb"]=pd.cut(x["z1"],[-99,-2,-1,0,1,2,99])
    g=x[x.pos%5==0].groupby("zb")["fwd5"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["after_day_move"]=g
    # book: daily returns by position side
    bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            a=b["postRebalance_current_allocation"].values
            c=b["close"].values
            g=a[:-1]*(c[1:]/c[:-1]-1)
            bk.append(pd.DataFrame({"side":np.sign(a[:-1]),"gain":g,"coin":coin}))
    bk=pd.concat(bk)
    out["book_gain_by_side"]=bk.groupby("side")["gain"].agg(["mean","count","sum"])
    return out
