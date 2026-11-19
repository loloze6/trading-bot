import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    hrs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float)
            r24 = cl / cl.shift(24) - 1
            mabs = r24.abs().shift(1).rolling(1440, min_periods=200).mean()
            z = r24 / mabs
            ret1 = cl.pct_change()
            vol = ret1.rolling(480, min_periods=100).std()
            vr = vol / vol.rolling(2400, min_periods=480).mean()
            ts = pd.to_datetime(b["timestamp"])
            for h in (24, 72):
                idx = np.arange(0, len(b) - h, h)
                fr = (cl.shift(-h) / cl - 1).iloc[idx]
                d = pd.DataFrame({"coin": c, "w": w, "h": h, "z": z.iloc[idx].values,
                                  "vr": vr.iloc[idx].values, "fr": fr.values,
                                  "fc": b["forecast"].iloc[idx].values,
                                  "reg": b["regime"].iloc[idx].values,
                                  "pr24": r24.iloc[idx].values})
                rows.append(d)
            hh = pd.DataFrame({"coin": c, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                               "r": ret1, "pos": b["postRebalance_current_allocation"].shift(1),
                               "pr": ret1})
            hrs.append(hh)
    g = pd.concat(rows)
    g = g.dropna(subset=["z", "fr"])
    g["mu"] = g.groupby(["coin", "h"])["fr"].transform("mean")
    g["ex"] = g["fr"] - g["mu"]
    g["fade"] = -np.sign(g["z"]) * g["ex"]
    g["zb"] = pd.cut(g["z"], [-np.inf, -2, -1, -0.5, 0.5, 1, 2, np.inf])
    g["vrb"] = pd.cut(g["vr"], [0, 0.8, 1.0, 1.25, np.inf])
    def summ(x):
        return pd.Series({"n": len(x), "mean_ex": x["ex"].mean(),
                          "t": x["ex"].mean() / (x["ex"].std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    for h in (24, 72):
        gh = g[g.h == h]
        out[f"ex ret by z bucket h{h}"] = gh.groupby("zb", observed=True).apply(summ)
        out[f"ex ret by z bucket x vol h{h}"] = gh.groupby(["vrb", "zb"], observed=True).apply(summ)
        big = gh[gh.z.abs() >= 1.6]
        out[f"fade |z|>=1.6 by vol h{h}"] = big.assign(ex=big.fade).groupby("vrb", observed=True).apply(summ)
        out[f"fade |z|>=1.6 by sign h{h}"] = big.assign(ex=big.fade, s=np.sign(big.z)).groupby(["s", "vrb"], observed=True).apply(summ)
        out[f"ex ret by vol h{h}"] = gh.groupby(["coin", "vrb"], observed=True).apply(summ)
    H = pd.concat(hrs).dropna()
    def hs(x):
        return pd.Series({"n": len(x), "mean_bp": x["r"].mean() * 1e4,
                          "t": x["r"].mean() / (x["r"].std() / np.sqrt(len(x)))})
    out["hour ret"] = H.groupby("hour").apply(hs)
    out["weekday ret"] = H.groupby(["wd"]).apply(hs)
    # book
    D = []
    for c in days:
        for w, d in days[c].items():
            D.append(d.assign(coin=c, w=w))
    D = pd.concat(D).dropna(subset=["book_return"])
    out["book by coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["book by window mean"] = D.groupby("w")["book_return"].mean().to_frame()
    # position gain: market vs timing
    H["gain"] = H["pos"] * H["pr"]
    mu = H.groupby("coin")["pr"].transform("mean")
    H["mkt"] = H["pos"] * mu
    out["gain split bp/bar"] = H.groupby("coin")[["gain", "mkt"]].mean() * 1e4
    out["gain by pos sign"] = H.assign(s=np.sign(H.pos)).groupby(["coin", "s"]).apply(
        lambda x: pd.Series({"n": len(x), "gain_bp": x.gain.mean() * 1e4, "t": x.gain.mean() / (x.gain.std() / np.sqrt(len(x)))}))
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c]])
    T["db"] = pd.cut(T["duration_minutes"] / 60, [0, 6, 24, 72, 1e6])
    out["trades by side/dur"] = T.groupby(["side", "db"], observed=True).agg(
        n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"),
        gross=("profit_loss_percent", "mean"))
    return out
