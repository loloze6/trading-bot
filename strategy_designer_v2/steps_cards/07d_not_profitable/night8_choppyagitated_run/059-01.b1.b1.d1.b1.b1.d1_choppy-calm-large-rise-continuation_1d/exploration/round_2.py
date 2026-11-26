def explore(data):
    import pandas as pd, numpy as np
    bars, trades, days = data["bars"], data["trades"], data["days"]
    out = {}
    # features per bar
    feats = {}
    G = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            s = b["close"].astype(float)
            n = len(s)
            r7 = s / s.shift(7) - 1
            mabs = r7.abs().rolling(30).mean()
            sr = r7 / mabs
            r60 = s / s.shift(60) - 1
            r30 = s / s.shift(30) - 1
            hi30 = s.rolling(30).max()
            nh = s / hi30
            f = pd.DataFrame({"ts": b["timestamp"], "sr": sr, "r60": r60, "r30": r30, "nh": nh,
                              "fc": b["forecast"], "reg": b["regime"], "close": s})
            f["f14"] = s.shift(-14) / s - 1
            f["f28"] = s.shift(-28) / s - 1
            f["f7"] = s.shift(-7) / s - 1
            feats[(c, w)] = f
            for p in range(0, n - 14, 14):
                row = f.iloc[p].to_dict(); row["coin"] = c; row["w"] = w
                G.append(row)
    G = pd.DataFrame(G)
    d14 = G["f14"].mean(); d28 = G["f28"].mean()
    def summ(x, col="f14", d=None):
        d = d14 if d is None else d
        e = x[col].dropna() - d
        return pd.Series({"n": len(e), "mean_ex": e.mean(), "mean_tot": e.mean() + d,
                          "t": e.mean() / (e.std() / np.sqrt(len(e))) if len(e) > 2 else np.nan})
    sig = G[(G["reg"] == "unknown") & (G["fc"] > 0)].copy()
    sig["srb"] = pd.cut(sig["sr"], [-9, 0.5, 1.0, 1.5, 9])
    out["sig_by_raw_sr_f14"] = sig.groupby("srb").apply(summ).round(4)
    out["sig_by_raw_sr_f28"] = sig.groupby("srb").apply(lambda x: summ(x, "f28", d28)).round(4)
    # condition alone: near 30d high, no signal, all bars of grid (incl outside profile)
    G["nhb"] = np.where(G["nh"] >= 0.97, "near_hi", "below")
    nos = G[~((G["reg"] == "unknown") & (G["fc"] > 0))]
    out["nosig_all_by_nearhi_f14"] = nos.groupby("nhb").apply(summ).round(4)
    out["nosig_all_by_nearhi_f28"] = nos.groupby("nhb").apply(lambda x: summ(x, "f28", d28)).round(4)
    out["nosig_rise_sr>0.5_by_nearhi"] = nos[nos["sr"] > 0.5].groupby("nhb").apply(summ).round(4)
    sig["nhb"] = np.where(sig["nh"] >= 0.97, "near_hi", "below")
    sig["strong"] = np.where(sig["sr"] > 0.5, "sr>0.5", "sr<=0.5")
    out["sig_strong_x_nearhi"] = sig.groupby(["strong", "nhb"]).apply(summ).round(4)
    out["sig_strong_x_r30"] = sig.groupby(["strong", np.where(sig["r30"] > 0, "r30>0", "r30<=0")]).apply(summ).round(4)
    # trades with entry features
    T = []
    for c in trades:
        for w, t in trades[c].items():
            if t is None or len(t) == 0 or (c, w) not in feats: continue
            f = feats[(c, w)].set_index("ts")
            for _, r in t.iterrows():
                et = r["entry_time"]
                try:
                    fr = f.loc[f.index <= et].iloc[-1]
                except Exception:
                    continue
                T.append({"coin": c, "w": w, "net": r["net_profit_loss_percent"], "sr": fr["sr"], "nh": fr["nh"],
                          "r30": fr["r30"], "r60": fr["r60"], "f14": fr["f14"], "f28": fr["f28"],
                          "days": r["duration_minutes"] / 1440})
    T = pd.DataFrame(T)
    T["srb"] = pd.cut(T["sr"], [-9, 0, 0.5, 1.0, 1.5, 9])
    agg = dict(n=("net", "size"), mean_net=("net", "mean"), med_net=("net", "median"),
               f14=("f14", "mean"), f28=("f28", "mean"), days=("days", "mean"))
    out["trades_by_raw_sr"] = T.groupby("srb").agg(**agg).round(3)
    T["nhb"] = np.where(T["nh"] >= 0.97, "near_hi", "below")
    out["trades_by_nearhi"] = T.groupby("nhb").agg(**agg).round(3)
    T["r30b"] = np.where(T["r30"] > 0, "r30>0", "r30<=0")
    out["trades_by_r30"] = T.groupby("r30b").agg(**agg).round(3)
    bad = T[T["w"].isin(["w7", "w9", "w12", "w14"])]
    out["losing_windows_trades"] = bad.groupby("srb").agg(**agg).round(3)
    out["losing_windows_nearhi"] = bad.groupby("nhb").agg(**agg).round(3)
    return out
