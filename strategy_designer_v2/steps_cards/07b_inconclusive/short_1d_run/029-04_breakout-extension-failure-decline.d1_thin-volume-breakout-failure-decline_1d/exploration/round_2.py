def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    def grid_ret(c, h):
        out = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                out.append(cl[i + h] / cl[i] - 1)
        return np.array(out)
    drift = {c: {h: grid_ret(c, h).mean() for h in (1, 3, 5, 10)} for c in bars}
    usual = {c: grid_ret(c, 5).std() for c in bars}
    rows = []
    allfail = []
    for c, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; hi = df["high"].values; vol = df["volume"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            thcol = "debug_info.components.thin_fail.last_history_value"
            thin = df[thcol] if thcol in df.columns else None
            n = len(df)
            r20 = pd.Series(cl).pct_change(20).values
            r60 = pd.Series(cl).pct_change(60).values
            seen = set()
            for i in range(1, n):
                if f[i] <= -2 and f[i - 1] > -0.5:
                    cell = i // H
                    if cell in seen: continue
                    seen.add(cell)
                    rec = dict(coin=c, win=w, year=ts[i].year, thin=(thin.iloc[i] if thin is not None else np.nan),
                               fc=f[i], r20=r20[i], r60=r60[i])
                    for h in (1, 3, 5, 10):
                        rec[f"u{h}"] = -(cl[i + h] / cl[i] - 1 - drift[c][h]) if i + h < n else np.nan
                    rows.append(rec)
            ph = pd.Series(hi).shift(1).rolling(20).max().values
            vr = vol / pd.Series(vol).shift(1).rolling(20).mean().values
            above = cl > ph
            seen2 = set()
            for i in range(25, n - 10):
                if above[i]: continue
                for k in range(1, 4):
                    j = i - k
                    if above[j]:
                        if cl[i] < ph[j] and not any(above[j+1:i+1]):
                            cell = i // H
                            if cell not in seen2:
                                seen2.add(cell)
                                allfail.append(dict(coin=c, vr=vr[j], year=ts[i].year, r60=r60[i],
                                    u5=-(cl[i+5]/cl[i]-1-drift[c][5]), u10=-(cl[i+10]/cl[i]-1-drift[c][10]),
                                    u3=-(cl[i+3]/cl[i]-1-drift[c][3])))
                        break
    d = pd.DataFrame(rows); a = pd.DataFrame(allfail)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "hit": (x > 0).mean()})
    res = {}
    res["cases_by_horizon"] = pd.DataFrame({h: summ(d, h) for h in ("u1", "u3", "u5", "u10")}).T
    res["by_coin"] = d.groupby("coin").apply(summ)
    res["by_year"] = d.groupby("year").apply(summ)
    d["thin_q"] = pd.qcut(d["thin"].rank(method="first"), 3, labels=["low", "mid", "high"])
    res["by_thin_tercile"] = d.groupby("thin_q").apply(summ)
    d["trend60"] = np.where(d["r60"] > 0, "up60", "down60")
    res["by_trend60"] = d.groupby("trend60").apply(summ)
    res["median_and_trim"] = pd.Series({"n": len(d), "median_u5": d["u5"].median(),
        "mean_without_top3": d["u5"].sort_values().iloc[:-3].mean(), "usual": np.mean(list(usual.values()))})
    res["allfail_horizon"] = pd.DataFrame({h: summ(a, h) for h in ("u3", "u5", "u10")}).T
    a["vq"] = pd.qcut(a["vr"].rank(method="first"), 4, labels=["q1thin", "q2", "q3", "q4heavy"])
    res["allfail_by_volq"] = a.groupby("vq").apply(summ)
    res["allfail_by_volq_u10"] = a.groupby("vq").apply(lambda g: summ(g, "u10"))
    a["thinflag"] = np.where(a["vr"] < 1, "thin", "heavy")
    res["allfail_thin_vs_heavy"] = a.groupby("thinflag").apply(summ)
    a["trend60"] = np.where(a["r60"] > 0, "up60", "down60")
    res["allfail_by_trend60"] = a.groupby("trend60").apply(summ)
    res["allfail_by_coin"] = a.groupby("coin").apply(summ)
    sp = stats.spearmanr(a["vr"], a["u5"], nan_policy="omit")
    res["allfail_spearman_vr_u5"] = pd.Series([sp[0], sp[1]], index=["rho", "p"])
    return res
