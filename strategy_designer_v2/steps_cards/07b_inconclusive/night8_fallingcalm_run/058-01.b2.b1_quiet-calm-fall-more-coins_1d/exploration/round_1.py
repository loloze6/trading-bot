def explore(data):
    import numpy as np, pandas as pd, json
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            v = df["volume"].values.astype(float)
            ret30 = pd.Series(c).pct_change(30).values
            vol30 = pd.Series(v).rolling(30).mean().values
            raw = [np.nan]*n
            if "debug_info.components" in df.columns:
                for i, x in enumerate(df["debug_info.components"].values):
                    try:
                        d = x if isinstance(x, dict) else json.loads(x)
                        raw[i] = float(d["quiet_vol"]["last_history_value"])
                    except Exception:
                        pass
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4],
                                     ret=c[i+h]/c[i]-1, fc=float(df["forecast"].iloc[i]),
                                     reg=df["regime"].iloc[i], r30=ret30[i], raw=raw[i]))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["adj"] = R["ret"] - R["drift"]
    out = {}
    def slope_t(s, x="fc"):
        s = s.dropna(subset=[x, "adj"])
        if len(s) < 15 or s[x].std() == 0:
            return (len(s), np.nan, np.nan)
        X = s[x] - s[x].mean(); y = s["adj"] - s["adj"].mean()
        b = (X*y).sum()/(X*X).sum()
        e = y - b*X
        g = pd.DataFrame({"d": s["day"].values, "u": (X*e).values}).groupby("d")["u"].sum()
        se = np.sqrt((g**2).sum())/(X*X).sum()
        return (len(s), b, b/se)
    T = R[R.reg == "trending"]
    # horizons
    hz = []
    for h in [1, 3, 5, 10, 20]:
        s = T[T.h == h]
        n, b, t = slope_t(s)
        n2, b2, t2 = slope_t(s, "r30")
        neg = s[s.fc < 0]["adj"]; zer = s[s.fc == 0]["adj"]
        hz.append(dict(h=h, n=n, slope_fc=b, t_fc=t, slope_r30=b2, t_r30=t2,
                       mean_neg=neg.mean(), n_neg=len(neg), mean_zero=zer.mean(), n_zero=len(zer),
                       mean_all=s["adj"].mean(), mean_tot=s["ret"].mean()))
    out["by_horizon_inregime"] = pd.DataFrame(hz)
    s5 = T[T.h == 5].copy()
    out["coin_5d"] = pd.DataFrame([dict(coin=k, n=slope_t(g)[0], slope=slope_t(g)[1], t=slope_t(g)[2],
                                        mean_adj=g.adj.mean(), mean_tot=g.ret.mean()) for k, g in s5.groupby("coin")])
    out["year_5d"] = pd.DataFrame([dict(year=k, n=slope_t(g)[0], slope=slope_t(g)[1], t=slope_t(g)[2],
                                        mean_adj=g.adj.mean(), mean_tot=g.ret.mean()) for k, g in s5.groupby("year")])
    s5["fcq"] = pd.qcut(s5["fc"].rank(method="first"), 4, labels=["most_quiet", "q2", "q3", "least"])
    out["fc_quartile_5d"] = s5.groupby("fcq").agg(n=("adj", "size"), fc=("fc", "mean"), raw=("raw", "mean"),
                                                   adj=("adj", "mean"), tot=("ret", "mean"),
                                                   t=("adj", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))))
    s5r = s5.dropna(subset=["r30"]).copy()
    s5r["depth"] = pd.qcut(s5r["r30"], 3, labels=["deep", "mid", "shallow"])
    s5r["quiet"] = np.where(s5r.fc < s5r.fc.median(), "quieter", "louder")
    out["depth_x_quiet_5d"] = s5r.groupby(["depth", "quiet"]).agg(n=("adj", "size"), r30=("r30", "mean"),
                                                                   adj=("adj", "mean"), tot=("ret", "mean"))
    # raw volume ratio slope (graded both sides)
    out["raw_slope_by_h"] = pd.DataFrame([dict(h=h, **dict(zip(["n", "slope", "t"], slope_t(T[T.h == h], "raw"))))
                                          for h in [1, 3, 5, 10, 20]])
    # outside regime, ret30<0, for comparison: r30 slope at 5d
    O = R[(R.reg != "trending") & (R.h == 5) & (R.r30 < 0)]
    out["outside_r30_slope_5d"] = pd.Series(dict(zip(["n", "slope", "t"], slope_t(O, "r30"))))
    out["regimes"] = R[R.h == 5]["reg"].value_counts()
    return out
