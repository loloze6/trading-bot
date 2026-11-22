import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            hi = c.rolling(30).max(); lo = c.rolling(30).min()
            rng = (hi - lo).replace(0, np.nan)
            pos = (c - (hi + lo) / 2) / (rng / 2)
            net = (c - c.shift(29)).abs()
            flat = 1 - net / rng
            ret90 = c / c.shift(90) - 1
            year = pd.to_datetime(d["timestamp"]).dt.year
            for h in [3, 5, 10]:
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(d), h)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h,
                    "pos": pos.iloc[idx].values, "flat": flat.iloc[idx].values,
                    "ret90": ret90.iloc[idx].values,
                    "mr": (d["regime"].iloc[idx] == "mean_reversion").values,
                    "fc": d["forecast"].iloc[idx].values,
                    "fwd": fwd.iloc[idx].values, "year": year.iloc[idx].values}))
    A = pd.concat(rows).dropna(subset=["fwd"])
    A["un"] = A["fwd"] - A.groupby(["coin", "h"])["fwd"].transform("mean")
    A = A.dropna(subset=["pos", "flat"])
    A["g"] = A["pos"] * A["flat"]
    out = {}
    def sl(g):
        if len(g) < 15: return pd.Series({"n": len(g), "spear": np.nan, "slope": np.nan, "t": np.nan})
        r = stats.linregress(g["g"], g["un"])
        return pd.Series({"n": len(g), "spear": stats.spearmanr(g["g"], g["un"])[0],
                          "slope": r.slope, "t": r.slope / r.stderr})
    out["slope_g_by_h_mr"] = A.groupby(["h", "mr"]).apply(sl)
    B = A[A.h == 5]
    Bm = B[B.mr]
    out["h5_mr_by_coin"] = Bm.groupby("coin").apply(sl)
    out["h5_mr_by_year"] = Bm.groupby("year").apply(sl)
    out["h5_mr_by_flat_tercile"] = Bm.assign(ft=pd.qcut(Bm.flat, 3, labels=["trendy", "mid", "flat"])).groupby("ft").apply(sl)
    out["h5_by_ret90_quint"] = B.dropna(subset=["ret90"]).assign(q=pd.qcut(B.dropna(subset=["ret90"]).ret90, 5, labels=False)).groupby("q").apply(sl)
    # top vs bottom quintile difference in mr, Welch
    q = pd.qcut(Bm.pos, 5, labels=False)
    top = Bm.un[q == 4]; bot = Bm.un[q == 0]
    out["h5_mr_topq_minus_botq"] = pd.Series({"diff": top.mean() - bot.mean(),
        "welch_t": stats.ttest_ind(top, bot, equal_var=False).statistic,
        "top_mean": top.mean(), "top_t": top.mean()/(top.std()/np.sqrt(len(top))), "n_top": len(top),
        "bot_mean": bot.mean(), "bot_t": bot.mean()/(bot.std()/np.sqrt(len(bot))), "n_bot": len(bot)})
    # step5 cases by coin
    C = B[B.fc <= -2]
    out["step5_cases_by_coin"] = C.groupby("coin")["un"].agg(["count", "mean"])
    out["step5_cases_by_year"] = C.groupby("year")["un"].agg(["count", "mean"])
    return out
