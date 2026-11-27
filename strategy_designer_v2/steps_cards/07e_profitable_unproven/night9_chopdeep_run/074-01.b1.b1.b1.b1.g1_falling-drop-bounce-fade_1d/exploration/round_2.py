import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []; allrets = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].values); h = b["high"].values; l = b["low"].values
            r1 = c.pct_change(); allrets.append(r1.dropna().values)
            rng = pd.Series((h - l) / c.values); ratio = rng / rng.rolling(20).mean()
            sd20 = r1.rolling(20).std()
            fall5 = (c.shift(1) / c.shift(6) - 1) / (sd20 * np.sqrt(5))
            tr60 = c / c.shift(60) - 1
            f1 = c.shift(-1) / c - 1
            for t in range(len(b)):
                if r1[t] > 0 and ratio[t] > 1 and tr60[t] < -0.10 and not np.isnan(f1[t]):
                    rows.append(dict(coin=coin, w=w, year=pd.Timestamp(b["timestamp"][t]).year,
                                     day=str(pd.Timestamp(b["timestamp"][t]).date()),
                                     fall5=fall5[t], ratio=ratio[t], f1=f1[t], fc=b["forecast"][t]))
    df = pd.DataFrame(rows); drift = np.concatenate(allrets).mean()
    df["u1"] = -(df["f1"] - drift)
    def pooled(g):
        dd = (g["u1"] - g["u1"].mean()).groupby(g["day"]).sum()
        se = np.sqrt((dd ** 2).sum()) / len(g) if len(g) > 1 else np.nan
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=g["u1"].mean(), t_pooled=g["u1"].mean() / se if se else np.nan))
    # all wide up days in falling, graded by prior 5-day fall (no threshold)
    df["fall5_bin"] = pd.cut(df["fall5"], [-99, -2, -1, 0, 99], labels=["<-2", "-2..-1", "-1..0", ">0"])
    out["wideup_falling_by_fall5"] = df.groupby("fall5_bin").apply(pooled)
    out["by_fall5_bin_year"] = df.groupby(["year", "fall5_bin"]).apply(pooled)["mean"].unstack()
    out["spearman_all_wideup_falling"] = pd.Series({"fall5_vs_u1": stats.spearmanr(df["fall5"], df["u1"], nan_policy="omit")[0],
                                                    "ratio_vs_u1": stats.spearmanr(df["ratio"], df["u1"], nan_policy="omit")[0],
                                                    "n": len(df)})
    deep = df[df.fall5 <= -1]
    out["deep_no2018"] = pooled(deep[deep.year != 2018])
    # book: drift part vs timing
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; d.append(x)
    D = pd.concat(d)
    bookd = D.groupby("day")["book_return"].mean().dropna()
    mdrift = D["coin_return"].dropna().mean()
    pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            pos.append(b["postRebalance_current_allocation"].values)
    pos = np.concatenate(pos)
    out["book_parts"] = pd.Series({"book_mean_daily": bookd.mean(), "coin_mean_daily": mdrift,
                                   "mean_position": pos.mean(), "drift_part_approx": pos.mean() * mdrift,
                                   "sharpe_book": bookd.mean() / bookd.std() * np.sqrt(365)})
    return out
