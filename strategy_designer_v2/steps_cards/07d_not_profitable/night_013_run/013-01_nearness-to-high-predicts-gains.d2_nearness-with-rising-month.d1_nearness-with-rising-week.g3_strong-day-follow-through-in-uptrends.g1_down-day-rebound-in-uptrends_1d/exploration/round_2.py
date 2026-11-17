import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            c = b["close"]
            for h in (1,2,3,5):
                b[f"r{h}"] = c.shift(-h)/c - 1
            b["ret30"] = c/c.shift(30) - 1
            b["ret7"] = c/c.shift(7) - 1
            b["ret1"] = c/c.shift(1) - 1
            lr = np.log(c).diff()
            b["vol30"] = lr.rolling(30).std()
            b["z1"] = b["ret1"]/b["vol30"]
            b["alloc"] = b["postRebalance_current_allocation"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["pg"] = b["alloc"]*b["r1"]
            b["coin"] = coin; b["wn"] = int(w[1:])
            b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    B["late"] = B.wn>=20
    # pg and fee by period late vs early
    out["late_vs_early"] = B.groupby("late").agg(pg=("pg","mean"),fee=("fee","mean"),long=("alloc", lambda s:(s>0).mean()),r1=("r1","mean"))
    A = B[(B.forecast>0)].copy()
    out["active_late_vs_early"] = A.groupby("late").agg(r1=("r1","mean"),r3=("r3","mean"),r5=("r5","mean"),pg=("pg","mean"),fee=("fee","mean"),n=("r1","size"))
    # down days all regimes graded by z1, by ret30 sign, non-overlapping by horizon
    res = {}
    for h in (1,3,5):
        G = B[(B.pos % h)==0].copy()
        G = G[G.z1<0]
        G["drift"] = G.groupby("coin")[f"r{h}"].transform("mean")
        for reg,sub in G.groupby(G.ret30>0):
            s = sub.dropna(subset=[f"r{h}","z1"])
            sl = stats.linregress(-s.z1, s[f"r{h}"])
            res[(h,"up30" if reg else "down30")] = {"slope":sl.slope,"t":sl.slope/sl.stderr,"mean":s[f"r{h}"].mean(),"n":len(s)}
    out["graded_by_h_regime"] = pd.DataFrame(res).T
    # active bars: graded by ret30 quartile, non-overlap h=3
    G = B[(B.pos % 3)==0]
    G = G[(G.z1<0)&(G.ret30>0)].dropna(subset=["r3","ret30"]).copy()
    G["q"]=pd.qcut(G.ret30,4,labels=False)
    out["r3_by_ret30q_nonoverlap"] = G.groupby("q").agg(r30=("ret30","mean"),r3=("r3","mean"),n=("r3","size"))
    G1 = B[(B.z1<0)&(B.ret30>0)].dropna(subset=["r1","ret30"]).copy()
    G1["q"]=pd.qcut(G1.ret30,5,labels=False)
    out["r1_by_ret30q"] = G1.groupby("q").agg(r30=("ret30","mean"),r1=("r1","mean"),t=("r1",lambda s:s.mean()/s.std()*np.sqrt(len(s))),n=("r1","size"))
    # the ret7 within active: weak week?
    A["q7"]=pd.qcut(A.ret7,4,labels=False,duplicates="drop")
    out["active_by_ret7"] = A.groupby("q7").agg(r7=("ret7","mean"),r1=("r1","mean"),r3=("r3","mean"),pg=("pg","mean"),n=("r1","size"))
    # turnover: share of alloc changes and fee by forecast size
    out["trades_per_bar_fee"] = pd.Series({"bars_with_fee":(B.fee>1e-9).mean(),"mean_fee_when":B.loc[B.fee>1e-9,"fee"].mean(),
        "holding_days_mean":(B.alloc>0).sum()/max(1,((B.alloc>0)&(B.previous_allocation<=0)).sum())})
    return out
