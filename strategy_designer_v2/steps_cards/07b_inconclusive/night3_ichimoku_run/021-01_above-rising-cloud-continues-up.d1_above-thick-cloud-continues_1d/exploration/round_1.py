def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 26
    rows = []
    for coin, wins in bars.items():
        # coin mean 26-bar return over all windows (grid)
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        mu = np.mean(allr); sd = np.std(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; hi = df["high"]; lo = df["low"]
            mid = lambda n: (hi.rolling(n).max() + lo.rolling(n).min()) / 2
            a = ((mid(9) + mid(26)) / 2).shift(26)
            b = mid(52).shift(26)
            top = np.maximum(a, b); cm = (a + b) / 2
            width = (a - b).abs() / c
            slope = cm / cm.shift(26) - 1
            pos = c / top - 1
            yr = pd.to_datetime(df["timestamp"]).dt.year
            for h in [5, 10, 26, 52]:
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, win=w, year=yr.iloc[i], h=h,
                        reg=df["regime"].iloc[i] == "trending", fc=df["forecast"].iloc[i],
                        width=width.iloc[i], slope=slope.iloc[i], pos=pos.iloc[i],
                        ret=c.iloc[i + h] / c.iloc[i] - 1, mu26=mu, sd26=sd))
    R = pd.DataFrame(rows)
    out = {}
    def reg(d, x, y="ex"):
        d = d.dropna(subset=[x, y])
        if len(d) < 8: return (len(d), np.nan, np.nan)
        r = stats.linregress(d[x], d[y]); return (len(d), r.slope, r.slope / r.stderr)
    # coin mean per horizon
    R["mu_h"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["ex"] = R["ret"] - R["mu_h"]
    g26 = R[R.h == 26]
    # level effect: in regime vs out
    lv = []
    for h in [5, 10, 26, 52]:
        d = R[R.h == h]
        ins, outr = d[d.reg]["ex"].dropna(), d[~d.reg]["ex"].dropna()
        t = stats.ttest_ind(ins, outr, equal_var=False).statistic
        t1 = ins.mean() / (ins.std() / np.sqrt(len(ins)))
        n, s, ts = reg(d[d.reg], "fc")
        nw, sw, tw = reg(d[d.reg], "width")
        lv.append(dict(h=h, n_in=len(ins), ex_in=ins.mean(), t_in=t1, ex_out=outr.mean(), t_in_minus_out=t,
                       fc_slope_t=ts, width_slope_t=tw))
    out["by_horizon"] = pd.DataFrame(lv)
    ins = g26[g26.reg]
    pc = []
    for coin, d in ins.groupby("coin"):
        n, s, t = reg(d, "fc"); pc.append(dict(coin=coin, n=n, mean_ex=d.ex.mean(), fc_t=t,
                                               slope_t=reg(d, "slope")[2], pos_t=reg(d, "pos")[2]))
    out["by_coin_26"] = pd.DataFrame(pc)
    py = []
    for y, d in ins.groupby("year"):
        n, s, t = reg(d, "fc"); py.append(dict(year=y, n=n, mean_ex=d.ex.mean(), fc_t=t))
    out["by_year_26"] = pd.DataFrame(py)
    d = ins.dropna(subset=["fc"]).copy()
    d["q"] = pd.qcut(d.fc.rank(method="first"), 4, labels=False)
    out["fc_quartiles_26"] = d.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"), width=("width", "mean"),
                                                 ex=("ex", "mean"), ex_sd=("ex", "std"))
    # alt predictors inside regime at 26
    alt = {}
    for x in ["width", "slope", "pos"]:
        alt[x] = reg(ins, x)[2]
    alt["n"] = len(ins)
    out["alt_predictors_t_26"] = pd.Series(alt)
    d2 = ins.dropna(subset=["pos"]).copy()
    d2["q"] = pd.qcut(d2.pos.rank(method="first"), 4, labels=False)
    out["pos_quartiles_26"] = d2.groupby("q").agg(n=("ex", "size"), pos=("pos", "mean"), ex=("ex", "mean"))
    return out
