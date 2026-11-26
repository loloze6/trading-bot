def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r = pd.Series(c).pct_change()
            vol30 = r.rolling(30, min_periods=20).std()
            vol10 = r.rolling(10, min_periods=8).std()
            raw = df.get("debug_info.components.dip.last_history_value")
            hi5 = pd.Series(c).rolling(5, min_periods=1).max()
            ret5back = pd.Series(c).pct_change(5)
            for h in (5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ret=c[i + h] / c[i] - 1,
                                     fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                                     raw=(raw.iloc[i] if raw is not None else np.nan),
                                     dd=(c[i] / hi5.iloc[i] - 1),
                                     vol30=vol30.iloc[i], vratio=vol10.iloc[i] / vol30.iloc[i],
                                     back5=ret5back.iloc[i]))
    d = pd.DataFrame(rows)
    d = d.join(d.groupby(["coin", "h"])["ret"].mean().rename("drift"), on=["coin", "h"])
    d["ex"] = d["ret"] - d["drift"]
    d = d.join(d[d.h == 5].groupby("coin")["vol30"].median().rename("mv"), on="coin")
    d["agit"] = np.where(d["vol30"] > d["mv"], "agit", "calm")
    act = d[(d.fc != 0) & d.fc.notna()].dropna(subset=["raw"]).copy()
    act["araw"] = act["raw"].abs()
    act["af"] = act["fc"].abs()
    out = {}

    def sl(g, x):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 15:
            return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        s = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr, mean_ex=g["ex"].mean()))

    out["raw_by_h_agit"] = act.groupby(["h", "agit"]).apply(lambda g: sl(g, "araw"))
    out["raw_by_h"] = act.groupby("h").apply(lambda g: sl(g, "araw"))
    out["raw_h5_by_coin"] = act[act.h == 5].groupby("coin").apply(lambda g: sl(g, "araw"))
    out["raw_h5_by_year"] = act[act.h == 5].groupby("w").apply(lambda g: sl(g, "araw"))[["n", "t"]]
    out["raw_h5_noXRP"] = sl(act[(act.h == 5) & (act.coin != "XRPUSD")], "araw")
    out["fc_raw_corr"] = act[act.h == 5][["af", "araw"]].corr().iloc[0, 1]
    a5 = act[act.h == 5].copy()
    a5["q"] = pd.qcut(a5["araw"], 5, labels=False, duplicates="drop")
    out["raw_h5_quint_by_agit"] = a5.groupby(["agit", "q"])["ex"].agg(["count", "mean"]).unstack(0)
    return out
