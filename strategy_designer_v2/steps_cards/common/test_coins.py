import coins


def test_groups_split_the_universe():
    port, univ = coins.portfolio_group(), [c for v in coins.CATEGORIES.values() for c in v]
    assert len(univ) == 32 and len(coins.FINAL) == 7 and len(port) == 25
    assert not set(port) & set(coins.FINAL) and set(port) | set(coins.FINAL) == set(univ)
    assert all(sum(c in v for c in coins.FINAL) == 1 for v in coins.CATEGORIES.values())


def test_research_draw_is_fixed_by_the_run_name_and_takes_one_coin_per_category_that_has_a_drawable_one():
    pool = [c for c in coins.portfolio_group() if c not in ("TAO", "PEPE", "SUI")]      # AI has no drawable coin
    a = coins.research_draw("night10_example_run", pool)
    assert a == coins.research_draw("night10_example_run", pool) and len(a) == 8 == len(set(a))
    assert set(a) <= set(pool) and not set(a) & set(coins.FINAL)
    assert all(any(c in v for c in a) for k, v in coins.CATEGORIES.items() if k != "ai")
    assert "DOGE" in a                                   # the only drawable meme coin is in every draw
    assert coins.research_draw("another_run", pool) != a


def test_a_coins_first_90_days_are_not_usable():
    d = coins.first_usable_day("SUI")
    assert not coins.usable("SUI", d.replace(day=1) if d.day > 1 else d - __import__("datetime").timedelta(days=1))
    assert coins.usable("SUI", d)


def test_a_hole_longer_than_a_day_leaves_the_window_out():
    import datetime as dt
    days = [dt.date(2022, 1, 1) + dt.timedelta(days=i) for i in range(-120, 120) if i not in (10, 50, 51)]
    assert coins.longest_hole(days, "2022-01-01", "2022-04-30") == 2
    assert coins.longest_hole(days, "2022-01-01", "2022-02-15") == 1            # one missing day: ignored
    assert coins.left_out("BTC", "2022-01-01", "2022-02-15", days=days) is None
    assert coins.left_out("BTC", "2022-01-01", "2022-04-30", days=days) == "a hole of 2 days"
    assert coins.longest_hole(days, "2022-04-01", "2022-05-10") == 10           # stopped before the window's end
    assert coins.left_out("SUI", "2023-01-01", "2023-04-30") == "the coin's first 90 days"


def test_the_real_files_holes_in_the_research_windows():
    """XRP misses 2 days in May 2022 (its file): left out of that window only."""
    import json
    wins = json.loads(coins.WINDOWS.read_text())
    out = [w["label"] for w in wins if coins.left_out("XRP", w["test"]["start"], w["test"]["end"])]
    assert out == ["2016-01", "2016-05", "2016-09", "2017-01", "2017-05", "2022-05"]   # its first 90 days, the hole


YEAR2 = 790 * 86400          # a test's warm-up: the size the market-profile detector asks on daily bars


def test_a_history_shorter_than_the_warm_up_leaves_the_window_out():
    import datetime as dt
    days = [dt.date(2020, 1, 1) + dt.timedelta(days=i) for i in range(1500)]
    assert coins.warmup_start("2022-03-01", YEAR2) == dt.date(2020, 1, 1)         # 790 days before
    why = "the coin's history is shorter than the plan's warm-up: 790 days asked"
    assert coins.left_out("X", "2022-02-28", "2022-03-31", days=days, warmup_seconds=YEAR2) == why     # one day short
    assert coins.left_out("X", "2022-03-01", "2022-03-31", days=days, warmup_seconds=YEAR2) is None    # covered exactly
    assert coins.left_out("X", "2020-02-01", "2020-03-31", days=days, warmup_seconds=YEAR2) == "the coin's first 90 days"
    assert coins.left_out("X", "2022-03-01", "2022-03-31", days=days) is None      # no warm-up asked: the 90 days only
    assert coins.warmup_days(3600 * 30) == 2                                      # hourly bars: days rounded up


def test_the_drawable_coins_on_the_real_files():
    """data_use.md, 1.3, counted on 2026-11-27: 19 of the 25 portfolio coins, none in AI."""
    import json
    wins = json.loads(coins.WINDOWS.read_text())
    assert len(coins.check_half(wins)) == 14 and coins.draw_need(wins) == 7
    counts = coins.testable_counts(YEAR2, wins)
    ok = coins.drawable(counts, coins.draw_need(wins))
    assert sorted(set(counts) - set(ok)) == ["LDO", "NEAR", "ONDO", "PEPE", "SUI", "TAO"]
    assert counts["TAO"] == 0 and counts["AVAX"] == 7 and counts["BTC"] == 14
    assert sum(len(coins.testable(c, YEAR2, wins)) for c in coins.portfolio_group()) == 331


def test_a_run_s_data_use(monkeypatch):
    monkeypatch.setattr(coins, "detector_warmup", lambda python: YEAR2)
    du = coins.new_data_use("night10_example_run", "py")
    assert du["version"] == 2 and du["windows"] == "04_backtest/windows/research_2016.json"
    assert du["draw"]["warmup_days"] == 790 and du["draw"]["check_windows"] == 14 and du["draw"]["needed"] == 7
    ok = [c for c, n in du["draw"]["testable"].items() if n >= 7]
    assert len(ok) == 19 and du["research_coins"] == coins.research_draw("night10_example_run", ok)
    assert coins.data_use_file("x_run") == coins.STEPS / "orchestration" / "loop" / "x_run" / "data_use.json"
    assert coins.data_use("no_such_test_run") is None
