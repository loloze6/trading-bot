def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; days = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"]); c = b["close"].values; n = len(b)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            n1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            n2 = np.full(n, np.nan); n2[:-2] = c[2:]/c[:-2]-1
            r2b = np.full(n, np.nan); r2b[2:] = c[2:]/c[:-2]-1  # sat->sun two-day? (fri close->sun close)
            vol = b["volume"].values
            vrel = vol/pd.Series(vol).rolling(28, min_periods=10).mean().values
            sd = pd.Series(r1).rolling(60, min_periods=20).std().values
            alloc = b["postRebalance_current_allocation"].values
            tpv = b["total_portfolio_value"].values; pv = b["postRebalance_total_value"].values
            rows.append(pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday.values, "r1": r1, "n1": n1,
                "n2": n2, "fri_sun": r2b, "vrel": vrel, "sd": sd, "alloc": alloc, "gain": alloc*n1,
                "fee": (tpv-pv)/tpv, "year": ts.dt.year.values}))
        for w, d in data["days"][coin].items():
            days.append(d.assign(coin=coin, w=w))
    A = pd.concat(rows, ignore_index=True); D = pd.concat(days, ignore_index=True)
    out = {}
    m1 = A.n1.mean(); m2 = A.groupby("coin").n2.mean()
    sun = A[A.wd == 6].dropna(subset=["r1", "n2", "sd"]).copy()
    sun["z"] = sun.r1/sun.sd
    sun["ex2"] = sun.n2 - sun.coin.map(A.groupby("coin").n1.mean()*2)
    def tt(x): x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    # both sides, symmetric: x = -z * ex2 ; monday only vs mon+tue
    sun["ex1"] = sun.n1 - sun.coin.map(A.groupby("coin").n1.mean())
    out["short_rise_only_mon"] = tt(-sun.z.clip(lower=0)*sun.ex1)
    out["short_rise_only_montue"] = tt(-sun.z.clip(lower=0)*sun.ex2)
    out["long_fall_only_montue"] = tt(-sun.z.clip(upper=0)*sun.ex2)
    out["both_sides_montue"] = tt(-sun.z*sun.ex2)
    # raw (not excess) short gain on rose Sundays: short pays only if fall exceeds drift
    out["raw_short_gain_rise_montue"] = tt(-sun[sun.r1 > 0].n2)
    # weekday comparison: same-sized z on other days, next 2 days excess
    A["z"] = A.r1/A.sd
    A["ex2"] = A.n2 - A.coin.map(A.groupby("coin").n1.mean()*2)
    g = A.dropna(subset=["z", "ex2"])
    out["slope_ex2_on_z_by_weekday"] = g.groupby("wd").apply(lambda d: pd.Series({
        "slope": stats.linregress(d.z, d.ex2).slope, "t": stats.linregress(d.z, d.ex2).slope/stats.linregress(d.z, d.ex2).stderr, "n": len(d)}))
    # rose sunday in low vs high weekend volume, by z thirds
    s = sun[sun.r1 > 0].dropna(subset=["vrel"]).copy()
    s["zq"] = pd.qcut(s.z, 3, labels=["small", "mid", "big"])
    s["vq"] = pd.qcut(s.vrel, 2, labels=["lowvol", "highvol"])
    out["rise_ex2_by_size_and_vol"] = s.pivot_table(index="zq", columns="vq", values="ex2", aggfunc="mean")
    out["fall_ex2_by_size"] = sun[sun.r1 <= 0].assign(zq=lambda d: pd.qcut(d.z, 3, labels=["big", "mid", "small"])).groupby("zq").ex2.agg(["mean", "count"])
    # book: daily returns, fees on active bars
    act = A[A.alloc.abs() > 1e-9]
    out["active_gain_vs_fee"] = pd.Series({"gain_per_active": act.gain.mean(), "fee_per_trade_bar": A.fee[A.fee > 0].mean(),
        "n_fee_bars": (A.fee > 0).sum(), "n_active": len(act), "drift_cost_per_active": (act.alloc*m1).mean()})
    br = D.dropna(subset=["book_return"])
    out["book_daily_by_year"] = br.assign(year=pd.to_datetime(br.day).dt.year).groupby("year").agg(book=("book_return", "mean"), coin=("coin_return", "mean"))
    return out
