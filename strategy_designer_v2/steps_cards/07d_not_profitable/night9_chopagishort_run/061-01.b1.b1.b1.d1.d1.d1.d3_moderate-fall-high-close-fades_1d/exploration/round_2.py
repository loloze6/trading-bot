def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # 1. trades with their entry characteristics
    rows = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if not len(t):
                continue
            b = data["bars"][coin][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).astype(float).replace(0, np.nan)
            loc = (c - b["low"]) / rng
            r5 = c / c.shift(5) - 1; r20 = c / c.shift(20) - 1; r60 = c / c.shift(60) - 1
            r1 = c / c.shift(1) - 1
            vol10 = r1.rolling(10).std(); vol60 = r1.rolling(60).std()
            for _, tr in t.iterrows():
                et = pd.to_datetime(tr["entry_time"])
                i = int(np.argmin(np.abs((ts - et).dt.total_seconds().values)))
                rows.append(dict(coin=coin, w=w, net=tr["net_profit_loss_percent"],
                                 dur=tr["duration_minutes"] / 1440, loc=loc.iloc[i], r5=r5.iloc[i],
                                 r20=r20.iloc[i], r60=r60.iloc[i], r1=r1.iloc[i],
                                 volratio=vol10.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                 fc=tr["entry_forecast"], year=et.year))
    T = pd.DataFrame(rows)
    out["trades sorted by net (worst 8)"] = T.sort_values("net").head(8).drop(columns=["w"]).round(3)
    out["trades best 6"] = T.sort_values("net").tail(6).drop(columns=["w"]).round(3)
    out["trades by year"] = T.groupby("year")["net"].agg(["count", "mean", "sum"])
    out["trades by duration>5d"] = T.groupby(T["dur"] > 5.5)["net"].agg(["count", "mean", "sum"])
    out["trades by r1>0 at entry"] = T.groupby(T["r1"] > 0)["net"].agg(["count", "mean", "sum"])
    out["trades by volratio>1"] = T.groupby(T["volratio"] > 1)["net"].agg(["count", "mean", "sum"])
    out["trades by r20<-0.15"] = T.groupby(T["r20"] < -0.15)["net"].agg(["count", "mean", "sum"])

    # 2. horizons and gradedness in broad case P & hi & neg5 & r20<0, and P & hi
    res = []; grad = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).astype(float).replace(0, np.nan)
            loc = (c - b["low"]) / rng
            r5 = c / c.shift(5) - 1; r20 = c / c.shift(20) - 1
            r1 = c / c.shift(1) - 1
            P = b["regime"].isin(["mean_reversion", "unknown"])
            for H in [2, 3, 5, 10]:
                fwd = c.shift(-H) / c - 1
                for i in range(0, len(b), H):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    res.append(dict(coin=coin, H=H, fwd=fwd.iloc[i], P=bool(P.iloc[i]),
                                    loc=loc.iloc[i], r5=r5.iloc[i], r20=r20.iloc[i], r1=r1.iloc[i],
                                    ts=pd.Timestamp(b["timestamp"].iloc[i]).floor("D")))
    D = pd.DataFrame(res)
    D["drift"] = D.groupby(["coin", "H"])["fwd"].transform("mean")
    D["un"] = -(D["fwd"] - D["drift"])

    def summ(s):
        if len(s) < 3:
            return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan, days=len(s)))
        mu = s["un"].mean()
        g = (s["un"] - mu).groupby(s["ts"]).sum()
        se = np.sqrt((g ** 2).sum()) / len(s)
        return pd.Series(dict(n=len(s), mean=mu, t=mu / se, days=len(g)))

    hz = {}
    for H in [2, 3, 5, 10]:
        d = D[D["H"] == H]
        hz[f"H{H} P&hi&neg5&r20<0"] = summ(d[d.P & (d["loc"] >= .5) & (d.r5 < 0) & (d.r20 < 0)])
        hz[f"H{H} P&hi&neg5"] = summ(d[d.P & (d["loc"] >= .5) & (d.r5 < 0)])
        hz[f"H{H} P&hi"] = summ(d[d.P & (d["loc"] >= .5)])
        hz[f"H{H} P&lo&neg5"] = summ(d[d.P & (d["loc"] < .5) & (d.r5 < 0)])
        hz[f"H{H} P&neg5 any loc"] = summ(d[d.P & (d.r5 < 0)])
        hz[f"H{H} noP&hi&neg5&r20<0"] = summ(d[~d.P & (d["loc"] >= .5) & (d.r5 < 0) & (d.r20 < 0)])
    out["horizons"] = pd.DataFrame(hz).T
    d = D[(D["H"] == 5) & D.P & (D.r5 < 0)].copy()
    d["q"] = pd.cut(d["loc"], [0, .33, .5, .67, .85, 1.0001], include_lowest=True)
    out["H5 P&neg5 by loc"] = d.groupby("q")["un"].agg(["count", "mean"])
    d2 = D[(D["H"] == 5) & D.P & (D["loc"] >= .5)].copy()
    d2["q"] = pd.cut(d2["r5"], [-1, -0.1, -0.03, 0, 0.05, 10])
    out["H5 P&hi by r5"] = d2.groupby("q")["un"].agg(["count", "mean"])
    d3 = D[(D["H"] == 5) & D.P & (D["loc"] >= .5) & (D.r5 < 0)].copy()
    d3["q"] = pd.cut(d3["r20"], [-1, -0.2, -0.1, 0, 10])
    out["H5 P&hi&neg5 by r20"] = d3.groupby("q")["un"].agg(["count", "mean"])
    return out
