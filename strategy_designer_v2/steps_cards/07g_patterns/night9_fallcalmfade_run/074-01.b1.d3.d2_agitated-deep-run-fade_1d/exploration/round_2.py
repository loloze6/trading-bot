def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            run = np.zeros(len(b)); cnt = 0; loss = np.zeros(len(b)); cum = 0.0
            for i in range(len(b)):
                ri = r.iloc[i]
                if np.isnan(ri):
                    cnt = 0; cum = 0.0; continue
                if ri < 0:
                    cnt += 1; cum += ri
                else:
                    run[i] = cnt; loss[i] = cum; cnt = 0; cum = 0.0
            vol30 = r.abs().rolling(30, min_periods=20).mean()
            sd30 = r.rolling(30, min_periods=20).std()
            ret60 = c / c.shift(60) - 1
            rows.append(pd.DataFrame({"coin": coin, "w": w, "r": r, "nxt": nxt, "run": run,
                "depth": -loss / vol30, "ret60": ret60, "sd30": sd30,
                "inprof": (b["regime"] != "chop").values,
                "year": pd.to_datetime(b["timestamp"]).dt.year}))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["nxt", "r"])
    mu = D.groupby("coin")["nxt"].mean()
    D["unx"] = D["nxt"] - D["coin"].map(mu)
    def summ(g):
        x = g["unx"]
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    D["trend"] = pd.cut(D["ret60"], [-np.inf, -0.10, 0.10, np.inf], labels=["fall", "chop", "rise"])
    med = D.groupby("coin")["sd30"].transform("median")
    D["agit"] = np.where(D["sd30"] > med, "agit", "calm")
    out = {}
    up = D[(D["r"] > 0)]
    brk = up[up["run"] >= 2].copy()
    ob = brk[~brk["inprof"]]
    out["out-prof run-break(2+) by trend x agit"] = ob.dropna(subset=["trend"]).groupby(["trend", "agit"]).apply(summ)
    out["out-prof non-break up days (run 0) by trend"] = up[(up["run"] == 0) & ~up["inprof"]].dropna(subset=["trend"]).groupby("trend").apply(summ)
    ob = ob.dropna(subset=["depth"])
    ob["dq"] = pd.qcut(ob["depth"], 3, labels=False, duplicates="drop")
    out["out-prof run-break by depth tercile"] = ob.groupby("dq").apply(summ)
    out["out-prof run-break by year"] = ob.groupby("year").apply(summ)
    ib = brk[brk["inprof"]].dropna(subset=["depth"]).copy()
    ib["dq"] = pd.qcut(ib["depth"], 3, labels=False, duplicates="drop")
    out["in-prof run-break by depth tercile"] = ib.groupby("dq").apply(summ)
    allb = brk.dropna(subset=["depth"]).copy()
    allb["dq"] = pd.qcut(allb["depth"], 3, labels=False, duplicates="drop")
    out["all run-break by depth tercile"] = allb.groupby("dq").apply(summ)
    out["all run-break by year"] = allb.groupby("year").apply(summ)
    out["all run-break by coin"] = allb.groupby("coin").apply(summ)
    return out
