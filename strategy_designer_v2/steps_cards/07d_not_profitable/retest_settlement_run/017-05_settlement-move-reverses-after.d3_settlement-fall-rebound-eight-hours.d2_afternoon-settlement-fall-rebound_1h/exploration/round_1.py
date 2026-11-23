def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; trades = data["trades"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        nonov = {h: [] for h in (8, 16, 24)}
        for w, b in wins.items():
            c = b["close"].values
            for h in nonov:
                idx = np.arange(0, len(c) - h, h)
                nonov[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: np.mean(v) for h, v in nonov.items()}
        sd8 = np.std(nonov[8], ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            r2 = c / c.shift(2) - 1
            mabs = r2.abs().rolling(720, min_periods=120).mean()
            sc = r2 / mabs
            r4 = c / c.shift(4) - 1
            sc4 = r4 / (r4.abs().rolling(720, min_periods=120).mean())
            r24p = c / c.shift(24) - 1
            vol_ratio = r2.abs().rolling(48).mean() / mabs
            volr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean()
            df = pd.DataFrame({
                "coin": coin, "w": w, "hour_close": (ts.dt.hour + 1) % 24,
                "year": ts.dt.year, "sc": sc, "sc4": sc4, "r24p": r24p / mabs,
                "volratio": vol_ratio, "volu": volr,
                "f8": c.shift(-8) / c - 1, "f16": c.shift(-16) / c - 1, "f24": c.shift(-24) / c - 1,
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "sd8": sd8})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (8, 16, 24):
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(lambda k: drift[k][h])
    def summ(g, col="f8"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(),
                          "t": x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    S = A[(A.hour_close == 16) & (A.sc < 0)].copy()
    S["q"] = pd.qcut(-S["sc"], 5, labels=False)
    out = {}
    out["fall quintile (4=largest) f8 total"] = S.groupby("q").apply(summ)
    out["fall quintile u8"] = S.groupby("q").apply(lambda g: summ(g, "u8"))
    out["fall quintile f24 total"] = S.groupby("q").apply(lambda g: summ(g, "f24"))
    out["fall quintile f16 total"] = S.groupby("q").apply(lambda g: summ(g, "f16"))
    out["by coin f8"] = S.groupby("coin").apply(summ)
    out["by year f8"] = S.groupby("year").apply(summ)
    # same fall at other closing hours (control)
    O = A[(A.sc < 0)].copy()
    O["big"] = (-O["sc"]) > S["sc"].abs().quantile(0.8)
    out["big fall by close hour f8"] = O[O.big].groupby("hour_close").apply(summ)
    # vol regime and prior 24h trend among top-2 quintiles
    T = S[S.q >= 3].copy()
    T["vq"] = pd.qcut(T["volratio"], 3, labels=False)
    out["top falls by vol tercile f8"] = T.groupby("vq").apply(summ)
    T["tq"] = pd.qcut(T["r24p"], 3, labels=False)
    out["top falls by prior24h tercile f8"] = T.groupby("tq").apply(summ)
    T["vu"] = pd.qcut(T["volu"], 3, labels=False)
    out["top falls by volume tercile f8"] = T.groupby("vu").apply(summ)
    # trades
    tr = pd.concat([t.assign(coin=k) for k, ws in trades.items() for t in ws.values()], ignore_index=True)
    tr["eq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades by entry fc quintile"] = tr.groupby("eq").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda x: x.mean() / 60), fc=("entry_forecast", "mean"))
    out["trades side"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    out["share of 16h falls with fc>0"] = float((S.fc > 0).mean())
    return out
