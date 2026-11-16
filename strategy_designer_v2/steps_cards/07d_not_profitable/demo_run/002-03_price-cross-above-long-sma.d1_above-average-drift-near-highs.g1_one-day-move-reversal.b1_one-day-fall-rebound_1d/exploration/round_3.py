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
            b["fee"] = (b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            b["net"] = (b["pos"]*b["nxt"]).fillna(0) - b["fee"].fillna(0)
            b["dist"] = b["close"]/b["close"].rolling(50, min_periods=30).mean()-1
            b["vol60"] = r.rolling(60, min_periods=40).std()
            b["absd"] = (b["dist"]/(b["vol60"]*np.sqrt(50))).abs()
            b["ret20"] = b["close"]/b["close"].shift(20)-1
            b["coin"] = c; b["w"] = w; b["i"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(b[["coin","w","i","day","pos","nxt","fee","net","dist","absd","ret20"]])
    B = pd.concat(rows, ignore_index=True)
    B["wn"] = B["w"].str[1:].astype(int)
    act = B[(B["pos"].abs()>1e-9) & B["nxt"].notna()].copy()
    act["d6"] = pd.qcut(act["absd"], 6)
    g = act.groupby("d6").agg(n=("net","size"), net=("net","mean"), nxt=("nxt","mean"), fee=("fee","mean"))
    g["t_net"] = act.groupby("d6")["net"].apply(lambda s: s.mean()/s.std()*np.sqrt(len(s)))
    out["net_by_absd6"] = g
    qs = act["absd"].quantile([1/3, 2/3]).values
    def book(weight):
        x = B.assign(v=B["net"]*weight)
        d = x.groupby(["wn","day"])["v"].mean().reset_index().sort_values(["wn","day"])
        s = d["v"]; v = (1+s).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(s))-1
        return pd.Series({"mean": s.mean(), "sharpe": s.mean()/s.std()*np.sqrt(365), "maxdd": dd, "calmar": yr/abs(dd)})
    a = B["absd"].fillna(0)
    out["variants"] = pd.DataFrame({
        "as_is": book(1.0),
        "far_only": book((a > qs[1]).astype(float)),
        "not_mid": book(((a <= qs[0]) | (a > qs[1])).astype(float)),
        "graded_absd": book((a/ a[a>0].median()).clip(upper=3)),
    })
    # deepest fall w8-w9 composition
    f = act[act["wn"].isin([8,9])].copy()
    f["dq"] = pd.cut(f["absd"], [-1, qs[0], qs[1], 99], labels=["near","mid","far"])
    f["side"] = np.where(f["dist"]>0, "above", "below")
    out["w8w9_by_dq_side"] = f.groupby(["wn","dq","side"]).agg(n=("net","size"), net_sum=("net","sum"), nxt=("nxt","mean"))
    act["dq"] = pd.cut(act["absd"], [-1, qs[0], qs[1], 99], labels=["near","mid","far"])
    out["window_net_by_dq"] = act.groupby("dq")["net"].apply(lambda s: s.groupby(act.loc[s.index,"wn"]).sum().lt(0).mean()).rename("share_windows_negative")
    return out
