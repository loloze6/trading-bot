import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    wins = sorted(bars[coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily
    recs = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day","book_return","coin_return"]].copy(); d["coin"]=c; frames.append(d)
        df = pd.concat(frames)
        g = df.groupby("day").agg(b=("book_return","mean"), h=("coin_return","mean")).reset_index()
        g["w"]=w; recs.append(g)
    B = pd.concat(recs, ignore_index=True).dropna()
    B["v"]=(1+B["b"]).cumprod(); B["hv"]=(1+B["h"]).cumprod()
    B["peak"]=B["v"].cummax(); B["dd"]=B["v"]/B["peak"]-1
    i = B["dd"].idxmin(); pk = B.loc[:i,"v"].idxmax()
    out["deepest fall"] = pd.Series({"dd":B.loc[i,"dd"],"days":i-pk,"start_w":B.loc[pk,"w"],"end_w":B.loc[i,"w"],
        "hold_ret_during":B.loc[i,"hv"]/B.loc[pk,"hv"]-1})
    # per-window book vs hold
    pw = B.groupby("w").agg(book=("b","sum"),hold=("h","sum"),mindd=("dd","min"))
    pw = pw.loc[[w for w in wins if w in pw.index]]
    out["per window sum returns"] = pw
    # bar-level
    rows=[]
    for c in coins:
        for w in wins:
            if w not in bars[c]: continue
            b = bars[c][w].copy()
            b["r1"]=b["close"].shift(-1)/b["close"]-1
            b["ret20"]=b["close"]/b["close"].shift(20)-1
            b["ma50"]=b["close"]/b["close"].rolling(50,min_periods=20).mean()-1
            b["vs"]=b["volume"]/b["volume"].shift(1).rolling(20).mean()
            rng=(b["high"]-b["low"]).replace(0,np.nan)
            b["low_close"]=(b["high"]-b["close"])/rng
            b["dayret"]=b["close"]/b["open"]-1
            b["coin"]=c; b["w"]=w
            rows.append(b[["r1","ret20","ma50","vs","low_close","dayret","forecast","postRebalance_current_allocation","coin","w"]])
    X = pd.concat(rows, ignore_index=True)
    mu = X.groupby("coin")["r1"].mean()
    X["ex"]=X["r1"]-X["coin"].map(mu)
    X["alloc"]=X["postRebalance_current_allocation"]
    out["alloc/forecast dist"]=X[["forecast","alloc"]].describe().T
    X["fq"]=pd.cut(X["forecast"],[-0.1,1,5,10,15,20.1])
    out["by forecast bin"]=X.groupby("fq",observed=True).agg(n=("ex","size"),ex=("ex","mean"),r1=("r1","mean"),alloc=("alloc","mean"))
    X["trend"]=np.where(X["ma50"]>0,"above50","below50")
    X["sig"]=(X["vs"]>1.5)&(X["low_close"]>0.6)
    g=X.dropna(subset=["ex","ma50"]).groupby(["trend","sig"]).agg(n=("ex","size"),ex=("ex","mean"),sd=("ex","std"),alloc=("alloc","mean"))
    g["t"]=g["ex"]/(g["sd"]/np.sqrt(g["n"]))
    out["trend x signal"]=g
    # alloc contribution by trend
    X["pnl"]=X["alloc"]*X["r1"]
    out["pnl by trend"]=X.dropna(subset=["ma50"]).groupby("trend").agg(n=("pnl","size"),pnl=("pnl","mean"),alloc=("alloc","mean"),r1=("r1","mean"))
    X["r20q"]=pd.qcut(X["ret20"],5)
    out["pnl by ret20 quintile"]=X.dropna(subset=["ret20"]).groupby("r20q",observed=True).agg(n=("pnl","size"),pnl=("pnl","mean"),alloc=("alloc","mean"),r1=("r1","mean"),fc=("forecast","mean"))
    return out
