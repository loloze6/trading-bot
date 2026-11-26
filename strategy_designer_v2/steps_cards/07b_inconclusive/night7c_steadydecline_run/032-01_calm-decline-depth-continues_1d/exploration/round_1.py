def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r28 = c / c.shift(28) - 1
            rng = ((b["high"] - b["low"]) / b["close"]).astype(float)
            rr = rng.rolling(28).mean() / rng.rolling(360, min_periods=100).mean()
            vr = b["volume"].rolling(28).mean() / b["volume"].rolling(360, min_periods=100).mean()
            n = len(b)
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                                     fwd=c[i + h] / c[i] - 1, r28=r28[i], rr=rr[i], vr=vr[i],
                                     regime=b["regime"][i], fc=b["forecast"][i]))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["mu"]
    d["calm"] = d["regime"] == "trending"
    d["fall"] = d["r28"] < 0
    out = {}
    g = d[d.r28.notna()].copy()
    g["grp"] = np.where(g.calm, "calm", "notcalm") + np.where(g.fall, "_fall", "_rise")
    out["by_group_h"] = g.groupby(["h", "grp"])["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))]).round(4)
    s = g[g.fall].copy()
    s["dq"] = pd.qcut(s["r28"], 4, labels=["deep", "q2", "q3", "shallow"])
    out["fall_depth_calm_h5"] = s[s.h == 5].groupby(["calm", "dq"])["ex"].agg(["mean", "count"]).round(4)
    out["fall_depth_calm_h20"] = s[s.h == 20].groupby(["calm", "dq"])["ex"].agg(["mean", "count"]).round(4)
    c5 = s[(s.h == 5) & s.calm]
    out["calmfall_h5_by_coin"] = c5.groupby("coin")["ex"].agg(["mean", "count"]).round(4)
    out["calmfall_h5_by_window"] = c5.groupby("w")["ex"].agg(["mean", "count"]).round(4)
    # slope of excess on r28 over falls, per h, calm and not
    res = []
    for h in [1, 3, 5, 10, 20]:
        for cm in [True, False]:
            x = s[(s.h == h) & (s.calm == cm)]
            if len(x) > 10:
                lr = stats.linregress(x["r28"], x["ex"])
                res.append(dict(h=h, calm=cm, n=len(x), slope=lr.slope, t=lr.slope / lr.stderr))
    out["slope_ex_on_r28_falls"] = pd.DataFrame(res).round(4)
    # vol ratio as grading among falls h5
    s5 = s[s.h == 5].copy()
    s5["rrq"] = pd.qcut(s5["rr"], 3, labels=["lowrange", "mid", "highrange"])
    out["falls_h5_by_rangeratio"] = s5.groupby("rrq")["ex"].agg(["mean", "count"]).round(4)
    return out
