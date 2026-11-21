def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy()
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            d["yr"] = pd.to_datetime(d["day"]).dt.year
            cr = d["coin_return"]
            d["prev7"] = (1 + cr).rolling(7).apply(np.prod, raw=True).shift(1) - 1
            d["vol30"] = cr.rolling(30, min_periods=15).std().shift(1)
            d["prev1"] = cr.shift(1)
            d["coin"] = c; d["win"] = w
            rows.append(d)
    dd = pd.concat(rows)
    dd = dd.dropna(subset=["coin_return"])
    # weekday by coin, t
    def tt(x): return x.mean()/x.std()*np.sqrt(len(x)) if len(x) > 2 else np.nan
    out["wd_by_coin_t"] = dd.groupby(["coin", "wd"])["coin_return"].apply(tt).unstack().round(2)
    out["wd_by_coin_mean_bps"] = (dd.groupby(["coin", "wd"])["coin_return"].mean().unstack()*1e4).round(1)
    # cross-coin average per day, then weekday t (removes correlation)
    avg = dd.groupby(["win", "day"]).agg(r=("coin_return", "mean"), wd=("wd", "first"), yr=("yr", "first"))
    out["wd_avgcoins_t"] = avg.groupby("wd")["r"].agg(["mean", "count", tt]).round(5)
    out["sat_minus_rest_by_year"] = avg.groupby("yr").apply(lambda g: pd.Series(dict(
        sat=g.r[g.wd == 5].mean(), rest=g.r[g.wd != 5].mean(), n_sat=(g.wd == 5).sum(),
        t=stats.ttest_ind(g.r[g.wd == 5], g.r[g.wd != 5], equal_var=False).statistic))).round(4)
    # windows: share of windows with positive sat mean
    wm = avg.groupby(["win", "wd"])["r"].mean().unstack()
    out["share_windows_pos_by_wd"] = (wm > 0).mean().round(3)
    # graded: Saturday return vs prev7 and vol30 per coin (rank within coin)
    s = dd[dd.wd == 5].dropna(subset=["prev7", "vol30"]).copy()
    for f in ["prev7", "vol30", "prev1"]:
        s["rk"] = s.groupby("coin")[f].rank(pct=True)
        top = s.coin_return[s.rk > 0.67]; bot = s.coin_return[s.rk <= 0.33]
        out[f"sat_by_{f}"] = pd.Series(dict(rho=stats.spearmanr(s.rk, s.coin_return)[0],
            top=top.mean(), mid=s.coin_return[(s.rk > 0.33) & (s.rk <= 0.67)].mean(), bot=bot.mean(),
            t=stats.ttest_ind(top, bot, equal_var=False).statistic, n=len(s))).round(4)
    # Fri+Sat combined (2-day) vs vol30
    fs = dd[dd.wd.isin([4, 5])].dropna(subset=["vol30"]).copy()
    fs["rk"] = fs.groupby("coin")["vol30"].rank(pct=True)
    fs["z"] = fs.coin_return / fs.vol30
    out["frisat_z_by_vol_tercile"] = fs.groupby(pd.cut(fs.rk, [0, .33, .67, 1]))["coin_return"].agg(["mean", "count", tt]).round(4)
    return out
