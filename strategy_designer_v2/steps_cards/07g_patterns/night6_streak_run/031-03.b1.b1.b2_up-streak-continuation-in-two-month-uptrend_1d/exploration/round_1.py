def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 20
    rows = []
    rows5 = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            up = (r > 0).astype(int); dn = (r < 0).astype(int)
            us = up.groupby((up != up.shift()).cumsum()).cumsum() * up
            ds = dn.groupby((dn != dn.shift()).cumsum()).cumsum() * dn
            r30 = c / c.shift(30) - 1; r60 = c / c.shift(60) - 1; r10 = c/c.shift(10)-1
            vol = r.rolling(30).std()
            volrank = vol.rolling(365, min_periods=60).rank(pct=True)
            f20 = c.shift(-H) / c - 1
            f5 = c.shift(-5) / c - 1
            z = r / r.rolling(60, min_periods=20).std()
            dfw = pd.DataFrame({"coin": coin, "w": w, "ts": b["timestamp"], "us": us, "ds": ds, "r30": r30, "r60": r60,
                                "r10": r10, "vol": vol, "volrank": volrank, "f20": f20, "f5": f5, "z": z,
                                "fc": b["forecast"], "pos": b["postRebalance_current_allocation"], "r1": r})
            g = dfw.iloc[::H].copy(); rows.append(g)
            g5 = dfw.iloc[::5].copy(); rows5.append(g5)
            daily.append(dfw)
    G = pd.concat(rows); G5 = pd.concat(rows5); D = pd.concat(daily)
    G = G.dropna(subset=["f20"])
    G["u"] = G["f20"] - G.groupby("coin")["f20"].transform("mean")
    G5 = G5.dropna(subset=["f5"]); G5["u"] = G5["f5"] - G5.groupby("coin")["f5"].transform("mean")
    def summ(df, key, col="u"):
        a = df.groupby(key)[col].agg(["mean", "count", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.round(4)
    out = {}
    G["trend"] = np.where((G.r30 > 0) & (G.r60 > 0), "both_up", np.where((G.r30 < 0) & (G.r60 < 0), "both_dn", "mixed"))
    out["fwd20 unusual by trend regime"] = summ(G.dropna(subset=["r60"]), "trend")
    G["usb"] = G["us"].clip(upper=5); G["dsb"] = G["ds"].clip(upper=5)
    out["fwd20 by up streak (both_up)"] = summ(G[G.trend == "both_up"], "usb")
    out["fwd20 by up streak (all)"] = summ(G, "usb")
    out["fwd20 by down streak (all)"] = summ(G, "dsb")
    Gq = G.dropna(subset=["r60"]).copy()
    Gq["r60q"] = pd.qcut(Gq["r60"], 5, labels=False)
    out["fwd20 by r60 quintile"] = summ(Gq, "r60q")
    Gq["r30q"] = pd.qcut(Gq["r30"], 5, labels=False)
    out["fwd20 by r30 quintile"] = summ(Gq, "r30q")
    Gv = G.dropna(subset=["volrank"]).copy(); Gv["vq"] = pd.qcut(Gv["volrank"], 5, labels=False, duplicates="drop")
    out["fwd20 by vol rank quintile"] = summ(Gv, "vq")
    G5q = G5.dropna(subset=["z"]).copy()
    G5q["zb"] = pd.cut(G5q["z"], [-99, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 99])
    out["fwd5 by last-day z"] = summ(G5q, "zb")
    G5q2 = G5.dropna(subset=["r10"]).copy(); G5q2["r10q"] = pd.qcut(G5q2["r10"], 5, labels=False)
    out["fwd5 by r10 quintile"] = summ(G5q2, "r10q")
    D["wd"] = pd.to_datetime(D["ts"]).dt.weekday
    D["r1u"] = D["r1"] - D.groupby("coin")["r1"].transform("mean")
    out["daily ret by weekday"] = summ(D.dropna(subset=["r1"]), "wd", "r1u")
    D["yr"] = pd.to_datetime(D["ts"]).dt.year
    # book positions
    D["gain"] = D["pos"] * D.groupby(["coin", "w"])["r1"].shift(-1)
    out["position gain by trend (daily)"] = D.dropna(subset=["gain", "r60"]).assign(
        tr=lambda x: np.where((x.r30 > 0) & (x.r60 > 0), "both_up", "other")).groupby("tr")["gain"].agg(["mean", "count", "sum"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    T["fcb"] = pd.cut(T["entry_forecast"], [-1, 5, 10, 15, 21])
    out["trades by entry forecast"] = T.groupby("fcb")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    T["days"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["days"], [0, 20, 30, 60, 120, 9999])
    out["trades by duration days"] = T.groupby("db")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    out["trades overall"] = T["net_profit_loss_percent"].describe().round(3)
    return out
