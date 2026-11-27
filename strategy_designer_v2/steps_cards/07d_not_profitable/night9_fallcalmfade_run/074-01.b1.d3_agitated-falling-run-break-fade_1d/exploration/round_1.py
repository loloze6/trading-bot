def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns, mean across coins per day, chained in window order
    wins = sorted({w for c in data["days"] for w in data["days"][c]}, key=lambda s: int(s[1:]))
    chain = []
    for w in wins:
        frames = []
        for c in data["days"]:
            if w in data["days"][c]:
                d = data["days"][c][w][["day", "book_return"]].copy()
                d["coin"] = c
                frames.append(d)
        df = pd.concat(frames)
        m = df.groupby("day")["book_return"].mean().dropna().sort_index()
        chain.append(pd.DataFrame({"w": w, "r": m.values}))
    ch = pd.concat(chain, ignore_index=True)
    v = (1 + ch["r"]).cumprod()
    dd = v / v.cummax() - 1
    ch["dd"] = dd.values
    out["book by window"] = ch.groupby("w").agg(mean=("r", "mean"), sum=("r", "sum"), worst=("r", "min"), mindd=("dd", "min")).reindex(wins)
    out["max dd"] = float(dd.min())
    # worst 10 book days, which window
    out["worst days"] = ch.nsmallest(10, "r")[["w", "r"]].reset_index(drop=True)

    # per-position-bar records
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            prev = np.r_[np.nan, cl[1:] / cl[:-1] - 1]  # today's return
            dr = pd.Series(cl).pct_change()
            sd30 = dr.rolling(30, min_periods=10).std().values
            # down-run count before today's up close
            down = (dr < 0).values
            runs = np.zeros(len(b)); runloss = np.zeros(len(b))
            k = 0; lo = 0.0
            for i in range(len(b)):
                if i > 0 and down[i]:
                    k += 1; lo = (1 + lo) * (1 + dr.iloc[i]) - 1
                else:
                    runs[i] = k; runloss[i] = lo
                    k = 0; lo = 0.0
            t60 = pd.Series(cl).pct_change(60).values
            alloc = b["postRebalance_current_allocation"].values
            for i in range(len(b) - 1):
                if alloc[i] < 0 or (runs[i] >= 2 and prev[i] > 0):
                    rows.append(dict(coin=c, w=w, alloc=alloc[i], fc=b["forecast"].iloc[i], nxt=r[i], upday=prev[i],
                                     upz=prev[i] / sd30[i] if sd30[i] > 0 else np.nan, run=runs[i],
                                     depth=-runloss[i] / sd30[i] if sd30[i] > 0 else np.nan, t60=t60[i],
                                     inpos=alloc[i] < 0, reg=b["regime"].iloc[i], sd30=sd30[i]))
    P = pd.DataFrame(rows)
    P["gain"] = -P["alloc"].clip(upper=0) * 0 + P["alloc"] * P["nxt"]
    A = P[P.inpos]
    out["n in pos"] = len(A)
    def g(df, col, q=None):
        x = pd.qcut(df[col], q, duplicates="drop") if q else df[col]
        gg = df.groupby(x, observed=True)
        return pd.DataFrame({"n": gg.size(), "shortret": -gg["nxt"].mean(), "t": -gg["nxt"].mean() / (gg["nxt"].std() / np.sqrt(gg.size())),
                             "gain_mean": gg["gain"].mean(), "gain_sum": gg["gain"].sum(), "worst": gg["gain"].min()})
    out["pos by window"] = g(A, "w")
    out["pos by coin"] = g(A, "coin")
    out["pos by run"] = g(A.assign(runc=A.run.clip(upper=5)), "runc")
    out["pos by upday z"] = g(A, "upz", 4)
    out["pos by depth"] = g(A, "depth", 4)
    out["pos by alloc"] = g(A.assign(a=-A.alloc), "a", 4)
    out["pos by sd30"] = g(A, "sd30", 4)
    out["pos by t60"] = g(A, "t60", 4)
    out["worst 15 trades"] = A.nsmallest(15, "gain")[["coin", "w", "alloc", "nxt", "upz", "run", "depth", "t60", "sd30"]].reset_index(drop=True)
    # run breaks outside the position (all profiles) for comparison
    O = P[~P.inpos]
    out["run breaks not in pos, by t60 sign"] = g(O.assign(f=np.sign(O.t60 + 0.10)), "f")
    out["run breaks not in pos, by upz"] = g(O, "upz", 4)
    return out
