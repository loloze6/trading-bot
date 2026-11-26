def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            stretch = (c / sma - 1) / sd
            fc = b["forecast"].astype(float)
            chop = (b["regime"] == "unknown")
            ts = pd.to_datetime(b["timestamp"])
            sdr = sd.rolling(60, min_periods=30).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, stretch=stretch[i], fc=fc[i], chop=chop[i],
                                     fwd=fwd[i], year=ts[i].year, day=ts[i].normalize(), sdr=sdr[i]))
    g = pd.DataFrame(rows).dropna(subset=["stretch", "fwd"])
    g["drift"] = g.groupby(["coin", "h"])["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    out = {}
    def daytest(s, col="ex"):
        dd = s.groupby("day")[col].sum()
        n = len(dd)
        m = s[col].mean()
        se = dd.std() * np.sqrt(n) / len(s)
        return m, m / se if se > 0 else np.nan, len(s), n
    for h in (5, 10):
        gh = g[g.h == h]
        res = {}
        for ch in (True, False):
            for side, cond in (("below", gh.stretch < 0), ("above", gh.stretch > 0)):
                s = gh[(gh.chop == ch) & cond]
                sl = stats.linregress(s["stretch"], s["ex"])
                m, t, n, nd = daytest(s.assign(ex=s.ex * np.sign(s.stretch)))
                res[f"chop{ch}_{side}"] = dict(slope=sl.slope, slope_t=sl.slope / sl.stderr,
                                               mean_cont=m, t_day=t, n=n, days=nd)
        out[f"h{h}_side_slopes"] = pd.DataFrame(res).T
        s = gh[gh.chop]
        # graded in raw stretch, choppy, below side: quantile buckets
        sb = s[s.stretch < 0].copy()
        sb["qb"] = pd.qcut(sb["stretch"], 4, labels=False)
        out[f"h{h}_chop_below_quartiles"] = sb.groupby("qb").agg(mean_ex=("ex", "mean"), n=("ex", "size"),
                                                                 mean_stretch=("stretch", "mean"))
        # standardised forecast vs raw
        sf = s[s.fc < 0]
        if len(sf) > 5:
            sl = stats.linregress(-sf["fc"], sf["ex"])
            out[f"h{h}_chop_forecast_slope"] = f"slope {sl.slope:.5f} t {sl.slope/sl.stderr:.2f} n {len(sf)}; corr(fc,stretch) {np.corrcoef(sf.fc, sf.stretch)[0,1]:.2f}"
        # by year, choppy below: continuation mean
        out[f"h{h}_chop_below_by_year"] = sb.groupby("year").agg(mean_ex=("ex", "mean"), n=("ex", "size"))
        out[f"h{h}_chop_below_by_coin"] = sb.groupby("coin").agg(mean_ex=("ex", "mean"), n=("ex", "size"))
        sb2 = sb.dropna(subset=["sdr"])
        sb2["vb"] = (sb2.sdr > 0.5).astype(int)
        out[f"h{h}_chop_below_by_volrank60"] = sb2.groupby("vb").agg(mean_ex=("ex", "mean"), n=("ex", "size"))
        # non-choppy: stretch both sides, by year
        nc = gh[~gh.chop].copy()
        nc["cont"] = nc.ex * np.sign(nc.stretch)
        out[f"h{h}_nonchop_cont_by_year"] = nc.groupby("year").agg(mean_cont=("cont", "mean"), n=("cont", "size"))
    return out
