def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            vol720 = r1.rolling(720, min_periods=240).std()
            z = r1 / vol24
            vr = vol24 / vol720
            ts = pd.to_datetime(b["timestamp"], utc=True)
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "vr": vr,
                               "regime": b["regime"], "hour": ts.dt.hour, "year": ts.dt.year,
                               "fc": b["forecast"]})
            for h in (24, 72, 168):
                fr = c.shift(-h) / c - 1
                df[f"f{h}"] = fr
                g = np.zeros(len(c), bool); g[::h] = True
                df[f"g{h}"] = g
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    res = []
    for h in (24, 72, 168):
        G = D[D[f"g{h}"]].dropna(subset=[f"f{h}", "z", "vr"]).copy()
        drift = G.groupby("coin")[f"f{h}"].transform("mean")
        G["ex"] = (G[f"f{h}"] - drift) * -np.sign(G["z"])
        G["tot"] = G[f"f{h}"] * -np.sign(G["z"])
        G["az"] = G["z"].abs()
        G["zb"] = pd.cut(G["az"], [0, 0.5, 1, 1.5, 2, 3, 100])
        G["vb"] = pd.cut(G["vr"], [0, 0.8, 1, 1.3, 1.7, 2.5, 100])
        for (vb, zb), s in G.groupby(["vb", "zb"], observed=True):
            if len(s) < 30: continue
            res.append({"h": h, "vr": str(vb), "absz": str(zb), "n": len(s),
                        "ex_mean%": 100*s["ex"].mean(), "tot%": 100*s["tot"].mean(),
                        "t": s["ex"].mean()/(s["ex"].std()/np.sqrt(len(s)))})
    R = pd.DataFrame(res)
    out["grid h24 by vr x absz"] = R[R.h == 24].drop(columns="h").reset_index(drop=True)
    out["grid h72 by vr x absz"] = R[R.h == 72].drop(columns="h").reset_index(drop=True)
    out["grid h168 by vr x absz"] = R[R.h == 168].drop(columns="h").reset_index(drop=True)
    # side and hour, h24, vr>1, |z|>1.5
    G = D[D["g24"]].dropna(subset=["f24", "z", "vr"]).copy()
    drift = G.groupby("coin")["f24"].transform("mean")
    G["ex"] = (G["f24"] - drift) * -np.sign(G["z"])
    S = G[(G.vr > 1) & (G.z.abs() > 1.5)]
    S["side"] = np.where(S.z > 0, "short(after up)", "long(after down)")
    out["side h24 vr>1 |z|>1.5"] = S.groupby("side")["ex"].agg(["count", "mean", "std"]).assign(t=lambda x: x["mean"]/(x["std"]/np.sqrt(x["count"])))
    S["hb"] = S["hour"] // 4 * 4
    out["hour block h24 vr>1 |z|>1.5"] = S.groupby("hb")["ex"].agg(["count", "mean"])
    out["coin h24 vr>1 |z|>1.5"] = S.groupby("coin")["ex"].agg(["count", "mean"])
    # trades
    T = []
    for coin in trades:
        for w, t in trades[coin].items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["hours"] = T["duration_minutes"]/60
    out["trades"] = T.groupby("side").agg(n=("side", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"), hours=("hours", "median"))
    T["fb"] = pd.cut(T["entry_forecast"].abs(), [0, 2, 5, 10, 15, 20.01])
    out["trades by |entry fc|"] = T.groupby("fb", observed=True).agg(n=("side", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
