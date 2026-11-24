def explore(data):
    import numpy as np, pandas as pd
    coin = list(data["bars"].keys())[0]
    B = data["bars"][coin]
    rows = []
    for w in sorted(B.keys(), key=lambda s: int(s[1:])):
        b = B[w].copy().reset_index(drop=True)
        c = b["close"]; b["w"] = w; b["wi"] = int(w[1:])
        b["r1"] = c.shift(-1)/c - 1
        b["ret"] = c.pct_change()
        b["vol30"] = b["ret"].rolling(30).std()
        b["z"] = b["ret"]/b["vol30"]
        b["pos"] = b["postRebalance_current_allocation"]
        b["prev"] = b["previous_allocation"]
        b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"])/b["total_portfolio_value"]
        b["gain"] = b["pos"]*b["r1"]
        b["net"] = b["gain"] - b["fee"].shift(-1).fillna(0)
        rows.append(b)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    cost = 0.0031/2  # per unit of turnover approx (fee+slip per side)
    def book(posser, label):
        res = []
        for w, g in A.groupby("wi"):
            p = posser(g).fillna(0).values
            prev = np.r_[0, p[:-1]]
            turn = np.abs(p - prev)
            r = (p * g["r1"].fillna(0).values) - turn*cost
            res.append(pd.Series(r[:-1]))
        r = pd.concat(res, ignore_index=True)
        v = (1+r).cumprod(); dd = (v/v.cummax()-1).min()
        yr = v.iloc[-1]**(365/len(r)) - 1
        return {"mean": r.mean(), "sharpe": r.mean()/r.std()*np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr/abs(dd), "turn/day": None}
    res = {}
    res["as tested (approx)"] = book(lambda g: g["pos"], "")
    res["long only"] = book(lambda g: g["pos"].clip(lower=0), "")
    res["short only"] = book(lambda g: g["pos"].clip(upper=0), "")
    res["long only x1.5"] = book(lambda g: (1.5*g["pos"]).clip(lower=0, upper=2), "")
    res["long only, |z|>0.7"] = book(lambda g: g["pos"].clip(lower=0).where(g["z"].abs() > 0.7, 0), "")
    res["both, |z|>0.7"] = book(lambda g: g["pos"].where(g["z"].abs() > 0.7, 0), "")
    res["long, held 3 bars after"] = book(lambda g: g["pos"].clip(lower=0).rolling(3, min_periods=1).max(), "")
    out["books"] = pd.DataFrame(res).T.drop(columns="turn/day")
    # deep fall windows: contribution by side
    A["side"] = np.sign(A["pos"])
    A["grp"] = np.where(A["wi"].between(20, 24), "w20-24", np.where(A["wi"].between(3, 6), "w3-6", "other"))
    g = A.dropna(subset=["r1"]).groupby(["grp", "side"]).agg(n=("gain", "size"), gain=("gain", "mean"), net=("net", "mean"), sumnet=("net", "sum"), r1=("r1", "mean"))
    out["falls by side"] = g
    # coin next-day after down days vs up days, all bars (condition check for side)
    A2 = A.dropna(subset=["r1", "z"])
    q = pd.qcut(A2["z"], 10)
    gg = A2.groupby(q).agg(n=("r1", "size"), r1=("r1", "mean"), sd=("r1", "std"))
    gg["t"] = gg["r1"]/(gg["sd"]/np.sqrt(gg["n"])); gg.index = gg.index.astype(str)
    out["coin next day by z decile"] = gg
    out["coin mean r1"] = float(A2["r1"].mean())
    # 2-day forward after down days by z decile, non-overlapping not needed for shape
    return out
