import pandas as pd, numpy as np

def explore(data):
    out = {}
    # book daily returns: per window, mean over coins per day
    days = data["days"]; bars = data["bars"]
    coins = list(days.keys())
    wins = sorted(set(w for c in coins for w in days[c]), key=lambda s: int(s[1:]))
    rows = []
    for w in wins:
        dfs = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                dfs.append(d)
        d = pd.concat(dfs)
        g = d.groupby("day")[["book_return", "coin_return"]].mean().sort_index()
        g["win"] = w
        rows.append(g.dropna())
    book = pd.concat(rows).reset_index()
    eq = (1 + book["book_return"]).cumprod()
    dd = eq / eq.cummax() - 1
    book["dd"] = dd.values
    # yearly & maxdd
    n = len(book)
    yr = eq.iloc[-1] ** (365 / n) - 1
    out["book summary"] = pd.Series({"days": n, "yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(),
                                     "hold_yearly": (1+book["coin_return"]).cumprod().iloc[-1]**(365/n)-1,
                                     "hold_maxdd": ((1+book["coin_return"]).cumprod()/(1+book["coin_return"]).cumprod().cummax()-1).min()})
    # drawdown episodes
    peak = eq.cummax()
    ep = []
    i = 0
    vals = eq.values; pk = peak.values
    start = None
    for k in range(n):
        if vals[k] < pk[k] - 1e-12:
            if start is None: start = k
        else:
            if start is not None:
                ep.append((start, k)); start = None
    if start is not None: ep.append((start, n - 1))
    epr = []
    for s, e in ep:
        seg = dd.iloc[s:e+1]
        tr = seg.idxmin()
        epr.append({"start_pos": s, "trough_pos": tr, "end_pos": e, "depth": seg.min(),
                    "days_to_trough": tr - s + 1, "wins": ",".join(sorted(set(book["win"].iloc[s:tr+1]), key=lambda x:int(x[1:]))),
                    "coin_ret_to_trough": (1+book["coin_return"].iloc[s:tr+1]).prod()-1,
                    "book_ret_to_trough": (1+book["book_return"].iloc[s:tr+1]).prod()-1})
    epr = pd.DataFrame(epr).sort_values("depth").head(8)
    out["deepest falls"] = epr.drop(columns=["start_pos","end_pos"])
    # per-window book and coin
    pw = book.groupby("win").agg(book=("book_return", lambda x: (1+x).prod()-1),
                                 coin=("coin_return", lambda x: (1+x).prod()-1),
                                 worst_dd=("dd","min"))
    pw = pw.loc[sorted(pw.index, key=lambda x:int(x[1:]))]
    out["per window"] = pw
    # bar-level gains with features
    br = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]
            b["nxt"] = cl.shift(-1)/cl - 1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * b["nxt"]
            b["ret30"] = cl/cl.shift(30)-1
            b["ret7"] = cl/cl.shift(7)-1
            b["dist60"] = cl/cl.rolling(60, min_periods=30).max()-1
            b["vol20"] = cl.pct_change().rolling(20).std()
            b["coin"] = c; b["win"] = w
            br.append(b[["pos","gain","nxt","ret30","ret7","dist60","vol20","forecast","coin","win"]])
    B = pd.concat(br).dropna(subset=["gain"])
    B["side"] = np.sign(B["pos"])
    out["gain by side"] = B.groupby("side")["gain"].agg(["count","mean","std","sum"])
    for f in ["ret30","ret7","dist60","vol20"]:
        sub = B.dropna(subset=[f])
        sub = sub[sub["pos"]!=0]
        q = pd.qcut(sub[f], 5, labels=False)
        out[f"gain by {f} quintile, long/short"] = sub.groupby([q, "side"])["gain"].agg(["count","mean","sum"]).unstack()
    out["gain by coin side"] = B[B.pos!=0].groupby(["coin","side"])["gain"].sum().unstack()
    return out
