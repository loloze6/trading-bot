def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    out = {}
    H = []; M = []; TH = []
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            p = np.arange(0, len(c) - 48, 48)
            g.append(c[p + 48] / c[p] - 1)
        g = np.concatenate(g); drift, sd = np.nanmean(g), np.nanstd(g)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            H.append(pd.DataFrame({"hour": ts.dt.hour.values, "wd": ts.dt.weekday.values,
                                   "year": ts.dt.year.values, "r": r1, "coin": coin}))
            cts = ts + pd.Timedelta(hours=1)
            tsv = ts.values
            for i in np.where((cts.dt.hour == 0).values)[0]:
                if i - 48 < 0 or i + 96 >= len(c): continue
                if (tsv[i + 96] - tsv[i - 48]) != np.timedelta64(144, 'h'): continue
                d = int(cts.iloc[i].weekday())
                past = c[i] / c[i - 48] - 1
                row = dict(coin=coin, year=ts.iloc[i].year, d=d, past=past, pz=past / sd,
                           r0_24=c[i + 24] / c[i] - 1, r24_48=c[i + 48] / c[i + 24] - 1,
                           r48_96=c[i + 96] / c[i + 48] - 1,
                           flag=df["regime"].iloc[i] == "mean_reversion", fc=df["forecast"].iloc[i])
                if d == 0: M.append(row)
                if d == 4:
                    row["fu"] = (c[i + 48] / c[i] - 1 - drift) / sd
                    row["absprev"] = abs(c[i - 48] / c[max(i - 216, 0)] - 1) if i - 216 >= 0 else np.nan
                    TH.append(row)
    H = pd.concat(H)
    late = H[H.hour.isin([21, 22])]
    def tt(x): return pd.Series(dict(mean=x.mean(), t=x.mean() / x.std() * np.sqrt(x.count()), n=x.count()))
    out["h21_22_by_year"] = late.groupby("year")["r"].apply(tt).unstack()
    out["h21_22_by_wd"] = late.groupby("wd")["r"].apply(tt).unstack()
    out["h21_22_by_coin"] = late.groupby("coin")["r"].apply(tt).unstack()
    H["absprev"] = H.groupby("coin")["r"].shift(1).abs()
    out["h21_22_vs_other_hours_mean"] = pd.Series(dict(late=late["r"].mean(), other=H[~H.hour.isin([21, 22])]["r"].mean(),
        welch_t=stats.ttest_ind(late["r"].dropna(), H[~H.hour.isin([21, 22])]["r"].dropna(), equal_var=False).statistic))
    M = pd.DataFrame(M)
    mt = M[M.flag & (M.fc <= -2)]
    out["monday_cases_split"] = mt[["r0_24", "r24_48", "r48_96"]].apply(tt).T
    TH = pd.DataFrame(TH)
    TH["q"] = pd.qcut(TH["pz"], 5, labels=False)
    out["thu_close_quintiles"] = TH.groupby("q").agg(n=("fu", "size"), pz=("pz", "mean"), fu=("fu", "mean"),
                                                     r0_24=("r0_24", "mean"), r24_48=("r24_48", "mean"))
    def sl(s):
        r = stats.linregress(s["pz"], s["fu"]); return pd.Series(dict(n=len(s), slope=r.slope, t=r.slope / r.stderr))
    out["thu_slope_by_year"] = TH.groupby("year").apply(sl)
    T = []
    for coin, wins in trades.items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["fb"] = pd.cut(T["entry_forecast"], [-21, -6, -4, -2, -1, 0.01])
    T["db"] = pd.cut(T["duration_minutes"] / 60, [0, 47, 49, 100, 200, 1e5])
    out["trades_by_forecast"] = T.groupby("fb").agg(n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["trades_by_duration_h"] = T.groupby("db").agg(n=("profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"))
    et = pd.to_datetime(T["entry_time"], utc=True)
    out["trades_entry_weekday_hour"] = pd.crosstab(et.dt.weekday, et.dt.hour).iloc[:, :6] if et.dt.hour.nunique() > 1 else et.dt.weekday.value_counts()
    return out
