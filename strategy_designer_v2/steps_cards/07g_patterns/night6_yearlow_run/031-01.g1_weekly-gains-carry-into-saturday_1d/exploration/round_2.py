def explore(data):
    import pandas as pd, numpy as np
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                "pos": np.arange(len(b)),
                "r1": r1, "r4prev": c.shift(1) / c.shift(5) - 1, "r5": c / c.shift(5) - 1,
                "vol": vol,
                "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1, "fwd3": c.shift(-3) / c - 1,
                "fwd1b": c.shift(-2) / c.shift(-1) - 1,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["nextwd"] = (d["wd"] + 1) % 7
    for h, col in [(1, "fwd1"), (2, "fwd2"), (3, "fwd3")]:
        d["ex%d" % h] = d[col] - d.groupby("coin")[col].transform("mean")
    d["exb"] = d["fwd1b"] - d.groupby("coin")["fwd1"].transform("mean")
    d["z1"] = d["r1"] / d["vol"]
    d["z4"] = d["r4prev"] / (d["vol"] * 2)
    d["z5"] = d["r5"] / (d["vol"] * np.sqrt(5))
    out = {}

    def daytt(s, col):
        s = s.dropna(subset=[col])
        n = len(s); m = s[col].mean()
        gs = (s[col] - m).groupby(s["day"]).sum(); D = len(gs)
        if D < 3: return (np.nan, np.nan, D)
        se = np.sqrt((gs**2).sum() * D / (D - 1)) / n
        return (m, m / se, D)

    # A: decompose Friday's weekly return: Friday's own day vs the 4 days before
    r = []
    for wd in range(7):
        s = d[d.nextwd == wd].dropna(subset=["z1", "z4", "ex1"])
        a = daytt(s.assign(x=s.z1 * s.ex1), "x"); b = daytt(s.assign(x=s.z4 * s.ex1), "x")
        r.append((wd, a[0], a[1], b[0], b[1], a[2]))
    out["slope proxy: z1 and z4prev x next excess, by next weekday"] = pd.DataFrame(
        r, columns=["nextwd", "z1prod", "z1t", "z4prod", "z4t", "days"])

    # B: Friday z5 quintile -> Sat, Sun (day after), and Fri->Mon
    fri = d[d.nextwd == 5].dropna(subset=["z5"]).copy()
    fri["q"] = pd.qcut(fri["z5"], 5, labels=False)
    r = []
    for q, s in fri.groupby("q"):
        r.append((q, *daytt(s, "ex1")[:2], *daytt(s, "exb")[:2], *daytt(s, "ex3")[:2], len(s)))
    out["Fri z5 quintile: Sat ex, Sun ex, Fri->Mon ex"] = pd.DataFrame(
        r, columns=["q", "sat", "sat_t", "sun", "sun_t", "3d", "3d_t", "n"])

    # C: Saturday's own move -> Sunday (Sat bars, next Sunday)
    sat = d[d.nextwd == 6].dropna(subset=["z1", "ex1"]).copy()
    sat["q"] = pd.qcut(sat["z1"], 5, labels=False)
    r = []
    for q, s in sat.groupby("q"):
        r.append((q, *daytt(s, "ex1")[:2], len(s)))
    out["Sat own z1 quintile -> Sunday excess"] = pd.DataFrame(r, columns=["q", "mean", "t", "n"])

    # D: non-overlapping grid by weekday-specific moves: Friday z1 quintile -> Sat
    fri2 = d[d.nextwd == 5].dropna(subset=["z1", "ex1"]).copy()
    fri2["q"] = pd.qcut(fri2["z1"], 5, labels=False)
    r = []
    for q, s in fri2.groupby("q"):
        r.append((q, *daytt(s, "ex1")[:2], len(s)))
    out["Fri own z1 quintile -> Sat excess"] = pd.DataFrame(r, columns=["q", "mean", "t", "n"])

    # E: book: share of gain by coin and top/bottom days of book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["win"] = w
            x["wd"] = pd.to_datetime(x["day"], utc=True).dt.weekday
            bk.append(x)
    bk = pd.concat(bk, ignore_index=True)
    bookd = bk.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"),
                                            wd=("wd", "first")).dropna()
    out["book mean return by weekday"] = bookd.groupby("wd")["br"].agg(["mean", "count", "sum"])
    out["book by coin: mean daily return"] = bk.groupby("coin")["book_return"].mean()
    top = bookd["br"].quantile(0.99); bot = bookd["br"].quantile(0.01)
    out["book top1% / bottom1% days: mean coin return that day"] = pd.Series({
        "top_n": (bookd.br >= top).sum(), "top_coinret": bookd.loc[bookd.br >= top, "cr"].mean(),
        "bot_n": (bookd.br <= bot).sum(), "bot_coinret": bookd.loc[bookd.br <= bot, "cr"].mean(),
        "share_of_total_gain_top1pct": bookd.loc[bookd.br >= top, "br"].sum() / bookd.br.sum()})
    return out
