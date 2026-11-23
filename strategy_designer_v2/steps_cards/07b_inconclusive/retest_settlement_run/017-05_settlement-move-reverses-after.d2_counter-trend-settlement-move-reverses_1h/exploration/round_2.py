def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        dr = {}
        for h in [2, 4, 8]:
            g = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                g.extend(list(c[idx + h] / c[idx] - 1))
            dr[h] = (np.mean(g), np.std(g))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"]
            d = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year,
                              "hr": (ts + pd.Timedelta(hours=1)).dt.hour,
                              "pre": c / c.shift(2) - 1, "tr": c / c.shift(24) - 1})
            for h in [2, 4, 8]:
                d[f"x{h}"] = (c.shift(-h) / c - 1 - dr[h][0])
                d[f"s{h}"] = d[f"x{h}"] / dr[h][1]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True).dropna(subset=["pre", "tr", "x8"])
    D["sgn"] = np.sign(D.tr)
    opp = ((D.pre < 0) & (D.tr > 0)) | ((D.pre > 0) & (D.tr < 0))
    S = D[opp].copy()
    for h in [2, 4, 8]:
        S[f"e{h}"] = S[f"x{h}"] * S.sgn
        S[f"z{h}"] = S[f"s{h}"] * S.sgn
    def ts_(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    res = {}
    res["e2_by_close_hour"] = S.groupby("hr")["e2"].apply(ts_).unstack()
    S["sett"] = np.where(S.hr.isin([0, 8, 16]), "settlement", "other")
    res["e2_e4_strength_sett_vs_other"] = S.groupby("sett")[["e2", "e4", "z2", "z4", "z8"]].mean()
    st = S[S.sett == "settlement"].copy()
    res["e2_settlement_by_year"] = st.groupby("year")["e2"].apply(ts_).unstack()
    res["e2_settlement_by_coin"] = st.groupby("coin")["e2"].apply(ts_).unstack()
    st["trq"] = pd.qcut(st.tr.abs(), 5, labels=False)
    res["e2_settlement_by_trend_quintile"] = st.groupby("trq")["e2"].apply(ts_).unstack()
    res["e2_settlement_by_hour"] = st.groupby("hr")["e2"].apply(ts_).unstack()
    x = st.tr.abs(); y = st.e2
    res["slope_e2_on_abs_trend"] = float(np.polyfit(x, y, 1)[0])
    return res
