def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = [6, 24, 72, 120, 240]
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        rs = []
        for w, b in ws.items():
            c = b["close"].values
            rs.append(np.diff(np.log(c)))
        drift[coin] = np.mean(np.concatenate(rs))
    for coin, ws in data["bars"].items():
        mu = drift[coin]
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=120).mean().shift(1)
            z = r24 / scale
            day = pd.to_datetime(b["timestamp"]).dt.floor("D").reset_index(drop=True)
            r7 = c / c.shift(168) - 1
            r30 = c / c.shift(720) - 1
            for side, cond in (("down", z <= -1.0), ("up", z >= 1.0)):
                first = cond & ~cond.shift(1, fill_value=False)
                idx = np.where(first.values)[0]
                lastday = None
                for i in idx:
                    if day[i] == lastday:
                        continue
                    lastday = day[i]
                    rec = {"side": side, "coin": coin, "z": z[i], "r7": r7[i], "r30": r30[i]}
                    for h in H:
                        if i + h < len(c):
                            rec[f"x{h}"] = np.log(c[i + h] / c[i]) - mu * h
                    rows.append(rec)
    df = pd.DataFrame(rows)
    df["zbin"] = pd.cut(df["z"].abs(), [1, 1.5, 2, 3, 100])
    out = {}
    def summ(g):
        d = {}
        for h in H:
            x = g[f"x{h}"].dropna()
            d[f"m{h}_bps"] = x.mean() * 1e4
            d[f"t{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        d["n"] = len(g)
        return pd.Series(d)
    out["by_side_zbin"] = df.groupby(["side", "zbin"], observed=True).apply(summ)
    dn = df[df.side == "down"].copy()
    dn["trend30"] = np.where(dn["r30"] > 0, "30d_up", "30d_down")
    out["down_by_trend30"] = dn.groupby(["trend30", "zbin"], observed=True).apply(summ)
    out["down_by_coin"] = dn.groupby("coin").apply(summ)
    # book
    br = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            br.append(d[["book_return", "coin_return"]].assign(coin=coin, w=w))
    br = pd.concat(br).dropna()
    out["book_mean_daily"] = br["book_return"].mean()
    out["coin_mean_daily"] = br["coin_return"].mean()
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = pd.Series({"n": len(tr), "gross_mean_pct": tr["profit_loss_percent"].mean(),
                               "net_mean_pct": tr["net_profit_loss_percent"].mean(),
                               "dur_h_median": tr["duration_minutes"].median() / 60})
    return out
