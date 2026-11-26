def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    grid = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            s = pd.Series(c)
            ret60 = s.pct_change(60).values
            ret30 = s.pct_change(30).values
            ret7 = s.pct_change(7).values
            dr = s.pct_change()
            vol30 = dr.rolling(30).std().values
            r7abs = s.pct_change(7).abs().rolling(30).mean().values
            f = df["forecast"].fillna(0).values
            reg = df["regime"].astype(str).values
            raw = df.get("debug_info.components.scaled_week.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            grid.setdefault(coin, [])
            for i in range(0, n - 7, 7):
                grid[coin].append(c[i + 7] / c[i] - 1)
                rows.append({"coin": coin, "win": w, "f": f[i], "reg": reg[i], "ret60": ret60[i], "ret30": ret30[i],
                             "ret7": ret7[i], "sc7": ret7[i] / r7abs[i] if r7abs[i] and not np.isnan(r7abs[i]) else np.nan,
                             "raw": raw[i], "vol30": vol30[i],
                             "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                             "fwd7": c[i + 7] / c[i] - 1})
    d = pd.DataFrame(rows)
    mu = {k: np.mean(v) for k, v in grid.items()}
    d["ex7"] = d["fwd7"] - d["coin"].map(mu)

    def ts(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    tr = d[d.reg == "trending"].copy()
    out["regime counts on grid"] = d["reg"].value_counts()
    out["trending: week up vs not"] = pd.DataFrame({"f>0": ts(tr[tr.f > 0]["ex7"]), "f==0": ts(tr[tr.f <= 0]["ex7"])}).T
    act = d[d.f > 0].copy()
    act["r60h"] = np.where(act.ret60 > 0, "ret60>0", "ret60<=0")
    out["active by 60d sign"] = act.groupby("r60h")["ex7"].apply(ts).unstack()
    act["scq"] = pd.qcut(act["sc7"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["active by raw scaled week tercile"] = act.groupby("scq")["ex7"].apply(ts).unstack()
    out["active scaled week mean by tercile"] = act.groupby("scq")["sc7"].mean()
    act["r7q"] = pd.qcut(act["ret7"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["active by ret7 tercile"] = act.groupby("r7q")["ex7"].apply(ts).unstack()
    out["corr sc7 ex7 / ret7 ex7 / ret30 ex7"] = pd.Series({
        "sc7": act[["sc7", "ex7"]].corr().iloc[0, 1],
        "ret7": act[["ret7", "ex7"]].corr().iloc[0, 1],
        "ret30": act[["ret30", "ex7"]].corr().iloc[0, 1],
        "ret60": act[["ret60", "ex7"]].corr().iloc[0, 1]})
    # whole-grid graded test of scaled week, no regime
    g = d.dropna(subset=["sc7", "ex7"]).copy()
    g["q"] = pd.qcut(g["sc7"].rank(method="first"), 5, labels=False)
    out["all grid by scaled-week quintile"] = g.groupby("q")["ex7"].apply(ts).unstack()
    out["active by year, 60d sign"] = act.groupby(["year", "r60h"])["ex7"].mean().unstack()
    return out
