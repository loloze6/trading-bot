def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [120, 240]
    rows = []
    drift = {}
    usual = {}
    for coin, ws in data["bars"].items():
        for h in H:
            rs = []
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, b in ws.items():
            c = b["close"].values.astype(float)
            f = b["forecast"].fillna(0).values.astype(float)
            raw = b["debug_info.components.surge_near_high.last_history_value"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            hi = pd.Series(c).rolling(720, min_periods=24).max().values
            prox = c / hi
            r720 = pd.Series(c).pct_change(720).values
            r240 = pd.Series(c).pct_change(240).values
            trough = 0.0; taken = set()
            for i in range(len(c)):
                fi = max(f[i], 0)
                if fi < trough: trough = fi
                if fi - trough >= 2:
                    trough = fi
                    cell = i // 120
                    if cell in taken: continue
                    taken.add(cell)
                    d = dict(coin=coin, win=w, year=ts.iloc[i].year, fc=f[i], raw=raw[i],
                             prox=prox[i], r720=r720[i], r240=r240[i])
                    for h in H:
                        d[f"u{h}"] = (c[i + h] / c[i] - 1 - drift[(coin, h)]) if i + h < len(c) else np.nan
                        d[f"s{h}"] = d[f"u{h}"] / usual[(coin, h)]
                    rows.append(d)
    df = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"n{h}"] = len(x); out[f"m{h}"] = x.mean()
            out[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
            out[f"str{h}"] = g[f"s{h}"].dropna().mean()
        return pd.Series(out)
    res = {}
    res["all"] = summ(df).to_frame().T
    df["trend_up"] = df["r720"] > 0
    res["by_30d_trend_sign"] = df.groupby("trend_up").apply(summ)
    df["p3"] = pd.qcut(df["prox"].rank(method="first"), 3, labels=False)
    res["trend_x_prox_tercile"] = df.groupby(["trend_up", "p3"]).apply(summ)
    df["f3"] = pd.qcut(df["fc"].rank(method="first"), 3, labels=False)
    res["trend_x_forecast_tercile"] = df.groupby(["trend_up", "f3"]).apply(summ)
    cor = []
    for v in ["fc", "raw", "prox", "r720", "r240"]:
        for h in H:
            s = df[[v, f"u{h}"]].dropna()
            rho, p = stats.spearmanr(s[v], s[f"u{h}"])
            cor.append(dict(var=v, h=h, n=len(s), spearman=rho, p=p))
    res["spearman"] = pd.DataFrame(cor)
    up = df[df["trend_up"]]
    cor2 = []
    for v in ["fc", "raw", "prox", "r720"]:
        for h in H:
            s = up[[v, f"u{h}"]].dropna()
            rho, p = stats.spearmanr(s[v], s[f"u{h}"])
            cor2.append(dict(var=v, h=h, n=len(s), spearman=rho, p=p))
    res["spearman_in_uptrend"] = pd.DataFrame(cor2)
    res["uptrend_by_year"] = up.groupby("year").apply(summ)
    res["uptrend_by_coin"] = up.groupby("coin").apply(summ)
    return res
