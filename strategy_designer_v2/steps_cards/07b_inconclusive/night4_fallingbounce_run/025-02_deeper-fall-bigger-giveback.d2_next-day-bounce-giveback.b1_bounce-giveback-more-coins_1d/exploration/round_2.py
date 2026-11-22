def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}
        for h in [1, 3, 5]:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[h] = np.mean(rs)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            vsr = r / r.rolling(20).std()
            n = len(c)
            for h in [1, 3, 5]:
                b[f"u{h}"] = -(c.shift(-h) / c - 1 - drift[h])
            b["vsr"] = vsr
            b["coin"] = coin
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            b["pos"] = np.arange(n)
            rows.append(b[["coin", "year", "pos", "regime", "forecast", "vsr", "u1", "u3", "u5"]])
    df = pd.concat(rows, ignore_index=True)
    df = df.dropna(subset=["vsr"])
    df["falling"] = df["regime"] == "mean_reversion"
    df["vbin"] = pd.cut(df["vsr"], [-99, -1, 0, 0.5, 1, 1.5, 2, 3, 99])

    def tstat(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})

    out = {}
    for name, g in [("falling", df[df.falling]), ("not_falling", df[~df.falling])]:
        res = g.groupby("vbin").apply(lambda s: pd.concat([tstat(s["u1"]).add_prefix("u1_"),
                                                          pd.Series({"u3": s["u3"].mean(), "u5": s["u5"].mean()})]))
        out[f"u1_by_vsr_{name}"] = res
    # all falling-regime bars, 5-day grid, to see drift of falling coins
    fall = df[df.falling]
    out["falling_all_bars_u1"] = tstat(fall["u1"])
    out["falling_all_bars_u5_grid"] = tstat(fall[fall.pos % 5 == 0]["u5"])
    # cases forecast<=-2: up vs down day following share
    cases = df[df.forecast <= -2]
    out["cases_share_next_down"] = pd.Series({"share_u1_pos": (cases["u1"] > 0).mean(),
                                              "median_u1": cases["u1"].median()})
    # grading within years: big vs small half by vsr
    med = cases["vsr"].median()
    cases = cases.assign(big=cases["vsr"] > med)
    out["big_minus_small_by_year"] = cases.groupby("year").apply(
        lambda g: pd.Series({"big": g[g.big]["u1"].mean(), "small": g[~g.big]["u1"].mean(), "n": len(g)}))
    return out
