def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    coins = list(data["days"].keys())
    wins = list(data["days"][coins[0]].keys())
    # ---- book daily (mean across coins) in window order
    rows = []
    for w in wins:
        b = {}; c = {}
        for k in coins:
            d = data["days"][k].get(w)
            if d is None: continue
            b[k] = d.set_index("day")["book_return"]; c[k] = d.set_index("day")["coin_return"]
        B = pd.DataFrame(b); C = pd.DataFrame(c)
        df = pd.DataFrame({"book": B.mean(axis=1), "hold": C.mean(axis=1)})
        df["w"] = w; df["pos"] = range(len(df))
        rows.append(df.dropna())
    P = pd.concat(rows, ignore_index=True)
    eq = (1 + P["book"]).cumprod(); dd = eq / eq.cummax() - 1
    P["dd"] = dd.values
    t = int(dd.values.argmin()); pk = int(eq.iloc[:t+1].values.argmax())
    out["overall"] = pd.Series({"book_mean": P.book.mean(), "hold_mean": P.hold.mean(),
        "book_sh": P.book.mean()/P.book.std()*np.sqrt(365), "hold_sh": P.hold.mean()/P.hold.std()*np.sqrt(365),
        "maxdd": dd.min(), "fall_days": t-pk, "peak_win": P.w.iloc[pk], "trough_win": P.w.iloc[t],
        "hold_ret_in_fall": (1+P.hold.iloc[pk+1:t+1]).prod()-1, "book_ret_in_fall": (1+P.book.iloc[pk+1:t+1]).prod()-1})
    # per window
    g = P.groupby("w", sort=False)
    out["per_window"] = pd.DataFrame({"book_mean_bps": g.book.mean()*1e4, "hold_mean_bps": g.hold.mean()*1e4,
        "book_min_dd": g.apply(lambda x: ((1+x.book).cumprod()/(1+x.book).cumprod().cummax()-1).min()), "n": g.size()})
    # ---- per coin bar-level, cases
    cases = []; percoin = []; drift_tl = []
    for k in coins:
        allr = []
        for w, bars in data["bars"][k].items():
            bars = bars.reset_index(drop=True)
            cl = bars.close.values; hi = bars.high.values; lo = bars.low.values
            r18 = np.full(len(cl), np.nan); r18[:-18] = cl[18:]/cl[:-18]-1
            allr.append(r18[::18])
            al = bars.postRebalance_current_allocation.values
            g1 = np.r_[al[:-1]*(cl[1:]/cl[:-1]-1), np.nan]
            percoin.append({"coin": k, "w": w, "gain": np.nansum(g1), "avg_alloc": np.nanmean(np.abs(al))})
            pmax = pd.Series(hi).shift(1).rolling(12).max().values
            rng = (hi-lo)/cl
            r7 = pd.Series(rng).rolling(42).mean().values; r60 = pd.Series(rng).rolling(360).mean().values
            ret60 = np.r_[np.full(360, np.nan), cl[360:]/cl[:-360]-1] if len(cl) > 360 else np.full(len(cl), np.nan)
            ret7 = np.r_[np.full(42, np.nan), cl[42:]/cl[:-42]-1]
            ret2 = np.r_[np.full(12, np.nan), cl[12:]/cl[:-12]-1]
            brk = (cl > pmax)
            strength = (cl - pmax)/cl
            idx = np.arange(len(cl)); cell = idx//18
            df = pd.DataFrame({"brk": brk, "cell": cell, "r18": r18, "q": r60/r7, "ret60": ret60, "ret7": ret7,
                "ret2": ret2, "str": strength/ (rng*0+r7), "barret": np.r_[np.nan, cl[1:]/cl[:-1]-1]/r7, "fc": bars.forecast.values})
            df = df[df.brk & df.r18.notna()].groupby("cell").first()
            df["coin"] = k; df["w"] = w
            cases.append(df)
        a = np.concatenate(allr); a = a[~np.isnan(a)]
        drift_tl.append({"coin": k, "drift": a.mean(), "sd": a.std()})
    D = pd.DataFrame(drift_tl).set_index("coin")
    X = pd.concat(cases)
    X["u"] = X.r18 - X.coin.map(D.drift)
    out["drift"] = D
    out["cases_by_coin"] = X.groupby("coin").u.agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    def grp(col):
        q = pd.qcut(X[col], 5, labels=False, duplicates="drop")
        return X.groupby(q).agg(mean_u=("u", "mean"), mean_x=(col, "mean"), n=("u", "size"),
            t=("u", lambda s: s.mean()/s.std()*np.sqrt(len(s))))
    for col in ["q", "ret60", "ret7", "ret2", "str", "barret"]:
        out["by_" + col] = grp(col)
    PC = pd.DataFrame(percoin)
    out["gain_by_coin"] = PC.groupby("coin")[["gain", "avg_alloc"]].mean()
    return out
