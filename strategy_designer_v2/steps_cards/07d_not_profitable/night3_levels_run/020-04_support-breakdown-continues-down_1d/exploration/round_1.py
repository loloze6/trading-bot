def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rc = "debug_info.components.support_break.last_history_value"
    rows = []; bk = []
    drift = {}
    for coin, ws in data["bars"].items():
        rets = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                rets.append(c[i+5]/c[i]-1)
        drift[coin] = (np.mean(rets), np.std(rets))
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            raw = b[rc].fillna(0) if rc in b else pd.Series(0, index=b.index)
            nz = (raw != 0).astype(int)
            run = nz.groupby((nz == 0).cumsum()).cumsum()
            r30 = c / c.shift(30) - 1
            r5p = c / c.shift(5) - 1
            hi90 = c.rolling(90, min_periods=20).max()
            dd90 = c / hi90 - 1
            fc = b["forecast"]
            alloc = b["postRebalance_current_allocation"]
            for i in range(0, len(b) - 5, 5):
                if fc[i] < 0:
                    fr = c[i+5]/c[i]-1
                    rows.append(dict(coin=coin, w=w, total=-fr, unusual=-(fr-drift[coin][0]),
                                     raw=raw[i], run=run[i], r30=r30[i], r5p=r5p[i], dd90=dd90[i],
                                     fc=fc[i], yr=b["timestamp"].iloc[i].year if hasattr(b["timestamp"].iloc[i],'year') else pd.to_datetime(b["timestamp"].iloc[i]).year))
        for w, d in data["days"][coin].items():
            d = d.dropna(subset=["book_return"])
            bk.append(pd.DataFrame(dict(coin=coin, w=w, br=d["book_return"].values, cr=d["coin_return"].values)))
    R = pd.DataFrame(rows)
    def summ(g):
        return pd.Series(dict(n=len(g), total=g.total.mean(), unusual=g.unusual.mean(),
                              t=stats.ttest_1samp(g.total, 0).statistic if len(g) > 2 else np.nan))
    out = {}
    out["all short grid cases"] = summ(R)
    R["runb"] = pd.cut(R.run, [-1, 0, 2, 5, 15, 40, 1000])
    out["by days below level"] = R.groupby("runb").apply(summ)
    R["r30b"] = pd.qcut(R.r30, 5)
    out["by 30d return"] = R.groupby("r30b").apply(summ)
    R["dd90b"] = pd.qcut(R.dd90, 5)
    out["by dist from 90d high"] = R.groupby("dd90b").apply(summ)
    R["r5b"] = pd.qcut(R.r5p, 5)
    out["by prior 5d return"] = R.groupby("r5b").apply(summ)
    R["fcb"] = pd.qcut(R.fc, 4, duplicates="drop")
    out["by forecast"] = R.groupby("fcb").apply(summ)
    out["by year"] = R.groupby("yr").apply(summ)
    out["by coin"] = R.groupby("coin").apply(summ)
    B = pd.concat(bk)
    out["book daily by coin"] = B.groupby("coin").agg(mean=("br", "mean"), sd=("br", "std"), coinmean=("cr", "mean"))
    return out
