import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 6, 6):
                rs.append(c[i + 6] / c[i] - 1)
        drift[coin] = np.mean(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values; o = df["open"].values
            rng = (hi - lo) / c
            rngrel = rng / pd.Series(rng).shift(1).rolling(20, min_periods=10).mean().values
            cl = np.where(hi > lo, (hi - c) / np.where(hi > lo, hi - lo, 1), np.nan)
            ret5 = pd.Series(c).pct_change(5).values
            ts = pd.to_datetime(df["timestamp"])
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values
            n = len(c)
            for i in range(1, n - 6):
                rows.append(dict(coin=coin, win=w, pos=i, day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                 reg=reg[i], fc=fc[i], cl_prev=cl[i-1],
                                 rr_prev=rngrel[i-1], dret_prev=c[i-1]/c[i-2]-1 if i >= 2 else np.nan,
                                 ret5_prev=ret5[i-1], body_prev=(c[i-1]-o[i-1])/c[i-1],
                                 u6=c[i+6]/c[i]-1-drift[coin]))
    A = pd.DataFrame(rows)
    def ct(s, col="s6"):
        s = s.dropna(subset=[col])
        if len(s) < 8: return dict(n=len(s), days=np.nan, mean=np.nan, t=np.nan)
        m = s[col].mean()
        dev = s.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return dict(n=len(s), days=s["day"].nunique(), mean=m, t=m / se)
    def tab(s, by, col="s6"):
        return pd.DataFrame([dict(key=str(k), **ct(g, col)) for k, g in s.groupby(by, observed=True)])
    act = A[A["fc"] < 0].copy()
    act["cell"] = act["pos"] // 6
    cases = act.sort_values("pos").groupby(["coin", "win", "cell"]).head(1).copy()
    cases["s6"] = -cases["u6"]
    res = {}
    res["all_cases"] = pd.DataFrame([ct(cases)])
    res["by_year"] = tab(cases, "year")
    cases["rrq"] = pd.qcut(cases["rr_prev"], 3, labels=["narrow", "mid", "wide"])
    res["by_prev_range_rel"] = tab(cases, "rrq")
    cases["dq"] = pd.qcut(cases["dret_prev"], 3, labels=["bigfall", "mid", "up_or_small"])
    res["by_prev_day_return"] = tab(cases, "dq")
    cases["r5q"] = pd.qcut(cases["ret5_prev"], 3, labels=["fell5d", "mid", "rose5d"])
    res["by_prev_5d_return"] = tab(cases, "r5q")
    cases["bq"] = pd.qcut(cases["body_prev"], 3, labels=["red_body", "mid", "green_or_small"])
    res["by_prev_body"] = tab(cases, "bq")
    cases["k"] = cases["rrq"].astype(str) + "_" + cases["dq"].astype(str)
    res["range_x_dayret"] = tab(cases, "k")
    # agitated grid bars, all closes, low-close side graded: correlation by window sign
    ag = A[(A["reg"] != "chop") & (A["pos"] % 6 == 0)].dropna(subset=["cl_prev", "u6"]).copy()
    ag["s6"] = -ag["u6"]
    ag["bot"] = ag["cl_prev"] >= 0.75
    res["agitated_bottom_vs_rest_by_window"] = pd.DataFrame(
        [dict(win=w, bottom=g[g.bot]["s6"].mean(), rest=g[~g.bot]["s6"].mean(), nb=int(g.bot.sum()))
         for w, g in ag.groupby("win")])
    return res
