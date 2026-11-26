def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allgrid = {}
    for coin in bars:
        # coin mean 30-day return over grid of all windows, and for other horizons
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            comp = df.get("debug_info.components")
            for h in (10, 20, 30, 45):
                for i in range(0, n - h, h):
                    allgrid.setdefault((coin, h), []).append(c[i + h] / c[i] - 1)
            for i in range(0, n - 30, 30):
                r = {"coin": coin, "w": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                     "regime": df["regime"].iloc[i], "fc": df["forecast"].iloc[i],
                     "volu": df["volume"].iloc[i]}
                for h in (10, 20, 30, 45):
                    r["r%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                raw = np.nan
                if comp is not None:
                    v = comp.iloc[i]
                    try:
                        if isinstance(v, str):
                            import json, ast
                            try: v = json.loads(v)
                            except Exception: v = ast.literal_eval(v)
                        if isinstance(v, dict) and "vol_drop" in v:
                            raw = v["vol_drop"].get("last_history_value", np.nan)
                    except Exception:
                        pass
                r["raw"] = raw
                # 14d/90d volume ratio from bars if possible
                if i >= 89:
                    vv = df["volume"].values
                    r["vr"] = vv[i-13:i+1].mean() / vv[i-89:i+1].mean() - 1
                else:
                    r["vr"] = np.nan
                # 30-day past return
                r["past30"] = c[i] / c[i-30] - 1 if i >= 30 else np.nan
                rows.append(r)
    g = pd.DataFrame(rows)
    for h in (10, 20, 30, 45):
        mu = {k[0]: np.mean(v) for k, v in allgrid.items() if k[1] == h}
        g["x%d" % h] = g["r%d" % h] - g["coin"].map(mu)
    out = {}
    out["regime counts"] = g["regime"].value_counts()
    reg = g[g["regime"] == "mean_reversion"].copy()
    out["n regime, raw nonnull, vr nonnull"] = f"{len(reg)}, {reg['raw'].notna().sum()}, {reg['vr'].notna().sum()}"
    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std(ddof=1)/np.sqrt(len(s))) if len(s)>1 else np.nan})
    out["regime excess by horizon"] = pd.DataFrame({h: tt(reg["x%d" % h]) for h in (10, 20, 30, 45)})
    out["nonregime excess by horizon"] = pd.DataFrame({h: tt(g[g.regime!="mean_reversion"]["x%d" % h]) for h in (10, 20, 30, 45)})
    out["regime x30 by coin"] = reg.groupby("coin")["x30"].apply(tt).unstack()
    out["regime x30 by year"] = reg.groupby("year")["x30"].apply(tt).unstack()
    reg["fcb"] = pd.cut(reg["fc"], [-21, -2, -0.001, 0.001, 21], labels=["<=-2", "(-2,0)", "0", ">0"])
    out["regime x30 by forecast bin"] = reg.groupby("fcb")["x30"].apply(tt).unstack()
    for col in ("raw", "vr", "past30"):
        s = reg[[col, "x30"]].dropna()
        if len(s) > 5:
            lr = stats.linregress(s[col], s["x30"])
            out["slope x30 on " + col] = f"n={len(s)} slope={lr.slope:.4f} t={lr.slope/lr.stderr:.2f}"
            try:
                s["q"] = pd.qcut(s[col], 3, labels=["low", "mid", "high"])
                out["x30 by tercile " + col] = s.groupby("q")["x30"].apply(tt).unstack()
            except Exception:
                pass
    s = g[["vr", "x30"]].dropna()
    lr = stats.linregress(s["vr"], s["x30"])
    out["all bars: slope x30 on vr"] = f"n={len(s)} slope={lr.slope:.4f} t={lr.slope/lr.stderr:.2f}"
    out["comp sample type"] = str(type(bars["BTCUSD"]["w1"]["debug_info.components"].dropna().iloc[0]))[:60] if bars["BTCUSD"]["w1"]["debug_info.components"].notna().any() else "none"
    return out
