def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats as st
    out = {}
    rows = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            b = data["bars"][c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"]); dd = dd.set_index("day")
            dd["pos_prev"] = last["postRebalance_current_allocation"].shift(1).reindex(dd.index)
            dd["fc_prev"] = last["forecast"].shift(1).reindex(dd.index)
            cl = dd["close"]
            dd["ret30_prev"] = (cl / cl.shift(30) - 1).shift(1)
            dd["ret90_prev"] = (cl / cl.shift(90) - 1).shift(1)
            r = dd["coin_return"]
            v30 = r.rolling(30).std(); v90 = r.rolling(90).std()
            dd["vratio_prev"] = (v30 / v90).shift(1)
            dd["fwd14"] = cl.shift(-14) / cl - 1
            dd["pos_i"] = np.arange(len(dd))
            dd["coin"] = c; dd["window"] = w
            rows.append(dd.reset_index())
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    D["side"] = np.sign(D["pos_prev"])
    # book by abs position quintile among active days
    A = D[D["pos_prev"].abs() > 0].dropna(subset=["book_return"]).copy()
    A["absq"] = pd.qcut(A["pos_prev"].abs(), 4, labels=False)
    out["by_abs_pos"] = A.groupby("absq").agg(n=("book_return", "size"), abs_pos=("pos_prev", lambda s: s.abs().mean()), book=("book_return", "mean"), book_sd=("book_return", "std"), signed_coin=("coin_return", "mean"))
    # book by side x sign of 90d return
    A2 = A.dropna(subset=["ret90_prev"]).copy()
    A2["trend90"] = np.where(A2["ret90_prev"] > 0, "up90", "down90")
    out["side_x_trend90"] = A2.groupby(["side", "trend90"]).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"), t=("book_return", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    A3 = A.dropna(subset=["ret30_prev"]).copy()
    A3["trend30"] = np.where(A3["ret30_prev"] > 0, "up30", "down30")
    out["side_x_trend30"] = A3.groupby(["side", "trend30"]).agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))
    # non-overlapping 14d grid, active forecast: signed fwd return by trend90
    G = D[(D["pos_i"] % 14 == 0) & (D["fc_prev"].notna())].copy()
    G = G[G["fc_prev"] != 0].dropna(subset=["fwd14", "ret90_prev"])
    G["signed"] = np.sign(G["fc_prev"]) * G["fwd14"]
    G["trend90"] = np.where(G["ret90_prev"] > 0, "up90", "down90")
    out["grid_signed_by_trend"] = G.groupby([np.sign(G["fc_prev"]), "trend90"]).agg(n=("signed", "size"), mean_signed=("signed", "mean"), t=("signed", lambda s: s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan))
    # vol ratio: rising vol inside calm regime
    A4 = A.dropna(subset=["vratio_prev"]).copy()
    A4["vq"] = pd.qcut(A4["vratio_prev"], 3, labels=["falling", "mid", "rising"])
    out["by_vol_ratio"] = A4.groupby(["vq", "side"]).agg(n=("book_return", "size"), book=("book_return", "mean"), sd=("book_return", "std"))
    # deepest drawdown period: windows 2..? by side contribution
    seg = D[(D["wn"] >= 2) & (D["wn"] <= 6)]
    out["w2_w6_by_side"] = seg.groupby(["coin", "side"]).agg(n=("book_return", "size"), sum_book=("book_return", "sum"), coin=("coin_return", "mean"))
    out["by_window"] = D.groupby("wn").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), long=("side", lambda s: (s > 0).mean()), short=("side", lambda s: (s < 0).mean()))
    return out
