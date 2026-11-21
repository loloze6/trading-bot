def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        wl = list(wins.keys())
        for wi, w in enumerate(wl):
            b = wins[w]
            c = b["close"].astype(float).reset_index(drop=True)
            if len(c) < 900:
                continue
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            sc24 = r24 / r24.abs().rolling(720, min_periods=360).mean()
            r168 = c / c.shift(168) - 1
            sc168 = r168 / r168.abs().rolling(720, min_periods=360).mean()
            depth = c / c.rolling(720, min_periods=360).max() - 1
            for h in (72, 168):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(c), h)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "half": int(wi >= len(wl) / 2), "h": h,
                    "fwd": fwd.iloc[idx].values, "sc24": sc24.iloc[idx].values,
                    "sc168": sc168.iloc[idx].values, "depth": depth.iloc[idx].values,
                    "yr": ts.iloc[idx].dt.year.values, "wd": ts.iloc[idx].dt.weekday.values}))
    D = pd.concat(rows).dropna(subset=["fwd"])
    g = D.groupby(["coin", "h"])["fwd"]
    D["unus"] = D["fwd"] - g.transform("mean")
    D["str"] = D["unus"] / g.transform("std")
    out = {}
    def qb(x, var, q=5):
        return x.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
    def summ(x, keys):
        t = x.groupby(keys).agg(n=("unus", "size"), unus=("unus", "mean"), strength=("str", "mean"), sd=("unus", "std"))
        t["t"] = t.unus / (t.sd / np.sqrt(t.n))
        return t.drop(columns="sd").round(4)
    for var, h in [("sc168", 72), ("sc168", 168), ("depth", 168), ("sc24", 72)]:
        x = D[D.h == h].dropna(subset=[var]).copy()
        x["b"] = qb(x, var)
        top = x[x.b == 4]; bot = x[x.b == 0]
        out[f"{var}_h{h}_top_by_coin"] = summ(top, "coin")
        out[f"{var}_h{h}_top_by_half"] = summ(top, "half")
        out[f"{var}_h{h}_top_by_year"] = summ(top, "yr")
        if var == "sc24":
            out["sc24_h72_bot_by_coin"] = summ(bot, "coin")
            out["sc24_h72_bot_by_half"] = summ(bot, "half")
        # top minus rest, Welch
        rest = x[x.b != 4]
        tt = stats.ttest_ind(top.unus, rest.unus, equal_var=False)
        out[f"{var}_h{h}_top_minus_rest"] = f"diff {top.unus.mean()-rest.unus.mean():.4f}, t {tt.statistic:.2f}, n {len(top)}/{len(rest)}"
        # per-coin Spearman over all cases
        pc = []
        for coin, y in x.groupby("coin"):
            rho, p = stats.spearmanr(y[var], y["unus"])
            pc.append({"coin": coin, "n": len(y), "rho": round(rho, 3), "p": round(p, 3)})
        out[f"{var}_h{h}_spearman_by_coin"] = pd.DataFrame(pc).set_index("coin")
    x = D[D.h == 72]
    out["weekday_h72_by_half"] = summ(x, ["wd", "half"])
    out["weekday_h72_t"] = summ(x, "wd")
    return out
