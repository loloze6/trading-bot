import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    H = 10
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; h = df["high"].values; l = df["low"].values
            n = len(df)
            s = pd.Series(c)
            hh20 = pd.Series(h).rolling(20).max().shift(1).values
            ll20 = pd.Series(l).rolling(20).min().shift(1).values
            pos20 = (c - ll20) / (hh20 - ll20)
            brk = c / hh20 - 1
            ret10 = s.pct_change(10).values
            ret1 = s.pct_change(1).values
            vol20 = pd.Series(np.log(c)).diff().rolling(20).std().values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, pos20=pos20[i], brk=brk[i], ret10=ret10[i], ret1=ret1[i],
                                 vol20=vol20[i], fc=df["forecast"].iloc[i],
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                 fr=c[i + H] / c[i] - 1))
    g = pd.DataFrame(rows)
    g["ex"] = g["fr"] - g.groupby("coin")["fr"].transform("mean")
    out = {}
    d = g.dropna(subset=["pos20", "ex"]).copy()
    d["q"] = pd.qcut(d["pos20"].rank(method="first"), 5, labels=False)
    out["pos20_top_vs_rest_by_coin"] = d.groupby("coin").apply(lambda x: pd.Series({
        "top": x.loc[x.q == 4, "ex"].mean(), "rest": x.loc[x.q < 4, "ex"].mean(),
        "t": stats.ttest_ind(x.loc[x.q == 4, "ex"], x.loc[x.q < 4, "ex"], equal_var=False).statistic,
        "n_top": (x.q == 4).sum()}))
    out["pos20_top_vs_rest_by_year"] = d.groupby("year").apply(lambda x: pd.Series({
        "diff": x.loc[x.q == 4, "ex"].mean() - x.loc[x.q < 4, "ex"].mean(),
        "t": stats.ttest_ind(x.loc[x.q == 4, "ex"], x.loc[x.q < 4, "ex"], equal_var=False).statistic,
        "n_top": (x.q == 4).sum()}))
    b = d[d["brk"] > 0]
    out["breakout_n"] = len(b)
    out["breakout_mean_ex_t"] = f"{b['ex'].mean():.4f} t={b['ex'].mean()/(b['ex'].std()/np.sqrt(len(b))):.2f}"
    if len(b) > 20:
        r = stats.linregress(b["brk"], b["ex"]); out["breakout_size_slope_t"] = f"{r.slope:.3f} t={r.slope/r.stderr:.2f}"
    # pos20 slope controlling ret10
    dd = g.dropna(subset=["pos20", "ret10", "ex"])
    X = np.column_stack([np.ones(len(dd)), dd["pos20"], dd["ret10"]])
    beta, *_ = np.linalg.lstsq(X, dd["ex"].values, rcond=None)
    res = dd["ex"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(dd) - 3)
    out["ols_pos20_ret10"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["c", "pos20", "ret10"])
    # pos20 effect by vol level
    dd = dd.copy(); dd = dd.dropna(subset=["vol20"])
    dd["vq"] = dd.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    out["pos20_slope_by_volterc"] = dd.groupby("vq").apply(lambda x: pd.Series({
        "slope": stats.linregress(x["pos20"], x["ex"]).slope,
        "t": stats.linregress(x["pos20"], x["ex"]).slope / stats.linregress(x["pos20"], x["ex"]).stderr, "n": len(x)}))
    # weekday daily coin return by coin and year
    D = []
    for coin, wins in days.items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; D.append(x)
    D = pd.concat(D).dropna(subset=["coin_return"])
    D["day"] = pd.to_datetime(D["day"]); D["wd"] = D["day"].dt.weekday; D["year"] = D["day"].dt.year
    D["cm"] = D.groupby("coin")["coin_return"].transform("mean")
    D["exd"] = D["coin_return"] - D["cm"]
    out["sat_minus_other_by_coin"] = D.groupby("coin").apply(lambda x: pd.Series({
        "diff": x.loc[x.wd == 5, "coin_return"].mean() - x.loc[x.wd != 5, "coin_return"].mean(),
        "t": stats.ttest_ind(x.loc[x.wd == 5, "coin_return"], x.loc[x.wd != 5, "coin_return"], equal_var=False).statistic}))
    out["sat_minus_other_by_year"] = D.groupby("year").apply(lambda x: pd.Series({
        "diff": x.loc[x.wd == 5, "coin_return"].mean() - x.loc[x.wd != 5, "coin_return"].mean(),
        "t": stats.ttest_ind(x.loc[x.wd == 5, "coin_return"], x.loc[x.wd != 5, "coin_return"], equal_var=False).statistic}))
    # market-wide: average across coins per day, weekday t
    M = D.groupby("day")["coin_return"].mean().reset_index(); M["wd"] = M["day"].dt.weekday
    mt = M.groupby("wd")["coin_return"].agg(["mean", "std", "count"]); mt["t"] = mt["mean"] / (mt["std"] / np.sqrt(mt["count"]))
    out["daymean_by_weekday"] = mt
    # daily reversal: next-day return after large 1-day moves (per coin standardised)
    D = D.sort_values(["coin", "w", "day"])
    D["next"] = D.groupby(["coin", "w"])["coin_return"].shift(-1)
    D["z"] = D.groupby("coin")["coin_return"].transform(lambda x: (x - x.mean()) / x.std())
    E = D.dropna(subset=["next", "z"]).copy()
    E["nex"] = E["next"] - E["cm"]
    E["zq"] = pd.qcut(E["z"].rank(method="first"), 10, labels=False)
    zt = E.groupby("zq")["nex"].agg(["mean", "std", "count"]); zt["t"] = zt["mean"] / (zt["std"] / np.sqrt(zt["count"]))
    out["next_day_by_today_decile"] = zt
    return out
