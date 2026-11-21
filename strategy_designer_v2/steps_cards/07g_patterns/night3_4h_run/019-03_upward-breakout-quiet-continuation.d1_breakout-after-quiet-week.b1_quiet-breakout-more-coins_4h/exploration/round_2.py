import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo) / c
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "fwd": c.shift(-H) / c - 1,
                "r1d": c / c.shift(6) - 1,
                "r7d": c / c.shift(42) - 1,
                "vr": rng.rolling(42).mean() / rng.rolling(180).mean(),
                "vr60": rng.rolling(42).mean() / rng.rolling(360).mean(),
                "year": ts.dt.year,
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            g = f.iloc[::H].copy(); g["window"] = w
            recs.append(g)
        d = pd.concat(recs).dropna(subset=["fwd"])
        mu, sd = d["fwd"].mean(), d["fwd"].std()
        d["s"] = (d["fwd"] - mu) / sd
        d["u"] = d["fwd"] - mu
        d["coin"] = coin
        rows.append(d)
    D = pd.concat(rows)
    out = {}
    x = D.dropna(subset=["vr", "s"]).copy()
    x["q"] = x.groupby("coin")["vr"].rank(pct=True)
    x["q5"] = pd.cut(x["q"], [0, .2, .4, .6, .8, 1], labels=False, include_lowest=True)
    out["vr_quintile_unusual_raw"] = x.groupby("q5")["u"].agg(["mean", "median", "count"])
    def tt(g):
        top = g.loc[g.q5 == 4, "s"]; bot = g.loc[g.q5 == 0, "s"]
        r = stats.spearmanr(g["vr"], g["s"])[0] if len(g) > 10 else np.nan
        return pd.Series({"n": len(g), "rho": r, "top_minus_bot_s": top.mean() - bot.mean(),
                          "t": stats.ttest_ind(top, bot, equal_var=False).statistic if len(top) > 2 and len(bot) > 2 else np.nan,
                          "top_u": x.loc[top.index.intersection(g.index)].shape[0]})
    out["vr_by_year"] = x.groupby("year").apply(tt)
    out["vr_by_coin"] = x.groupby("coin").apply(tt)
    # loud & direction of 7d move
    y = x.dropna(subset=["r7d"]).copy()
    y["loud"] = y["q"] > 2/3
    y["dir"] = np.where(y["r7d"] > 0, "up7d", "down7d")
    gg = y.groupby(["loud", "dir"])["s"].agg(["mean", "count", "std"])
    gg["t"] = gg["mean"] / (gg["std"] / np.sqrt(gg["count"]))
    out["loud_x_dir"] = gg
    # graded inside loud: spearman vr vs s within loud & up7d, within loud & down7d
    res = {}
    for k, g in y.groupby(["loud", "dir"]):
        r, p = stats.spearmanr(g["vr"], g["s"]); res[str(k)] = {"rho": r, "p": p, "n": len(g)}
    out["graded_within"] = pd.DataFrame(res).T
    # 60d version
    z = D.dropna(subset=["vr60", "s"])
    out["vr60_spearman"] = pd.Series(stats.spearmanr(z["vr60"], z["s"]), index=["rho", "p"])
    # r1d reversal by year
    r1 = D.dropna(subset=["r1d", "s"])
    out["r1d_by_year"] = r1.groupby("year").apply(lambda g: pd.Series({"rho": stats.spearmanr(g["r1d"], g["s"])[0], "n": len(g)}))
    # book long when loud vs quiet: alloc mean by vr quintile
    out["book_alloc_by_vr_q"] = x.groupby("q5")["alloc"].agg(["mean", lambda v: (v > 0).mean()])
    return out
