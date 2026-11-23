def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    cost = 0.0019
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; ts = pd.to_datetime(b["timestamp"])
            hc = (ts.dt.hour + 1) % 24
            r1n = c.shift(-1) / c - 1
            al = b["postRebalance_current_allocation"].fillna(0)
            pal = b["previous_allocation"].fillna(0)
            r2 = c / c.shift(2) - 1
            mabs = r2.abs().rolling(720, min_periods=120).mean()
            sc = r2 / mabs
            vr = r2.abs().rolling(48).mean() / mabs
            df = pd.DataFrame({"coin": coin, "w": w, "hc": hc, "al": al,
                               "gain": al * r1n, "turn": (al - pal).abs(),
                               "fc": b["forecast"], "sc": sc, "vr": vr,
                               "f8": c.shift(-8) / c - 1, "f24": c.shift(-24) / c - 1,
                               "val": b["postRebalance_total_value"], "tpv": b["total_portfolio_value"]})
            df["fee"] = df["tpv"] - df["val"]
            df["fee_rel"] = df["fee"] / df["tpv"]
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    A["hs"] = (A["hc"] - 16) % 24  # hours since 16:00 close
    g = A.groupby("hs")
    out["by hours since 16:00: share in pos, mean alloc, gain bp, fee bp"] = pd.DataFrame({
        "in_pos": g["al"].apply(lambda x: (x.abs() > 1e-6).mean()),
        "mean_al": g["al"].mean(),
        "gain_bp": g["gain"].mean() * 1e4,
        "fee_bp": g["fee_rel"].mean() * 1e4})
    out["totals bp per bar: gain, fee"] = pd.Series({"gain": A["gain"].mean() * 1e4,
        "fee": A["fee_rel"].mean() * 1e4, "mean_abs_al_in_pos": A.loc[A.al.abs() > 1e-6, "al"].abs().mean(),
        "turnover_per_bar": A["turn"].mean()})
    # condition check: high vol at 16:00, with vs without fall
    S = A[A.hc == 16].copy()
    S["vq"] = pd.qcut(S["vr"], 3, labels=False)
    S["fallq"] = np.where(S.sc >= 0, "rise", np.where(-S.sc > S.loc[S.sc < 0, "sc"].abs().quantile(0.6), "bigfall", "smallfall"))
    def summ(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))})
    out["16h f8 by vol tercile x fall"] = S.groupby(["vq", "fallq"])["f8"].apply(summ).unstack()
    out["16h f24 by vol tercile x fall"] = S.groupby(["vq", "fallq"])["f24"].apply(summ).unstack()
    # forecast bins vs f8 among 16h
    F = S[S.fc > 0].copy()
    F["fb"] = pd.cut(F.fc, [0, 2, 5, 10, 19.99, 20.01])
    out["16h f8 by forecast bin"] = F.groupby("fb")["f8"].apply(summ).unstack()
    # book daily returns by year-ish: by window
    d = pd.concat([x.assign(coin=k, w=w) for k, ws in days.items() for w, x in ws.items()])
    out["book daily mean bp by window"] = d.groupby("w")["book_return"].mean().mul(1e4)
    return out
