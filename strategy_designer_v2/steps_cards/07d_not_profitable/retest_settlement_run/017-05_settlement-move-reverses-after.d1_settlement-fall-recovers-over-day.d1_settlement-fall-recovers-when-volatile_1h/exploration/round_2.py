def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    drift = {}
    for coin in bars:
        r = []
        for w, df in bars[coin].items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            r += list(c[idx + 24] / c[idx] - 1)
        drift[coin] = np.mean(r)
    rows = []; brows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"]; n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            ch = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            hr = np.log(c).diff()
            vol7 = hr.rolling(168).std()
            vr = (vol7 / vol7.rolling(720, min_periods=200).mean()).values
            r30 = (c / c.shift(720) - 1).values
            r7 = (c / c.shift(168) - 1).values
            a = df["postRebalance_current_allocation"].values
            g = np.full(n, np.nan); g[:n-1] = a[:n-1] * (c.values[1:] / c.values[:-1] - 1)
            brows.append(pd.DataFrame({"g": g, "a": a, "r30": r30, "vr": vr, "coin": coin}))
            for h in (24, 72):
                fwd = np.full(n, np.nan); fwd[:n-h] = c.values[h:] / c.values[:n-h] - 1
                d = pd.DataFrame({"cell": np.arange(n)//h, "sett": np.isin(ch, [0, 16]), "f": df["forecast"].values,
                                  "fwd": fwd, "vr": vr, "r30": r30, "r7": r7})
                s = d[d.sett].groupby("cell").first().dropna(subset=["fwd", "r30"])
                rows.append(s.assign(coin=coin, h=h))
    R = pd.concat(rows)
    R["ex"] = R["fwd"] - R["coin"].map(drift) * R["h"] / 24
    def summ(g):
        return pd.Series({"n": len(g), "tot%": 100*g.fwd.mean(), "ex%": 100*g.ex.mean(),
                          "t": g.ex.mean()/(g.ex.std()/np.sqrt(len(g)))})
    R["up30"] = R["r30"] > 0
    R["up7"] = R["r7"] > 0
    R["hivr"] = R["vr"] > 1.0
    R["strong"] = R["f"] >= 2
    R["fb"] = pd.cut(R["f"], [-0.01, 0.0001, 2, 5, 10, 30])
    out["by h x up30 x strong"] = R.groupby(["h", "up30", "strong"]).apply(summ)
    out["by h x up7 x strong"] = R.groupby(["h", "up7", "strong"]).apply(summ)
    U = R[R.up30]
    out["up30: by h x forecast bucket"] = U.groupby(["h", "fb"]).apply(summ)
    out["by h x up30 x hivr (strong only)"] = R[R.strong].groupby(["h", "up30", "hivr"]).apply(summ)
    B = pd.concat(brows).dropna(subset=["g", "r30"])
    B["up30"] = B["r30"] > 0
    B["in"] = B["a"].abs() > 1e-6
    out["book bar gain by up30 (in position)"] = B[B["in"]].groupby("up30").agg(n=("g", "count"), mean_bp=("g", lambda x: 1e4*x.mean()),
        sum_share=("g", "sum"), alloc=("a", "mean"))
    # deepest fall: per coin per window, worst drawdown of book and coin
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            bv = d["book_value"]; cv = d["close"]
            bd = (bv / bv.cummax() - 1).min(); cd = (cv / cv.cummax() - 1).min()
            dd.append({"window": w, "book_dd": bd, "coin_dd": cd})
    DD = pd.DataFrame(dd).groupby("window").mean()
    out["window mean deepest fall book vs coin"] = DD.sort_values("book_dd").head(8)
    return out
