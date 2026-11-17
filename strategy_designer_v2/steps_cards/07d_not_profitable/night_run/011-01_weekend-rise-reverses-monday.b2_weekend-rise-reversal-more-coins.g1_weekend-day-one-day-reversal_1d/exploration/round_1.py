import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; days=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            b["ts"]=pd.to_datetime(b["timestamp"],utc=True)
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["ret"]=b["close"].pct_change()
            b["vol"]=b["ret"].rolling(20).std()
            b["z"]=b["ret"]/b["vol"]
            b["pos"]=b["postRebalance_current_allocation"]
            b["fee"]=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["coin"]=c; b["win"]=w; b["year"]=b["ts"].dt.year; b["wd"]=b["ts"].dt.weekday
            rows.append(b[["coin","win","year","wd","r1","ret","z","pos","fee","regime"]])
        for w,d in data["days"][c].items():
            d=d.copy(); d["coin"]=c; d["win"]=w
            d["year"]=pd.to_datetime(d["day"]).dt.year
            days.append(d)
    B=pd.concat(rows); D=pd.concat(days)
    mu=B.groupby("coin")["r1"].mean()
    B["mu"]=B["coin"].map(mu)
    B["g"]=B["pos"]*B["r1"]; B["drift"]=B["pos"]*B["mu"]; B["timing"]=B["pos"]*(B["r1"]-B["mu"])
    act=B[B["pos"].abs()>1e-9]
    out={}
    out["by_weekday_active"]=B.groupby("wd").agg(n=("g","size"),meanpos=("pos","mean"),abspos=("pos",lambda x:x.abs().mean()),gain=("g","mean"),drift=("drift","mean"),timing=("timing","mean"),fee=("fee","mean"))
    act=act.copy(); act["side"]=np.sign(act["pos"])
    out["by_side"]=act.groupby("side").agg(n=("g","size"),gain=("g","mean"),timing=("timing","mean"),drift=("drift","mean"),fee=("fee","mean"))
    act["zq"]=pd.qcut(act["z"],5,labels=False)
    out["by_zq"]=act.groupby("zq").agg(n=("g","size"),z=("z","mean"),pos=("pos","mean"),gain=("g","mean"),timing=("timing","mean"),r1=("r1","mean"))
    out["by_year_bars"]=B.groupby("year").agg(gain=("g","mean"),drift=("drift","mean"),timing=("timing","mean"),fee=("fee","mean"))
    dd=D.groupby(["win","day"]).agg(br=("book_return","mean"),cr=("coin_return","mean")).dropna()
    out["daily"]=pd.Series({"book_mean":dd.br.mean(),"book_sd":dd.br.std(),"hold_mean":dd.cr.mean(),"hold_sd":dd.cr.std(),"n":len(dd),"share_days_zero":(dd.br.abs()<1e-9).mean(),"total_fee_per_bar":B["fee"].mean(),"gross_g_per_bar":B["g"].mean()})
    dd2=dd.reset_index(); dd2["year"]=pd.to_datetime(dd2["day"]).dt.year
    out["daily_by_year"]=dd2.groupby("year").agg(book=("br","mean"),hold=("cr","mean"),n=("br","size"))
    return out
