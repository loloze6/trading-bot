def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    rows24 = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean()
            vr = v / v.rolling(720, min_periods=240).mean()
            r24p = c / c.shift(24) - 1
            vol24 = r1.rolling(168, min_periods=100).std()
            f4 = c.shift(-4) / c - 1
            f24 = c.shift(-24) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            g = pd.DataFrame({"coin": coin, "w": w, "r1": r1, "sc": r1 / mabs, "vr": vr,
                              "f4": f4, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                              "vol": vol24, "r24p": r24p / (mabs * np.sqrt(24))})
            idx4 = np.arange(0, len(df), 4)
            rows.append(g.iloc[idx4])
            idx24 = np.arange(0, len(df), 24)
            h = g.iloc[idx24].copy(); h["f24"] = f24.iloc[idx24].values
            rows24.append(h)
    A = pd.concat(rows).dropna(subset=["f4", "sc", "vr"])
    A["u4"] = A["f4"] - A.groupby("coin")["f4"].transform("mean")
    A["dir"] = np.sign(A["sc"])
    A["mag"] = pd.cut(A["sc"].abs(), [0, 1, 2, 3, 5, 1e9], labels=["<1", "1-2", "2-3", "3-5", ">5"])
    A["vb"] = pd.cut(A["vr"], [0, 0.7, 1.0, 2.0, 4.0, 1e9], labels=["<.7", ".7-1", "1-2", "2-4", ">4"])
    A["sig"] = A["u4"] * A["dir"]  # continuation in hour's direction
    def tab(gb, col):
        t = gb[col].agg(["mean", "count", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.drop(columns="std")
    out["cont4_by_mag_dir"] = tab(A.groupby(["mag", "dir"], observed=True), "sig")
    out["cont4_by_vol_mag>2"] = tab(A[A["sc"].abs() > 2].groupby(["vb", "dir"], observed=True), "sig")
    out["u4_by_hour"] = tab(A.groupby("hour"), "u4")
    out["u4_by_weekday"] = tab(A.groupby("wd"), "u4")
    A["volq"] = A.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["cont4_by_volq_mag>2"] = tab(A[A["sc"].abs() > 2].groupby("volq"), "sig")
    B = pd.concat(rows24).dropna(subset=["f24", "r24p"])
    B["u24"] = B["f24"] - B.groupby("coin")["f24"].transform("mean")
    B["q"] = B.groupby("coin")["r24p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["u24_by_past24_quint"] = tab(B.groupby("q"), "u24")
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].mean()
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades"] = T.groupby("coin").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                         net=("net_profit_loss_percent", "mean"),
                                         dur=("duration_minutes", "median"))
    return out
