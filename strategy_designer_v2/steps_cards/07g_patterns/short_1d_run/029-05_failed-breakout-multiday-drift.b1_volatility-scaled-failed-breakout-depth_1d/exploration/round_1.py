def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 8
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            if n < 40:
                continue
            s = pd.Series(c)
            r1 = s.pct_change()
            vol = r1.rolling(20).std()
            hi20 = s.shift(1).rolling(20).max()
            lo20 = s.shift(1).rolling(20).min()
            ret5 = s / s.shift(5) - 1
            ret20 = s / s.shift(20) - 1
            # failed breakdown: close above old 20d low within 3 days after a close below it
            brk_dn = (s < lo20)
            brk_up = (s > hi20)
            fbd = np.zeros(n); fbu = np.zeros(n)
            for t in range(n):
                for k in range(1, 4):
                    j = t - k
                    if j >= 21 and brk_dn.iloc[j] and c[t] > lo20.iloc[j] and not brk_dn.iloc[t]:
                        fbd[t] = (c[t] - lo20.iloc[j]) / (vol.iloc[t] * c[t]) if vol.iloc[t] > 0 else np.nan
                        break
                for k in range(1, 4):
                    j = t - k
                    if j >= 21 and brk_up.iloc[j] and c[t] < hi20.iloc[j] and not brk_up.iloc[t]:
                        fbu[t] = (hi20.iloc[j] - c[t]) / (vol.iloc[t] * c[t]) if vol.iloc[t] > 0 else np.nan
                        break
            dow = pd.to_datetime(b["timestamp"]).dt.dayofweek.values
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[t+H]/c[t]-1, r1z=r1.iloc[t]/vol.iloc[t] if vol.iloc[t]>0 else np.nan,
                                 r5=ret5.iloc[t], r20=ret20.iloc[t], vol=vol.iloc[t],
                                 dhi=(c[t]-hi20.iloc[t])/(vol.iloc[t]*c[t]) if vol.iloc[t]>0 else np.nan,
                                 brkup=bool(brk_up.iloc[t]), brkdn=bool(brk_dn.iloc[t]),
                                 fbd=fbd[t], fbu=fbu[t], fc=b["forecast"].iloc[t]))
            for t in range(1, n):
                daily.append(dict(coin=coin, r=c[t]/c[t-1]-1, dow=dow[t], rprevz=(r1.iloc[t-1]/vol.iloc[t-1]) if t>=21 and vol.iloc[t-1]>0 else np.nan))
    df = pd.DataFrame(rows)
    dd = pd.DataFrame(daily)
    drift = df.groupby("coin")["fwd"].transform("mean")
    df["ex"] = df["fwd"] - drift
    out = {}
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, "mean_fwd": g["fwd"].mean()})
    out["drift_by_coin_8d"] = df.groupby("coin")["fwd"].agg(["mean","std","count"])
    for col in ["r1z","r5","r20","vol","dhi"]:
        q = pd.qcut(df[col], 5, labels=False, duplicates="drop")
        out[f"fwd8_by_{col}_quintile"] = df.groupby(q).apply(summ)
    out["fwd8_breakout_up_vs_not"] = df.groupby("brkup").apply(summ)
    out["fwd8_breakout_down_vs_not"] = df.groupby("brkdn").apply(summ)
    out["fwd8_failed_breakdown"] = df.groupby(df["fbd"]>0).apply(summ)
    out["fwd8_failed_breakout"] = df.groupby(df["fbu"]>0).apply(summ)
    out["fwd8_by_coin_r20_hilo"] = df.assign(up=df["r20"]>df.groupby("coin")["r20"].transform("median")).groupby(["coin","up"]).apply(summ)
    # daily
    dd["ex"] = dd["r"] - dd.groupby("coin")["r"].transform("mean")
    out["daily_by_dow"] = dd.groupby("dow")["ex"].agg(["count","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    q = pd.qcut(dd["rprevz"], 5, labels=False)
    out["daily_next_by_prev_day_z_quintile"] = dd.groupby(q)["ex"].agg(["count","mean", lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bk.append(d.assign(coin=coin, w=w))
    bk = pd.concat(bk)
    out["book_by_window_sum"] = bk.groupby("w")[["book_return","coin_return"]].sum()
    out["book_by_coin"] = bk.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tr = pd.concat(tr)
    out["trades_by_coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades_win_share"] = float((tr["net_profit_loss_percent"]>0).mean())
    return out
