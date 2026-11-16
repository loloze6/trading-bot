def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b["close"].pct_change()
            b["nxt"] = b["close"].shift(-1)/b["close"]-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["nxt"]
            b["dist"] = b["close"]/b["close"].rolling(50, min_periods=30).mean()-1
            b["vol20"] = r.rolling(20).std()
            b["vol60"] = r.rolling(60, min_periods=40).std()
            b["absd"] = (b["dist"]/(b["vol60"]*np.sqrt(50))).abs()
            b["z"] = r/b["vol20"].shift(1)
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["net"] = b["gain"]-b["fee"].shift(-1).fillna(0)*0 - b["fee"]
            v = (1+b["gain"].fillna(0)).cumprod()
            b["bookdd"] = v/v.cummax()-1
            b["coin"] = c; b["w"] = w
            rows.append(b[["coin","w","pos","nxt","gain","fee","net","dist","absd","z","vol20","bookdd"]])
    B = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    act = B[B["pos"].abs()>1e-9].copy()
    act["zq"] = pd.qcut(act["z"], 5, labels=["z1big","z2","z3","z4","z5small"])
    act["dq"] = pd.qcut(act["absd"], 3, labels=["near","mid","far"])
    out["z_fee_net"] = act.groupby("zq").agg(n=("gain","size"), gain=("gain","mean"), fee=("fee","mean"), net=("net","mean"), pos=("pos","mean"))
    out["absd_fee_net"] = act.groupby("dq").agg(n=("gain","size"), gain=("gain","mean"), fee=("fee","mean"), net=("net","mean"), nxt=("nxt","mean"))
    g = act.groupby(["dq","zq"]).agg(n=("nxt","size"), nxt=("nxt","mean"), net=("net","mean"))
    g["t_nxt"] = act.groupby(["dq","zq"])["nxt"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))
    out["absd_x_z"] = g
    # net contribution share of total net
    tot = act["net"].sum()
    out["net_share_by_z"] = act.groupby("zq")["net"].sum()/tot
    out["net_share_by_absd"] = act.groupby("dq")["net"].sum()/tot
    # dist sign within far
    act["side"] = np.where(act["dist"]>0,"above","below")
    out["far_by_side"] = act[act["dq"]=="far"].groupby("side").agg(n=("nxt","size"), nxt=("nxt","mean"), net=("net","mean"))
    # state when coin-level book in deep drawdown
    act["ddstate"] = pd.cut(act["bookdd"], [-1,-0.2,-0.1,0.01], labels=["dd>20","dd10-20","dd<10"])
    out["by_dd"] = act.groupby("ddstate").agg(n=("nxt","size"), nxt=("nxt","mean"), net=("net","mean"), absd=("absd","mean"))
    return out
