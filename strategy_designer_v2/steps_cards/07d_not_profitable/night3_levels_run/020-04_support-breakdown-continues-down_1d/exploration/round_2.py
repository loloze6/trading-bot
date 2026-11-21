def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rc = "debug_info.components.support_break.last_history_value"
    rows = []; bk = []
    for coin, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                rets.append(c[i+5]/c[i]-1)
        dm = np.mean(rets)
        dmd = []
        for w, d in data["days"][coin].items():
            dmd += list(d["coin_return"].dropna().values)
        dmd = np.mean(dmd)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            raw = b[rc].fillna(0) if rc in b else pd.Series(0, index=b.index)
            r60 = c / c.shift(60) - 1
            ma50 = c / c.rolling(50, min_periods=50).mean() - 1
            r10 = c / c.shift(10) - 1
            fc = b["forecast"]
            for i in range(0, len(b) - 5, 5):
                if fc[i] < 0:
                    fr = c[i+5]/c[i]-1
                    rows.append(dict(coin=coin, total=-fr, unusual=-(fr-dm), raw=raw[i],
                                     r60=r60[i], ma50=ma50[i], r10=r10[i]))
            a = b["postRebalance_current_allocation"].values
            g = a[:-1] * (c.values[1:]/c.values[:-1]-1)
            bk.append(dict(coin=coin, gain=g.mean(), drift=(a[:-1]*dmd).mean(), short_share=(a < 0).mean()))
    R = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), total=g.total.mean(), unusual=g.unusual.mean(),
                              t=stats.ttest_1samp(g.unusual, 0).statistic if len(g) > 2 else np.nan))
    out = {}
    R["rawb"] = pd.qcut(R.raw, 5, duplicates="drop")
    out["by raw depth x touches"] = R.groupby("rawb").apply(summ)
    R["r60b"] = pd.qcut(R.r60, 5)
    out["by 60d return"] = R.groupby("r60b").apply(summ)
    R["ma50b"] = pd.qcut(R.ma50, 5)
    out["by close vs 50d mean"] = R.groupby("ma50b").apply(summ)
    R["r10b"] = pd.qcut(R.r10, 5)
    out["by 10d return"] = R.groupby("r10b").apply(summ)
    R["trend"] = np.where(R.r60 < -0.1, "60d down>10%", np.where(R.r60.isna(), "na", "other"))
    R["rawt"] = pd.qcut(R.raw, 3, labels=["low", "mid", "high"], duplicates="drop")
    out["trend x raw tercile"] = R.groupby(["trend", "rawt"]).apply(summ)
    out["book gain split"] = pd.DataFrame(bk).groupby("coin").mean()
    return out
