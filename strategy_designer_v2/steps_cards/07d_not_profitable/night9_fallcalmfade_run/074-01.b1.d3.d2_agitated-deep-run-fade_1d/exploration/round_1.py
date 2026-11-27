def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, mean over coins per day, by window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index().dropna()
    B = B.sort_values(["wn", "day"]).reset_index(drop=True)
    v = (1 + B["br"]).cumprod()
    dd_ = v / v.cummax() - 1
    B["dd"] = dd_
    out["book_summary"] = pd.Series({"days": len(B), "mean": B.br.mean(), "sd": B.br.std(),
                                     "maxdd": dd_.min(), "end_value": v.iloc[-1]})
    # per window
    out["by_window"] = B.groupby("wn").agg(sum_br=("br", "sum"), mean_cr=("cr", "mean"), mindd=("dd", "min"), n=("br", "size"))
    # drawdown episodes: top 5 by depth
    peak = v.cummax()
    ep = (dd_ == 0).cumsum()
    E = pd.DataFrame({"ep": ep, "dd": dd_, "wn": B.wn, "br": B.br})
    eps = E.groupby("ep").agg(depth=("dd", "min"), length=("dd", "size"), w_start=("wn", "first"), w_end=("wn", "last"),
                              worst_day=("br", "min"), n_loss_days=("br", lambda s: (s < 0).sum()))
    out["dd_episodes"] = eps.sort_values("depth").head(6)
    # ---- cases
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            mad = pd.Series(np.abs(r)).rolling(30, min_periods=20).mean().values
            n = len(b)
            run = np.zeros(n, int)
            for i in range(1, n):
                run[i] = run[i-1] + 1 if r[i] < 0 else 0
            for i in range(2, n - 1):
                if r[i] > 0 and run[i-1] >= 2:
                    k = run[i-1]
                    if i - 1 - k < 0:
                        continue
                    loss = cl[i-1] / cl[i-1-k] - 1
                    # 20-day trend inside window as proxy
                    tr20 = cl[i] / cl[i-20] - 1 if i >= 20 else np.nan
                    cases.append(dict(coin=c, wn=int(w[1:]), k=k, depth=-loss / mad[i] if mad[i] > 0 else np.nan,
                                      up=r[i] / mad[i] if mad[i] > 0 else np.nan, nxt=r[i+1],
                                      nxt3=cl[min(i+3, n-1)] / cl[i] - 1 if i + 3 < n else np.nan,
                                      reg=b["regime"].iloc[i], alloc=b["postRebalance_current_allocation"].iloc[i],
                                      fc=b["forecast"].iloc[i], tr20=tr20))
    C = pd.DataFrame(cases)
    mu = D.groupby("coin")["coin_return"].mean()
    C["unus"] = -(C["nxt"] - C["coin"].map(mu))
    C["held"] = C["alloc"] < 0
    def g(s):
        return pd.Series({"n": len(s), "mean_short": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    out["by_regime"] = C.groupby("reg")["unus"].apply(g).unstack()
    out["held_vs_not"] = C.groupby("held")["unus"].apply(g).unstack()
    C["kb"] = C["k"].clip(upper=5)
    out["held_by_runlen"] = C[C.held].groupby("kb")["unus"].apply(g).unstack()
    out["notheld_by_runlen"] = C[~C.held].groupby("kb")["unus"].apply(g).unstack()
    H = C[C.held].copy()
    H["upq"] = pd.qcut(H["up"], 3, labels=["small_up", "mid_up", "big_up"])
    out["held_by_upday_size"] = H.groupby("upq")["unus"].apply(g).unstack()
    H["dq"] = pd.qcut(H["depth"], 3, labels=["shallow", "mid", "deep"])
    out["held_by_depth"] = H.groupby("dq")["unus"].apply(g).unstack()
    N = C[~C.held].copy()
    N["trb"] = pd.cut(N["tr20"], [-9, -0.1, 0.1, 9], labels=["fall20", "flat20", "rise20"])
    out["notheld_by_tr20"] = N.groupby("trb")["unus"].apply(g).unstack()
    H["trb"] = pd.cut(H["tr20"], [-9, -0.1, 0.1, 9], labels=["fall20", "flat20", "rise20"])
    out["held_by_tr20"] = H.groupby("trb")["unus"].apply(g).unstack()
    out["held_by_coin"] = H.groupby("coin")["unus"].apply(g).unstack()
    out["held_worst_cases_stats"] = pd.Series({"share_loss_gt_5pct": (H.unus < -0.05).mean(),
                                               "sum_losses_gt5": H.unus[H.unus < -0.05].sum(), "sum_all": H.unus.sum(),
                                               "mean_abs_alloc": H.alloc.abs().mean()})
    out["held_3day"] = g(-(H["nxt3"].dropna()))
    return out
