def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd30 = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "pos": np.arange(len(b)), "reg": b["regime"].astype(str),
                "sr": r / sd30,
                "sr2": c.pct_change(2) / (sd30 * np.sqrt(2)),
                "sr3": c.pct_change(3) / (sd30 * np.sqrt(3)),
                "sr4": c.pct_change(4) / (sd30 * np.sqrt(4)),
            })
            for h in (2, 3, 4):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for h in (2, 3, 4):
        g = d[d["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        d[f"x{h}"] = d[f"f{h}"] - d["coin"].map(m)
    d["day"] = d["ts"].dt.floor("D")
    P = d[d["reg"] == "unknown"]

    def slope_t(s, col, h):
        s = s.dropna(subset=[col, f"x{h}"])
        if len(s) < 40: return {"n": len(s)}
        x = s[col].values; y = s[f"x{h}"].values
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        e = y - X @ beta
        XtXi = np.linalg.inv(X.T @ X)
        sc = pd.DataFrame(X * e[:, None]).groupby(s["day"].values).sum().values
        G = len(sc)
        V = XtXi @ (sc.T @ sc) @ XtXi * G / (G - 1)
        return {"n": len(s), "days": G, "slope%": 100 * beta[1], "t": beta[1] / np.sqrt(V[1, 1])}

    def ct(s, days):
        dev = (s - s.mean()).groupby(days).sum(); G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / len(s)
        return s.mean() / se, G

    res = {}
    out = []
    for col, h in (("sr3", 3), ("sr2", 2), ("sr4", 4), ("sr3", 2), ("sr3", 4)):
        for off in range(h):
            s = P[P["pos"] % h == off]
            dd = slope_t(s, col, h); dd.update({"var": col, "h": h, "offset": off}); out.append(dd)
    res["offsets"] = pd.DataFrame(out)
    out = []
    s = P[P["pos"] % 3 == 0].dropna(subset=["sr3", "x3"])
    pos = s[s["sr3"] > 0]
    dd = slope_t(pos, "sr3", 3); dd.update({"subset": "sr3>0"}); out.append(dd)
    neg = s[s["sr3"] <= 0]
    dd = slope_t(neg, "sr3", 3); dd.update({"subset": "sr3<=0"}); out.append(dd)
    res["sign_split_h3"] = pd.DataFrame(out)
    q = []
    s = s.assign(b=pd.qcut(s["sr3"], 3, labels=False))
    for k, gg in s.groupby("b"):
        t, G = ct(gg["x3"], gg["day"])
        q.append({"tercile": k, "lo": gg["sr3"].min(), "hi": gg["sr3"].max(), "n": len(gg),
                  "days": G, "mean_x%": 100 * gg["x3"].mean(), "mean_f%": 100 * gg["f3"].mean(), "t": t})
    res["terciles_h3"] = pd.DataFrame(q)
    return res
