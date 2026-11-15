def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    # pooled mean daily return per coin over all windows
    mu = {}
    for c, ws in bars.items():
        rs = []
        for w, df in ws.items():
            r = df["close"].pct_change().dropna()
            rs.append(r)
        mu[c] = pd.concat(rs).mean()
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            fc = df["forecast"].values
            raw = df["debug_info.components.above_ma.last_history_value"].values if "debug_info.components.above_ma.last_history_value" in df else np.full(n, np.nan)
            r20b = pd.Series(cl).pct_change(20).values
            for h in [5, 10, 20, 40, 60]:
                for t in range(0, n, h):
                    if t + h < n:
                        rows.append(dict(coin=c, win=w, year=yr[t], h=h, fc=fc[t], raw=raw[t],
                                         past20=r20b[t],
                                         ex=cl[t + h] / cl[t] - 1 - h * mu[c]))
    d = pd.DataFrame(rows)

    def summ(g):
        x = g["ex"].dropna()
        n = len(x)
        m = x.mean()
        t = m / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, mean=m, t=t, hit=(x > 0).mean()))

    # by horizon: forecast>0 vs ==0
    d["on"] = d["fc"] > 0
    out["by_h_on"] = d.groupby(["h", "on"]).apply(summ)
    hw = []
    for h, g in d.groupby("h"):
        a = g[g.on]["ex"]; b = g[~g.on]["ex"]
        hw.append(dict(h=h, diff=a.mean() - b.mean(), welch_t=stats.ttest_ind(a, b, equal_var=False).statistic))
    out["on_minus_off"] = pd.DataFrame(hw)
    d20 = d[(d.h == 20) & d.on].copy()
    d20["fbin"] = pd.qcut(d20["fc"], 4, labels=["q1", "q2", "q3", "q4"])
    out["h20_on_by_fc_quartile"] = d20.groupby("fbin").apply(summ)
    d20["rbin"] = pd.qcut(d20["raw"].rank(method="first"), 4, labels=["r1", "r2", "r3", "r4"])
    out["h20_on_by_rawdist_quartile"] = d20.groupby("rbin").apply(summ)
    out["h20_on_by_coin"] = d20.groupby("coin").apply(summ)
    out["h20_on_by_year"] = d20.groupby("year").apply(summ)
    d20["p20"] = np.where(d20["past20"] > 0, "past20_up", "past20_down")
    out["h20_on_by_past20"] = d20.groupby("p20").apply(summ)
    d60 = d[(d.h == 60) & d.on]
    out["h60_on_by_coin"] = d60.groupby("coin").apply(summ)
    # median vs mean (skew)
    out["h20_on_median_ex"] = float(d20["ex"].median())
    out["h20_on_skew"] = float(stats.skew(d20["ex"].dropna()))
    # book: gain from market rise vs timing
    br, mk = [], []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            a = df["postRebalance_current_allocation"].values[:-1]
            r = df["close"].pct_change().shift(-1).values[:-1]
            br.append(np.nanmean(a * r)); mk.append(np.nanmean(a) * mu[c])
    out["book_bar_gain_vs_market_part"] = pd.Series(dict(total=np.mean(br), market=np.mean(mk), timing=np.mean(br) - np.mean(mk)))
    return out
