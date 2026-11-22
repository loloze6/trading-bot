def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    h = 5
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - h, h)
            rs += list(c[idx + h] / c[idx] - 1)
        drift = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            z = (r1 / r1.rolling(20, min_periods=10).std()).values
            reg = b["regime"].values
            f = b["forecast"].fillna(0).values
            for t in range(0, n - h, h):
                if not np.isfinite(z[t]):
                    continue
                rows.append(dict(coin=coin, fall=(reg[t] == "mean_reversion"), z=z[t], f=f[t],
                                 u=-(c[t + h] / c[t] - 1 - drift)))
    df = pd.DataFrame(rows)
    def summ(g):
        x = g["u"]
        return pd.Series(dict(m=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))), n=len(x)))
    df["zb"] = pd.cut(df["z"], [-np.inf, -1, 0, 0.5, 1, 1.5, 2, np.inf])
    res = {}
    res["grid_fall_vs_other"] = df.groupby("fall").apply(summ)
    res["grid_by_zbin_fall"] = df[df.fall].groupby("zb").apply(summ)
    res["grid_by_zbin_other"] = df[~df.fall].groupby("zb").apply(summ)
    res["fall_rise_minus_fall_down"] = pd.Series(dict(
        rise=df[df.fall & (df.z > 0)]["u"].mean(), down=df[df.fall & (df.z <= 0)]["u"].mean()))
    from scipy import stats
    a = df[df.fall & (df.z > 1)]["u"]; b2 = df[~df.fall & (df.z > 1)]["u"]
    res["bigrise_fall_minus_other_welch"] = pd.Series(dict(diff=a.mean() - b2.mean(),
        t=stats.ttest_ind(a, b2, equal_var=False).statistic, na=len(a), nb=len(b2)))
    return res
