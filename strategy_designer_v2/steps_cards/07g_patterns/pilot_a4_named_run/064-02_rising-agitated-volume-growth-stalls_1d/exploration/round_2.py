def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # drift per coin per horizon
    def drift(coin, H):
        rr = []
        for w, b in data["bars"][coin].items():
            c = b["close"].values
            for i in range(0, len(b) - H, H):
                rr.append(c[i + H] / c[i] - 1)
        return np.mean(rr) if rr else np.nan
    res = []
    for H in [1, 3, 10]:
        rows = []
        for coin, wins in data["bars"].items():
            dr = drift(coin, H)
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"]; h = b["high"]; l = b["low"]; v = b["volume"]
                lr = np.log(c).diff()
                f = pd.DataFrame({
                    "ret1": c.pct_change(), "ret3": c.pct_change(3), "ret10": c.pct_change(10),
                    "clv": (c - l) / (h - l).replace(0, np.nan),
                    "dist_hi20": c / h.rolling(20).max() - 1,
                    "vol10_vs30": lr.rolling(10).std() / lr.rolling(30).std(),
                    "vshock": np.log(v / v.rolling(20).mean()),
                    "upday_run": (lr > 0).astype(int).rolling(5).sum(),
                })
                f["fwd"] = c.shift(-H) / c - 1 - dr
                f["inprof"] = (b["regime"] == "unknown").astype(int)
                f["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
                rows.append(f.iloc[list(range(0, len(b) - H, H))])
        d = pd.concat(rows); p = d[(d.inprof == 1) & d.fwd.notna()]
        for ft in ["ret1","ret3","ret10","clv","dist_hi20","vol10_vs30","vshock","upday_run"]:
            q = p[[ft, "fwd", "day"]].dropna()
            if len(q) < 40: continue
            x = ((q[ft] - q[ft].mean()) / q[ft].std()).values
            X = np.c_[np.ones(len(q)), x]
            beta = np.linalg.lstsq(X, q["fwd"].values, rcond=None)[0]
            e = q["fwd"].values - X @ beta
            S = pd.DataFrame({"d": q["day"].values, "a": e, "b": e * x}).groupby("d")[["a","b"]].sum().values
            XtX = np.linalg.inv(X.T @ X); V = XtX @ (S.T @ S) @ XtX
            res.append({"H": H, "feat": ft, "n": len(q), "slope_sd": beta[1], "t": beta[1] / np.sqrt(V[1,1])})
    out["slopes_by_horizon"] = pd.DataFrame(res)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median","std"])
        out["trades_by_coin_side"] = T.groupby(["coin","side"])["net_profit_loss_percent"].agg(["count","mean"])
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            dd.append(dy.assign(coin=coin))
    D = pd.concat(dd).dropna(subset=["book_return"])
    act = D[D.book_return != 0]
    out["book_active_days"] = pd.Series({"n": len(act), "mean": act.book_return.mean(),
        "t": stats.ttest_1samp(act.book_return, 0).statistic,
        "top10_share_of_sum": act.book_return.nlargest(10).sum() / act.book_return.abs().sum(),
        "bottom10_share": act.book_return.nsmallest(10).sum() / act.book_return.abs().sum()})
    return out
