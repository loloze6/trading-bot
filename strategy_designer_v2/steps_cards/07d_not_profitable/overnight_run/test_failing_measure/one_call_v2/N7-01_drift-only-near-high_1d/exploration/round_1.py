import numpy as np, pandas as pd

def explore(data):
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    # book daily returns
    rows = []
    for c in coins:
        for w in wins:
            d = data["days"][c][w][["day","book_return","coin_return"]].copy()
            d["coin"] = c; d["w"] = w
            rows.append(d)
    D = pd.concat(rows)
    B = D.groupby(["w","day"],sort=False).agg(br=("book_return","mean"),cr=("coin_return","mean")).reset_index()
    B["wi"] = B["w"].str[1:].astype(int)
    B = B.sort_values(["wi","day"]).dropna(subset=["br"])
    eq = (1+B["br"]).cumprod().values
    peak = np.maximum.accumulate(eq); dd = eq/peak-1
    B["dd"] = dd
    # per-window stats
    ws = B.groupby("wi").agg(ret=("br",lambda x:(1+x).prod()-1), hold=("cr",lambda x:(1+x).prod()-1),
                             mindd=("dd","min"), n=("br","size"))
    out["window_stats"] = ws.round(4)
    # episodes: find troughs
    eps=[]; i=0; n=len(dd)
    while i<n:
        if dd[i]<0:
            j=i
            while j<n and dd[j]<0: j+=1
            k=i+np.argmin(dd[i:j])
            eps.append((dd[k], i, k, j, B["wi"].iloc[i], B["wi"].iloc[k]))
            i=j
        else: i+=1
    eps=sorted(eps)[:6]
    out["worst_episodes"]=pd.DataFrame(eps,columns=["depth","start","trough","end","w_start","w_trough"]).assign(len_to_trough=lambda x:x.trough-x.start)
    # bar features for active days
    F=[]
    for c in coins:
        for w in wins:
            b=data["bars"][c][w].copy()
            cl=b["close"]
            b["sma"]=cl.rolling(20).mean()
            b["dist"]=cl/b["sma"]-1
            hh=cl.rolling(20).max()
            b["athigh"]=(cl>=hh).astype(int)
            b["r5"]=cl.pct_change(5)
            b["r20"]=cl.pct_change(20)
            lr=np.log(cl).diff()
            b["vratio"]=lr.rolling(10).std()/lr.rolling(60).std()
            b["nxt"]=cl.shift(-1)/cl-1
            b["alloc"]=b["postRebalance_current_allocation"]
            b["coin"]=c; b["w"]=w
            F.append(b[["dist","athigh","r5","r20","vratio","nxt","alloc","coin","w","forecast"]])
    F=pd.concat(F).dropna(subset=["nxt","dist"])
    A=F[F["alloc"]>0].copy()
    out["active_share"]=float(len(A)/len(F))
    allmean=F.groupby("coin")["nxt"].mean()
    A["ex"]=A["nxt"]-A["coin"].map(allmean)
    def tab(col,q=5):
        g=A.groupby(pd.qcut(A[col],q,duplicates="drop"))["ex"]
        r=g.agg(["mean","std","count"]); r["t"]=r["mean"]/(r["std"]/np.sqrt(r["count"]))
        r["p5"]=g.quantile(0.05); return r.round(4)
    out["by_dist"]=tab("dist"); out["by_r5"]=tab("r5"); out["by_r20"]=tab("r20"); out["by_vratio"]=tab("vratio")
    out["by_coin"]=A.groupby("coin")["ex"].agg(["mean","std","count"]).round(4)
    return out
