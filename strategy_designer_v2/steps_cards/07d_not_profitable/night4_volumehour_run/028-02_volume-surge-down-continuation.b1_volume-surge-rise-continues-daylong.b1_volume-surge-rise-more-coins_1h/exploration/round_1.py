def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = [2, 6, 24]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        r24 = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            r24 += list(c[idx + 24] / c[idx] - 1)
        drift[coin] = np.mean(r24); usual[coin] = np.std(r24)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std()
            vr = b["volume"] / b["volume"].rolling(720, min_periods=240).mean()
            z = r / sd
            r168 = c / c.shift(168) - 1
            r720 = c / c.shift(720, ) - 1
            vol_reg = r.rolling(168).std() / sd
            n = len(b)
            cell = np.arange(n) // 24
            df = pd.DataFrame({"z": z, "vr": vr, "r168": r168, "r720": r720, "volreg": vol_reg,
                               "cell": cell, "fc": b["forecast"], "hour": pd.to_datetime(b["timestamp"]).dt.hour})
            for h in H:
                df[f"f{h}"] = c.shift(-h) / c - 1
            df.loc[n - 24:, ["f2", "f6", "f24"]] = np.nan
            df["coin"] = coin; df["win"] = w
            for side, cond in [("up", (df.z > 2) & (df.vr > 2)), ("down", (df.z < -2) & (df.vr > 2)),
                               ("up_lowvol", (df.z > 2) & (df.vr < 1.2)), ("down_lowvol", (df.z < -2) & (df.vr < 1.2))]:
                s = df[cond].groupby("cell").head(1).copy()
                s["side"] = side
                rows.append(s)
    cs = pd.concat(rows).dropna(subset=["f24"])
    cs["sgn"] = np.where(cs.side.str.startswith("up"), 1, -1)
    for h in H:
        cs[f"u{h}"] = cs.apply(lambda x: x[f"f{h}"] - drift[x.coin] * h / 24, axis=1) * cs.sgn
    def summ(g):
        return pd.Series({"n": len(g), **{f"u{h}%": g[f"u{h}"].mean() * 100 for h in H},
                          "t24": g.u24.mean() / (g.u24.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out["by side"] = cs.groupby("side").apply(summ)
    up = cs[cs.side == "up"].copy()
    up["prod"] = up.z * up.vr
    up["prodq"] = pd.qcut(up["prod"], 4, labels=False)
    out["up by prod quartile"] = up.groupby("prodq").apply(summ)
    up["trend7"] = pd.qcut(up.r168, 3, labels=["low", "mid", "high"])
    out["up by 7d return tercile"] = up.groupby("trend7").apply(summ)
    up["trend30"] = np.sign(up.r720)
    out["up by 30d return sign"] = up.groupby("trend30").apply(summ)
    up["vq"] = pd.qcut(up.volreg, 3, labels=["calm", "mid", "wild"])
    out["up by 7d vol/30d vol"] = up.groupby("vq").apply(summ)
    dn = cs[cs.side == "down"].copy()
    dn["trend30"] = np.sign(dn.r720)
    out["down by 30d return sign"] = dn.groupby("trend30").apply(summ)
    # book chain and falls
    dd = []
    allwins = sorted(data["days"]["BTCUSD"].keys(), key=lambda s: int(s[1:]))
    chain = []
    for w in allwins:
        frames = []
        for coin in data["days"]:
            if w in data["days"][coin]:
                d = data["days"][coin][w][["day", "book_return", "coin_return"]].set_index("day")
                frames.append(d.add_suffix("_" + coin))
        m = pd.concat(frames, axis=1)
        br = m[[c for c in m if c.startswith("book_return")]].mean(axis=1)
        cr = m[[c for c in m if c.startswith("coin_return")]].mean(axis=1)
        chain.append(pd.DataFrame({"win": w, "br": br.values, "cr": cr.values}))
    ch = pd.concat(chain).dropna().reset_index(drop=True)
    v = (1 + ch.br).cumprod(); dd = v / v.cummax() - 1
    ch["dd"] = dd.values
    out["book: mean br, cr, sharpe b, sharpe hold"] = pd.Series({
        "mean_br": ch.br.mean(), "mean_cr": ch.cr.mean(),
        "sh_b": ch.br.mean() / ch.br.std() * np.sqrt(365), "sh_h": ch.cr.mean() / ch.cr.std() * np.sqrt(365),
        "maxdd": dd.min(), "corr_b_c": ch.br.corr(ch.cr)})
    out["book by window"] = ch.groupby("win").agg(br=("br", "sum"), cr=("cr", "sum"), mindd=("dd", "min"))
    # allocation
    alls = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"]
            g = a * (b["close"].shift(-1) / b["close"] - 1)
            alls.append(pd.Series({"coin": coin, "mean_alloc": a.mean(), "share_in": (a.abs() > 1e-6).mean(), "gain": g.sum()}))
    al = pd.DataFrame(alls)
    out["alloc by coin"] = al.groupby("coin")[["mean_alloc", "share_in", "gain"]].mean()
    tr = pd.concat([t for wins in data["trades"].values() for t in wins.values()])
    out["trades"] = pd.Series({"n": len(tr), "mean_gross%": tr.profit_loss_percent.mean(), "mean_net%": tr.net_profit_loss_percent.mean(),
                               "win_net": (tr.net_profit_loss_percent > 0).mean(), "mean_hours": tr.duration_minutes.mean() / 60})
    return out
