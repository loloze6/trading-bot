def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["days"].keys())
    wins = sorted({w for c in coins for w in data["days"][c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            x = d[["day","book_return","coin_return"]].copy(); x["coin"] = c
            frames.append(x)
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index()
        g["w"] = w
        rows.append(g)
    B = pd.concat(rows).dropna(subset=["book"]).reset_index(drop=True)
    eq = (1+B["book"]).cumprod()
    dd = eq/eq.cummax()-1
    B["dd"] = dd.values
    yr = eq.iloc[-1]**(365/len(B))-1
    out["summary"] = pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr/-dd.min(), "ndays": len(B)})
    # drawdown episodes
    peak_idx = None; eps = []
    cm = eq.cummax()
    in_dd = False
    for i in range(len(B)):
        if dd.iloc[i] < 0 and not in_dd:
            in_dd = True; start = i-1 if i>0 else 0
        if in_dd and dd.iloc[i] == 0:
            seg = dd.iloc[start:i]; eps.append((start, seg.idxmin(), i, seg.min())); in_dd = False
    if in_dd:
        seg = dd.iloc[start:]; eps.append((start, seg.idxmin(), len(B)-1, seg.min()))
    E = pd.DataFrame(eps, columns=["s","trough","e","depth"]).sort_values("depth").head(8)
    E["w_start"] = B.loc[E.s,"w"].values; E["w_trough"] = B.loc[E.trough,"w"].values
    E["days_to_trough"] = E.trough-E.s
    E["hold_ret_same"] = [ (1+B.loc[a+1:b,"hold"]).prod()-1 for a,b in zip(E.s,E.trough)]
    out["deepest_falls"] = E.drop(columns=["s","trough","e"]).reset_index(drop=True)
    # by window
    out["by_window"] = B.groupby("w").agg(book=("book","sum"), hold=("hold","sum"), mindd=("dd","min")).reindex(wins)
    # trades analysis with context from bars
    T = []
    for c in coins:
        for w, b in data["bars"][c].items():
            t = data["trades"][c].get(w)
            if t is None or len(t)==0: continue
            b = b.copy(); b["ts"] = pd.to_datetime(b["timestamp"])
            r = b["close"].pct_change()
            b["vol20"] = r.rolling(20).std()
            b["vol60m"] = b["vol20"].rolling(120, min_periods=30).median()
            b["ret90"] = b["close"]/b["close"].shift(90)-1
            b["ret30"] = b["close"]/b["close"].shift(30)-1
            b["ret5"] = b["close"]/b["close"].shift(5)-1
            b["up"] = r/b["vol20"].shift(1)
            b["dist_hi"] = b["close"]/b["close"].rolling(60,min_periods=20).max()-1
            tt = t.copy(); tt["et"] = pd.to_datetime(tt["entry_time"])
            m = pd.merge_asof(tt.sort_values("et"), b[["ts","vol20","vol60m","ret90","ret30","ret5","up","dist_hi"]].sort_values("ts"), left_on="et", right_on="ts", direction="backward")
            m["coin"] = c; m["w"] = w
            T.append(m)
    T = pd.concat(T)
    T["pnl"] = T["net_profit_loss_percent"]
    T["volratio"] = T["vol20"]/T["vol60m"]
    out["trades_overall"] = pd.Series({"n": len(T), "mean": T.pnl.mean(), "median": T.pnl.median(), "share_win": (T.pnl>0).mean(), "worst10_mean": T.pnl.nsmallest(10).mean(), "days_mean": T.duration_minutes.mean()/1440})
    def bucket(col, q=4):
        x = T.dropna(subset=[col]).copy()
        x["b"] = pd.qcut(x[col], q, duplicates="drop")
        return x.groupby("b").agg(n=("pnl","size"), mean=("pnl","mean"), std=("pnl","std"), p10=("pnl", lambda s: s.quantile(.1)), win=("pnl", lambda s:(s>0).mean()), xmean=(col,"mean"))
    for col in ["ret90","ret30","ret5","up","volratio","vol20","dist_hi","entry_forecast"]:
        out["by_"+col] = bucket(col)
    out["by_coin"] = T.groupby("coin").pnl.agg(["size","mean","std","min"])
    return out
