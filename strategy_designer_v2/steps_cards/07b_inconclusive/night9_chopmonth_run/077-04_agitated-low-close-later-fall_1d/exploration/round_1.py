import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 6, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # drift per horizon over all windows, non-overlapping grid
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (hi - c) / np.where(rng > 0, rng, 1), np.nan)  # 0 high, 1 low
            ret60 = pd.Series(c).pct_change(60).values
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n):
                r = {}
                for h in H:
                    r[h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(dict(coin=coin, win=w, pos=i, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 cl_today=cl[i], cl_prev=cl[i - 1] if i > 0 else np.nan,
                                 reg=reg[i], fc=fc[i], ret60=ret60[i], dayret=(c[i]/c[i-1]-1) if i>0 else np.nan,
                                 **{f"r{h}": r[h] for h in H}))
    A = pd.DataFrame(rows)
    for h in H:
        A[f"u{h}"] = A[f"r{h}"] - A["coin"].map(lambda k: drift[(k, h)][0])
    def ct(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5: return (len(s), np.nan, np.nan, np.nan)
        g = s.groupby("day")[col].sum()
        m = s[col].mean()
        dev = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return (len(s), s.groupby('day').ngroups, m, m / se if se > 0 else np.nan)
    def tab(sub, col, by):
        out = []
        for k, g in sub.groupby(by):
            n, d, m, t = ct(g, col)
            out.append(dict(key=str(k), n=n, days=d, mean=m, t=t))
        return pd.DataFrame(out)
    res = {}
    # cases: active short bars on 6-grid (short sign: -u)
    act = A[A["fc"] < 0].copy()
    act["cell"] = act["pos"] // 6
    cases = act.sort_values("pos").groupby(["coin", "win", "cell"]).head(1).copy()
    for h in H:
        cases[f"s{h}"] = -cases[f"u{h}"]
    res["cases_by_horizon_shortdir"] = pd.DataFrame([dict(h=h, **dict(zip(["n","days","mean","t"], ct(cases, f"s{h}")))) for h in H])
    res["cases_by_coin_s6"] = tab(cases, "s6", "coin")
    res["cases_by_window_s6"] = tab(cases, "s6", "win")
    cases["trend"] = pd.cut(cases["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    res["cases_by_trend_s6"] = tab(cases, "s6", "trend")
    cases["clb"] = pd.cut(cases["cl_prev"], [0.75, 0.85, 0.95, 1.01], include_lowest=True)
    res["cases_by_clprev_s6"] = tab(cases, "s6", "clb")
    cases["drb"] = pd.qcut(cases["dayret"].shift(0), 3, labels=["prevday_low", "mid", "high"]) if False else None
    # agitated bars, all close locations, signal = today's close location -> forward returns from today (long direction)
    ag = A[(A["reg"] != "chop") & A["cl_today"].notna()].copy()
    ag["cell"] = ag["pos"] // 6
    ag["clq"] = pd.cut(ag["cl_today"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["top", "uppermid", "lowmid", "bottom"])
    g1 = ag[ag["pos"] % 6 == 0]
    for h in [1, 6]:
        res[f"agitated_by_clq_long_u{h}"] = tab(g1, f"u{h}", "clq")
    # skip-day version on agitated: return from day+1 to day+7 (u6 at lag) = cl_prev buckets on grid
    ag2 = A[(A["reg"] != "chop") & A["cl_prev"].notna()].copy()
    ag2["clq"] = pd.cut(ag2["cl_prev"], [-0.01, 0.25, 0.5, 0.75, 1.01], labels=["top", "uppermid", "lowmid", "bottom"])
    g2 = ag2[ag2["pos"] % 6 == 0]
    res["agitated_by_clprev_long_u6"] = tab(g2, "u6", "clq")
    g2t = g2.copy(); g2t["trend"] = pd.cut(g2t["ret60"], [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    g2t["k"] = g2t["trend"].astype(str) + "_" + g2t["clq"].astype(str)
    res["agitated_trend_x_clprev_long_u6"] = tab(g2t, "u6", "k")
    res["calm_by_clprev_long_u6"] = tab(A[(A["reg"] == "chop") & (A["pos"] % 6 == 0)].assign(clq=lambda d: pd.cut(d["cl_prev"], [-0.01,0.25,0.5,0.75,1.01], labels=["top","uppermid","lowmid","bottom"])), "u6", "clq")
    res["regimes"] = A["reg"].value_counts()
    return res
