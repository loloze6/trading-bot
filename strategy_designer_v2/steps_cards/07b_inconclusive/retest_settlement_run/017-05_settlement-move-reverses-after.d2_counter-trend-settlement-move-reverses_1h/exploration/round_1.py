def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        g8 = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 8, 8)
            g8.extend(list(c[idx + 8] / c[idx] - 1))
        drift[coin] = np.mean(g8); usual[coin] = np.std(g8)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"]
            closeh = (ts + pd.Timedelta(hours=1)).dt.hour
            pre = c / c.shift(2) - 1
            tr = c / c.shift(24) - 1
            out = {}
            for h in [1, 2, 4, 8, 16]:
                out[h] = c.shift(-h) / c - 1
            d = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "hr": closeh,
                              "pre": pre, "tr": tr, "fc": df["forecast"],
                              **{f"f{h}": out[h] for h in out}})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["pre", "tr", "f8"])
    D["drift"] = D["coin"].map(drift); D["usual"] = D["coin"].map(usual)
    opp = ((D.pre < 0) & (D.tr > 0)) | ((D.pre > 0) & (D.tr < 0))
    D["sgn"] = np.sign(D.tr)
    D["ex8"] = (D.f8 - D.drift) * D.sgn
    def tstat(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    S = D[opp]
    # by clock hour (settlement 0,8,16 vs placebo)
    byhr = S.groupby("hr")["ex8"].apply(tstat).unstack()
    sett = S[S.hr.isin([0, 8, 16])].copy()
    sett["side"] = np.where(sett.sgn > 0, "long_dip_in_up", "short_rally_in_down")
    res = {"by_close_hour_all_opp_cases": byhr}
    res["by_side"] = sett.groupby("side")["ex8"].apply(tstat).unstack()
    res["by_coin"] = sett.groupby("coin")["ex8"].apply(tstat).unstack()
    res["by_year"] = sett.groupby("year")["ex8"].apply(tstat).unstack()
    sett["trq"] = pd.qcut(sett.tr.abs(), 5, labels=False)
    res["by_abs_trend_quintile"] = sett.groupby("trq")["ex8"].apply(tstat).unstack()
    sett["preq"] = pd.qcut(sett.pre.abs(), 5, labels=False)
    res["by_abs_pre_quintile"] = sett.groupby("preq")["ex8"].apply(tstat).unstack()
    # reversal of pre-move signed by -sign(pre), other horizons
    hz = {}
    for h in [1, 2, 4, 8, 16]:
        hz[h] = tstat((sett[f"f{h}"]) * sett.sgn)
    res["settlement_horizons_trend_signed_raw"] = pd.DataFrame(hz).T
    # all settlement bars: forward signed against pre-move regardless of trend
    A = D[D.hr.isin([0, 8, 16])].copy()
    A["rev8"] = -(A.f8 - A.drift) * np.sign(A.pre)
    A["agree"] = np.where(opp.loc[A.index], "pre_against_trend", "pre_with_trend")
    res["all_settlement_reversal_of_pre_by_agree"] = A.groupby("agree")["rev8"].apply(tstat).unstack()
    A["mom8"] = (A.f8 - A.drift) * np.sign(A.tr)
    res["all_settlement_trend_follow_8h_by_agree"] = A.groupby("agree")["mom8"].apply(tstat).unstack()
    res["by_settlement_hour"] = sett.groupby("hr")["ex8"].apply(tstat).unstack()
    return res
