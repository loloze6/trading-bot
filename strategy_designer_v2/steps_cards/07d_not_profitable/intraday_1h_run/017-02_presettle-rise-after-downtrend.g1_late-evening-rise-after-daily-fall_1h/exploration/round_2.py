def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour; b["year"] = ts.dt.year
            c = b["close"]
            b["r2"] = c.shift(-2) / c - 1
            b["r3_from20"] = c.shift(-3) / c - 1
            b["ret24"] = c / c.shift(24) - 1
            b["ret72"] = c / c.shift(72) - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * (c.shift(-1) / c - 1)
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","year","hour","r2","r3_from20","ret24","ret72","pos","gross","fee"]])
    df = pd.concat(rows)
    # book daily: mean daily return, and gross vs fee per day
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin))
    dd = pd.concat(dd)
    out["book_daily"] = pd.Series({"book_mean": dd["book_return"].mean(), "coin_mean": dd["coin_return"].mean(),
        "n_days": dd["book_return"].notna().sum()})
    nd = dd["book_return"].notna().sum()
    out["gross_fee_per_coin_day"] = pd.Series({"gross_per_day": df["gross"].sum()/nd, "fee_per_day": df["fee"].sum()/nd})
    # 21:00 r2 by ret24 sign, by year
    d21 = df[df.hour==21].dropna(subset=["r2","ret24"]).copy()
    d21["up"] = np.where(d21.ret24>0, "rise24", "fall24")
    def tt(s): return pd.Series({"mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    out["h21_r2_by_sign_year"] = d21.groupby(["year","up"])["r2"].apply(tt).unstack()
    # slope of r2 on standardized ret24 at 21 by year (correlation)
    out["h21_corr_ret24_r2_by_year"] = d21.groupby("year").apply(lambda g: pd.Series({"corr": g.r2.corr(g.ret24), "n": len(g)}))
    # 20:00 bar: 2-bar return (20->22) by ret24 quintile
    d20 = df[df.hour==20].dropna(subset=["r2","ret24"]).copy()
    d20["q"] = d20.groupby("coin")["ret24"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["h20_r2_by_ret24_q"] = d20.groupby("q")["r2"].apply(tt).unstack()
    # 21: by ret72 quintile
    d21b = df[df.hour==21].dropna(subset=["r2","ret72"]).copy()
    d21b["q"] = d21b.groupby("coin")["ret72"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    out["h21_r2_by_ret72_q"] = d21b.groupby("q")["r2"].apply(tt).unstack()
    # 21 by coin, rise24 vs fall24
    out["h21_r2_by_coin_sign"] = d21.groupby(["coin","up"])["r2"].mean().unstack()
    return out
