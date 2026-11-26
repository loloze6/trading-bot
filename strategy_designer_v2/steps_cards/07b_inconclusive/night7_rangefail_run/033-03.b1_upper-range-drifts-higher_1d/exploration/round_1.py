def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            f = df["forecast"].astype(float).values
            ah = df.get("debug_info.components.above_high.last_history_value")
            ah = ah.astype(float).values if ah is not None else np.full(len(df), np.nan)
            rp = df.get("debug_info.components.range_pos.last_history_value")
            rp = rp.astype(float).values if rp is not None else np.full(len(df), np.nan)
            r1 = pd.Series(c).pct_change()
            tr60 = pd.Series(c).pct_change(60).values
            vol30 = r1.rolling(30).std()
            volmed = vol30.rolling(365, min_periods=120).median()
            agit = (vol30 > volmed).values
            agit_ok = volmed.notna().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (5, 10, 20):
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                                     yr=yr[i], f=f[i], ah=ah[i], rp=rp[i], ret=c[i+h]/c[i]-1,
                                     tr=tr60[i], ag=(agit[i] if agit_ok[i] else np.nan)))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    d["sret"] = d["ex"] * np.sign(d["f"])
    def slope_t(g):
        g = g.dropna(subset=["f", "ex"])
        if len(g) < 15 or g["f"].std() == 0: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan, mean_signed=np.nan))
        r = stats.linregress(g["f"], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr, mean_signed=g["sret"].mean()))
    out = {}
    out["by_h"] = d.groupby("h").apply(slope_t)
    d10 = d[d.h == 10].copy()
    out["h10_by_coin"] = d10.groupby("coin").apply(slope_t)
    out["h10_by_window"] = d10.groupby("w").apply(slope_t)
    out["h10_by_year"] = d10.groupby("yr").apply(slope_t)
    d10["fq"] = pd.qcut(d10["f"], 5, labels=False, duplicates="drop")
    out["h10_by_fquint"] = d10.groupby("fq").agg(n=("ex", "size"), fmean=("f", "mean"), ex_mean=("ex", "mean"),
                                                 ex_t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d10["side"] = np.where(d10["ah"] > 0, "above_high", np.where(d10["f"] > 0, "upper", "lower"))
    out["h10_by_side"] = d10.groupby("side").agg(n=("ex", "size"), ex_mean=("ex", "mean"),
                                                 ex_t=("ex", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    d10["trend"] = np.where(d10["tr"] > 0.10, "rising", np.where(d10["tr"] < -0.10, "falling",
                            np.where(d10["tr"].notna(), "choppy", "na")))
    out["h10_by_trend"] = d10.groupby("trend").apply(slope_t)
    d10["agit"] = d10["ag"].map({1.0: "agitated", 0.0: "calm", True: "agitated", False: "calm"}).fillna("na")
    out["h10_by_agit"] = d10.groupby("agit").apply(slope_t)
    out["h10_trend_agit"] = d10.groupby(["trend", "agit"]).apply(slope_t)
    out["h10_side_trend"] = d10.groupby(["trend", "side"]).agg(n=("ex", "size"), ex_mean=("ex", "mean"))
    d20 = d[d.h == 20].copy()
    d20["trend"] = np.where(d20["tr"] > 0.10, "rising", np.where(d20["tr"] < -0.10, "falling",
                            np.where(d20["tr"].notna(), "choppy", "na")))
    out["h20_by_trend"] = d20.groupby("trend").apply(slope_t)
    out["h20_by_coin"] = d20.groupby("coin").apply(slope_t)
    return out
