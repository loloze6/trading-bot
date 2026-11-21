def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 20
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rs) if rs else np.nan
        for w, b in wins.items():
            c = b["close"].values; f = b["forecast"].values
            raw = b.get("debug_info.components.rev_weighted.last_history_value")
            raw = raw.values if raw is not None else np.full(len(c), np.nan)
            c20 = pd.Series(c)
            r20past = (c20 / c20.shift(20) - 1).values
            vol = pd.Series(np.log(c)).diff().rolling(20).std().values
            vol120 = pd.Series(np.log(c)).diff().rolling(120).std().values
            for i in range(0, len(c) - H, H):
                fwd = c[i + H] / c[i] - 1
                rows.append(dict(coin=coin, w=w, f=f[i], raw=raw[i], fwd=fwd,
                                 ex=fwd - drift[coin], past20=r20past[i],
                                 volratio=vol[i] / vol120[i] if vol120[i] > 0 else np.nan))
    df = pd.DataFrame(rows)
    df["af"] = df.f.abs()
    df["bucket"] = pd.cut(df.af, [-0.01, 0.0001, 0.5, 1, 2, 5, 21])
    df["sx"] = np.sign(df.f) * df.ex
    df["side"] = np.sign(df.f)
    g = df[df.af > 0].groupby(["bucket", "side"]).sx.agg(["count", "mean",
          lambda x: x.mean() / x.std() * np.sqrt(len(x)) if len(x) > 2 else np.nan])
    g.columns = ["n", "mean_signed_excess", "t"]
    # past 20d return direction vs signal
    act = df[df.af > 0].copy()
    act["past_with_signal"] = np.sign(act.past20) == act.side
    p = act.groupby(["past_with_signal", act.af >= 2]).sx.agg(["count", "mean"])
    # book
    brs = []; long_g = []; short_g = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"].values
            r = pd.Series(b["close"].values).pct_change().shift(-1).values
            gain = a * r
            long_g.append(np.nansum(gain[a > 0])); short_g.append(np.nansum(gain[a < 0]))
            brs.append(dict(coin=coin, w=w, frac_long=(a > 0).mean(), frac_short=(a < 0).mean(),
                            meanabs=np.abs(a).mean(), gain=np.nansum(gain)))
    bdf = pd.DataFrame(brs)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    tdf = pd.concat(tr) if tr else pd.DataFrame()
    tsum = tdf.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"]) if len(tdf) else "none"
    tdf["eb"] = pd.cut(tdf.entry_forecast.abs(), [0, 0.5, 1, 2, 5, 21])
    tb = tdf.groupby("eb").net_profit_loss_percent.agg(["count", "mean", "median"])
    return {"by_bucket_side": g,
            "past20_vs_signal": p,
            "gain_long_vs_short": pd.Series({"long": sum(long_g), "short": sum(short_g)}),
            "book_by_coin": bdf.groupby("coin")[["frac_long", "frac_short", "meanabs", "gain"]].agg({"frac_long": "mean", "frac_short": "mean", "meanabs": "mean", "gain": "sum"}),
            "book_by_window": bdf.groupby("w")[["gain"]].sum(),
            "trades_by_side": tsum,
            "trades_by_entry_forecast": tb,
            "share_active_grid": float((df.af > 0).mean())}
