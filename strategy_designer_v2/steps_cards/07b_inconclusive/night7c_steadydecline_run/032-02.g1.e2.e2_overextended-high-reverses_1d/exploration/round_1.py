def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {}
    for coin, wins in bars.items():
        for h in (5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i+h]/c[i]-1)
            allret[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            mx = c.rolling(28, min_periods=28).max()
            at_high = (c >= mx) & mx.notna()
            at_high = at_high | (mx.isna() & (df["regime"] == "trending"))
            r28 = c / c.shift(28) - 1
            pp = df.get("debug_info.components.runup.post_pipeline_value")
            lh = df.get("debug_info.components.runup.last_history_value")
            n = len(df)
            for i in range(0, n, 5):
                if not at_high.iloc[i]:
                    continue
                rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                           strength=abs(pp.iloc[i]) if pp is not None and pd.notna(pp.iloc[i]) else 0.0,
                           raw=lh.iloc[i] if lh is not None else np.nan, r28=r28.iloc[i])
                for h in (5, 10, 20):
                    if i + h < n:
                        d, s = allret[(coin, h)]
                        rec[f"x{h}"] = c.iloc[i+h]/c.iloc[i]-1 - d
                        rec[f"z{h}"] = rec[f"x{h}"]/s
                rows.append(rec)
    R = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["excess by horizon (positive = rise beyond drift)"] = pd.DataFrame({h: tt(R[f"x{h}"]) for h in (5,10,20)}).T
    def slope(df, y, x):
        d = df[[y, x]].dropna()
        if len(d) < 10: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        r = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr})
    out["slopes"] = pd.DataFrame({f"{y}~{x}": slope(R, y, x) for y in ("x5","x10","x20") for x in ("strength","raw","r28")}).T
    R["sbin"] = pd.qcut(R["raw"].rank(method="first"), 4, labels=["q1","q2","q3","q4"]) if R["raw"].notna().sum() > 20 else np.nan
    out["x5 by raw quartile"] = R.groupby("sbin")["x5"].apply(tt).unstack()
    out["x20 by raw quartile"] = R.groupby("sbin")["x20"].apply(tt).unstack()
    out["raw quartile means"] = R.groupby("sbin")[["raw","strength","r28"]].mean()
    out["x5 by coin"] = R.groupby("coin")["x5"].apply(tt).unstack()
    out["x5 by window"] = R.groupby("w")["x5"].apply(tt).unstack()
    out["x5 by year"] = R.groupby("year")["x5"].apply(tt).unstack()
    out["share strength zero"] = float((R["strength"] == 0).mean())
    out["slope x5~strength by year"] = pd.DataFrame({y: slope(g, "x5", "strength") for y, g in R.groupby("year")}).T
    return out
