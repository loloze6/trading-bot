def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; hourly = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            v24 = r.rolling(24).std(); v720 = r.rolling(720).std()
            z = r / v24; ratio = v24 / v720
            ret24 = c / c.shift(24) - 1
            ts = pd.to_datetime(df["timestamp"], utc=True)
            n = len(df)
            fwd = c.shift(-24) / c - 1
            idx = np.arange(0, n, 24)
            rows.append(pd.DataFrame({"coin": coin, "w": w, "z": z.values[idx], "ratio": ratio.values[idx],
                                      "fwd": fwd.values[idx], "v24": v24.values[idx], "yr": ts.dt.year.values[idx]}))
            hourly.append(pd.DataFrame({"coin": coin, "w": w, "yr": ts.dt.year, "hour": (ts.dt.hour + 1) % 24,
                                        "r_next": c.shift(-1) / c - 1, "trend": ret24}))
    G = pd.concat(rows).dropna(subset=["z", "fwd", "ratio"])
    G["drift"] = G.groupby("coin")["fwd"].transform("mean")
    G["un"] = G["fwd"] - G["drift"]
    G["usual"] = G.groupby("coin")["fwd"].transform("std")
    out = {}
    def reg(d, x="z", y="un"):
        if len(d) < 50: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d[x], d[y]); return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    G["hi"] = G["ratio"] >= G["ratio"].quantile(0.6)
    out["24h slope by ratio>=q60 vs below"] = G.groupby("hi").apply(reg)
    Hi = G[G.hi].copy()
    Hi["zq"] = pd.qcut(Hi["z"].abs(), 4, labels=False)
    Hi["sun"] = -np.sign(Hi["z"]) * Hi["un"]       # reversal direction
    Hi["stot"] = -np.sign(Hi["z"]) * Hi["fwd"]
    Hi["str"] = Hi["sun"] / Hi["usual"]
    a = Hi.groupby("zq").agg(n=("sun", "size"), absz=("z", lambda x: x.abs().mean()), unusual=("sun", "mean"),
                             total=("stot", "mean"), strength=("str", "mean"))
    a["t"] = Hi.groupby("zq")["sun"].apply(lambda x: x.mean() / x.std() * np.sqrt(len(x)))
    out["high-ratio: reversal move by |z| quartile (24h)"] = a
    out["high-ratio 24h slope by coin"] = Hi.groupby("coin").apply(reg)
    out["high-ratio 24h slope by year"] = Hi.groupby("yr").apply(reg)
    # slope on |z|>2 subset only
    Hb = Hi[Hi.z.abs() > 2]
    out["high-ratio |z|>2 reversal"] = f"n {len(Hb)} mean rev {(-np.sign(Hb.z)*Hb.un).mean():.4%} t {((-np.sign(Hb.z)*Hb.un).mean()/(-np.sign(Hb.z)*Hb.un).std()*np.sqrt(len(Hb))):.2f}"
    H = pd.concat(hourly).dropna(subset=["r_next", "trend"])
    H["un"] = H["r_next"] - H.groupby("coin")["r_next"].transform("mean")
    H["sun_tr"] = np.sign(H["trend"]) * H["un"]
    H["trz"] = H["trend"] / H.groupby("coin")["trend"].transform("std")
    def tt(x): return x.mean() / x.std() * np.sqrt(len(x))
    for hr in (14, 21, 22):
        s = H[H.hour == hr]
        out[f"hour {hr} unusual t by year"] = s.groupby("yr")["un"].agg(["count", "mean", tt])
    out["hour 21 unusual t by coin"] = H[H.hour == 21].groupby("coin")["un"].agg(["count", "mean", tt])
    for hr in (16, 23, 13):
        s = H[H.hour == hr]
        out[f"hour {hr} trend-signed t by year"] = s.groupby("yr")["sun_tr"].agg(["count", "mean", tt])
        out[f"hour {hr} graded slope un~trend z"] = str(reg(s, "trz", "un").round(6).to_dict())
    return out
