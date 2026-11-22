import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        r = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 1)
            r.extend(list(c[idx + 1] / c[idx] - 1))
        dr = np.mean(r)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            z = r1 / r1.rolling(20, min_periods=20).std()
            r90 = c / c.shift(90) - 1
            fall = np.where(r90.notna(), r90 < 0, b["regime"] == "mean_reversion")
            f = b["forecast"].fillna(0).values
            low = 0.0
            n = len(b)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for t in range(n):
                case = False
                if f[t] >= 0:
                    low = 0.0
                elif f[t] <= low - 2:
                    case = True
                    low = f[t]
                ex1 = -(c.iloc[t + 1] / c.iloc[t] - 1 - dr) if t + 1 < n else np.nan
                rows.append(dict(coin=coin, win=w, year=yr[t], z=z.iloc[t], fall=bool(fall[t]),
                                 case=case, fc=abs(f[t]), ex1=ex1))
    df = pd.DataFrame(rows)
    out = {}
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    cs = df[df.case & df.ex1.notna()].copy()
    out["corr_z_vs_absforecast_cases"] = float(cs[["z", "fc"]].corr().iloc[0, 1])
    med = cs.z.median()
    top, bot = cs[cs.z > med].ex1, cs[cs.z <= med].ex1
    out["cases_zhalf_top_minus_bottom"] = pd.Series({"top_mean": top.mean(), "bot_mean": bot.mean(),
        "welch_t": stats.ttest_ind(top, bot, equal_var=False).statistic, "n_top": len(top), "n_bot": len(bot)})
    out["cases_spearman_z_ex1"] = pd.Series(stats.spearmanr(cs.z, cs.ex1)[:2], index=["rho", "p"])
    a = df[df.fall & (df.z > 1.5) & df.ex1.notna()]
    out["fall_z_gt1p5_by_coin"] = a.groupby("coin").ex1.apply(summ).unstack()
    out["fall_z_gt1p5_by_year"] = a.groupby("year").ex1.apply(summ).unstack()
    b2 = df[(~df.fall) & (df.z > 1.5) & df.ex1.notna()]
    out["fall_minus_rise_z_gt1p5"] = pd.Series({"fall_mean": a.ex1.mean(), "rise_mean": b2.ex1.mean(),
        "welch_t": stats.ttest_ind(a.ex1, b2.ex1, equal_var=False).statistic, "n_fall": len(a), "n_rise": len(b2)})
    pos = df[df.fall & (df.z > 0) & df.ex1.notna()]
    out["fall_upday_spearman_z_ex1"] = pd.Series(stats.spearmanr(pos.z, pos.ex1)[:2], index=["rho", "p"])
    return out
