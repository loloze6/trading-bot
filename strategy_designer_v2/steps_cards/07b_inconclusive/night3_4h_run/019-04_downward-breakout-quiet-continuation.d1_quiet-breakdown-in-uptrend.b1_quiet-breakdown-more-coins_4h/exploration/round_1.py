def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [6, 18, 36]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs) if rs else np.array([])
            drift[(coin, h)] = (np.nanmean(rs), np.nanstd(rs))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            prmin = lo.shift(1).rolling(12).min()
            prmax = hi.shift(1).rolling(12).max()
            mbr = (hi - lo).shift(1).rolling(180, min_periods=90).mean()
            width = (prmax - prmin) / mbr
            ret180 = c / c.shift(180) - 1
            brk = (c < prmin)
            depth = (prmin - c) / prmin
            fc = df["forecast"].values
            n = len(df)
            for h in H:
                for start in range(0, n - h, h):
                    seg = range(start, min(start + h, n - h))
                    # tested-case proxy: first bar in cell with forecast <= -2
                    for i in seg:
                        if brk.iloc[i] and not np.isnan(width.iloc[i]):
                            r = c.iloc[i + h] / c.iloc[i] - 1
                            m, s = drift[(coin, h)]
                            rows.append(dict(coin=coin, w=w, h=h, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                             up=ret180.iloc[i] > 0 if not np.isnan(ret180.iloc[i]) else np.nan,
                                             ret180=ret180.iloc[i], width=width.iloc[i], depth=depth.iloc[i],
                                             tested=fc[i] <= -2,
                                             unusual_short=-(r - m), total_short=-r, strength=-(r - m) / s))
                            break
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["unusual_short"]
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              total=g["total_short"].mean(), strength=g["strength"].mean()))
    out = {}
    out["by_h_up_tested"] = d.groupby(["h", "up", "tested"]).apply(summ)
    d18 = d[d.h == 18].copy()
    d18["wq"] = pd.qcut(d18["width"], 5, labels=False)
    out["h18_by_up_widthq"] = d18.groupby(["up", "wq"]).apply(summ)
    d18u = d18[d18.up == True].copy()
    d18u["rq"] = pd.qcut(d18u["ret180"], 4, labels=False)
    out["h18_up_by_ret180q"] = d18u.groupby("rq").apply(summ)
    d18u["dq"] = pd.qcut(d18u["depth"], 4, labels=False)
    out["h18_up_by_depthq"] = d18u.groupby("dq").apply(summ)
    out["h18_up_by_year"] = d18u.groupby("year").apply(summ)
    out["h18_up_by_coin"] = d18u.groupby("coin").apply(summ)
    d18d = d18[d18.up == False].copy()
    d18d["rq"] = pd.qcut(d18d["ret180"], 4, labels=False)
    out["h18_down_by_ret180q"] = d18d.groupby("rq").apply(summ)
    return out
