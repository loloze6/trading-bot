def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; days = data["days"]
    daily = {}  # variant -> list of per-coin daily series keyed (w, day)
    cases = []
    falls = []
    COST = 0.0019 / 2
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            day = ts.dt.floor("D")
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = (b["close"].shift(-1) / b["close"] - 1).fillna(0)
            lr = np.log(b["close"]).diff()
            vol = lr.rolling(24).std()
            volrank = vol.rolling(720, min_periods=200).rank(pct=True)
            t7 = b["close"] / b["close"].shift(168) - 1
            variants = {
                "actual_sim": pos,
                "long_only": pos.clip(lower=0),
                "short_only": pos.clip(upper=0),
                "long_only_highvol": pos.clip(lower=0).where(volrank > 2/3, 0),
                "long_only_not_lowvol": pos.clip(lower=0).where(volrank > 1/3, 0),
                "long_only_7d_down": pos.clip(lower=0).where(t7 < 0, 0),
                "hold": pd.Series(1.0, index=b.index),
            }
            for k, p in variants.items():
                p = p.fillna(0)
                g = p * r1 - (p.diff().abs().fillna(p.abs()) * COST)
                s = g.groupby(day).sum()
                s.index = [(w, d) for d in s.index]
                daily.setdefault(k, {}).setdefault(c, []).append(s)
            # actual book: deepest fall per coin-window
            d = days[c][w]
            v = d["book_value"].values
            peak = np.maximum.accumulate(v); dd = v / peak - 1
            i = int(np.argmin(dd)); j = int(np.argmax(v[:i+1])) if i > 0 else 0
            dsel = day.isin(pd.to_datetime(d["day"]).iloc[j:i+1].values) if i > j else pd.Series(False, index=b.index)
            if i > j:
                falls.append({"coin": c, "w": w, "dd%": dd[i]*100,
                              "coin_ret_in_fall%": (d["close"].values[i]/d["close"].values[j]-1)*100,
                              "mean_pos": pos[dsel].mean(), "share_short": (pos[dsel] < 0).mean(),
                              "days": i - j})
            idx = np.arange(0, len(b), 24)
            r24 = b["close"].shift(-24) / b["close"] - 1
            shock = lr / vol
            cases.append(pd.DataFrame({"coin": c, "r": r24.values[idx], "shock": shock.values[idx],
                                       "vr": volrank.values[idx], "t7": t7.values[idx]}))
    def stats_(series_by_coin):
        S = pd.concat({c: pd.concat(v) for c, v in series_by_coin.items()}, axis=1).mean(axis=1)
        # chain in window order
        wins = sorted(set(k[0] for k in S.index), key=lambda x: int(x[1:]))
        S = pd.concat([S[[k for k in S.index if k[0] == w]] for w in wins])
        val = (1 + S).cumprod(); mdd = (val / val.cummax() - 1).min()
        yr = val.iloc[-1] ** (365 / len(S)) - 1
        return {"sharpe": S.mean()/S.std()*np.sqrt(365), "mean%": S.mean()*100, "yearly%": yr*100,
                "maxdd%": mdd*100, "calmar": yr/abs(mdd) if mdd < 0 else np.nan}
    out["variants_sim_with_cost"] = pd.DataFrame({k: stats_(v) for k, v in daily.items()}).T.round(3)
    F = pd.DataFrame(falls).sort_values("dd%")
    out["deepest_falls_top15"] = F.head(15).drop(columns=["w"]).round(3).reset_index(drop=True)
    out["falls_corr_coinret_dd"] = float(np.corrcoef(F["coin_ret_in_fall%"], F["dd%"])[0, 1])
    C = pd.concat(cases).dropna()
    C["ur"] = C["r"] - C.groupby("coin")["r"].transform("mean")
    def tt(s): return pd.Series({"n": len(s), "mean%": s.mean()*100, "t": s.mean()/s.std()*np.sqrt(len(s))})
    C["volb"] = pd.cut(C["vr"], [0, 1/3, 2/3, 1.0], labels=["low", "mid", "high"])
    C["drop"] = np.where(C["shock"] < 0, "after_drop", "after_rise")
    # condition alone: raw 24h coin return (long) by vol band, all bars vs after drop
    out["long_raw_ret_by_vol_and_side"] = C.groupby(["volb", "drop"])["r"].apply(tt).unstack().round(3)
    out["long_raw_ret_by_vol_all"] = C.groupby("volb")["r"].apply(tt).unstack().round(3)
    D = C[C["shock"] < 0].copy()
    D["sb"] = pd.cut(-D["shock"], [0, 0.5, 1, 2, 3, 100])
    out["after_drop_raw_ret_by_size_and_vol"] = D.groupby(["volb", "sb"])["r"].apply(tt).unstack().round(3)
    C["t7s"] = np.where(C["t7"] < 0, "7d_down", "7d_up")
    out["long_raw_ret_by_7d_and_side"] = C.groupby(["t7s", "drop"])["r"].apply(tt).unstack().round(3)
    return out
