def explore(data):
    import pandas as pd, numpy as np
    out = {}
    hz = []; B = []
    for coin, wins in data["bars"].items():
        allg = []
        for w, b in wins.items():
            c = b["close"]; idx = np.arange(0, len(b) - 72, 72)
            allg.append((c.shift(-72) / c - 1).iloc[idx])
        mu72 = pd.concat(allg).mean()
        for w, b in wins.items():
            c = b["close"]; f = b["forecast"]; a = b["postRebalance_current_allocation"]
            r1 = c.shift(-1) / c - 1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            chg = (a - b["previous_allocation"]).abs()
            fs = np.sign(f); prev_fs = fs.shift(1)
            flip = (fs != prev_fs)
            B.append(pd.DataFrame({"coin": coin, "side": np.sign(a), "bk": pd.cut(f.abs(), [-0.01, 0.001, 5, 10, 20.01], labels=["0", "0-5", "5-10", "10-20"]),
                                   "gross": a * r1, "fee": fee, "chg": chg, "signflip": flip & (fs != 0)}))
            idx = np.arange(0, len(b) - 72, 72)
            fr = (c.shift(-72) / c - 1).iloc[idx]; ff = f.iloc[idx]
            m = ff != 0
            hz.append(pd.DataFrame({"coin": coin, "dir": np.sign(ff[m]), "big": ff[m].abs() >= 10,
                                    "ex": np.sign(ff[m]) * (fr[m] - mu72), "raw": fr[m]}))
    H = pd.concat(hz)
    def tt(x):
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["ex72_by_dir_big"] = H.groupby(["dir", "big"])["ex"].apply(tt).unstack()
    out["ex72_by_coin_dir"] = H.groupby(["coin", "dir"])["ex"].apply(tt).unstack()
    D = pd.concat(B)
    out["side_bucket"] = D.groupby(["side", "bk"], observed=True).agg(n=("gross", "size"), gross=("gross", "sum"), fee=("fee", "sum"), turnover=("chg", "sum"))
    out["fee_share_when_forecast_lt5"] = D.loc[D["bk"].isin(["0", "0-5"]), "fee"].sum() / D["fee"].sum()
    out["total_gross_fee"] = pd.Series({"gross": D["gross"].sum(), "fee": D["fee"].sum(), "long_gross": D.loc[D.side > 0, "gross"].sum(), "long_fee": D.loc[D.side > 0, "fee"].sum()})
    return out
