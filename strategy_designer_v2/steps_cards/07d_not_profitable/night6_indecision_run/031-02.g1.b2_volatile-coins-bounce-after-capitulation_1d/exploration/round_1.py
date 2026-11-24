import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    # book daily returns
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["book"])
    v = (1+B["book"]).cumprod(); peak = v.cummax(); dd = v/peak-1
    B["dd"] = dd.values; B["val"]=v.values
    out["maxdd"] = float(dd.min())
    # drawdown episodes: top falls
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book by year"] = B.groupby("year").agg(mean=("book","mean"), sum=("book","sum"), mindd=("dd","min"), n=("book","size"))
    out["book by window"] = B.groupby("wn").agg(sum=("book","sum"), mindd=("dd","min"))
    # worst book days
    out["worst 10 book days (ret, hold)"] = B.nsmallest(10,"book")[["wn","book","hold"]].reset_index(drop=True)
    # cases
    cs = []
    allret = {}
    for c in bars:
        rets=[]
        for w,b in bars[c].items():
            b=b.copy()
            r=b["close"].pct_change()
            rets.append(r.dropna())
        allret[c]=pd.concat(rets).mean()
        for w,b in bars[c].items():
            b=b.copy().reset_index(drop=True)
            r=b["close"].pct_change()
            sd=r.rolling(20).std()
            b["z"]=r/sd
            b["loc"]=(b["close"]-b["low"])/(b["high"]-b["low"])
            b["next"]=b["close"].shift(-1)/b["close"]-1
            b["ex"]=b["next"]-allret[c]
            b["r1"]=r
            b["r5"]=b["close"]/b["close"].shift(5)-1
            b["r20"]=b["close"]/b["close"].shift(20)-1
            b["rng"]=(b["high"]-b["low"])/b["close"]
            b["vol20"]=sd
            b["volrel"]=sd/sd.rolling(60,min_periods=20).mean()
            b["gap_next_open"]=np.nan
            b["coin"]=c; b["w"]=w
            b["year"]=pd.to_datetime(b["timestamp"]).dt.year
            b["alloc"]=b["postRebalance_current_allocation"]
            b["pos_ret"]=b["alloc"]*b["next"]
            b["vz"]=b["debug_info.components.vol20.post_pipeline_value"] if "debug_info.components.vol20.post_pipeline_value" in b else np.nan
            b["case"]=(b["regime"]=="mean_reversion")
            b["prevcase"]=b["case"].shift(1).fillna(False)
            cs.append(b)
    A=pd.concat(cs)
    C=A[A["case"] & A["next"].notna()].copy()
    out["n cases"]=len(C)
    def g(col, q=3):
        x=C.copy(); x["bin"]=pd.qcut(x[col],q,duplicates="drop")
        r=x.groupby("bin").agg(n=("ex","size"),mean_ex=("ex","mean"),std=("ex","std"),pos=("pos_ret","mean"),alloc=("alloc","mean"))
        r["t"]=r["mean_ex"]/(r["std"]/np.sqrt(r["n"]))
        return r.reset_index().astype({"bin":str})
    for col in ["z","loc","r5","r20","volrel","vz","rng","alloc","r1"]:
        out["by "+col]=g(col)
    out["by coin"]=C.groupby("coin").agg(n=("ex","size"),mean_ex=("ex","mean"),pos=("pos_ret","mean"),alloc=("alloc","mean"))
    out["by year"]=C.groupby("year").agg(n=("ex","size"),mean_ex=("ex","mean"),pos=("pos_ret","mean"))
    # concentration: share of position-return from worst cases
    out["pos_ret summary"]=C["pos_ret"].describe()
    out["worst 15 cases"]=C.nsmallest(15,"pos_ret")[["coin","year","z","loc","r5","r20","volrel","alloc","next"]].reset_index(drop=True)
    # cases on the day after a case (cluster)
    out["by prevcase"]=C.groupby("prevcase").agg(n=("ex","size"),mean_ex=("ex","mean"),pos=("pos_ret","mean"))
    return out
