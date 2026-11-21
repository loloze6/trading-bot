def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows_hour = []   # per hour of close, reversal of 2h move over next 8h, high vol
    rows_big = []    # large 24h moves vs next 24h / 72h
    rows_pre = []    # pre-move horizon variants at settlement
    for coin, wins in bars.items():
        # coin usual moves / drifts by horizon
        drift = {}; usual = {}
        for H in (8, 24, 72):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - H, H)
                rs.append(c[idx + H] / c[idx] - 1)
            rs = np.concatenate(rs); drift[H] = rs.mean(); usual[H] = rs.std()
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"]
            r1 = c.pct_change()
            vol24 = r1.rolling(24).std()
            vavg = vol24.rolling(720, min_periods=200).mean()
            vr = vol24 / vavg
            hour_close = (pd.to_datetime(d["timestamp"]) + pd.Timedelta(hours=1)).dt.hour
            r2 = c / c.shift(2) - 1
            r8p = c / c.shift(8) - 1
            r24p = c / c.shift(24) - 1
            f8 = c.shift(-8) / c - 1
            f24 = c.shift(-24) / c - 1
            f72 = c.shift(-72) / c - 1
            base = pd.DataFrame({"coin": coin, "hour": hour_close, "vr": vr,
                                 "r2": r2 / vavg, "r8p": r8p / vavg, "r24p": r24p / vavg,
                                 "s8": (f8 - drift[8]) / usual[8],
                                 "s24": (f24 - drift[24]) / usual[24],
                                 "s72": (f72 - drift[72]) / usual[72],
                                 "t8": f8, "pos": d["postRebalance_current_allocation"],
                                 "fc": d["forecast"]})
            rows_hour.append(base)
    B = pd.concat(rows_hour, ignore_index=True).dropna(subset=["vr", "r2", "s8"])
    # A. reversal of 2h move over next 8h by hour of close, high vol
    hv = B[B.vr >= 1]
    g = []
    for h, x in hv.groupby("hour"):
        v = -np.sign(x.r2) * x.s8
        g.append((h, len(x), v.mean(), v.mean() / v.std() * np.sqrt(len(x)),
                  (-np.sign(x.r2) * x.t8).mean() * 1e4))
    out["A_rev2h_next8h_by_hour_highvol"] = pd.DataFrame(g, columns=["hour", "n", "strength", "t", "total_bps"])
    # B. same, low vol, grouped settlement vs not
    B["settle"] = B.hour.isin([0, 8, 16])
    g = []
    for (s, hi), x in B.groupby(["settle", B.vr >= 1]):
        for H in ("s8", "s24"):
            xx = x.dropna(subset=[H])
            v = -np.sign(xx.r2) * xx[H]
            g.append((s, hi, H, len(xx), v.mean(), v.mean() / v.std() * np.sqrt(len(xx))))
    out["B_rev2h_settle_vs_not_vol"] = pd.DataFrame(g, columns=["settle", "highvol", "h", "n", "strength", "t"])
    # C. 24h move quintiles (one per day at hour 0), next 24h and 72h, by vol regime
    d0 = B[B.hour == 0].dropna(subset=["r24p", "s24"]).copy()
    d0["q"] = d0.groupby("coin")["r24p"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["C_24hmove_quintile_next24"] = d0.groupby(["q"]).agg(n=("s24", "size"), s24=("s24", "mean"), s72=("s72", "mean"))
    out["C2_24hmove_quint_highvol"] = d0[d0.vr >= 1.3].groupby("q").agg(n=("s24", "size"), s24=("s24", "mean"), s72=("s72", "mean"))
    # D. strength of 2h reversal vs |r2| size (settlement, high vol)
    sx = hv[hv.hour.isin([0, 8, 16])].copy()
    sx["qa"] = pd.qcut(sx.r2.abs(), 5, labels=False)
    sx["v"] = -np.sign(sx.r2) * sx.s8; sx["vt"] = -np.sign(sx.r2) * sx.t8 * 1e4
    out["D_settle_rev_by_size"] = sx.groupby("qa").agg(n=("v", "size"), strength=("v", "mean"), total_bps=("vt", "mean"))
    # E. vol ratio quintile vs reversal of 8h pre move over next 24h (all hours at 0 only)
    d0b = B[B.hour.isin([0, 8, 16])].dropna(subset=["r8p", "s24"]).copy()
    d0b["qv"] = pd.qcut(d0b.vr, 5, labels=False)
    d0b["v8"] = -np.sign(d0b.r8p) * d0b.s24
    out["E_rev8h_next24_by_volq"] = d0b.groupby("qv").agg(n=("v8", "size"), strength=("v8", "mean"))
    # F. trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()], ignore_index=True)
    T["af"] = pd.qcut(T.entry_forecast.abs(), 4, labels=False, duplicates="drop")
    out["F_trades_by_fc"] = T.groupby("af").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda s: s.mean() / 60))
    out["F2_trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
