import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; trades = data["trades"]
    H = [1, 4, 12, 24, 72]
    rows = []
    slow = []
    for coin in bars:
        for w, b in bars[coin].items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            vol = r1.rolling(24, min_periods=20).std()
            z1 = r1 / vol
            r24 = c / c.shift(24) - 1
            z24 = r24 / (vol * np.sqrt(24))
            r72 = c / c.shift(72) - 1
            z72 = r72 / (vol * np.sqrt(72))
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                fwd = (c.shift(-h) / c - 1).iloc[idx]
                df = pd.DataFrame({"coin": coin, "w": w, "h": h, "fwd": fwd.values,
                                   "z1": z1.iloc[idx].values, "z24": z24.iloc[idx].values,
                                   "z72": z72.iloc[idx].values,
                                   "hour": ts.iloc[idx].dt.hour.values})
                rows.append(df)
    d = pd.concat(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["drift"]
    out = {}
    res = []
    for sig in ["z1", "z24", "z72"]:
        for h in H:
            s = d[(d.h == h)].dropna(subset=[sig, "ex"])
            a = s[sig].abs()
            bins = pd.cut(a, [0, 1, 2, 3, 4, np.inf])
            mv = -np.sign(s[sig]) * s["ex"]
            tot = -np.sign(s[sig]) * s["fwd"]
            g = pd.DataFrame({"b": bins, "mv": mv, "tot": tot}).groupby("b", observed=True)
            for k, gg in g:
                n = len(gg)
                res.append({"sig": sig, "h": h, "absz": str(k), "n": n,
                            "unusual_%": 100 * gg.mv.mean(), "total_%": 100 * gg.tot.mean(),
                            "t": gg.mv.mean() / (gg.mv.std() / np.sqrt(n)) if n > 2 else np.nan})
    R = pd.DataFrame(res)
    out["z1_buckets"] = R[R.sig == "z1"].drop(columns="sig")
    out["z24_buckets"] = R[R.sig == "z24"].drop(columns="sig")
    out["z72_buckets"] = R[R.sig == "z72"].drop(columns="sig")
    # settlement hours for z1, h=1 and h=4: bar at close of hour 23,7,15 -> next hour is settlement
    s = d[(d.h == 1)].dropna(subset=["z1", "ex"]).copy()
    s["mv"] = -np.sign(s.z1) * s.ex
    s["big"] = s.z1.abs() > 2
    s["pre"] = s.hour.isin([23, 7, 15])
    out["z1_h1_by_preSettle_big"] = s.groupby(["pre", "big"]).mv.agg(["count", "mean"]).assign(mean=lambda x: x["mean"] * 100)
    # trades
    T = pd.concat([trades[c][w] for c in trades for w in trades[c]])
    out["trades"] = pd.Series({"n": len(T), "mean_gross_%": T.profit_loss_percent.mean(),
                               "mean_net_%": T.net_profit_loss_percent.mean(),
                               "median_dur_min": T.duration_minutes.median()})
    return out
