import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rr = ((h - l) / c).rolling(30, min_periods=20).mean()
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "s3": (c / c.shift(3) - 1) / rr,
                "s3sd": (c / c.shift(3) - 1) / (sd30 * np.sqrt(3)),
                "s1": r1 / sd30,
                "r60": c / c.shift(60) - 1,
                "r30": c / c.shift(30) - 1,
                "sd30": sd30,
                "sd90": r1.rolling(90, min_periods=60).std(),
                "f7": c.shift(-7) / c - 1, "f3": c.shift(-3) / c - 1, "f1": c.shift(-1) / c - 1,
                "day": ts.dt.floor("D"), "wd": ts.dt.dayofweek, "yr": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["agit"] = np.where(df.sd30 > df.sd90, "agit", "calm")
            df.loc[df.sd90.isna(), "agit"] = np.nan
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for hz in [7, 3, 1]:
        m = A[A.pos % hz == 0].groupby("coin")[f"f{hz}"].mean()
        A[f"x{hz}"] = A[f"f{hz}"] - A["coin"].map(m)
    A["trend"] = np.where(A.r30 > .1, "rising", np.where(A.r30 < -.1, "falling", "choppy"))
    A.loc[A.r30.isna(), "trend"] = np.nan

    def daycl(G, y):
        s = G.groupby("day")[y].sum()
        n = G.groupby("day")[y].size().sum()
        return pd.Series({"n": len(G), "days": len(s), "mean": G[y].mean(), "t_day": s.mean() / (s.std() / np.sqrt(len(s)))})

    def slope_t(G, x, y):
        G = G.dropna(subset=[x, y])
        r = stats.linregress(G[x], G[y])
        return pd.Series({"n": len(G), "slope": r.slope, "t": r.slope / r.stderr})

    # 1) agitated: 3-day rise -> next 7 (graded) and 3
    for hz in [7, 3]:
        G = A[(A.pos % hz == 0)].dropna(subset=["s3", f"x{hz}", "agit"])
        res = {}
        for ag in ["agit", "calm"]:
            for side in ["up", "dn"]:
                g = G[(G.agit == ag) & ((G.s3 > 0) if side == "up" else (G.s3 < 0))]
                res[(ag, side)] = pd.concat([slope_t(g, "s3", f"x{hz}"), daycl(g[g.s3.abs() > g.s3.abs().quantile(.5)], f"x{hz}").add_prefix("top_")])
        out[f"agit_s3_side_x{hz}"] = pd.DataFrame(res).T.round(4)
    # by trend within agitated, up side, x3
    G = A[(A.pos % 3 == 0)].dropna(subset=["s3", "x3", "agit", "trend"])
    res = {}
    for tr in ["rising", "choppy", "falling"]:
        g = G[(G.agit == "agit") & (G.trend == tr) & (G.s3 > 0)]
        res[tr] = slope_t(g, "s3", "x3")
    out["agit_up_by_trend_x3"] = pd.DataFrame(res).T.round(4)
    # by window half / year stability for agit up x3
    g = G[(G.agit == "agit") & (G.s3 > 0)]
    out["agit_up_by_year_x3"] = g.groupby("yr").apply(lambda q: slope_t(q, "s3", "x3")).round(4)
    # 2) one-day scaled return -> next day, by agit, both sides
    G1 = A.dropna(subset=["s1", "x1", "agit"])
    res = {}
    for ag in ["agit", "calm"]:
        for side in ["up", "dn"]:
            g = G1[(G1.agit == ag) & ((G1.s1 > 0) if side == "up" else (G1.s1 < 0))]
            res[(ag, side)] = pd.concat([slope_t(g, "s1", "x1"), daycl(g, "x1")])
    out["s1_agit_side_x1"] = pd.DataFrame(res).T.round(4)
    # up day next day by trend (all agit)
    res = {}
    for tr in ["rising", "choppy", "falling"]:
        g = G1[(G1.trend == tr) & (G1.s1 > 0)]
        res[tr] = pd.concat([slope_t(g, "s1", "x1"), daycl(g, "x1")])
    out["s1_up_by_trend_x1"] = pd.DataFrame(res).T.round(4)
    # 3) weekday by year (Thu+Fri minus Mon+Wed)
    A["wdg"] = A.wd.map({3: "ThFr", 4: "ThFr", 0: "MoWe", 2: "MoWe"})
    g = A.dropna(subset=["x1", "wdg"]).groupby(["yr", "wdg"])["x1"].mean().unstack()
    out["weekday_by_year"] = (g * 1e4).round(1)
    # 4) book: largest gain/loss days, what preceded
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk.book_return.quantile([.02, .98])
    out["book_tail"] = pd.DataFrame({
        "worst2%": bk[bk.book_return <= q.iloc[0]].mean(),
        "best2%": bk[bk.book_return >= q.iloc[1]].mean(),
        "all": bk.mean()}).round(4)
    # positions: allocation level vs next day return
    P = A.dropna(subset=["alloc", "x1"]).copy()
    P["aq"] = pd.cut(P.alloc, [-0.01, 0.01, 0.5, 1.0, 3])
    out["alloc_bin_x1"] = P.groupby("aq")["x1"].agg(["size", "mean"]).round(5)
    return out
