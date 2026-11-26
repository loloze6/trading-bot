def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [3, 7, 14, 21]
    rows = []
    drift = {}
    usual = {}
    # coin normal drift per horizon, non-overlapping grid over all visible windows
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = np.mean(rs) if rs else np.nan
            usual[(coin, h)] = np.std(rs, ddof=1) if len(rs) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r7 = c / c.shift(7) - 1
            base = r7.abs().rolling(30, min_periods=30).mean()
            sr = r7 / base
            tr60 = c / c.shift(60) - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            act = (df["regime"] == "trending").values
            fc = df["forecast"].fillna(0).values
            for i in range(n):
                g = i // 14
                rec = dict(coin=coin, w=w, i=i, cell=g, year=ts.iloc[i].year,
                           day=ts.iloc[i].normalize(), active=act[i], fc=fc[i],
                           sr=sr.iloc[i], tr60=tr60.iloc[i])
                for h in H:
                    if i + h < n:
                        ret = c.iloc[i + h] / c.iloc[i] - 1
                        rec[f"u{h}"] = ret - drift[(coin, h)]
                        rec[f"z{h}"] = (ret - drift[(coin, h)]) / usual[(coin, h)]
                    else:
                        rec[f"u{h}"] = np.nan
                        rec[f"z{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)

    def clus_t(x, col):
        x = x.dropna(subset=[col])
        if len(x) < 3:
            return (len(x), np.nan, np.nan, 0)
        m = x[col].mean()
        dev = (x[col] - m).groupby(x["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(x)
        return (len(x), m, m / se if se > 0 else np.nan, x["day"].nunique())

    # cases: first active bar per 14-bar grid cell
    cases = d[d["active"]].groupby(["coin", "w", "cell"]).head(1)
    out = {}
    hz = []
    for h in H:
        n, m, t, nd = clus_t(cases, f"u{h}")
        hz.append(dict(h=h, n=n, mean=m, t=t, days=nd,
                       strength=cases[f"z{h}"].mean()))
    out["cases_by_horizon"] = pd.DataFrame(hz)

    def grp(df, key, col="u14"):
        res = []
        for k, x in df.groupby(key):
            n, m, t, nd = clus_t(x, col)
            res.append(dict(key=k, n=n, mean=m, t=t, days=nd))
        return pd.DataFrame(res)

    out["cases_by_coin"] = grp(cases, "coin")
    out["cases_by_year"] = grp(cases, "year")
    out["cases_by_window"] = grp(cases, "w")
    cs = cases.dropna(subset=["sr"]).copy()
    cs["srbin"] = pd.cut(cs["sr"], [1, 1.5, 2, 2.5, 100], include_lowest=True).astype(str)
    out["cases_by_scaled_rise"] = grp(cs, "srbin")
    cs["fcbin"] = pd.qcut(cs["fc"], 3, duplicates="drop").astype(str)
    out["cases_by_forecast_tercile"] = grp(cs, "fcbin")
    cs["trbin"] = pd.cut(cs["tr60"], [-1, -0.05, 0, 0.05, 1]).astype(str)
    out["cases_by_tr60"] = grp(cs, "trbin")
    # unconditional: all bars on 14-grid start, by scaled rise bin (no profile), several horizons
    allg = d[(d["i"] % 14 == 0)].dropna(subset=["sr"]).copy()
    allg["srbin"] = pd.cut(allg["sr"], [-100, -1, 0, 1, 2, 100]).astype(str)
    for h in [7, 14]:
        out[f"all_bars_srbin_u{h}"] = grp(allg, "srbin", f"u{h}")
    return out
