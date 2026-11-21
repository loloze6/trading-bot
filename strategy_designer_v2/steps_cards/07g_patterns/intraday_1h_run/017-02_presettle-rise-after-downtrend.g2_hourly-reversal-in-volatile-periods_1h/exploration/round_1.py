def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r = b["close"].pct_change()
            fwd = b["close"].shift(-1) / b["close"] - 1
            sd24 = r.rolling(24).std()
            vol_avg = sd24.rolling(720, min_periods=200).mean()
            df = pd.DataFrame({
                "coin": coin, "win": w, "hour": ts.dt.hour, "wd": ts.dt.weekday,
                "year": ts.dt.year, "r": r, "fwd": fwd, "z": r / sd24,
                "vr": sd24 / vol_avg, "pos": b["postRebalance_current_allocation"],
                "prev": b["previous_allocation"], "fc": b["forecast"],
                "vol": b["volume"],
                "pv": b["total_portfolio_value"], "ppv": b["postRebalance_total_value"],
            })
            df["r24"] = b["close"] / b["close"].shift(24) - 1
            df["fwd4"] = b["close"].shift(-4) / b["close"] - 1
            df["fee"] = (df["pv"] - df["ppv"]) / df["pv"]
            df["turn"] = (df["pos"] - df["prev"]).abs()
            df["vrel"] = df["vol"] / df["vol"].rolling(168, min_periods=48).median()
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["fwd"].transform("mean")
    d["gain"] = d["pos"] * d["fwd"]
    d["timing"] = d["pos"] * (d["fwd"] - mu)
    out = {}
    def tstat(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>1 else np.nan, "n": len(x)})
    out["gross_vs_fee_per_bar"] = pd.DataFrame({"gross": [d["gain"].mean()], "fee": [d["fee"].mean()], "turnover": [d["turn"].mean()], "abs_pos": [d["pos"].abs().mean()]})
    # reversal coefficient by hour: mean of -sign(r)*fwd, and corr
    d["rev"] = -np.sign(d["r"]) * d["fwd"]
    out["rev_by_hour"] = d.groupby("hour")["rev"].apply(tstat).unstack()
    # by z-quintile
    d["zq"] = pd.qcut(d["z"], 10, labels=False, duplicates="drop")
    out["fwd_by_z_decile"] = d.groupby("zq").agg(z=("z","mean"), fwd=("fwd","mean"), fwd4=("fwd4","mean"), n=("fwd","count"))
    # by vol regime
    d["vq"] = pd.qcut(d["vr"], 5, labels=False, duplicates="drop")
    out["rev_by_volratio_q"] = d.groupby("vq")["rev"].apply(tstat).unstack()
    out["rev_by_coin"] = d.groupby("coin")["rev"].apply(tstat).unstack()
    out["rev_by_year"] = d.groupby("year")["rev"].apply(tstat).unstack()
    # volume relative by hour
    out["volrel_by_hour"] = d.groupby("hour")["vrel"].median()
    # 24h trend vs next hour, at funding hours vs other
    d["fund"] = d["hour"].isin([23,7,15]).map({True:"pre_fund",False:"other"})
    d["tr"] = -np.sign(d["r24"]) * d["fwd"]
    out["against24_by_fundhour"] = d.groupby("fund")["tr"].apply(tstat).unstack()
    d["r24q"] = pd.qcut(d["r24"], 5, labels=False)
    out["fwd_by_r24_q_grid24"] = d.groupby("r24q")["fwd"].apply(tstat).unstack()
    return out
