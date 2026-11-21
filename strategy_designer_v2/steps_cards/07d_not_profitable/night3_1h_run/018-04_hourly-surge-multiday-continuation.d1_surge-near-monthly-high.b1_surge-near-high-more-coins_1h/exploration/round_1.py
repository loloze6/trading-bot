def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # ---- book daily series: mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"), n=("coin", "count")).reset_index()
    B = B.sort_values(["wn", "day"]).dropna(subset=["book"]).reset_index(drop=True)
    eq = (1 + B["book"]).cumprod()
    peak = eq.cummax(); dd = eq / peak - 1
    B["dd"] = dd.values
    # drawdown episodes
    eps = []
    inside = False
    for i in range(len(B)):
        if B["dd"].iat[i] < 0 and not inside:
            inside = True; start = i
        if inside and (B["dd"].iat[i] == 0 or i == len(B) - 1):
            seg = B.iloc[start:i + 1]
            j = seg["dd"].idxmin()
            eps.append(dict(start_w=B["wn"].iat[start], trough_w=B["wn"].iat[j], depth=seg["dd"].min(),
                            days_to_trough=j - start + 1, days_total=len(seg),
                            book_to_trough=(1 + B["book"].iloc[start:j + 1]).prod() - 1,
                            hold_to_trough=(1 + B["hold"].iloc[start:j + 1]).prod() - 1,
                            s=start, t=j))
            inside = False
    E = pd.DataFrame(eps).sort_values("depth").head(6)
    out["deepest_falls"] = E.drop(columns=["s", "t"]).reset_index(drop=True)
    yrs = len(B) / 365
    out["book_summary"] = pd.Series(dict(days=len(B), yearly=eq.iat[-1] ** (1 / yrs) - 1, maxdd=dd.min(),
                                         hold_yearly=(1 + B["hold"]).prod() ** (1 / yrs) - 1,
                                         hold_maxdd=((1 + B["hold"]).cumprod() / (1 + B["hold"]).cumprod().cummax() - 1).min()))
    # per window
    W = B.groupby("wn").agg(book_sum=("book", "sum"), hold_sum=("hold", "sum"), mindd=("dd", "min"), days=("book", "size"))
    out["per_window"] = W
    # coins' position during the deepest fall
    top = E.iloc[0]
    days_in = B.iloc[int(top.s):int(top.t) + 1][["wn", "day"]]
    key = set(zip(days_in["wn"], days_in["day"]))
    D["in"] = [(a, b) in key for a, b in zip(D["wn"], D["day"])]
    out["coins_in_deepest"] = D[D["in"]].groupby("coin").agg(book=("book_return", "sum"), coin=("coin_return", "sum"), days=("day", "count")).sort_values("book").head(19)

    # ---- trade features at entry
    tr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            t = data["trades"][c].get(w) if isinstance(data["trades"][c], dict) else None
            if t is None or len(t) == 0: continue
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values
            lr = np.log(b["close"]).diff()
            h720 = b["close"].rolling(720, min_periods=200).max().values
            v24 = lr.rolling(24).std().values; v720 = lr.rolling(720, min_periods=200).std().values
            a24 = pd.Series(cl).pct_change(24).abs().rolling(720, min_periods=200).mean().values
            idx = np.searchsorted(ts.values, pd.to_datetime(t["entry_time"]).values)
            for k, i in enumerate(idx):
                if i >= len(b): continue
                def r(n):
                    return cl[i] / cl[i - n] - 1 if i >= n else np.nan
                tr.append(dict(coin=c, wn=int(w[1:]), net=t["net_profit_loss_percent"].iat[k],
                               r24=r(24), r168=r(168), r720=r(720), r2160=r(2160),
                               dist=cl[i] / h720[i] - 1 if not np.isnan(h720[i]) else np.nan,
                               surge=r(24) / a24[i] if a24[i] > 0 else np.nan,
                               volr=v24[i] / v720[i] if v720[i] > 0 else np.nan,
                               dur=t["duration_minutes"].iat[k] / 60))
    T = pd.DataFrame(tr)
    out["trades_summary"] = pd.Series(dict(n=len(T), mean_net=T["net"].mean(), median_net=T["net"].median(),
                                           win=(T["net"] > 0).mean(), mean_dur_h=T["dur"].mean()))
    for f in ["r720", "r2160", "r168", "dist", "surge", "volr"]:
        x = T.dropna(subset=[f])
        q = pd.qcut(x[f], 5, duplicates="drop")
        g = x.groupby(q, observed=True)["net"].agg(["count", "mean", "median", lambda s: (s > 0).mean(),
                                                    lambda s: s.mean() / s.std() * np.sqrt(len(s))])
        g.columns = ["n", "mean", "median", "win", "t"]
        g.index = [f"q{i+1} {iv.left:.3g}..{iv.right:.3g}" for i, iv in enumerate(g.index)]
        out["net_by_" + f] = g
    return out
