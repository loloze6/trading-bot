import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    # ---- book daily returns, chained in window order
    drows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = int(w[1:])
            drows.append(dd)
    D = pd.concat(drows)
    B = D.groupby(["w","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean")).reset_index().dropna()
    B = B.sort_values(["w","day"]).reset_index(drop=True)
    B["val"] = (1+B["book"]).cumprod()
    B["peak"] = B["val"].cummax()
    B["dd"] = B["val"]/B["peak"]-1
    B["hval"] = (1+B["hold"]).cumprod()
    # drawdown episodes
    i_trough = B["dd"].idxmin()
    ep = []
    Bc = B.copy()
    for k in range(4):
        it = Bc["dd"].idxmin()
        if np.isnan(it) if isinstance(it,float) else False: break
        pk_val = B.loc[it,"peak"]
        start = B.index[(B.index<=it)&(np.isclose(B["val"],pk_val))].max()
        after = B.index[(B.index>it)&(B["val"]>=pk_val)]
        end = after.min() if len(after) else B.index.max()
        seg = B.loc[start:it]
        ep.append({"rank":k+1,"depth":B.loc[it,"dd"],"days_to_trough":it-start,
                   "w_start":B.loc[start,"w"],"w_trough":B.loc[it,"w"],
                   "year_trough":pd.Timestamp(B.loc[it,"day"]).year,
                   "hold_ret_in_fall":(1+seg["hold"].iloc[1:]).prod()-1,
                   "hold_absmean_daily":seg["hold"].abs().mean(),
                   "book_hold_corr":seg["book"].corr(seg["hold"])})
        Bc.loc[start:end,"dd"]=0
    out["falls"] = pd.DataFrame(ep)
    out["overall"] = pd.Series({"maxdd":B["dd"].min(),"book_mean":B["book"].mean(),"book_sd":B["book"].std(),
                                "hold_mean":B["hold"].mean(),"corr_book_hold":B["book"].corr(B["hold"]),
                                "all_hold_absmean":B["hold"].abs().mean()})
    B["year"]=pd.to_datetime(B["day"]).dt.year
    out["by_year"] = B.groupby("year").agg(book=("book","mean"),sd=("book","std"),hold=("hold","mean"),n=("book","size"),
                                           minDD=("dd","min"))
    # ---- cases
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(cl).pct_change()
            vol24 = r1.rolling(24).std()
            p23 = pd.Series(cl).shift(1)/pd.Series(cl).shift(24)-1
            p7d = pd.Series(cl)/pd.Series(cl).shift(168)-1
            vol7d = r1.rolling(168).std()
            fwd = pd.Series(cl).shift(-24)/pd.Series(cl)-1
            # coin drift on grid
            g = pd.Series(cl[::24]); 
            f = b["forecast"].values
            idx = np.where(f!=0)[0]
            for i in idx:
                rows.append({"coin":c,"w":int(w[1:]),"hour":ts[i].hour,"year":ts[i].year,
                             "fc":f[i],"h1z":r1[i]/vol24[i] if vol24[i]>0 else np.nan,
                             "p23z":p23[i]/(vol24[i]*np.sqrt(23)) if vol24[i]>0 else np.nan,
                             "p7d":p7d[i],"volratio":vol24[i]/vol7d[i] if vol7d[i]>0 else np.nan,
                             "fwd":fwd[i],"alloc":b["postRebalance_current_allocation"].iloc[i],
                             "day":ts[i].floor("D")})
    C = pd.DataFrame(rows).dropna(subset=["fwd"])
    C = C.drop_duplicates(["coin","w","day"])
    C["side"]=np.sign(C["fc"])
    C["pnl"]=C["side"]*C["fwd"]
    out["case_hours"]=C["hour"].value_counts().head(5)
    def summ(g):
        return pd.Series({"n":len(g),"mean_pnl":g["pnl"].mean(),"t":g["pnl"].mean()/g["pnl"].std()*np.sqrt(len(g)),
                          "sd":g["pnl"].std(),"p05":g["pnl"].quantile(.05)})
    out["by_side"]=C.groupby("side").apply(summ)
    out["by_coin"]=C.groupby("coin").apply(summ)
    out["by_year_cases"]=C.groupby("year").apply(summ)
    C["fcq"]=pd.qcut(C["fc"].abs(),4,labels=False)
    out["by_fc_abs_q"]=C.groupby("fcq").apply(summ)
    C["p23q"]=pd.qcut(C["p23z"].abs(),4,labels=False)
    out["by_p23z_q"]=C.groupby("p23q").apply(summ)
    C["vrq"]=pd.qcut(C["volratio"],4,labels=False)
    out["by_volratio_q"]=C.groupby("vrq").apply(summ)
    # 7d trend aligned with side? side opposite to h1; p7d sign vs fade
    C["with7d"]=np.sign(C["p7d"])==C["side"]  # fade agrees with 7d trend
    out["by_fade_with_7d"]=C.groupby("with7d").apply(summ)
    C["p7q"]=pd.qcut(-C["side"]*C["p7d"],4,labels=False)  # higher = 7d run in direction faded
    out["by_7d_run_faded_q"]=C.groupby("p7q").apply(summ)
    return out
