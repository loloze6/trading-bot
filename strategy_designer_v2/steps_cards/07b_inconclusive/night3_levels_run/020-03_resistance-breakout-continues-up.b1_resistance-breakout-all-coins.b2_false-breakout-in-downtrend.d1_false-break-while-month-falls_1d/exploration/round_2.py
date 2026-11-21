def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []; base = []
    for coin, ws in bars.items():
        rets = [b["close"].pct_change().dropna() for b in ws.values()]
        drift = pd.concat(rets).mean()
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; n = len(c)
            r30 = pd.Series(c).pct_change(30).values
            fc = b["forecast"].fillna(0).values
            reg = b["regime"].values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            seen = set()
            for t in range(n - 10):
                cell = t // 10
                if reg[t] == "mean_reversion" and fc[t] <= -2 and cell not in seen:
                    seen.add(cell)
                    d = {"coin": coin, "year": yr[t], "r30": r30[t],
                         "brkday": c[t]/c[t-1]-1 if t >= 1 else np.nan}
                    for h in [1, 2, 10]:
                        d[f"x{h}"] = -(c[t+h]/c[t]-1) + drift*h
                    d["x2_10"] = -(c[t+10]/c[t+1]-1) + drift*9
                    rows.append(d)
            for h in [1, 10]:
                for t in range(30, n-h, h):
                    if not np.isnan(r30[t]) and r30[t] < 0:
                        base.append({"h": h, "r30": r30[t], "year": yr[t],
                                     "x": -(c[t+h]/c[t]-1) + drift*h})
    df = pd.DataFrame(rows); bs = pd.DataFrame(base)
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))), "hit": (s > 0).mean()})
    out = {}
    out["cases"] = pd.DataFrame({k: summ(df[k]) for k in ["x1","x2","x10","x2_10"]}).T
    df["dq"] = pd.qcut(df["r30"], 3, labels=["deep","mid","shallow"])
    out["x1_by_depth"] = df.groupby("dq")["x1"].apply(summ).unstack()
    df["bq"] = pd.qcut(df["brkday"], 3, labels=["small","mid","big"])
    out["x1_by_breakday"] = df.groupby("bq")["x1"].apply(summ).unstack()
    out["x10_by_breakday"] = df.groupby("bq")["x10"].apply(summ).unstack()
    out["brkday_range"] = df.groupby("bq")["brkday"].agg(["min","max"])
    b10 = bs[bs.h == 10].copy()
    b10["dq"] = pd.qcut(b10["r30"], 5, labels=["q1deep","q2","q3","q4","q5shallow"])
    out["base10_by_depth5"] = b10.groupby("dq")["x"].apply(summ).unstack()
    out["base10_by_year"] = b10.groupby("year")["x"].apply(summ).unstack()
    out["base10_depth_range"] = b10.groupby("dq")["r30"].agg(["min","max"])
    out["base1"] = summ(bs[bs.h == 1]["x"])
    return out
