def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["bars"].keys())
    # per coin per day: book return, held allocation, state at previous day close
    rows = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].astype(float)
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["nearhi"] = cl / cl.rolling(720, min_periods=120).max()
            b["r30"] = cl / cl.shift(720) - 1
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["gain"] = b["alloc"] * (cl.shift(-1) / cl - 1)
            d = b.groupby("day").agg(nearhi=("nearhi", "last"), r30=("r30", "last"),
                                     alloc=("alloc", "mean"), gain=("gain", "sum"),
                                     cret=("close", "last"))
            d["cret"] = d["cret"].pct_change()
            d["nearhi_prev"] = d["nearhi"].shift(1)
            d["r30_prev"] = d["r30"].shift(1)
            d["coin"] = c; d["w"] = w
            rows.append(d.reset_index(drop=True))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["gain", "nearhi_prev"])
    D["nh_b"] = pd.qcut(D["nearhi_prev"], 5)
    a = D.groupby("nh_b", observed=True).agg(gain_mean=("gain", "mean"), alloc=("alloc", "mean"),
                                              coin_ret=("cret", "mean"), n=("gain", "size"),
                                              gain_sd=("gain", "std"))
    a["gain_q05"] = D.groupby("nh_b", observed=True)["gain"].quantile(0.05)
    a["share_of_loss_days_lt_-3pct"] = D.groupby("nh_b", observed=True)["gain"].apply(lambda x: (x < -0.03).sum()) / (D["gain"] < -0.03).sum()
    out["book_day_by_nearhi_prev"] = a
    D2 = D.dropna(subset=["r30_prev"]).copy()
    D2["r30_b"] = pd.qcut(D2["r30_prev"], 5)
    b2 = D2.groupby("r30_b", observed=True).agg(gain_mean=("gain", "mean"), alloc=("alloc", "mean"),
                                                coin_ret=("cret", "mean"), n=("gain", "size"))
    b2["share_big_loss"] = D2.groupby("r30_b", observed=True)["gain"].apply(lambda x: (x < -0.03).sum()) / (D2["gain"] < -0.03).sum()
    out["book_day_by_r30_prev"] = b2
    # mean exposure when in position
    out["mean_alloc_when_in"] = float(D.loc[D.alloc > 0, "alloc"].mean())
    out["share_days_in"] = float((D.alloc > 0).mean())
    # Calmar of a book restricted to top-two nearhi quintiles (rough)
    return out
