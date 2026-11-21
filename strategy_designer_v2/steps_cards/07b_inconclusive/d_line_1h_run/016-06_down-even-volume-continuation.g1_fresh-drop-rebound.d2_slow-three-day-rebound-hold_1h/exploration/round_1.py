import numpy as np, pandas as pd
from scipy import stats

def _ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if len(x) < 10 or np.std(x) == 0:
        return np.nan, np.nan, len(x)
    r = stats.linregress(x, y)
    return r.slope, r.slope / r.stderr if r.stderr > 0 else np.nan, len(x)

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for p in range(0, n - 72, 72):
                if p + 72 >= n:
                    break
                d = dict(coin=coin, win=w, year=ts.iloc[p].year, reg=reg[p], fc=f[p],
                         r72=c[p+72]/c[p]-1, r24_72=c[p+72]/c[p+24]-1,
                         r0_6=c[p+6]/c[p]-1, r6_24=c[p+24]/c[p+6]-1, r0_24=c[p+24]/c[p]-1,
                         r0_2=c[p+2]/c[p]-1, r24_48=c[p+48]/c[p+24]-1, r48_72=c[p+72]/c[p+48]-1)
                rows.append(d)
    g = pd.DataFrame(rows)
    hcols = ["r72", "r0_2", "r0_6", "r6_24", "r0_24", "r24_48", "r48_72", "r24_72"]
    for h in hcols:
        g["x_" + h] = g[h] - g.groupby("coin")[h].transform("mean")
    mr = g[g.reg == "mean_reversion"].copy()
    out = {}
    hz = []
    for h in hcols:
        s, t, n = _ols(mr["fc"], mr["x_" + h])
        hz.append(dict(seg=h, slope=s, t=t, n=n))
    out["slope_by_segment_mr_grid"] = pd.DataFrame(hz)
    # forecast buckets
    mr["fb"] = pd.cut(mr["fc"], [-0.01, 0.01, 5, 10, 15, 20.01], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["by_forecast_bucket"] = mr.groupby("fb", observed=True).agg(
        n=("fc", "size"), x_r0_24=("x_r0_24", "mean"), x_r24_72=("x_r24_72", "mean"), x_r72=("x_r72", "mean"))
    pc = []
    for coin, d in mr.groupby("coin"):
        s, t, n = _ols(d["fc"], d["x_r72"]); s2, t2, _ = _ols(d["fc"], d["x_r0_24"]); s3, t3, _ = _ols(d["fc"], d["x_r24_72"])
        pc.append(dict(coin=coin, n=n, t72=t, t0_24=t2, t24_72=t3))
    out["by_coin"] = pd.DataFrame(pc)
    py = []
    for y, d in mr.groupby("year"):
        s, t, n = _ols(d["fc"], d["x_r72"]); s2, t2, _ = _ols(d["fc"], d["x_r0_24"]); s3, t3, _ = _ols(d["fc"], d["x_r24_72"])
        py.append(dict(year=y, n=n, t72=t, t0_24=t2, t24_72=t3))
    out["by_year"] = pd.DataFrame(py)
    # 24-bar grid, forecast vs next 24h excess, mean_reversion bars
    r2 = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].values; reg = df["regime"].values; n = len(df)
            for p in range(0, n - 24, 24):
                r2.append(dict(coin=coin, reg=reg[p], fc=f[p], r=c[p+24]/c[p]-1))
    g2 = pd.DataFrame(r2)
    g2["x"] = g2["r"] - g2.groupby("coin")["r"].transform("mean")
    m2 = g2[g2.reg == "mean_reversion"]
    s, t, n = _ols(m2["fc"], m2["x"])
    out["grid24_next24_slope"] = pd.DataFrame([dict(slope=s, t=t, n=n)])
    # book: gross vs fees
    fee = 0; gross = 0; ntr = 0
    for coin, wins in data["trades"].items():
        for w, tr in wins.items():
            ntr += len(tr); fee += tr["total_commission"].sum()
    out["trades_and_fee_sum"] = pd.DataFrame([dict(trades=ntr, commission_sum=fee)])
    # gross position gain per bar vs net
    gp = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            a = df["postRebalance_current_allocation"].values
            c = df["close"].values
            ret = np.r_[c[1:]/c[:-1]-1, np.nan]
            gp.append(dict(gross=np.nansum(a*ret), active=(np.abs(a) > 1e-9).mean(),
                           turnover=np.nansum(np.abs(np.diff(a)))))
    gp = pd.DataFrame(gp)
    out["gross_sum_bar_gain_turnover"] = gp.sum().to_frame().T
    dd = pd.concat([d for wins in data["days"].values() for d in wins.values()])
    out["book_daily_mean"] = float(dd["book_return"].mean())
    return out
