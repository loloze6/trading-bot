def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            r = b.close.pct_change()
            mad = r.abs().rolling(720, min_periods=200).mean().shift(1)
            z = r / mad
            vr = b.volume / b.volume.rolling(720, min_periods=200).mean()
            df = pd.DataFrame({"z": z, "vr": vr, "coin": c, "w": w})
            df["r720"] = b.close / b.close.shift(720) - 1
            df["r168"] = b.close / b.close.shift(168) - 1
            df["r24"] = b.close / b.close.shift(24) - 1
            for h in (6, 24):
                df[f"f{h}"] = b.close.shift(-h) / b.close - 1
            df["f1"] = b.close.shift(-1) / b.close - 1
            df["pos"] = b["postRebalance_current_allocation"]
            df["gain"] = df.pos * df.f1
            df["fc"] = b["forecast"]
            df["trade"] = (b["postRebalance_current_allocation"] - b["previous_allocation"]).abs()
            df["idx"] = np.arange(len(b))
            df["year"] = pd.to_datetime(b.timestamp).dt.year.values
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per bar over all windows
    d1 = A.groupby("coin").f1.mean()
    A["drift_gain"] = A.pos * A.coin.map(d1)
    A["timing_gain"] = A.gain - A.drift_gain
    out["bar_gain_decomp_bp"] = (A.groupby("coin")[["gain", "drift_gain", "timing_gain"]].mean() * 1e4)
    out["turnover_per_bar"] = A.groupby("coin").trade.mean()
    # fee drag per bar ~ turnover * 0.055% (half round trip)
    out["fee_drag_bp_per_bar"] = A.groupby("coin").trade.mean() * 5.5

    G = A[(A.idx % 6 == 0)].dropna(subset=["z", "vr", "f6"]).copy()
    drift6 = G.groupby("coin").f6.mean()
    G["u6"] = G.f6 - G.coin.map(drift6)
    q = G[(G.vr >= 0.5) & (G.vr <= 1.5) & (G.z > 0.5)].copy()

    def tt(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "short_u6_bp": -s.mean() * 1e4,
                          "t": -s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # quiet rises by 30-day trend tercile
    q["tr"] = pd.qcut(q.r720, 3, labels=["down", "mid", "up"])
    out["quiet_rise_short_u6_by_30d_trend"] = q.groupby("tr", observed=True).u6.apply(tt).unstack()
    q["t7"] = pd.qcut(q.r168, 3, labels=["down", "mid", "up"])
    out["quiet_rise_short_u6_by_7d_trend"] = q.groupby("t7", observed=True).u6.apply(tt).unstack()
    q["t1"] = pd.qcut(q.r24, 3, labels=["down", "mid", "up"])
    out["quiet_rise_short_u6_by_1d_ret"] = q.groupby("t1", observed=True).u6.apply(tt).unstack()
    out["quiet_rise_short_u6_by_year"] = q.groupby("year").u6.apply(tt).unstack()
    # forward 24h after quiet rises by 1d return
    G24 = A[(A.idx % 24 == 0)].dropna(subset=["z", "vr", "f24", "r24"]).copy()
    dr24 = G24.groupby("coin").f24.mean()
    G24["u24"] = G24.f24 - G24.coin.map(dr24)
    G24["t1"] = pd.qcut(G24.r24, 5)
    out["all_bars_u24_by_prior24h_quintile"] = G24.groupby("t1", observed=True).u24.apply(
        lambda s: pd.Series({"n": len(s), "bp": s.mean() * 1e4, "t": s.mean() / (s.std() / np.sqrt(len(s)))})).unstack()
    # book gain by 30d trend tercile on bars held short
    S = A[A.pos < 0].dropna(subset=["r720"]).copy()
    S["tr"] = pd.qcut(S.r720, 3, labels=["down", "mid", "up"])
    out["short_bar_gain_bp_by_30d_trend"] = S.groupby("tr", observed=True)[["gain", "timing_gain"]].mean() * 1e4
    # trades gross by entry forecast
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): tr.append(t)
    tr = pd.concat(tr)
    tr["fb"] = pd.cut(tr.entry_forecast.abs(), [0, 3, 8, 15, 20.1])
    out["trades_by_entry_forecast"] = tr.groupby("fb", observed=True).agg(n=("side", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("duration_minutes", lambda s: s.mean() / 60))
    return out
