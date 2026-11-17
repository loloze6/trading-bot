import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day","book_return","coin_return"]].copy()
            t["coin"]=c; t["w"]=w; rows.append(t)
    D = pd.concat(rows)
    D["wn"]=D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna()
    eq = (1+B["book_return"]).cumprod()
    dd = eq/eq.cummax()-1
    B["dd"]=dd.values
    out["book mean, sd, n"] = pd.Series({"mean":B.book_return.mean(),"sd":B.book_return.std(),"n":len(B),"maxdd":dd.min(),
        "hold_mean":B.coin_return.mean()})
    # drawdown by window: worst dd within each window and window return
    g = B.groupby("wn").agg(book=("book_return",lambda x:(1+x).prod()-1), coin=("coin_return",lambda x:(1+x).prod()-1),
                            mindd=("dd","min"))
    out["by window"]=g
    # per bar analysis
    br=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            r=b.close.pct_change()
            b["r"]=r
            b["nxt"]=b.close.shift(-1)/b.close-1
            b["pos"]=b.postRebalance_current_allocation
            b["gain"]=b.pos*b.nxt
            b["r20"]=b.close/b.close.shift(20)-1
            b["r5"]=b.close/b.close.shift(5)-1
            b["ma50"]=b.close/b.close.rolling(50).mean()-1
            b["vol30"]=r.rolling(30).std()
            b["vol90"]=r.rolling(90).std()
            b["volratio"]=b.vol30/b.vol90
            b["coin"]=c; b["wn"]=int(w[1:])
            br.append(b)
    X=pd.concat(br)
    X=X[X.pos.abs()>0]
    out["held bars n, mean gain"]=pd.Series({"n":len(X),"mean":X.gain.mean(),"t":X.gain.mean()/X.gain.std()*np.sqrt(len(X))})
    def grp(col,q=4):
        y=X.dropna(subset=[col,"gain"])
        y=y.assign(qq=pd.qcut(y[col],q,labels=False,duplicates="drop"))
        return y.groupby("qq").agg(lo=(col,"min"),hi=(col,"max"),n=("gain","size"),gain=("gain","mean"),nxt=("nxt","mean"),pos=("pos","mean"))
    out["by r20"]=grp("r20")
    out["by ma50"]=grp("ma50")
    out["by r5"]=grp("r5")
    out["by volratio"]=grp("volratio")
    out["by forecast"]=grp("forecast")
    out["by pos"]=grp("pos")
    return out
