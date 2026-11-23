def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # ---- book daily returns, per window
    rows = []
    for coin, wd in data["days"].items():
        for w, df in wd.items():
            d = df[["day","book_return","coin_return"]].copy()
            d["coin"] = coin; d["window"] = w
            rows.append(d)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["br"])
    v = (1+B["br"]).cumprod()
    B["dd"] = v/v.cummax()-1
    out["deepest_fall"] = float(B["dd"].min())
    # by window: book return sum, min dd within window chain
    gw = B.groupby("wn").agg(n=("br","size"), book_sum=("br","sum"), coin_sum=("cr","sum"), dd_min=("dd","min"))
    out["by_window"] = gw
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["by_year"] = B.groupby("year").agg(n=("br","size"), book_mean=("br","mean"), book_std=("br","std"), coin_mean=("cr","mean"))
    # worst 20 book days: coin return of market that day
    w20 = B.nsmallest(20,"br")
    out["worst20_days"] = pd.DataFrame({"br":w20["br"].values,"mkt":w20["cr"].values,"wn":w20["wn"].values})
    # ---- case analysis
    cases = []
    for coin, wd in data["bars"].items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            r = pd.Series(c).pct_change()
            s20 = r.rolling(20).std(); s60 = r.rolling(60).std()
            ret20 = pd.Series(c)/pd.Series(c).shift(20)-1
            vol = b["volume"]
            vrel = vol/vol.rolling(20).mean()
            for i in range(len(b)-2):
                if ts.iloc[i].weekday()==6 and b["forecast"].iloc[i]!=0 and not np.isnan(b["forecast"].iloc[i]):
                    sgn = np.sign(b["forecast"].iloc[i])
                    r2 = c[i+2]/c[i]-1
                    # book pnl of this coin over next 2 bars
                    a = b["postRebalance_current_allocation"].iloc[i]
                    a1 = b["postRebalance_current_allocation"].iloc[i+1]
                    pnl = a*(c[i+1]/c[i]-1)+a1*(c[i+2]/c[i+1]-1)
                    cases.append(dict(coin=coin, wn=int(w[1:]), year=ts.iloc[i].year, sgn=sgn, f=b["forecast"].iloc[i],
                        wk=r.iloc[i], r2=r2, s=sgn*r2, ratio=s20.iloc[i]/s60.iloc[i], ret20=ret20.iloc[i],
                        vrel=vrel.iloc[i], alloc=abs(a), pnl=pnl, s1=sgn*(c[i+1]/c[i]-1)))
    C = pd.DataFrame(cases)
    def summ(g):
        return pd.Series({"n":len(g),"mean_s":g["s"].mean(),"t":g["s"].mean()/(g["s"].std()/np.sqrt(len(g))),
                          "mean_pnl":g["pnl"].mean(),"sum_pnl":g["pnl"].sum(),"p5_pnl":g["pnl"].quantile(0.05),"alloc":g["alloc"].mean()})
    out["by_side"] = C.groupby("sgn").apply(summ)
    C["absf_q"] = pd.qcut(C["f"].abs(),5,labels=False,duplicates="drop")
    out["by_absforecast_q"] = C.groupby("absf_q").apply(summ)
    C["ratio_q"] = pd.qcut(C["ratio"],5,labels=False,duplicates="drop")
    out["by_ratio_q"] = C.groupby("ratio_q").apply(summ)
    C["trend_agree"] = np.sign(C["ret20"])==C["sgn"]
    out["by_trend_agree"] = C.groupby("trend_agree").apply(summ)
    C["ret20_q"] = pd.qcut(C["ret20"]*C["sgn"],5,labels=False,duplicates="drop")
    out["by_signed_ret20_q"] = C.groupby("ret20_q").apply(summ)
    C["vrel_q"] = pd.qcut(C["vrel"],5,labels=False,duplicates="drop")
    out["by_volrel_q"] = C.groupby("vrel_q").apply(summ)
    out["by_year_cases"] = C.groupby("year").apply(summ)
    out["share_pnl_day1"] = float(C["s1"].mean()/C["s"].mean())
    return out
