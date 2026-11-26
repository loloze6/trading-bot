def explore(data):
    import numpy as np, pandas as pd, json
    from scipy import stats
    bars = data["bars"]
    out = {}
    def comp_val(row_dc, key="vol_drop"):
        try:
            d = row_dc
            if isinstance(d, str):
                d = json.loads(d)
            if isinstance(d, dict) and key in d:
                v = d[key]
                if isinstance(v, dict):
                    return v.get("last_history_value", np.nan)
        except Exception:
            pass
        return np.nan
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in [10, 20, 30, 45]:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            col = "debug_info.components.vol_drop.last_history_value"
            if col in df.columns:
                vr = df[col].astype(float).values
            elif "debug_info.components" in df.columns:
                vr = df["debug_info.components"].apply(comp_val).astype(float).values
            else:
                vr = np.full(len(df), np.nan)
            v = df["volume"].astype(float)
            vr2 = (v.rolling(14).mean() / v.rolling(90, min_periods=45).mean() - 1).values
            c = df["close"].values
            reg = df["regime"].astype(str).values
            fc = df["forecast"].astype(float).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [10, 20, 30, 45]:
                for i in range(0, len(c) - h, h):
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], inreg=reg[i] == "mean_reversion",
                                     fc=fc[i], vr=vr[i], vr2=vr2[i],
                                     ex=r - drift[(coin, h)], tot=r, st=(r - drift[(coin, h)]) / usual[(coin, h)]))
    R = pd.DataFrame(rows)
    out["cols_sample"] = ", ".join([c for c in bars["BTCUSD"]["w7"].columns if "debug" in c][:15])
    def summ(g):
        n = len(g)
        m = g["ex"].mean()
        t = m / (g["ex"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, mean_ex=m, t=t, mean_tot=g["tot"].mean(), strength=g["st"].mean()))
    out["by_h_inregime"] = R.groupby(["h", "inreg"]).apply(summ)
    r30 = R[(R.h == 30) & R.inreg]
    out["reg30_by_coin"] = r30.groupby("coin").apply(summ)
    out["reg30_by_window"] = r30.groupby("w").apply(summ)
    out["reg30_by_year"] = r30.groupby("year").apply(summ)
    # volume relation
    res = {}
    for h in [10, 20, 30, 45]:
        g = R[(R.h == h) & R.inreg]
        for vc in ["vr", "vr2"]:
            gg = g.dropna(subset=[vc])
            if len(gg) > 5:
                s = stats.linregress(gg[vc], gg["ex"])
                res[(h, vc)] = dict(n=len(gg), slope=s.slope, t=s.slope / s.stderr, corr=s.rvalue)
            gg2 = gg.copy()
            if len(gg2) > 5:
                gg2["drop"] = gg2[vc] < 0
                a = gg2[gg2["drop"]]["ex"]; b = gg2[~gg2["drop"]]["ex"]
                res[(h, vc + "_drop_minus_nodrop")] = dict(n=len(a), slope=a.mean() - b.mean(),
                    t=stats.ttest_ind(a, b, equal_var=False).statistic if len(a) > 1 and len(b) > 1 else np.nan, corr=len(b))
    out["vol_relation"] = pd.DataFrame(res).T
    # quantiles of vr2 within regime 30
    g = r30.dropna(subset=["vr2"]).copy()
    if len(g) > 8:
        g["q"] = pd.qcut(g["vr2"], 3, labels=False, duplicates="drop")
        out["reg30_by_vr2_tercile"] = g.groupby("q").apply(summ)
    # all bars (not regime): volume drop relation h=30
    g = R[(R.h == 30)].dropna(subset=["vr2"])
    s = stats.linregress(g["vr2"], g["ex"])
    out["all30_vr2_slope_t"] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    return out
