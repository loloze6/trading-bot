import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d.dropna(subset=["book_return", "coin_return"]).copy()
            dd["coin"] = c; dd["w"] = w
            dd["year"] = pd.to_datetime(dd["day"]).dt.year
            rows.append(dd)
    D = pd.concat(rows)
    g = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    g["book_sharpe"] = D.groupby("coin")["book_return"].apply(lambda x: x.mean() / x.std() * np.sqrt(365))
    out["book_by_coin"] = g
    out["book_by_year"] = D.groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))

    # bar-level gain, fees
    recs = []; grid = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            pos = b["postRebalance_current_allocation"].fillna(0).values
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            recs.append(pd.DataFrame({"coin": c, "gross": pos * nxt, "fee": fee.values, "pos": pos}))
            r72 = pd.Series(cl).pct_change(72).values
            r24 = pd.Series(cl).pct_change(24).values
            r720 = pd.Series(cl).pct_change(720).values
            vol = pd.Series(np.log(cl)).diff().rolling(72).std().values
            fwd = np.r_[cl[72:] / cl[:-72] - 1, [np.nan] * 72]
            idx = np.arange(0, len(b), 72)
            grid.append(pd.DataFrame({"coin": c, "w": w, "r72": r72[idx], "r24": r24[idx], "r720": r720[idx],
                                      "vol": vol[idx], "fwd": fwd[idx],
                                      "fc": b["forecast"].values[idx],
                                      "reg": b["regime"].values[idx],
                                      "year": pd.to_datetime(b["timestamp"]).dt.year.values[idx]}))
    R = pd.concat(recs)
    out["gross_fee_by_coin_per_bar"] = R.groupby("coin")[["gross", "fee", "pos"]].mean()
    G = pd.concat(grid).dropna(subset=["fwd", "r72"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    dn = G[G["r72"] < 0].copy()
    up = G[G["r72"] >= 0]
    out["fwd_down_vs_up"] = pd.DataFrame({"down_mean_ex": [dn["ex"].mean()], "up_mean_ex": [up["ex"].mean()],
                                          "t": [stats.ttest_ind(dn["ex"], up["ex"], equal_var=False).statistic],
                                          "n_down": [len(dn)], "n_up": [len(up)]})
    dn["r72q"] = dn.groupby("coin")["r72"].transform(lambda x: pd.qcut(x, 4, labels=False))
    out["down_by_fall_quartile"] = dn.groupby("r72q")["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d2 = dn.dropna(subset=["r720"])
    d2["trend"] = np.where(d2["r720"] > 0, "30d_up", "30d_down")
    out["down_by_30d_trend"] = d2.groupby("trend")["ex"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    d3 = dn.dropna(subset=["fc"])
    d3["fcq"] = pd.qcut(d3["fc"].rank(method="first"), 4, labels=False)
    out["down_by_fc_quartile"] = d3.groupby("fcq")["ex"].agg(["mean", "count"])
    out["down_fcq_x_trend"] = d3.dropna(subset=["r720"]).assign(tr=lambda x: x["r720"] > 0).groupby(["tr", "fcq"])["ex"].agg(["mean", "count"])
    out["down_by_year"] = dn.groupby("year")["ex"].agg(["mean", "count"])
    dn["volq"] = dn.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["down_by_vol_tercile"] = dn.groupby("volq")["ex"].agg(["mean", "count"])
    return out
