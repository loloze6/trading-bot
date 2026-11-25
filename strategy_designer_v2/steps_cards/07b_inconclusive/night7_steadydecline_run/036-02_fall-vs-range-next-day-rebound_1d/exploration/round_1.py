def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    allret = {h: [] for h in (1, 2, 3, 5)}
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); h_ = df["high"].astype(float); l_ = df["low"].astype(float)
            rng = (h_ - l_).rolling(30).mean().shift(1)
            fall = (c.shift(1) - c).clip(lower=0)
            ratio = fall / rng
            r1 = c.pct_change()
            tr60 = c / c.shift(60) - 1
            sd30 = r1.rolling(30).std()
            med = sd30.rolling(365, min_periods=120).median()
            agit = sd30 > med
            ret5 = c / c.shift(5) - 1
            n = len(df)
            for hh in (1, 2, 3, 5):
                fr = c.shift(-hh) / c - 1
                allret[hh] += list(zip([coin]*n, fr.values, [i % hh == 0 for i in range(n)]))
            for i in range(n):
                if ratio.iloc[i] >= 1 and not np.isnan(ratio.iloc[i]):
                    d = dict(coin=coin, w=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                             ratio=ratio.iloc[i], fallpct=-r1.iloc[i], tr=tr60.iloc[i], ag=agit.iloc[i],
                             ret5=ret5.iloc[i], day=pd.Timestamp(df["timestamp"].iloc[i]).floor("D"),
                             wd=pd.Timestamp(df["timestamp"].iloc[i]).weekday())
                    for hh in (1, 2, 3, 5):
                        d[f"f{hh}"] = c.iloc[i+hh]/c.iloc[i]-1 if i+hh < n else np.nan
                    rows.append(d)
    cs = pd.DataFrame(rows)
    drift = {}
    for hh in (1, 2, 3, 5):
        a = pd.DataFrame(allret[hh], columns=["coin", "r", "g"]).dropna()
        a = a[a.g]
        drift[hh] = a.groupby("coin")["r"].mean()
    for hh in (1, 2, 3, 5):
        cs[f"x{hh}"] = cs[f"f{hh}"] - cs["coin"].map(drift[hh])
    def summ(g, col="x1"):
        s = g.dropna(subset=[col])
        ds = s.groupby("day")[col].sum()
        t = ds.mean()/(ds.std()/np.sqrt(len(ds))) if len(ds) > 2 else np.nan
        return pd.Series(dict(n=len(s), days=len(ds), mean=s[col].mean(), t_day=t,
                              rho=stats.spearmanr(s["ratio"], s[col])[0] if len(s) > 5 else np.nan))
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(cs, f"x{h}") for h in (1, 2, 3, 5)}).T
    out["by_coin"] = cs.groupby("coin").apply(summ)
    out["by_year"] = cs.groupby("year").apply(summ)
    out["by_window"] = cs.groupby("w").apply(summ)
    cs["rq"] = pd.qcut(cs["ratio"], 4, labels=["q1", "q2", "q3", "q4"])
    out["by_ratio_q"] = cs.groupby("rq").apply(summ)
    cs["trend"] = np.where(cs.tr > 0.10, "rising", np.where(cs.tr < -0.10, "falling", "choppy"))
    cs.loc[cs.tr.isna(), "trend"] = "na"
    cs["agl"] = np.where(cs.ag, "agitated", "calm")
    out["by_trend"] = cs.groupby("trend").apply(summ)
    out["by_agit"] = cs.groupby("agl").apply(summ)
    out["by_profile"] = cs.groupby(["trend", "agl"]).apply(summ)
    cs["r5q"] = pd.qcut(cs["ret5"], 3, labels=["deep5", "mid5", "up5"])
    out["by_prior5d"] = cs.groupby("r5q").apply(summ)
    out["by_rq_h3"] = cs.groupby("rq").apply(lambda g: summ(g, "x3"))
    out["by_trend_h3"] = cs.groupby("trend").apply(lambda g: summ(g, "x3"))
    out["median_x1_and_winshare"] = pd.Series(dict(med=cs.x1.median(), pos=(cs.x1 > 0).mean()))
    return out
