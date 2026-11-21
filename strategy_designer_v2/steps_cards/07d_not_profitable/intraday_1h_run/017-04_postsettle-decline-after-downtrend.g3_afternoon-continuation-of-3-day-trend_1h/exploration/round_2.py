def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            cl = b["close"].values
            n = len(b)
            r72 = pd.Series(cl) / pd.Series(cl).shift(72) - 1
            z = (r72 - r72.rolling(73, min_periods=20).mean()) / r72.rolling(73, min_periods=20).std()
            vol = pd.Series(cl).pct_change().rolling(72, min_periods=24).std()
            hrs = ts.dt.hour.values
            yr = ts.dt.year.values
            for i in range(n):
                if np.isnan(z.iloc[i]):
                    continue
                d = {"c": c, "w": w, "hour": hrs[i], "year": yr[i], "z": z.iloc[i], "vol": vol.iloc[i]}
                for h in (2, 4, 8, 24, 48):
                    d["r%d" % h] = cl[i + h] / cl[i] - 1 if i + h < n else np.nan
                recs.append(d)
    R = pd.DataFrame(recs)
    R["s"] = np.sign(R["z"])
    # signed 2h return by hour (z-weighted, /10 scale like forecast ~ z*10? use z)
    R["sr2"] = R["s"] * R["r2"]
    byhour = R.groupby("hour").agg(n=("sr2", "count"), signed_r2=("sr2", "mean"))
    byhour["t"] = R.groupby("hour")["sr2"].apply(lambda x: x.mean() / x.std() * np.sqrt(x.count()))
    S = R[R.hour == 15].copy()
    hz = {}
    for h in (2, 4, 8, 24, 48):
        x = (S["s"] * S["r%d" % h]).dropna()
        hz["h%d" % h] = {"signed_mean": x.mean(), "t": x.mean() / x.std() * np.sqrt(len(x)), "n": len(x)}
    hz = pd.DataFrame(hz).T
    # by |z| tercile and vol tercile at slot
    S["sr2"] = S["s"] * S["r2"]
    S["sr24"] = S["s"] * S["r24"]
    S["zq"] = pd.qcut(S["z"].abs().rank(method="first"), 3, labels=["low", "mid", "high"])
    S["vq"] = pd.qcut(S["vol"].rank(method="first"), 3, labels=["low", "mid", "high"])
    byz = S.groupby("zq").agg(sr2=("sr2", "mean"), sr24=("sr24", "mean"), vol=("vol", "mean"))
    byv = S.groupby("vq").agg(sr2=("sr2", "mean"), sr24=("sr24", "mean"), vol=("vol", "mean"),
                              sr2_over_vol=("sr2", lambda x: 0))
    byv["sr2_over_vol"] = byv["sr2"] / byv["vol"]
    byyear = S.groupby("year").agg(n=("sr2", "count"), sr2=("sr2", "mean"), sr24=("sr24", "mean"))
    return {"signed2h_by_hour": byhour, "slot_by_horizon": hz, "slot_by_absz": byz, "slot_by_vol": byv, "slot_by_year": byyear}
