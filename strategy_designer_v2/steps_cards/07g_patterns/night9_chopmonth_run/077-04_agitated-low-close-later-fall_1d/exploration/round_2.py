def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            n = len(b)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            rng = h - l
            cl = np.where(rng > 0, (c - l) / rng, np.nan)  # 1 high, 0 low
            ts = pd.to_datetime(b["timestamp"])
            reg = b["regime"].astype(str).values
            ret60 = np.full(n, np.nan); ret60[60:] = c[60:] / c[:-60] - 1
            f1to7 = np.full(n, np.nan)
            if n > 7: f1to7[:n-7] = c[7:] / c[1:n-6] - 1
            f1 = np.full(n, np.nan); f1[:n-1] = c[1:] / c[:-1] - 1
            f6 = np.full(n, np.nan)
            if n > 6: f6[:n-6] = c[6:] / c[:-6] - 1
            # agitation at next bar (signal bar) = regime of bar t+1 != chop
            agn = np.full(n, False); agn[:n-1] = reg[1:] != "chop"
            ag0 = reg != "chop"
            for i in range(n):
                rows.append((coin, w, i, ts[i].normalize(), ts[i].year, cl[i], f1[i], f6[i], f1to7[i], ret60[i], ag0[i], agn[i]))
    df = pd.DataFrame(rows, columns=["coin","w","pos","day","yr","cl","f1","f6","f17","r60","ag0","agn"])
    # drift: coin mean 6-bar return on 6-grid (from each bar) used for f17 (6-bar stretch)
    g6 = df[df.pos % 6 == 0]
    dr6 = g6.groupby("coin")["f6"].mean()
    df["f17x"] = df["f17"] - df.coin.map(dr6)
    g1 = df.groupby("coin")["f1"].mean()
    df["f1x"] = df["f1"] - df.coin.map(g1)
    def ct(x, days):
        x = np.asarray(x); m = x.mean(); N = len(x)
        S = pd.Series(x - m).groupby(np.asarray(days)).sum()
        return m, len(S), m / (np.sqrt((S**2).sum()) / N), N
    out = {}
    df["q"] = pd.cut(df.cl, [-0.01, .25, .5, .75, 1.01], labels=["low", "q2", "q3", "high"])
    # all 7 grid offsets averaged: cases on grid pos%7==k; report clustered t per offset for low and high in agitated
    res = []
    for k in range(7):
        g = df[(df.pos % 7 == k) & df.agn].dropna(subset=["f17x", "q"])
        for q in ["low", "high"]:
            s = g[g.q == q]
            m, nd, t, N = ct(s.f17x, s.day)
            res.append((k, q, round(m, 4), N, nd, round(t, 2)))
    out["offsets_agn_f17x"] = pd.DataFrame(res, columns=["off", "q", "mean", "N", "days", "t_day"])
    # full-sample graded (all bars, overlapping; read only mean by quartile, as description) and grid-0 clustered
    g = df[(df.pos % 7 == 0)].dropna(subset=["f17x", "q"])
    res = []
    for a in [False, True]:
        for q in ["low", "q2", "q3", "high"]:
            s = g[(g.agn == a) & (g.q == q)]
            m, nd, t, N = ct(s.f17x, s.day)
            res.append((a, q, round(m, 4), N, nd, round(t, 2)))
    out["grid0_by_agn_q"] = pd.DataFrame(res, columns=["agit", "q", "mean", "N", "days", "t_day"])
    # by window, agitated, high minus low mean (grid all offsets pooled, descriptive)
    a = df[df.agn].dropna(subset=["f17x", "q"])
    pw = a.groupby(["w", "q"])["f17x"].mean().unstack()[["low", "high"]]
    pw["high_minus_low"] = pw["high"] - pw["low"]
    out["by_window_pooled"] = pw.round(4)
    py = a.groupby(["yr", "q"])["f17x"].mean().unstack()[["low", "high"]]
    py["hml"] = py["high"] - py["low"]
    out["by_year_pooled"] = py.round(4)
    # trend split, grid 0 clustered
    df["tr"] = np.where(df.r60 > .1, "rising", np.where(df.r60 < -.1, "falling", np.where(df.r60.notna(), "choppy", "na")))
    g = df[(df.pos % 7 == 0) & df.agn & (df.tr != "na")].dropna(subset=["f17x", "q"])
    res = []
    for tr in ["rising", "choppy", "falling"]:
        for q in ["low", "q2", "q3", "high"]:
            s = g[(g.tr == tr) & (g.q == q)]
            if len(s) > 3:
                m, nd, t, N = ct(s.f17x, s.day)
                res.append((tr, q, round(m, 4), N, nd, round(t, 2)))
    out["trend_grid0"] = pd.DataFrame(res, columns=["tr", "q", "mean", "N", "days", "t_day"])
    # next-day reversal, agitated, grid 1 (all bars) clustered
    res = []
    for q in ["low", "q2", "q3", "high"]:
        s = df[df.agn & (df.q == q)].dropna(subset=["f1x"])
        m, nd, t, N = ct(s.f1x, s.day)
        res.append((q, round(m, 4), N, nd, round(t, 2)))
    out["nextday_agn"] = pd.DataFrame(res, columns=["q", "mean", "N", "days", "t_day"])
    # by coin pooled high-minus-low agitated
    pc = a.groupby(["coin", "q"])["f17x"].mean().unstack()[["low", "high"]]
    pc["hml"] = pc["high"] - pc["low"]
    out["by_coin_pooled"] = pc.round(4)
    return out
