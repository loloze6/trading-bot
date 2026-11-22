def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            c = df["close"].astype(float).reset_index(drop=True)
            n = len(c)
            r1 = c.pct_change()
            z = r1 / r1.rolling(20).std()
            r90 = c / c.shift(90) - 1
            rise = z >= 2
            grid = (np.arange(n) % 5 == 0)
            fwd = c.shift(-5) / c - 1
            ok = grid & fwd.notna()
            fc = df["forecast"].astype(float).reset_index(drop=True)
            reg = df["regime"].astype(str).reset_index(drop=True)
            yr = int(pd.to_datetime(df["timestamp"]).dt.year.iloc[0])
            rows.append(dict(coin=coin, w=w, year=yr, n=n,
                has90=int(r90.notna().sum()),
                rise_all=int(rise.sum()),
                rise_nohist=int((rise & r90.isna()).sum()),
                riseA_all=int((rise & (r90 > 0)).sum()),
                riseB_all=int((rise & (r90 < 0)).sum()),
                riseA_grid=int((rise & (r90 > 0) & ok).sum()),
                riseB_grid=int((rise & (r90 < 0) & ok).sum()),
                mr_bars=int((reg == "mean_reversion").sum()),
                fneg=int((fc < 0).sum()),
                fneg_grid=int(((fc < 0) & ok).sum())))
    t = pd.DataFrame(rows)
    cols = ["n", "has90", "rise_all", "rise_nohist", "riseA_all", "riseB_all",
            "riseA_grid", "riseB_grid", "mr_bars", "fneg", "fneg_grid"]
    out = {}
    out["totals"] = t[cols].sum()
    out["by_coin"] = t.groupby("coin")[cols].sum()
    out["by_year"] = t.groupby("year")[cols].sum()
    out["window_len"] = t["n"].describe()
    out["windows_with_any_90d_history"] = int((t["has90"] > 0).sum())
    return out
