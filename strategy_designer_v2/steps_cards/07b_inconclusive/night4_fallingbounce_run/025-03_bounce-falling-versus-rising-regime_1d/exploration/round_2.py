import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 5, 5)
            allr += list(c[idx + 5] / c[idx] - 1)
        dr = np.mean(allr)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            r1 = pd.Series(c).pct_change()
            z = (r1 / r1.shift(1).rolling(20).std()).values
            reg = df["regime"].values
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for s in range(0, n - 5, 5):
                cell = range(s, min(s + 5, n - 5))
                # strongest rise day in cell (by z), else the cell's first bar as a non-bounce baseline
                zz = [(z[i], i) for i in cell if not np.isnan(z[i])]
                if not zz:
                    continue
                zmax, i = max(zz)
                rows.append(dict(coin=coin, year=yr[i], reg=reg[i], z=zmax, f=f[i],
                                 x5=c[i+5]/c[i]-1-dr, x1=c[i+1]/c[i]-1,
                                 b5=c[s+5]/c[s]-1-dr))
    d = pd.DataFrame(rows)
    d = d[d.reg.isin(["trending", "mean_reversion"])]
    out = {}
    d["zbin"] = pd.cut(d.z, [-np.inf, 0, 1, 1.5, 2, 2.5, 3, np.inf])
    g = d.groupby(["zbin", "reg"])["x5"].agg(["count", "mean", "std"])
    g["t"] = g["mean"] / g["std"] * np.sqrt(g["count"])
    out["x5_by_rise_bin_and_regime"] = g
    res = {}
    for r in ["trending", "mean_reversion"]:
        s = d[d.reg == r]
        sl = stats.linregress(s.z, s.x5)
        res[r] = dict(n=len(s), slope=sl.slope, t=sl.slope / sl.stderr)
        s2 = s[s.z >= 1.5]
        sl2 = stats.linregress(s2.z, s2.x5)
        res[r + "_z>=1.5"] = dict(n=len(s2), slope=sl2.slope, t=sl2.slope / sl2.stderr)
    out["slope_x5_on_rise_within_regime"] = pd.DataFrame(res).T
    # baseline regime gap (cell start, any day) by year vs bounce gap by year
    yy = {}
    for y, s in d.groupby("year"):
        T = s[s.reg == "trending"]; M = s[s.reg == "mean_reversion"]
        Tb = T[T.z >= 2]; Mb = M[M.z >= 2]
        yy[y] = dict(base_gap=T.b5.mean() - M.b5.mean(), nT=len(T), nM=len(M),
                     bounce_gap=Tb.x5.mean() - Mb.x5.mean(), nTb=len(Tb), nMb=len(Mb))
    out["regime_gap_baseline_vs_bounce_by_year"] = pd.DataFrame(yy).T
    T = d[d.reg == "trending"]; M = d[d.reg == "mean_reversion"]
    out["baseline_gap_all_cells"] = pd.Series(dict(gap=T.b5.mean() - M.b5.mean(),
        t=stats.ttest_ind(T.b5, M.b5, equal_var=False).statistic, nT=len(T), nM=len(M)))
    out["share_forecast_at_cap"] = float((d.f.abs() >= 19.99).mean())
    out["z_of_capped_forecast"] = d.loc[d.f.abs() >= 19.99, "z"].describe()
    return out
