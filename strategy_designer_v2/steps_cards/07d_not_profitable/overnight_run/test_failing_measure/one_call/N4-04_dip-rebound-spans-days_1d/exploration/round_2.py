def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    # coin mean 1-bar and 3-bar over all windows
    cm1, cm3 = {}, {}
    for c in coins:
        r1s, r3s = [], []
        for w in wins:
            cl = data["bars"][c][w]["close"].reset_index(drop=True)
            r1s.append(cl.pct_change().dropna()); r3s.append((cl.shift(-3)/cl-1).dropna())
        cm1[c] = pd.concat(r1s).mean(); cm3[c] = pd.concat(r3s).mean()
    ev = []
    dayrows = []
    for c in coins:
        for w in wins:
            b = data["bars"][c][w].reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            z = (r1 - r1.rolling(60, min_periods=20).mean()) / r1.rolling(60, min_periods=20).std()
            f1 = cl.shift(-1)/cl - 1; f3 = cl.shift(-3)/cl - 1
            dd20 = cl / cl.rolling(20).max() - 1
            r5 = cl.pct_change(5); r20 = cl.pct_change(20)
            downs = (r1 < 0).astype(int)
            streak = downs.groupby((downs == 0).cumsum()).cumsum()
            vol = r1.rolling(20).std(); volratio = vol / r1.rolling(60).std()
            last = -10
            for i in range(len(b)):
                if b["forecast"].iloc[i] > 0 and not np.isnan(f3.iloc[i]) and i - last >= 3:
                    ev.append({"coin": c, "win": w, "z": z.iloc[i], "r1": r1.iloc[i], "f1": f1.iloc[i] - cm1[c],
                               "f3": f3.iloc[i] - cm3[c], "streak": streak.iloc[i], "dd20": dd20.iloc[i],
                               "r5": r5.iloc[i], "r20": r20.iloc[i], "volratio": volratio.iloc[i],
                               "prevr1": r1.iloc[i-1] if i > 0 else np.nan})
                    last = i
            # days: book value per bar for book daily
    E = pd.DataFrame(ev)
    out["n_events"] = len(E)
    def g(col, q=4):
        G = E.groupby(pd.qcut(E[col], q, duplicates="drop"))["f3"]
        r = G.agg(["mean", "count", "std"]); r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["share_lt_-10pct"] = E.groupby(pd.qcut(E[col], q, duplicates="drop"))["f3"].apply(lambda x: (x < -0.10).mean())
        return r
    out["f3_by_streak"] = E.groupby(E["streak"].clip(upper=4))["f3"].agg(["mean", "count", "std"])
    out["f3_by_dd20"] = g("dd20")
    out["f3_by_r5"] = g("r5")
    out["f3_by_z"] = g("z")
    out["f3_by_volratio"] = g("volratio")
    out["f3_by_r20"] = g("r20")
    out["f3_by_prevr1_sign"] = E.groupby(E["prevr1"] < 0)["f3"].agg(["mean", "count", "std"])
    # book daily, deepest drawdowns
    rows = []
    for w in wins:
        frames = [data["days"][c][w].set_index("day")[["book_return", "coin_return"]].add_suffix("_" + c) for c in coins]
        df = pd.concat(frames, axis=1)
        br = df[[f"book_return_{c}" for c in coins]].mean(axis=1).fillna(0)
        eq = (1 + br).cumprod(); dd = eq / eq.cummax() - 1
        trough = dd.values.argmin()
        peak = eq.values[:trough+1].argmax()
        seg = df.iloc[peak+1:trough+1]
        contrib = {c: seg[f"book_return_{c}"].fillna(0).sum()/len(coins) for c in coins}
        rows.append({"win": w, "dd": dd.min(), "len_days": trough - peak,
                     "worst_coin": min(contrib, key=contrib.get), "worst_contrib": min(contrib.values()),
                     "share_from_worst": min(contrib.values()) / sum(contrib.values()) if sum(contrib.values()) < 0 else np.nan,
                     "n_bad_days_lt_-2pct": int((br.iloc[peak+1:trough+1] < -0.02).sum()),
                     "loss_in_lt_-2pct_days": br.iloc[peak+1:trough+1][br.iloc[peak+1:trough+1] < -0.02].sum()})
    out["dd_episodes"] = pd.DataFrame(rows).set_index("win").sort_values("dd").head(10)
    return out
