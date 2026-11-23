def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = [12, 24, 48, 72, 96]
    rows = []
    drift = {}
    usual = {}
    for c in bars:
        for h in H:
            g = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                g.append(cl[idx + h] / cl[idx] - 1)
            g = np.concatenate(g)
            drift[(c, h)] = g.mean(); usual[(c, h)] = g.std()
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            cl = df["close"].values
            r24 = pd.Series(cl).pct_change(24).values
            r720 = pd.Series(cl).pct_change(720).values
            r168 = pd.Series(cl).pct_change(168).values
            hv = pd.Series(cl).pct_change().rolling(720).std().values
            hv_med = pd.Series(hv).rolling(4320, min_periods=720).median().values
            sel = np.where((ts.dt.weekday == 6) & (ts.dt.hour == 23) & (df["forecast"].fillna(0) != 0))[0]
            for i in sel:
                d = {"coin": c, "w": w, "year": ts[i].year, "f": df["forecast"].iloc[i],
                     "r24": r24[i], "r720": r720[i], "r168": r168[i], "hv": hv[i], "hvrel": hv[i] / hv_med[i] if hv_med[i] == hv_med[i] else np.nan,
                     "alloc": df["postRebalance_current_allocation"].iloc[i]}
                for h in H:
                    if i + h < len(cl):
                        tot = cl[i + h] / cl[i] - 1
                        s = np.sign(d["f"])
                        d[f"tot{h}"] = s * tot
                        d[f"unu{h}"] = s * (tot - drift[(c, h)])
                    else:
                        d[f"tot{h}"] = np.nan; d[f"unu{h}"] = np.nan
                rows.append(d)
    cs = pd.DataFrame(rows)
    cs["side"] = np.where(cs["f"] > 0, "long", "short")
    cs["absf"] = cs["f"].abs()
    def summ(g):
        out = {"n": len(g)}
        for h in H:
            x = g[f"tot{h}"].dropna()
            out[f"tot{h}%"] = 100 * x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(out)
    res = {}
    res["all"] = summ(cs).to_frame().T
    res["by_side"] = cs.groupby("side").apply(summ)
    cs["fq"] = pd.qcut(cs["absf"], 5, labels=False)
    res["by_absf_quintile"] = cs.groupby("fq").apply(summ)
    cs["r24q"] = pd.qcut(cs["r24"].abs(), 5, labels=False)
    res["by_abs_sunday_ret_quintile"] = cs.groupby("r24q").apply(summ)
    cs["hvq"] = pd.qcut(cs["hvrel"], 3, labels=False)
    res["by_rel_vol_tercile"] = cs.groupby("hvq").apply(summ)
    # trend alignment: is the bet with or against 30-day trend
    cs["with_trend720"] = np.sign(cs["f"]) == np.sign(cs["r720"])
    res["by_with_30d_trend"] = cs.groupby("with_trend720").apply(summ)
    cs["with_trend168"] = np.sign(cs["f"]) == np.sign(cs["r168"])
    res["by_with_7d_trend"] = cs.groupby("with_trend168").apply(summ)
    res["by_coin"] = cs.groupby("coin").apply(summ)
    res["by_year"] = cs.groupby("year").apply(summ)
    # book daily
    bd = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["w"] = w; x["coin"] = c
            bd.append(x)
    bd = pd.concat(bd)
    port = bd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    port["wn"] = port["w"].str[1:].astype(int)
    port = port.sort_values(["wn", "day"]).dropna()
    v = (1 + port["book_return"]).cumprod().values
    dd = v / np.maximum.accumulate(v) - 1
    port["dd"] = dd
    imin = int(np.argmin(dd)); peak = int(np.argmax(v[:imin + 1]))
    res["deepest_fall"] = pd.Series({"dd%": 100 * dd[imin], "days_long": imin - peak, "start_w": port["w"].iloc[peak], "end_w": port["w"].iloc[imin],
                                     "coin_ret_during%": 100 * ((1 + port["coin_return"].iloc[peak:imin + 1]).prod() - 1)}).to_frame()
    res["book_by_window"] = port.groupby("wn").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), mindd=("dd", "min"))
    res["sunday_ret_vs_cap"] = pd.Series({"corr_absf_absr24": cs[["absf"]].assign(a=cs["r24"].abs()).corr().iloc[0, 1],
                                          "mean_alloc_abs": cs["alloc"].abs().mean()}).to_frame()
    return res
