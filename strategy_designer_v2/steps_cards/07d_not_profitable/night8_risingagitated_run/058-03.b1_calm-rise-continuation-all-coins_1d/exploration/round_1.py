def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wn = lambda w: int(w[1:])
    # ---- book daily returns
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    B = D.groupby(["window", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).reset_index()
    B["wn"] = B["window"].map(wn)
    B = B.sort_values(["wn", "day"]).reset_index(drop=True)
    B["br"] = B["br"].fillna(0)
    v = (1 + B["br"]).cumprod()
    peak = v.cummax()
    dd = v / peak - 1
    B["dd"] = dd
    # episodes
    eps = []
    i = 0; n = len(B)
    in_ep = False
    for k in range(n):
        if dd[k] < 0 and not in_ep:
            in_ep = True; start = k
        if in_ep and (dd[k] == 0 or k == n - 1):
            seg = B.iloc[start:k + 1]
            j = seg["dd"].idxmin()
            eps.append((start, j, k, seg["dd"].min()))
            in_ep = False
    eps = sorted(eps, key=lambda e: e[3])[:6]
    ep_tab = []
    for s, j, e, m in eps:
        seg = B.iloc[s:j + 1]
        ep_tab.append({"window": B.loc[s, "window"], "depth": m, "days_to_trough": j - s + 1,
                       "coin_mean_ret_in_fall": (1 + seg["cr"].fillna(0)).prod() - 1})
    out["deepest_falls"] = pd.DataFrame(ep_tab)
    out["book_dd_max"] = float(dd.min())
    # ---- bar-level features for coins
    feats = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.pct_change()
            f = pd.DataFrame({
                "coin": c, "window": w,
                "pos": b["postRebalance_current_allocation"].fillna(0),
                "fc": b["forecast"].fillna(0),
                "dist": cl / cl.rolling(20).mean() - 1,
                "ret5": cl / cl.shift(5) - 1,
                "ret1": r1,
                "ret20": cl / cl.shift(20) - 1,
                "vol10": r1.rolling(10).std(),
                "vol60": r1.rolling(60).std(),
                "nxt": cl.shift(-1) / cl - 1,
                "fwd5": cl.shift(-5) / cl - 1,
                "grid": (np.arange(len(b)) % 5 == 0),
                "regime": b["regime"],
            })
            f["gain"] = f["pos"] * f["nxt"]
            f["vr"] = f["vol10"] / f["vol60"]
            feats.append(f)
    F = pd.concat(feats, ignore_index=True)
    drift5 = F[F.grid].groupby("coin")["fwd5"].mean()
    F["ex5"] = F["fwd5"] - F["coin"].map(drift5)
    held = F[F.pos > 0].copy()
    out["n_held_bars"] = int(len(held))
    def tab(df, col, q=4, val="gain"):
        df = df.dropna(subset=[col, val])
        df = df.assign(b=pd.qcut(df[col], q, duplicates="drop"))
        g = df.groupby("b", observed=True)[val]
        return pd.DataFrame({"n": g.size(), "mean": g.mean(),
                             "t": g.mean() / (g.std() / np.sqrt(g.size())),
                             "share_neg_sum": g.apply(lambda x: x[x < 0].sum())})
    out["held_gain_by_dist"] = tab(held, "dist")
    out["held_gain_by_ret5"] = tab(held, "ret5")
    out["held_gain_by_vr"] = tab(held, "vr")
    out["held_gain_by_ret1"] = tab(held, "ret1")
    # grid: signal vs condition alone
    G = F[F.grid & F.ex5.notna()]
    sig = G[G.fc > 0]; nos = G[(G.fc == 0) & (G.regime == "unknown")]
    out["grid_sig_ex5_by_fc"] = tab(sig, "fc", 4, "ex5")
    out["grid_sig_ex5_by_vr"] = tab(sig, "vr", 3, "ex5")
    out["grid_sig_ex5_by_ret5"] = tab(sig, "ret5", 3, "ex5")
    out["grid_inprofile_nosig_ex5"] = pd.Series({"n": len(nos), "mean": nos.ex5.mean()})
    # trades
    T = pd.concat([t.assign(coin=c, window=w) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["days"] = T["duration_minutes"] / 1440
    out["trades_summary"] = pd.Series({"n": len(T), "mean_net": T.net_profit_loss_percent.mean(),
                                       "mean_gross": T.profit_loss_percent.mean(),
                                       "median_days": T.days.median(),
                                       "worst10_sum": T.net_profit_loss_percent.nsmallest(10).sum(),
                                       "total_sum": T.net_profit_loss_percent.sum()})
    T["db"] = pd.cut(T.days, [0, 5.5, 10, 20, 400])
    out["trades_by_duration"] = T.groupby("db", observed=True)["net_profit_loss_percent"].agg(["size", "mean", "sum"])
    out["held_by_coin"] = held.groupby("coin")["gain"].agg(["size", "mean", "sum"])
    out["held_by_window"] = held.groupby("window")["gain"].agg(["size", "mean", "sum"])
    return out
