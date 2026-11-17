import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            cl=b["close"]
            b["ret"]=cl.pct_change()
            b["vol"]=b["ret"].rolling(20).std()
            b["z"]=b["ret"]/b["vol"]
            for h in (1,2,3):
                b[f"r{h}"]=cl.shift(-h)/cl-1
            b["r2only"]=cl.shift(-2)/cl.shift(-1)-1
            b["r3only"]=cl.shift(-3)/cl.shift(-2)-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=c; b["win"]=w; b["wd"]=b["ts"].dt.weekday; b["year"]=b["ts"].dt.year
            b["volu"]=b["volume"]/b["volume"].rolling(20).median()
            rows.append(b[["coin","win","wd","year","z","ret","vol","r1","r2","r3","r2only","r3only","pos","fee","volu"]])
    B=pd.concat(rows)
    mu=B.groupby("coin")["r1"].mean(); B["mu"]=B["coin"].map(mu)
    out={}
    W=B[B["wd"].isin([5,6])].dropna(subset=["z","r1"]).copy()
    W["g"]=W["pos"]*W["r1"]
    W["az"]=pd.qcut(W["z"].abs(),5,labels=False)
    # fee of opening on this bar plus fee of closing on Monday bar approx: use fee on bar and next bar
    out["by_absz"]=W.groupby("az").agg(n=("g","size"),absz=("z",lambda x:x.abs().mean()),abspos=("pos",lambda x:x.abs().mean()),gain=("g","mean"),fee=("fee","mean"),fade1=("r1",lambda x:np.nan))
    W["f1"]=-np.sign(W["z"])*(W["r1"]-W["mu"])
    W["f2only"]=-np.sign(W["z"])*(W["r2only"]-W["mu"])
    W["f3only"]=-np.sign(W["z"])*(W["r3only"]-W["mu"])
    def tt(x): x=x.dropna(); return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    res={}
    for d in (5,6):
        for az in range(5):
            s=W[(W.wd==d)&(W.az==az)]
            res[(d,az)]={"fade_day1":s["f1"].mean(),"fade_day2":s["f2only"].mean(),"fade_day3":s["f3only"].mean(),"n":len(s)}
    out["fade_by_day_absz"]=pd.DataFrame(res).T
    # weekday same
    K=B[~B["wd"].isin([5,6])].dropna(subset=["z","r1"]).copy()
    K["f1"]=-np.sign(K["z"])*(K["r1"]-K["mu"])
    K["az"]=pd.qcut(K["z"].abs(),5,labels=False)
    out["weekday_fade_absz"]=K.groupby("az")["f1"].mean()
    # volume effect on weekend
    W["vq"]=pd.qcut(W["volu"],3,labels=False)
    out["weekend_fade_by_volume"]=W.groupby(["vq"]).apply(lambda s: pd.Series({"f1":s["f1"].mean(),"t":tt(s["f1"])["t"],"gain":s["g"].mean(),"fee":s["fee"].mean(),"n":len(s)}))
    # combined sat+sun 2-day move reversed over Mon
    S=B[B["wd"]==6].dropna(subset=["r1"]).copy()
    out["sum_fee_vs_gross"]=pd.Series({"weekend_gross_per_bar":W["g"].mean(),"weekend_fee_per_bar":W["fee"].mean(),"monday_fee_per_bar":B[B.wd==0]["fee"].mean(),"turnover_sat":(B[B.wd==5]["pos"]-0).abs().mean()})
    return out
