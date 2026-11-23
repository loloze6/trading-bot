def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    hourly = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r = c.pct_change()
            v24 = r.rolling(24).std()
            v720 = r.rolling(720).std()
            z = r / v24
            ratio = v24 / v720
            ret24 = r.rolling(24).sum()  # approx 24h trend (log-ish)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            vol = df["volume"].astype(float)
            vrel = vol / vol.rolling(168).median()
            n = len(df)
            for h in (1, 4, 24):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, n, h)
                sub = pd.DataFrame({"coin": coin, "w": w, "h": h, "z": z.values[idx], "ratio": ratio.values[idx],
                                    "fwd": fwd.values[idx], "trend": ret24.values[idx],
                                    "hour": ts.dt.hour.values[idx], "wd": ts.dt.weekday.values[idx]})
                rows.append(sub)
            hourly.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                                        "r_next": c.shift(-1) / c - 1, "z": z, "trend": ret24,
                                        "vrel": vrel, "ratio": ratio}))
    G = pd.concat(rows).dropna(subset=["z", "fwd"])
    G["drift"] = G.groupby(["coin", "h"])["fwd"].transform("mean")
    G["un"] = G["fwd"] - G["drift"]
    out = {}
    def reg(d):
        if len(d) < 50: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        s = stats.linregress(d["z"], d["un"])
        return pd.Series({"n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    out["slope un~z by horizon (all regimes)"] = G.groupby("h").apply(reg)
    G2 = G.dropna(subset=["ratio"]).copy()
    G2["rq"] = pd.qcut(G2["ratio"], 5, labels=False)
    out["slope un~z by h x volratio quintile"] = G2.groupby(["h", "rq"]).apply(reg).unstack("h")
    # sign continuation by |z| bucket at 24h
    g24 = G2[G2.h == 24].copy()
    g24["zq"] = pd.qcut(g24["z"].abs(), 5, labels=False)
    g24["sun"] = np.sign(g24["z"]) * g24["un"]
    out["24h signed unusual by |z| quintile"] = g24.groupby("zq")["sun"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    g4 = G2[G2.h == 4].copy()
    g4["zq"] = pd.qcut(g4["z"].abs(), 5, labels=False)
    g4["sun"] = np.sign(g4["z"]) * g4["un"]
    out["4h signed unusual by |z| quintile"] = g4.groupby("zq")["sun"].agg(["count", "mean", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["slope 24h by coin"] = G[G.h == 24].groupby("coin").apply(reg)
    H = pd.concat(hourly).dropna(subset=["r_next"])
    H["un"] = H["r_next"] - H.groupby("coin")["r_next"].transform("mean")
    # next-hour return by hour of the next bar (bar that opens at hour+1)
    H["nexthour"] = (H["hour"] + 1) % 24
    hh = H.groupby("nexthour")["un"].agg(["count", "mean", "std"])
    hh["t"] = hh["mean"] / hh["std"] * np.sqrt(hh["count"])
    H["strend"] = np.sign(H["trend"])
    H["sun_tr"] = H["strend"] * H["un"]
    t2 = H.groupby("nexthour")["sun_tr"].agg(["mean", "std", "count"])
    hh["trend_signed_mean"] = t2["mean"]
    hh["trend_signed_t"] = t2["mean"] / t2["std"] * np.sqrt(t2["count"])
    hh["vrel_med"] = H.groupby("hour")["vrel"].median().reindex(hh.index).values
    out["next-hour unusual by its opening hour UTC"] = hh.drop(columns="std")
    wd = H.groupby("wd")["un"].agg(["count", "mean", "std"]); wd["t"] = wd["mean"]/wd["std"]*np.sqrt(wd["count"])
    out["next-hour unusual by weekday"] = wd.drop(columns="std")
    # 1h reversal: next hour vs z
    Hz = H.dropna(subset=["z"])
    s = stats.linregress(Hz["z"], Hz["un"])
    out["1h slope next-hour un ~ z, all bars"] = f"slope {s.slope:.3e} t {s.slope/s.stderr:.2f} n {len(Hz)}"
    return out
