def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            pos = b["postRebalance_current_allocation"].values
            dist = b["debug_info.components.closeness.last_history_value"].values
            vol = b["volume"].values
            nxt = np.r_[c[1:]/c[:-1]-1, np.nan]
            for t in range(n-1):
                p30 = c[t]/c[t-30]-1 if t>=30 else np.nan
                v = vol[max(0,t-29):t+1]
                vr = vol[t]/np.mean(v) if len(v)>=10 else np.nan
                rows.append(dict(coin=coin, w=w, pos=pos[t], dist=dist[t], nxt=nxt[t], p30=p30, vr=vr, gain=pos[t]*nxt[t]))
    R = pd.DataFrame(rows).dropna(subset=["nxt"])
    cm = R.groupby("coin").nxt.mean()
    R["mkt"] = R.pos*R.coin.map(cm)
    R["timing"] = R.gain-R.mkt
    R["side"] = np.where(R.pos>0.01,"long",np.where(R.pos<-0.01,"short","flat"))
    out["by side"] = R.groupby("side").agg(n=("gain","size"), pos=("pos","mean"), gain=("gain","mean"), mkt=("mkt","mean"), timing=("timing","mean"), nxt=("nxt","mean"))
    out["mkt vs timing total"] = f"gain {R.gain.mean():.6f} mkt {R.mkt.mean():.6f} timing {R.timing.mean():.6f}"
    # distance deciles: next-day coin return (excess) and mean pos
    R["ex"] = R.nxt - R.coin.map(cm)
    R["dd"] = pd.qcut(R.dist, 10, labels=False, duplicates="drop")
    out["next-day excess by distance decile"] = R.groupby("dd").agg(dist=("dist","mean"), ex=("ex","mean"), pos=("pos","mean"), gain=("gain","mean"), n=("ex","size"))
    # near high (top 20% of dist): by past 30d return tercile
    nh = R[R.dist >= R.dist.quantile(0.8)].dropna(subset=["p30"]).copy()
    nh["pt"] = pd.qcut(nh.p30, 3, labels=False)
    out["near high: by past30 tercile"] = nh.groupby("pt").agg(p30=("p30","mean"), ex=("ex","mean"), pos=("pos","mean"), gain=("gain","mean"), n=("ex","size"))
    far = R[R.dist <= R.dist.quantile(0.4)].dropna(subset=["p30"]).copy()
    far["pt"] = pd.qcut(far.p30, 3, labels=False)
    out["far below: by past30 tercile"] = far.groupby("pt").agg(p30=("p30","mean"), ex=("ex","mean"), pos=("pos","mean"), gain=("gain","mean"), n=("ex","size"))
    # all bars: next-day excess by past30 quintile
    a = R.dropna(subset=["p30"]).copy(); a["pq"]=pd.qcut(a.p30,5,labels=False)
    out["all: next-day excess by past30 quintile"] = a.groupby("pq").agg(p30=("p30","mean"), ex=("ex","mean"), pos=("pos","mean"), gain=("gain","mean"))
    # book drawdown: chained daily book in window order
    D=[]
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd=d[["day","book_return"]].copy(); dd["w"]=w; D.append(dd)
    D=pd.concat(D); g=D.groupby(["w","day"]).book_return.mean().reset_index()
    g["wn"]=g.w.str[1:].astype(int); g=g.sort_values(["wn","day"])
    eq=(1+g.book_return.fillna(0)).cumprod(); ddn=eq/eq.cummax()-1
    g["dd"]=ddn.values
    out["max dd, yearly"] = f"maxdd {ddn.min():.4f} yearly {(eq.iloc[-1]**(365/len(g))-1):.4f}"
    out["window min dd"] = g.groupby("wn").agg(mindd=("dd","min"), ret=("book_return","sum")).sort_values("mindd").head(8)
    return out
