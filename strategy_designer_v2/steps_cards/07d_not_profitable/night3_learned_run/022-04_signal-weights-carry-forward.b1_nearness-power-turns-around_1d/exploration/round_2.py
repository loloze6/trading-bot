def explore(data):
    import pandas as pd, numpy as np
    days = data["days"]; bars = data["bars"]
    rows = []
    for c in days:
        for w, d in days[c].items():
            d = d.copy(); d["coin"] = c; d["window"] = w
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            g = b.groupby("day").agg(alloc=("postRebalance_current_allocation", "last"),
                                     fc=("forecast", "last"))
            d["dayk"] = pd.to_datetime(d["day"]).dt.floor("D")
            d = d.merge(g, left_on="dayk", right_index=True, how="left")
            d["prev_alloc"] = d["alloc"].shift(1)
            d["prev_fc"] = d["fc"].shift(1)
            d["ret20"] = (d["close"] / d["close"].shift(20) - 1).shift(1)
            d["hi90"] = (d["close"] / d["close"].rolling(90, min_periods=20).max() - 1).shift(1)
            d["fwd5"] = d["close"].shift(-5) / d["close"] - 1
            d["hi90now"] = d["close"] / d["close"].rolling(90, min_periods=20).max() - 1
            d["r20now"] = d["close"] / d["close"].shift(20) - 1
            rows.append(d)
    a = pd.concat(rows)
    a["wn"] = a["window"].str[1:].astype(int)
    a["side"] = np.sign(a["prev_alloc"]).map({1: "long", -1: "short", 0: "flat"})
    a["dd_win"] = a["wn"].between(14, 21)
    a["hiq"] = a.groupby("coin")["hi90"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    a["r20q"] = a.groupby("coin")["ret20"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out = {}
    tot = a["book_return"].sum()
    out["sum_share_by_hiq_side"] = (a.groupby(["hiq", "side"])["book_return"].sum() / tot).unstack()
    out["dd_vs_rest_hiq_side"] = a.groupby(["dd_win", "hiq", "side"])["book_return"].agg(["mean", "count"]).unstack()
    # portfolio-level: daily mean of short-near-high contributions
    a["cat"] = np.where((a["side"] == "short") & (a["hiq"] == 4), "short_nearhigh",
                np.where(a["side"] == "short", "short_other",
                np.where(a["side"] == "long", "long", "flat")))
    ncoins = a.groupby(["wn", "dayk"])["book_return"].transform("count")
    a["contrib"] = a["book_return"] / ncoins
    out["contrib_by_cat_dd"] = a.groupby(["dd_win", "cat"])["contrib"].sum().unstack()
    # graded: forward 5-day coin return (non-overlap) by nearness quintile, at signal close
    s = a.groupby(["coin", "window"], group_keys=False).apply(lambda x: x.iloc[::5])
    s = s.dropna(subset=["fwd5", "hi90now"])
    s["hq"] = s.groupby("coin")["hi90now"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd5_by_nearness"] = s.groupby("hq")["fwd5"].agg(["mean", "std", "count"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    s["rq"] = s.groupby("coin")["r20now"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd5_by_r20"] = s.groupby("rq")["fwd5"].agg(["mean", "std", "count"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["count"])))
    # forecast sign share by nearness quintile
    s["fs"] = np.sign(s["fc"])
    out["fc_sign_by_nearness"] = s.groupby("hq")["fs"].value_counts(normalize=True).unstack()
    # forecast*fwd by nearness quintile
    s["g"] = s["fc"] / 10 * s["fwd5"]
    out["gain_by_nearness"] = s.groupby("hq")["g"].agg(["mean", "count"])
    return out
