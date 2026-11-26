def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    H = [5, 10, 20, 40]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            raw = df.get("debug_info.components.vol_growth.last_history_value")
            post = df.get("debug_info.components.vol_growth.post_pipeline_value")
            vol = df["volume"].astype(float)
            # 30d vs prior 30d log volume ratio recomputed within window
            m30 = vol.rolling(30).mean()
            lr = np.log(m30 / m30.shift(30))
            r20p = pd.Series(c).pct_change(20)
            dr = pd.Series(c).pct_change()
            sd30 = dr.rolling(30).std()
            sd90med = sd30.rolling(90, min_periods=30).median()
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 20):
                rec = {"coin": coin, "w": w, "i": i, "year": ts.iloc[i].year,
                       "day": ts.iloc[i].normalize(),
                       "fc": df["forecast"].iloc[i], "regime": df["regime"].iloc[i],
                       "raw": raw.iloc[i] if raw is not None else np.nan,
                       "post": post.iloc[i] if post is not None else np.nan,
                       "lr": lr.iloc[i], "r20p": r20p.iloc[i],
                       "agit": (sd30.iloc[i] > sd90med.iloc[i]) if pd.notna(sd90med.iloc[i]) else np.nan}
                for h in H:
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows)
    for h in H:
        g[f"m{h}"] = g.groupby("coin")[f"f{h}"].transform("mean")
        g[f"u{h}"] = g[f"f{h}"] - g[f"m{h}"]
    act = g[g["regime"] == "mean_reversion"].copy()
    act["side"] = np.sign(act["raw"].fillna(act["lr"]))
    def ct(x, days):
        s = pd.Series(x.values, index=days.values).groupby(level=0).sum()
        k = len(s)
        m = x.mean()
        se = np.sqrt(((s - s.mean() * 0) ** 2).sum()) / len(x) if len(x) > 1 else np.nan
        return m, (m / se if se and se > 0 else np.nan), len(x), k
    out = {}
    # sign-based unusual move per horizon
    hz = []
    for h in H:
        a = act.dropna(subset=[f"u{h}", "side"])
        v = a["side"] * a[f"u{h}"]
        m, t, nn, k = ct(v - v.mean() + v.mean(), a["day"])
        dev = v - v.mean()
        s = pd.Series(dev.values, index=a["day"].values).groupby(level=0).sum()
        t2 = v.mean() / (np.sqrt((s ** 2).sum()) / len(v))
        main = a["fc"] / 10 * a[f"u{h}"]
        dm = main - main.mean()
        s2 = pd.Series(dm.values, index=a["day"].values).groupby(level=0).sum()
        hz.append({"h": h, "n": len(v), "days": len(s), "sign_unusual": v.mean(), "t_sign": t2,
                   "main": main.mean(), "t_main": main.mean() / (np.sqrt((s2 ** 2).sum()) / len(main))})
    out["by_horizon_activegrid"] = pd.DataFrame(hz)
    a = act.dropna(subset=["u20", "side"]).copy()
    a["v"] = a["side"] * a["u20"]
    a["fcside_agree"] = np.sign(a["fc"]) == a["side"]
    out["share_fc_sign_agrees_raw"] = float(a["fcside_agree"].mean())
    out["corr_fc_raw"] = float(a[["fc", "raw"]].corr().iloc[0, 1]) if a["raw"].notna().sum() > 3 else np.nan
    def summ(grp):
        return a.groupby(grp).agg(n=("v", "size"), mean_v=("v", "mean"), sd=("v", "std"),
                                  mean_u20=("u20", "mean"), mean_raw=("raw", "mean"))
    out["by_side"] = summ("side")
    out["by_coin"] = summ("coin")
    out["by_year"] = summ("year")
    out["by_agit"] = summ("agit")
    a["q"] = pd.qcut(a["raw"].rank(method="first"), 5, labels=False)
    out["by_raw_quintile"] = a.groupby("q").agg(n=("u20", "size"), raw=("raw", "mean"),
                                                u20=("u20", "mean"), f20=("f20", "mean"), fc=("fc", "mean"))
    a["fq"] = pd.qcut(a["fc"].abs().rank(method="first"), 3, labels=False)
    out["by_absfc_tercile"] = a.groupby("fq").agg(n=("v", "size"), absfc=("fc", lambda x: x.abs().mean()), mean_v=("v", "mean"))
    out["spearman_raw_u20"] = float(a[["raw", "u20"]].corr(method="spearman").iloc[0, 1])
    out["spearman_fc_u20"] = float(a[["fc", "u20"]].corr(method="spearman").iloc[0, 1])
    out["n_active_grid"] = len(act)
    return out
