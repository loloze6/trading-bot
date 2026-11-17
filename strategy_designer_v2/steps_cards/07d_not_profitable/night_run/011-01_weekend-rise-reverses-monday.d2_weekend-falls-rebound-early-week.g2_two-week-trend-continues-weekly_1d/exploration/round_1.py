def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(days.keys())
    # build per-coin daily frame with position at day end and features
    rows = []
    for c in coins:
        for w, d in days[c].items():
            b = bars[c][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            last = b.groupby("day").last()
            dd = d.copy(); dd["day"] = pd.to_datetime(dd["day"])
            dd = dd.merge(last[["postRebalance_current_allocation","forecast","sizing_realised_vol"]], left_on="day", right_index=True, how="left")
            dd["pos_prev"] = dd["postRebalance_current_allocation"].shift(1)
            dd["fc_prev"] = dd["forecast"].shift(1)
            r = dd["coin_return"]
            dd["vol20_prev"] = r.rolling(20).std().shift(1)
            dd["vol60_prev"] = r.rolling(60).std().shift(1)
            dd["volratio_prev"] = dd["vol20_prev"]/dd["vol60_prev"]
            dd["ret14_prev"] = (dd["close"]/dd["close"].shift(14)-1).shift(1)
            dd["ret3_prev"] = (dd["close"]/dd["close"].shift(3)-1).shift(1)
            dd["ret60_prev"] = (dd["close"]/dd["close"].shift(60)-1).shift(1)
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows, ignore_index=True)
    # book series
    wins = sorted(D["window"].unique(), key=lambda s: int(s[1:]))
    book = D.groupby(["window","day"])["book_return"].mean().reset_index()
    book["wn"] = book["window"].str[1:].astype(int)
    book = book.sort_values(["wn","day"]).dropna(subset=["book_return"])
    eq = (1+book["book_return"]).cumprod()
    dd_ = eq/eq.cummax()-1
    book["dd"] = dd_.values
    out["overall"] = pd.Series({"n_days":len(book),"mean":book.book_return.mean(),"std":book.book_return.std(),
        "maxdd":dd_.min(),"yearly":eq.iloc[-1]**(365/len(book))-1})
    # per window
    pw = book.groupby("wn").agg(ret=("book_return",lambda x:(1+x).prod()-1), n=("book_return","size"), worstday=("book_return","min"))
    pw["mindd_in_window"] = book.groupby("wn")["dd"].min()
    hold = D.groupby(["window","day"])["coin_return"].mean().reset_index()
    hold["wn"]=hold["window"].str[1:].astype(int)
    pw["hold"] = hold.groupby("wn")["coin_return"].apply(lambda x:(1+x.dropna()).prod()-1)
    pw["year"] = book.groupby("wn")["day"].first().dt.year
    out["per_window"] = pw
    # loss days decomposition by coin
    D["contrib"] = D["book_return"]
    D["absfc"] = D["fc_prev"].abs()
    D["side"] = np.sign(D["pos_prev"])
    D["aligned_rise"] = np.sign(D["ret14_prev"])==D["side"]
    # book return by quantiles of volatility ratio and others
    for col in ["volratio_prev","vol20_prev","absfc","ret3_prev"]:
        x = D.dropna(subset=[col,"book_return"])
        q = pd.qcut(x[col],5,duplicates="drop")
        g = x.groupby(q)["book_return"].agg(["mean","std","count",lambda s:s.quantile(0.01)])
        out["by_"+col] = g
    # 3-day return against position side: is the book losing after sharp counter moves?
    x = D.dropna(subset=["ret3_prev","pos_prev","book_return"]).copy()
    x["r3_signed"] = x["ret3_prev"]*np.sign(x["pos_prev"])/x["vol20_prev"]
    q = pd.qcut(x["r3_signed"],5)
    out["by_r3_signed"] = x.groupby(q)["book_return"].agg(["mean","std","count"])
    x["r60_signed"] = x["ret60_prev"]*np.sign(x["pos_prev"])
    q = pd.qcut(x["r60_signed"].dropna(),5)
    out["by_r60_signed"] = x.dropna(subset=["r60_signed"]).groupby(q)["book_return"].agg(["mean","std","count"])
    out["by_side"] = x.groupby("side")["book_return"].agg(["mean","std","count"])
    out["by_side_year"] = x.groupby([x["day"].dt.year,"side"])["book_return"].mean().unstack()
    return out
