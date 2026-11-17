def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    perwin = []
    binrows = []
    fees = []
    # coin mean daily return over all windows
    for coin, wins in data["days"].items():
        cr_all = pd.concat([d["coin_return"] for d in wins.values()]).dropna()
        mu = cr_all.mean()
        for w, d in wins.items():
            b = data["bars"][coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            pos = b.groupby("day")["postRebalance_current_allocation"].last()
            fc = b.groupby("day")["forecast"].last()
            dh = b.groupby("day")["debug_info.components.dist_high.last_history_value"].last()
            dd = d.copy()
            dd["day"] = pd.to_datetime(dd["day"]).dt.floor("D")
            dd = dd.set_index("day")
            dd["pos_prev"] = pos.shift(1).reindex(dd.index)
            dd["fc_prev"] = fc.shift(1).reindex(dd.index)
            dd["dh_prev"] = dh.shift(1).reindex(dd.index)
            dd["coin"] = coin; dd["win"] = w; dd["mu"] = mu
            rows.append(dd.reset_index())
            perwin.append({"coin": coin, "win": w, "book": (1+dd["book_return"].fillna(0)).prod()-1,
                           "hold": (1+dd["coin_return"].fillna(0)).prod()-1,
                           "meanpos": dd["pos_prev"].mean()})
            t = data["trades"][coin][w]
            if len(t):
                fees.append({"coin": coin, "n": len(t), "gross": t["profit_loss_percent"].sum(),
                             "net": t["net_profit_loss_percent"].sum()})
    D = pd.concat(rows, ignore_index=True).dropna(subset=["book_return", "coin_return"])
    D["mkt"] = D["pos_prev"] * D["mu"]
    out["book_vs_hold"] = pd.DataFrame({
        "book_mean": [D.book_return.mean()], "hold_mean": [D.coin_return.mean()],
        "book_sd": [D.book_return.std()], "hold_sd": [D.coin_return.std()],
        "mean_pos": [D.pos_prev.mean()], "share_short": [(D.pos_prev < 0).mean()],
        "share_flat": [(D.pos_prev.abs() < 0.01).mean()],
        "mkt_part": [D.mkt.mean()], "timing": [D.book_return.mean() - D.mkt.mean()]})
    D["posbin"] = pd.cut(D.pos_prev, [-3, -0.5, -0.1, 0.1, 0.5, 1, 3])
    out["by_pos"] = D.groupby("posbin", observed=True).agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin=("coin_return", "mean"), mu=("mu", "mean"))
    D["dhbin"] = pd.qcut(D.dh_prev, 6)
    out["by_dist_high"] = D.groupby("dhbin", observed=True).agg(n=("book_return", "size"),
        book=("book_return", "mean"), coin=("coin_return", "mean"), pos=("pos_prev", "mean"))
    out["by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        pos=("pos_prev", "mean"), short=("pos_prev", lambda s: (s < 0).mean()))
    out["fees"] = pd.DataFrame(fees).groupby("coin").sum() if fees else "none"
    # daily book across coins
    P = D.groupby(["win", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean"),
                                      pos=("pos_prev", "mean"), dh=("dh_prev", "mean")).reset_index()
    P["wn"] = P.win.str[1:].astype(int)
    P = P.sort_values(["wn", "day"])
    out["port_by_window"] = P.groupby("wn").agg(book=("book", lambda s: (1+s).prod()-1),
        hold=("hold", lambda s: (1+s).prod()-1), pos=("pos", "mean"))
    eq = (1 + P.book).cumprod(); dd = eq / eq.cummax() - 1
    out["max_dd"] = float(dd.min())
    # worst 5% book days: what held
    q = P.book.quantile(0.05)
    out["worst_days"] = pd.DataFrame({"n": [(P.book <= q).sum()], "pos": [P.pos[P.book <= q].mean()],
        "hold": [P.hold[P.book <= q].mean()], "dh": [P.dh[P.book <= q].mean()],
        "pos_all": [P.pos.mean()], "dh_all": [P.dh.mean()]})
    return out
