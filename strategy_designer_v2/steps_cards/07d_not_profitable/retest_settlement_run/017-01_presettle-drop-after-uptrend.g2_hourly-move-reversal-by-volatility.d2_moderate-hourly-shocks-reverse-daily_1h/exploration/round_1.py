def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    # 1. book vs holding by coin, turnover and fee drag
    rows = []
    gross_rows = []
    cases = []
    for c in bars:
        bd = []; cd = []; turn = 0; nbars = 0; gross = 0; fees = 0
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            d = days[c][w]
            bd.append(d["book_return"].dropna()); cd.append(d["coin_return"].dropna())
            pos = b["postRebalance_current_allocation"].fillna(0)
            prev = b["previous_allocation"].fillna(0)
            r1 = b["close"].shift(-1) / b["close"] - 1
            g = pos * r1
            turn += (pos - prev).abs().sum(); nbars += len(b)
            gross += g.sum()
            fees += ((b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]).clip(lower=0).sum()
            gb = pd.DataFrame({"g": g, "side": np.sign(pos), "hour": b["timestamp"].dt.hour if hasattr(b["timestamp"], "dt") else pd.to_datetime(b["timestamp"]).dt.hour})
            gross_rows.append(gb.assign(coin=c))
            # grid cases, 24h
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            lr = np.log(b["close"]).diff()
            shock = lr / lr.rolling(24).std()
            ret24 = b["close"].shift(-24) / b["close"] - 1
            trend7 = b["close"] / b["close"].shift(168) - 1
            trend24 = b["close"] / b["close"].shift(24) - 1
            vol24 = lr.rolling(24).std()
            idx = np.arange(0, len(b), 24)
            cases.append(pd.DataFrame({"coin": c, "w": w, "f": b["forecast"].values[idx], "shock": shock.values[idx],
                                       "r": ret24.values[idx], "t7": trend7.values[idx], "t24": trend24.values[idx],
                                       "vol": vol24.values[idx], "hour": ts.dt.hour.values[idx],
                                       "pos": pos.values[idx]}))
        bd = pd.concat(bd); cd = pd.concat(cd)
        rows.append({"coin": c, "book_sh": bd.mean()/bd.std()*np.sqrt(365), "hold_sh": cd.mean()/cd.std()*np.sqrt(365),
                     "book_mean%": bd.mean()*100, "turnover_per_day": turn/nbars*24,
                     "gross_per_day%": gross/nbars*24*100, "fee_per_day%": fees/nbars*24*100})
    out["by_coin"] = pd.DataFrame(rows).round(4)
    G = pd.concat(gross_rows)
    out["gross_by_side_per_bar_bp"] = (G.groupby("side")["g"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"]*1e4)).round(3)
    C = pd.concat(cases).dropna(subset=["r", "shock"])
    mu = C.groupby("coin")["r"].transform("mean")
    C["ur"] = C["r"] - mu
    C["dirr"] = np.sign(-C["shock"]) * C["ur"]
    C["absr"] = np.sign(-C["shock"]) * C["r"]
    C["sb"] = pd.cut(C["shock"].abs(), [0, 0.5, 1, 1.5, 2, 3, 100])
    def tt(s): return pd.Series({"n": len(s), "mean%": s.mean()*100, "t": s.mean()/s.std()*np.sqrt(len(s))})
    out["fade_by_abs_shock"] = C.groupby("sb")["dirr"].apply(tt).unstack().round(3)
    C["side"] = np.where(C["shock"] < 0, "long_after_drop", "short_after_rise")
    out["fade_by_side"] = C.groupby("side")["absr"].apply(tt).unstack().round(3)
    C["trend_vs_shock"] = np.where(np.sign(C["t7"]) == np.sign(C["shock"]), "shock_with_7d_trend", "shock_against_7d_trend")
    out["fade_by_trend_alignment"] = C.dropna(subset=["t7"]).groupby("trend_vs_shock")["dirr"].apply(tt).unstack().round(3)
    C["volq"] = C.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=["lowvol", "midvol", "highvol"]))
    out["fade_by_vol_tercile"] = C.groupby("volq")["dirr"].apply(tt).unstack().round(3)
    C["t24b"] = C.groupby("coin")["t24"].transform(lambda v: pd.qcut((v).abs(), 3, labels=["small24", "mid24", "big24"]))
    C["t24dir"] = np.sign(-C["t24"]) * C["ur"]
    out["fade_24h_return_by_size"] = C.dropna(subset=["t24"]).groupby("t24b")["t24dir"].apply(tt).unstack().round(3)
    # 4h shock grouping: sum of last 4h relative to vol
    out["fade_by_hour_of_grid"] = C.groupby("hour")["dirr"].apply(tt).unstack().round(3)
    # window book vs coin
    wr = []
    for w in days[list(days)[0]]:
        b = np.mean([ (1+days[c][w]["book_return"].dropna()).prod()-1 for c in days if w in days[c]])
        h = np.mean([ (1+days[c][w]["coin_return"].dropna()).prod()-1 for c in days if w in days[c]])
        wr.append({"w": w, "book%": b*100, "hold%": h*100})
    out["by_window"] = pd.DataFrame(wr).round(2)
    return out
