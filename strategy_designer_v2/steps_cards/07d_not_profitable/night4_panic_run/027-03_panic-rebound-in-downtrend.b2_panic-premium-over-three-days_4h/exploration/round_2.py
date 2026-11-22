def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    # 1) forward excess at several horizons after a broad panic (z<=-1, ratio>=1.5), grid by horizon
    hz = {"1d": 6, "3d": 18, "7d": 42, "14d": 84}
    res = []
    for name, H in hz.items():
        allr = []; recs = []
        for c in bars:
            for w, b in bars[c].items():
                s = b["close"].reset_index(drop=True); n = len(s)
                r6 = s / s.shift(6) - 1
                z = r6 / r6.abs().rolling(180, min_periods=30).mean()
                rg = ((b["high"] - b["low"]) / b["close"]).reset_index(drop=True)
                ratio = rg.rolling(6).mean() / rg.rolling(180, min_periods=30).mean()
                for i in range(0, n - H, H):
                    allr.append((c, s[i + H] / s[i] - 1))
                    for j in range(i, i + H):
                        if j + H < n and z[j] <= -1 and ratio[j] >= 1.5:
                            recs.append((c, s[j + H] / s[j] - 1, ratio[j])); break
        A = pd.DataFrame(allr, columns=["c", "r"]); mu = A.groupby("c").r.mean(); usd = A.groupby("c").r.std()
        R = pd.DataFrame(recs, columns=["c", "r", "ratio"]); R["ex"] = R.r - R.c.map(mu)
        R["st"] = R.ex / R.c.map(usd)
        res.append(dict(h=name, n=len(R), mean_ex=R.ex.mean(), t=R.ex.mean() / (R.ex.std() / np.sqrt(len(R))), strength=R.st.mean(), total=R.r.mean()))
    out["broad_panic_by_horizon"] = pd.DataFrame(res).set_index("h")
    # 2) book position stats: allocation when in, realised vol, number of distinct holding days
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].fillna(0)
            inp = a.abs() > 1e-6
            rows.append(dict(c=c, inbars=inp.sum(), panicbars=(b["regime"] == "mean_reversion").sum(),
                             fc_pos=(b["forecast"] > 0).sum(), alloc_mean=a[inp].mean() if inp.any() else np.nan,
                             vol=b["sizing_realised_vol"][inp].mean() if inp.any() else np.nan))
    P = pd.DataFrame(rows)
    out["position_by_coin"] = P.groupby("c").agg({"inbars": "sum", "panicbars": "sum", "fc_pos": "sum", "alloc_mean": "mean", "vol": "mean"})
    # 3) trades: return by duration bucket, and worst trades' context
    tr = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["c"] = c; tr.append(t)
    T = pd.concat(tr)
    T["durd"] = pd.cut(T.duration_minutes / 1440, [0, 3.5, 7, 14, 30, 999])
    out["trades_by_duration"] = T.groupby("durd").net_profit_loss_percent.agg(["count", "mean", "median", "min"])
    # 4) book daily: share of book gain in days with position vs not; deepest drawdown per window chain
    dd = []
    for c in days:
        for w, d in days[c].items():
            br = d.book_return.fillna(0); v = (1 + br).cumprod()
            dd.append(dict(c=c, maxdd=(v / v.cummax() - 1).min(), active_days=(br.abs() > 1e-9).sum(), ndays=len(br)))
    DD = pd.DataFrame(dd)
    out["dd_by_coin"] = DD.groupby("c").agg({"maxdd": "min", "active_days": "sum", "ndays": "sum"})
    return out
