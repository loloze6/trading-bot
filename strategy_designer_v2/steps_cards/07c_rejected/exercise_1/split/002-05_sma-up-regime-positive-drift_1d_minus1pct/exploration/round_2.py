def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    allb = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["oc_next"] = b["close"].shift(-1) / b["open"].shift(-1) - 1
            b["gap_next"] = b["open"].shift(-1) / b["close"] - 1
            b["hl_next"] = b["high"].shift(-1) / b["low"].shift(-1) - 1
            b["inst"] = b["forecast"] > 0
            b["inst_next"] = b["inst"].shift(-1)
            b["win"] = w
            allb.append(b)
    A = pd.concat(allb).dropna(subset=["nxt"])
    g = A.groupby(["win", "inst"])
    out["gap_oc_by_win"] = g.agg(n=("nxt", "size"), gap=("gap_next", "mean"), oc=("oc_next", "mean"),
                                 oc_up=("oc_next", lambda x: (x > 0).mean()), gap_std=("gap_next", "std"),
                                 hl=("hl_next", "mean"))
    def tt(x):
        r = stats.ttest_1samp(x.dropna(), 0); return r.statistic
    out["t_components"] = A.groupby("inst").agg(gap_t=("gap_next", tt), oc_t=("oc_next", tt),
                                                 oc_up=("oc_next", lambda x: (x > 0).mean()),
                                                 gap_neg=("gap_next", lambda x: (x < 0).mean()))
    oi = stats.ttest_ind(A[A.inst].oc_next, A[~A.inst].oc_next, equal_var=False)
    out["oc_welch_in_vs_out"] = f"diff={A[A.inst].oc_next.mean()-A[~A.inst].oc_next.mean():.5f} t={oi.statistic:.2f}"
    A["trans"] = A["inst"].astype(int).astype(str) + "->" + A["inst_next"].astype(float).fillna(-1).astype(int).astype(str)
    out["by_transition"] = A.groupby("trans").agg(n=("nxt", "size"), nxt=("nxt", "mean"), gap=("gap_next", "mean"), oc=("oc_next", "mean"))
    out["gap_quant_in"] = A[A.inst]["gap_next"].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    out["gap_quant_out"] = A[~A.inst]["gap_next"].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(win=w))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"),
                                              win_share=("net_profit_loss_percent", lambda x: (x > 0).mean()),
                                              dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    D = pd.concat([d.assign(win=w) for c, ws in data["days"].items() for w, d in ws.items()])
    out["book_vs_coin_by_win"] = D.groupby("win").agg(book=("book_return", lambda x: (1 + x.dropna()).prod() - 1),
                                                      coin=("coin_return", lambda x: (1 + x.dropna()).prod() - 1))
    return out
