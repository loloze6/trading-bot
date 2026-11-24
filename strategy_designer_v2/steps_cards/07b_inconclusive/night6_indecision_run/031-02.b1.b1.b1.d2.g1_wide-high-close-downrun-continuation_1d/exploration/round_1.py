import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    recs = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            drift[(coin, h)] = (np.nanmean(rs), np.nanstd(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            o, hi, lo, c = df["open"], df["high"], df["low"], df["close"]
            rng = hi - lo
            mr = rng.rolling(20, min_periods=20).mean()
            mult = rng / mr
            loc = (c - lo) / rng.replace(0, np.nan)
            fall = c.shift(1) / c.shift(6) - 1
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(n):
                if not (mult.iloc[i] >= 1.5 and loc.iloc[i] >= 0.75):
                    continue
                for h in H:
                    if i + h >= n:
                        continue
                    ret = c.iloc[i + h] / c.iloc[i] - 1
                    d, s = drift[(coin, h)]
                    recs.append(dict(coin=coin, win=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     h=h, cell=i // h, fell=fall.iloc[i] < 0, fall5=fall.iloc[i],
                                     mult=mult.iloc[i], r60=r60.iloc[i],
                                     body=(c.iloc[i] / o.iloc[i] - 1), dayret=c.iloc[i] / c.iloc[i - 1] - 1 if i > 0 else np.nan,
                                     un=-(ret - d), tot=-ret, strength=-(ret - d) / s))
    R = pd.DataFrame(recs)
    R = R.drop_duplicates(subset=["coin", "win", "h", "cell", "fell"])

    def st(g):
        dd = g.groupby("day")["un"].sum()
        m = g["un"].mean()
        nd = len(dd)
        se = np.sqrt((dd - dd.mean()).pow(2).sum()) / len(g) if nd > 1 else np.nan
        # clustered t: sum of day sums / sqrt(sum of squared day sums of deviations)
        dev = (g["un"] - m)
        ds = dev.groupby(g["day"]).sum()
        t = m * len(g) / np.sqrt((ds ** 2).sum()) if nd > 1 else np.nan
        return pd.Series(dict(n=len(g), days=nd, mean_un=m, t=t, hit=(g["un"] > 0).mean(), mean_tot=g["tot"].mean()))

    out = {}
    out["by_h_fell"] = R.groupby(["h", "fell"]).apply(st)
    F = R[(R.fell) & (R.h == 3)].copy()
    out["by_coin"] = F.groupby("coin").apply(st)
    out["by_year"] = F.groupby("year").apply(st)
    F["mq"] = pd.qcut(F["mult"], 4, labels=False, duplicates="drop")
    out["by_mult_q"] = F.groupby("mq").apply(st)
    F["fq"] = pd.qcut(F["fall5"], 4, labels=False, duplicates="drop")
    out["by_fall_q (0=deepest)"] = F.groupby("fq").apply(st)
    F["bull60"] = F["r60"] > 0
    out["by_r60_sign"] = F.groupby("bull60").apply(st)
    F["bodyup"] = F["dayret"] > 0
    out["by_day_up"] = F.groupby("bodyup").apply(st)
    return out
