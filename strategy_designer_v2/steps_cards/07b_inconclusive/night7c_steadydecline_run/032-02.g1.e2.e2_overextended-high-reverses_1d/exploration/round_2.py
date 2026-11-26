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
            pp = df.get("debug_info.components.runup.post_pipeline_value")
            lh = df.get("debug_info.components.runup.last_history_value")
            n = len(df)
            for i in range(0, n, 5):
                if not at_high.iloc[i]:
                    continue
                rec = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                           strength=abs(pp.iloc[i]) if pp is not None and pd.notna(pp.iloc[i]) else 0.0,
                           raw=lh.iloc[i] if lh is not None else np.nan,
                           fc=df["forecast"].iloc[i])
                for h in (5, 10, 20):
                    if i + h < n:
                        d, s = allret[(coin, h)]
                        rec[f"x{h}"] = c.iloc[i+h]/c.iloc[i]-1 - d
                rows.append(rec)
    R = pd.DataFrame(rows)
    out = {}
    def slope(df, y, x):
        d = df[[y, x]].dropna()
        if len(d) < 8: return pd.Series({"n": len(d), "slope": np.nan, "t": np.nan})
        r = stats.linregress(d[x], d[y])
        return pd.Series({"n": len(d), "slope": r.slope, "t": r.slope/r.stderr})
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    out["slope raw by coin x5/x20"] = pd.concat({y: pd.DataFrame({k: slope(g, y, "raw") for k, g in R.groupby("coin")}).T for y in ("x5","x20")}, axis=1)
    out["slope raw by year x5/x20"] = pd.concat({y: pd.DataFrame({k: slope(g, y, "raw") for k, g in R.groupby("year")}).T for y in ("x5","x20")}, axis=1)
    out["strength vs raw corr, spearman"] = float(R[["strength","raw"]].corr(method="spearman").iloc[0,1])
    out["strength quantiles"] = R["strength"].describe()
    out["share strength>=19.9"] = float((R["strength"] >= 19.9).mean())
    R["rb"] = pd.cut(R["raw"], [-10, 1, 2, 2.5, 3, 100])
    out["by raw band x5,x10,x20"] = pd.concat({y: R.groupby("rb")[y].apply(tt).unstack() for y in ("x5","x10","x20")}, axis=1)
    top = R[R["raw"] >= R["raw"].quantile(0.75)]
    out["top quartile x5 by coin"] = top.groupby("coin")["x5"].apply(tt).unstack()
    out["top quartile x5 by year"] = top.groupby("year")["x5"].apply(tt).unstack()
    out["slope raw, raw>=median, x5/x10/x20"] = pd.DataFrame({y: slope(R[R["raw"] >= R["raw"].median()], y, "raw") for y in ("x5","x10","x20")}).T
    out["slope raw, raw<median, x5/x20"] = pd.DataFrame({y: slope(R[R["raw"] < R["raw"].median()], y, "raw") for y in ("x5","x20")}).T
    return out
