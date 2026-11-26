import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [2, 5, 10, 20]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr) if rr else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            loc = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            ret1 = pd.Series(c).pct_change()
            sd20 = ret1.rolling(20).std()
            gain = (ret1 / sd20).values
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(c)
            for i in range(n):
                if reg[i] == "chop":
                    continue
                rec = dict(coin=coin, w=w, i=i, cell10=i // 10, reg=reg[i], loc=loc[i],
                           gain=gain[i], fc=fc[i], year=yr[i],
                           ts=str(df["timestamp"].iloc[i])[:10])
                for h in H:
                    if i + h < n:
                        rec[f"u{h}"] = -(c[i + h] / c[i] - 1 - drift[(coin, h)])
                        rec[f"t{h}"] = -(c[i + h] / c[i] - 1)
                    else:
                        rec[f"u{h}"] = np.nan; rec[f"t{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    sit = d[d.reg == "mean_reversion"]
    cases = sit.sort_values("i").groupby(["coin", "w", "cell10"]).head(1)

    def summ(g, col="u10"):
        x = g[col].dropna()
        if len(x) < 3:
            return pd.Series(dict(n=len(x), mean=x.mean(), t=np.nan))
        byday = g.dropna(subset=[col]).groupby("ts")[col].sum()
        nd = len(byday)
        m = x.sum() / len(x)
        # pooled t: daily sums
        t = byday.mean() / (byday.std(ddof=1) / np.sqrt(nd)) if nd > 2 else np.nan
        return pd.Series(dict(n=len(x), days=nd, mean=m, t=t))

    out = {}
    out["cases_by_horizon"] = pd.DataFrame({f"u{h}": summ(cases, f"u{h}") for h in H} |
                                           {f"t{h}": summ(cases, f"t{h}") for h in H}).T
    # baseline: in-profile non-situation bars on 10-grid
    base = d[(d.reg == "unknown") & (d.i % 10 == 0)]
    out["profile_nonsit_grid"] = pd.DataFrame({f"u{h}": summ(base, f"u{h}") for h in H}).T
    allprof = d[d.i % 10 == 0]
    out["profile_all_grid"] = pd.DataFrame({f"u{h}": summ(allprof, f"u{h}") for h in H}).T
    cases = cases.copy()
    cases["locb"] = pd.cut(cases["loc"], [0.74, 0.85, 0.95, 1.01])
    out["by_loc"] = cases.groupby("locb", observed=True).apply(summ)
    cases["gainb"] = pd.cut(cases["gain"], [0, 0.33, 0.66, 1.2])
    out["by_gain"] = cases.groupby("gainb", observed=True).apply(summ)
    cases["fcq"] = pd.qcut(cases["fc"].abs(), 3, duplicates="drop")
    out["by_absfc"] = cases.groupby("fcq", observed=True).apply(summ)
    out["by_coin"] = cases.groupby("coin").apply(summ)
    out["by_window"] = cases.groupby("w").apply(summ)
    out["by_year"] = cases.groupby("year").apply(summ)
    out["corr_loc_u10"] = float(cases[["loc", "u10"]].dropna().corr().iloc[0, 1])
    out["corr_gain_u10"] = float(cases[["gain", "u10"]].dropna().corr().iloc[0, 1])
    return out
