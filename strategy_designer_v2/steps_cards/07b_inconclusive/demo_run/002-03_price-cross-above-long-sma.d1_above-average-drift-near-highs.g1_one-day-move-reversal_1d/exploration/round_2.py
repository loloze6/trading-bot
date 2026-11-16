import numpy as np, pandas as pd
from scipy import stats

def tt(x):
    x=pd.Series(x).dropna()
    return x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan

def explore(data):
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            d=df.copy().reset_index(drop=True)
            d["nxt"]=d["close"].shift(-1)/d["close"]-1
            d["pos"]=d["postRebalance_current_allocation"]
            d["gain"]=d["pos"]*d["nxt"]
            # book return from postRebalance value to next postRebalance value (after fees)
            d["bret"]=d["postRebalance_total_value"].shift(-1)/d["postRebalance_total_value"]-1
            # pre-fee: pre-trade value next bar over post-trade value this bar
            d["bpre"]=d["total_portfolio_value"].shift(-1)/d["postRebalance_total_value"]-1
            d["turn"]=(d["postRebalance_current_allocation"]-d["previous_allocation"]).abs()
            r1=d["close"].pct_change()
            sd=r1.rolling(20).std()
            d["z"]=r1/sd
            sma=d["close"].rolling(50).mean()
            d["trend"]=np.where(d["close"]>sma,"above50","below50")
            d.loc[sma.isna(),"trend"]=np.nan
            for h in (1,3,5):
                fr=d["close"].shift(-h)/d["close"]-1
                g=np.full(len(d),np.nan); g[::h]=fr.values[::h]
                d[f"f{h}"]=g
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    a=pd.concat(rows,ignore_index=True)
    out={}
    out["book_per_bar"]=pd.Series({"gain_pos_x_nxt":a["gain"].mean(),"book_after_fee":a["bret"].mean(),
        "book_pre_fee":a["bpre"].mean(),"fee_drag":(a["bpre"]-a["bret"]).mean(),"turnover_mean":a["turn"].mean()})
    out["book_by_coin"]=a.groupby("coin").agg(gain=("gain","mean"),after=("bret","mean"),pre=("bpre","mean"),turn=("turn","mean"))
    # forward returns by horizon, side, using z (no excess needed: compare to coin mean)
    res=[]
    for h in (1,3,5):
        col=f"f{h}"
        b=a.dropna(subset=[col,"z"]).copy()
        b[col]=b[col]-b.groupby("coin")[col].transform("mean")
        for side,m in (("fall",b["z"]<0),("rise",b["z"]>0)):
            s=b[m]
            r=stats.linregress(-s["z"],s[col])
            res.append({"h":h,"side":side,"n":len(s),"slope_on_-z":r.slope,"t":r.slope/r.stderr})
        r=stats.linregress(-b["z"],b[col])
        res.append({"h":h,"side":"both","n":len(b),"slope_on_-z":r.slope,"t":r.slope/r.stderr})
    out["horizon_side"]=pd.DataFrame(res)
    b=a.dropna(subset=["f1","z","trend"]).copy()
    b["ex"]=b["f1"]-b.groupby("coin")["f1"].transform("mean")
    res=[]
    for (tr,side),s in b.groupby(["trend",np.where(b["z"]<0,"fall","rise")]):
        r=stats.linregress(-s["z"],s["ex"])
        res.append({"trend":tr,"side":side,"n":len(s),"slope":r.slope,"t":r.slope/r.stderr})
    out["trend_side_h1"]=pd.DataFrame(res)
    return out
