def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourrows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour
            c = b["close"]
            b["r1"] = c.shift(-1) / c - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gross"] = b["pos"] * b["r1"]
            b["fee"] = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            b["ret24"] = c / c.shift(24) - 1
            b["r2"] = c.shift(-2) / c - 1
            b["coin"] = coin; b["win"] = w
            rows.append(b[["coin","win","hour","r1","r2","pos","gross","fee","ret24","forecast"]])
    df = pd.concat(rows)
    # gross vs fees
    out["gross_vs_fee_per_bar_sum"] = pd.Series({
        "gross_sum": df["gross"].sum(), "fee_sum": df["fee"].sum(),
        "n_active_bars": int((df["pos"].abs() > 1e-9).sum()),
        "mean_pos_active": df.loc[df["pos"].abs() > 1e-9, "pos"].mean()})
    out["by_coin_gross_fee"] = df.groupby("coin").agg(gross=("gross","sum"), fee=("fee","sum"))
    # hour-of-day mean 1h return, all coins (non-overlapping by construction for h=1)
    g = df.groupby("hour")["r1"].agg(["mean","std","count"])
    g["t"] = g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["hour_mean_r1"] = g[["mean","t","count"]]
    # 21:00 bars: 2-bar return by ret24 quintile
    d21 = df[df["hour"]==21].dropna(subset=["r2","ret24"]).copy()
    d21["q"] = d21.groupby("coin")["ret24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    gq = d21.groupby("q")["r2"].agg(["mean","std","count"])
    gq["t"] = gq["mean"]/(gq["std"]/np.sqrt(gq["count"]))
    out["h21_r2_by_ret24_quintile"] = gq
    # all hours: 2-bar return (grid at even hours) by ret24 quintile, for comparison
    da = df[df["hour"]%2==1].dropna(subset=["r2","ret24"]).copy()
    da["q"] = da.groupby("coin")["ret24"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    ga = da.groupby("q")["r2"].agg(["mean","std","count"])
    ga["t"] = ga["mean"]/(ga["std"]/np.sqrt(ga["count"]))
    out["allodd_hours_r2_by_ret24_quintile"] = ga
    # position held at 21,22 by hour gross
    act = df[df["pos"].abs()>1e-9]
    out["active_by_hour"] = act.groupby("hour").agg(n=("gross","size"), gross_mean=("gross","mean"), fee_mean=("fee","mean"), pos=("pos","mean"))
    # fee by hour (where trades happen)
    out["fee_by_hour"] = df.groupby("hour")["fee"].sum()[lambda s: s>0]
    # ret24 quintile at 21 and the 2h return by year
    d21["year"] = None
    return out
