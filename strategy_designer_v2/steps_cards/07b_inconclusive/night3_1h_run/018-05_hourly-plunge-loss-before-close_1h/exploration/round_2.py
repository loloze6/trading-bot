def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            rets.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(rets))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            day = ts.dt.floor("D")
            f = b["forecast"].values
            c = b["close"].values
            n = len(b)
            prev = np.r_[np.nan, f[:-1]]
            cross = (f <= -2) & (prev > -2)
            dser = pd.Series(day)
            last_idx = dser.groupby(dser).transform(lambda s: s.index[-1]).values
            seen = set()
            last_used72 = -10**9
            for i in np.where(cross)[0]:
                d = day.iloc[i]
                if d in seen:
                    continue
                seen.add(d)
                j = int(last_idx[i])
                r = {"eod": -(c[j] / c[i] - 1) + mu * (j - i)}
                for h in (24, 72):
                    r["h%d" % h] = -(c[i + h] / c[i] - 1) + mu * h if i + h < n else np.nan
                # non-overlapping 72h cases
                if i - last_used72 >= 72 and i + 72 < n:
                    r["h72no"] = r["h72"]
                    last_used72 = i
                else:
                    r["h72no"] = np.nan
                r["tr30"] = c[i] / c[i - 720] - 1 if i >= 720 else np.nan
                r.update(coin=coin, win=w, f=f[i], year=ts.iloc[i].year)
                rows.append(r)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for k in ["eod", "h24", "h72", "h72no"]:
            x = g[k].dropna()
            out[k + "_bp"] = x.mean() * 1e4
            out[k + "_t"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
            out[k + "_n"] = len(x)
        return pd.Series(out)
    df["trb"] = pd.qcut(df["tr30"], 3, labels=["down", "mid", "up"])
    df["trb5"] = pd.qcut(df["tr30"], 5, labels=["q1", "q2", "q3", "q4", "q5"])
    ex = df[df["year"] != 2018]
    yt = df.groupby(["year", "trb"], observed=True)["h72no"].agg(["mean", "count"])
    yt["mean"] *= 1e4
    sp = {}
    for k in ["eod", "h24", "h72no"]:
        x = df[["tr30", k]].dropna()
        sp[k] = stats_rho = pd.Series(x["tr30"]).rank().corr(x[k].rank())
    return {
        "trend5": df.groupby("trb5", observed=True).apply(summ),
        "trend3_ex2018": ex.groupby("trb", observed=True).apply(summ),
        "year_x_trend_h72no": yt.unstack(),
        "coin_x_trend_h72no": (df.groupby(["coin", "trb"], observed=True)["h72no"].mean() * 1e4).unstack(),
        "spearman_tr30": pd.Series(sp),
        "tr30_quantiles": df["tr30"].quantile([0.2, 0.333, 0.5, 0.667, 0.8]),
    }
