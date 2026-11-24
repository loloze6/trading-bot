def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 20
    rows = []
    base_rows = []
    drift = {}; usual = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                g.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(g) if g else np.nan
        usual[coin] = np.std(g, ddof=1) if len(g) > 1 else np.nan
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            up = np.r_[False, c[1:] > c[:-1]]
            streak = np.zeros(n, int)
            for i in range(1, n):
                streak[i] = streak[i - 1] + 1 if up[i] else 0
            ret30 = pd.Series(c).pct_change(30).values
            low = 0.0; taken = set()
            for i in range(n):
                if f[i] <= 0:
                    low = 0.0; continue
                if f[i] - low >= 2:
                    cell = i // H
                    low = f[i]
                    if cell in taken: continue
                    taken.add(cell)
                    rec = dict(coin=coin, win=w, year=ts[i].year, day=ts[i].normalize(),
                               f=f[i], streak=streak[i], ret30=ret30[i])
                    for h in (1, 3, 5, 10, 20, 40):
                        rec["r%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                    rec["u20"] = rec["r20"] - drift[coin] if not np.isnan(rec["r20"]) else np.nan
                    rec["s20"] = rec["u20"] / usual[coin]
                    rows.append(rec)
                else:
                    low = min(low, f[i])
            # baseline: grid bars with ret30>0
            for i in range(0, n - H, H):
                if ret30[i] > 0:
                    base_rows.append(dict(coin=coin, u20=c[i+H]/c[i]-1-drift[coin], day=ts[i].normalize(), year=ts[i].year))
    d = pd.DataFrame(rows).dropna(subset=["u20"])
    b = pd.DataFrame(base_rows)
    def tday(x):
        s = (x["u20"] - x["u20"].mean()).groupby(x["day"]).sum()
        se = np.sqrt((s**2).sum()) / len(x) if len(x) else np.nan
        return x["u20"].mean() / se if se > 0 else np.nan
    def summ(x):
        return pd.Series({"n": len(x), "days": x["day"].nunique(), "mean_u20": x["u20"].mean(), "t_day": tday(x)})
    out = {}
    out["all_cases"] = summ(d)
    out["baseline_ret30pos_grid"] = summ(b)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["baseline_by_year"] = b.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 3, labels=["lo","mid","hi"])
    out["by_forecast_third"] = d.groupby("fq").apply(summ)
    d["sb"] = pd.cut(d["streak"], [-1, 2, 3, 4, 5, 100])
    out["by_streak_len"] = d.groupby("sb").apply(summ)
    d["r30q"] = pd.qcut(d["ret30"], 3)
    out["by_ret30_third"] = d.groupby("r30q").apply(summ)
    hz = {}
    for h in (1, 3, 5, 10, 20, 40):
        x = d.dropna(subset=["r%d" % h])
        x = x.assign(u20=x["r%d" % h])
        hz["h%d_raw" % h] = [len(x), x["u20"].mean(), tday(x)]
    out["horizons_raw_return"] = pd.DataFrame(hz, index=["n","mean","t_day"]).T
    out["median_u20"] = d["u20"].median()
    out["share_pos_u20"] = (d["u20"] > 0).mean()
    return out
