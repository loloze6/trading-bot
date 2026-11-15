def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            raw = df["debug_info.components.sma_cross.last_history_value"].values
            sg = np.sign(raw)
            since = np.full(len(df), np.nan)
            cnt = np.nan
            for i in range(len(df)):
                if i > 0 and not np.isnan(sg[i]) and not np.isnan(sg[i-1]) and sg[i] != sg[i-1]:
                    cnt = 0
                elif not np.isnan(cnt):
                    cnt += 1
                since[i] = cnt if not np.isnan(cnt) else np.nan
            lr = np.log(pd.Series(c)).diff()
            vol20 = lr.rolling(20).std().values
            r20 = pd.Series(c).pct_change(20).values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in (10, 20):
                for i in range(0, len(df) - h, h):
                    rows.append((coin, w, h, yr[i], f[i], raw[i], sg[i], since[i], vol20[i], r20[i], c[i + h] / c[i] - 1))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "yr", "f", "raw", "sg", "since", "vol", "r20", "ret"])
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "ex": g.ex.mean(), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "hit": (g.ret > 0).mean()})
    for h in (10, 20):
        dh = d[d.h == h].copy()
        dh["state"] = np.where(dh.sg > 0, "above", "below")
        dh["fresh"] = pd.cut(dh.since, [-1, 10, 30, 60, 1e9], labels=["0-10d", "11-30d", "31-60d", ">60d"])
        out[f"state_fresh_h{h}"] = dh.groupby(["state", "fresh"]).apply(summ)
        out[f"state_year_h{h}"] = dh.groupby(["yr", "state"]).apply(summ).unstack()["ex"]
    d10 = d[d.h == 10].copy()
    d10["vq"] = d10.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    d10["state"] = np.where(d10.sg > 0, "above", "below")
    out["vol_state_h10"] = d10.groupby(["vq", "state"]).apply(summ)
    d10["mq"] = pd.qcut(d10.r20.rank(method="first"), 3, labels=False)
    out["mom20_state_h10"] = d10.groupby(["mq", "state"]).apply(summ)
    out["state_coin_h10"] = d10.groupby(["coin", "state"]).apply(summ).unstack()["ex"]
    return out
