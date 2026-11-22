import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    hr_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(720, min_periods=300).std().values
            n = len(c)
            hr_rows.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values,
                                         "wd": ts.dt.weekday.values, "r": r1.values}))
            idx = np.where(ts.dt.hour.values == 23)[0]
            for i in idx:
                if i - 168 < 0 or i + 48 >= n or np.isnan(vol[i]):
                    continue
                if (ts.iloc[i + 48] - ts.iloc[i - 168]) != pd.Timedelta(hours=216):
                    continue
                s = vol[i] * np.sqrt(48)
                past48 = c[i] / c[i - 48] - 1
                prior120 = c[i - 48] / c[i - 168] - 1
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 past48=past48, past48z=past48 / s,
                                 prior120z=prior120 / (vol[i] * np.sqrt(120)),
                                 f24=c[i + 24] / c[i] - 1, f48=c[i + 48] / c[i] - 1, s=s))
    ev = pd.DataFrame(rows)
    drift = ev.groupby("coin")["f48"].mean()
    ev["f48x"] = ev["f48"] - ev["coin"].map(drift)
    ev["f48z"] = ev["f48"] / ev["s"]
    tfun = lambda x: x.mean() / (x.std() / np.sqrt(len(x)))

    res = []
    for wd, g in ev.groupby("wd"):
        sl = stats.linregress(g["past48z"], g["f48z"])
        res.append(dict(anchor_wd=wd, n=len(g), slope=sl.slope, t=sl.slope / sl.stderr, corr=sl.rvalue))
    out["fwd48z_on_past48z_by_anchor_weekday(6=Sun)"] = pd.DataFrame(res)

    su = ev[ev.wd == 6].copy()
    su["q"] = pd.qcut(su["past48z"], 5, labels=False)
    out["sunday_weekend_quintiles"] = su.groupby("q").agg(
        n=("f48x", "size"), wk_z=("past48z", "mean"), f48x_mean=("f48x", "mean"),
        f48x_t=("f48x", tfun), f24_mean=("f24", "mean"))
    su["wk_sign"] = np.sign(su["past48"]); su["pr_sign"] = np.sign(su["prior120z"])
    out["sunday_wk_x_prior"] = su.groupby(["wk_sign", "pr_sign"]).agg(
        n=("f48x", "size"), f48x=("f48x", "mean"), t=("f48x", tfun))

    res = []
    for k, gg in su.groupby("coin"):
        sl = stats.linregress(gg["past48z"], gg["f48z"])
        res.append(dict(coin=k, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr))
    out["sunday_slope_by_coin"] = pd.DataFrame(res)
    res = []
    for k, gg in su.groupby("year"):
        sl = stats.linregress(gg["past48z"], gg["f48z"])
        res.append(dict(year=k, n=len(gg), slope=sl.slope, t=sl.slope / sl.stderr))
    out["sunday_slope_by_year"] = pd.DataFrame(res)
    # prior-week z on forward, Sunday anchors (multivariate)
    X = np.column_stack([np.ones(len(su)), su["past48z"], su["prior120z"]])
    beta, *_ = np.linalg.lstsq(X, su["f48z"].values, rcond=None)
    resid = su["f48z"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * resid.var(ddof=3)
    out["sunday_multireg(b_const,b_wkend,b_prior)"] = pd.DataFrame(
        {"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "wkend_z", "prior_z"])

    out["f48x_by_anchor_wd"] = ev.groupby("wd").agg(n=("f48x", "size"), mean=("f48x", "mean"), t=("f48x", tfun))

    H = pd.concat(hr_rows).dropna()
    agg = dict(mean_bp=lambda x: x.mean() * 1e4, t=tfun, sd_bp=lambda x: x.std() * 1e4)
    out["mean_ret_by_hour_bp"] = H.groupby("hour")["r"].agg(**agg)
    out["mean_ret_by_weekday_bp"] = H.groupby("wd")["r"].agg(**agg)

    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"] = D.groupby("wd").agg(
        n=("book_return", "size"), book_bp=("book_return", lambda x: x.mean() * 1e4),
        coin_bp=("coin_return", lambda x: x.mean() * 1e4))

    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_by_coin"] = T.groupby("coin").agg(
        n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda x: (x > 0).mean()),
        dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
