def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]; days = data["days"]
    rows = []; hrs = []
    for coin, wins in bars.items():
        # normal drift and usual move, 48h grid
        g = []
        for w, df in wins.items():
            c = df["close"].values
            p = np.arange(0, len(c) - 48, 48)
            g.append(c[p + 48] / c[p] - 1)
        g = np.concatenate(g) if g else np.array([])
        drift, sd = np.nanmean(g), np.nanstd(g)
        for w, df in wins.items():
            ts = pd.to_datetime(df["timestamp"], utc=True)
            cts = ts + pd.Timedelta(hours=1)
            c = df["close"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            hrs.append(pd.DataFrame({"hour": ts.dt.hour.values, "wd": ts.dt.weekday.values, "r": r1, "coin": coin}))
            tsv = ts.values
            mask = (cts.dt.hour == 0).values
            idx = np.where(mask)[0]
            for i in idx:
                if i - 48 < 0 or i + 48 >= len(c):
                    continue
                if (tsv[i] - tsv[i - 48]) != np.timedelta64(48, 'h') or (tsv[i + 48] - tsv[i]) != np.timedelta64(48, 'h'):
                    continue
                past = c[i] / c[i - 48] - 1
                fwd = c[i + 48] / c[i] - 1
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, d=int(cts.iloc[i].weekday()),
                                 past=past, pz=past / sd, fu=(fwd - drift) / sd, fuu=fwd - drift, fwd=fwd,
                                 flag=df["regime"].iloc[i] == "mean_reversion", fc=df["forecast"].iloc[i]))
    R = pd.DataFrame(rows)
    out = {}
    def summ(s):
        if len(s) < 10:
            return pd.Series(dict(n=len(s)))
        sl = stats.linregress(s["pz"], s["fu"])
        up = s[s.past > 0]["fuu"]; dn = s[s.past < 0]["fuu"]
        return pd.Series(dict(n=len(s), corr=sl.rvalue, slope=sl.slope, t_slope=sl.slope / sl.stderr,
                              fu_after_up=up.mean(), t_up=up.mean() / up.std() * np.sqrt(len(up)),
                              fu_after_dn=dn.mean(), t_dn=dn.mean() / dn.std() * np.sqrt(len(dn))))
    out["by_start_weekday"] = R.groupby("d").apply(summ)
    out["monday_by_volflag"] = R[R.d == 0].groupby("flag").apply(summ)
    out["weekday_by_volflag_tue_to_sun"] = R[R.d != 0].assign(f=R.flag).groupby("f").apply(summ)
    m = R[(R.d == 0)].copy()
    m["q"] = pd.qcut(m["pz"], 5, labels=False)
    out["monday_quintiles"] = m.groupby(["flag", "q"]).agg(n=("fuu", "size"), pz=("pz", "mean"), fuu=("fuu", "mean"), fwd=("fwd", "mean"))
    out["monday_cases_by_year"] = R[(R.d == 0) & (R.fc <= -2)].groupby("year")["fuu"].agg(["size", "mean", "std"])
    out["regime_counts_on_close00"] = R.groupby(["d", "flag"]).size().unstack()
    H = pd.concat(hrs)
    hh = H.groupby("hour")["r"].agg(["mean", "std", "size"]); hh["t"] = hh["mean"] / hh["std"] * np.sqrt(hh["size"])
    out["hour_ret"] = hh[["mean", "t", "size"]]
    ww = H.groupby("wd")["r"].agg(["mean", "std", "size"]); ww["t"] = ww["mean"] / ww["std"] * np.sqrt(ww["size"])
    out["weekday_ret"] = ww[["mean", "t", "size"]]
    T = []
    for coin, wins in trades.items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"),
                                          net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
