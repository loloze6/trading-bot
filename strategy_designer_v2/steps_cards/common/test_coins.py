import coins


def test_groups_split_the_universe():
    port, univ = coins.portfolio_group(), [c for v in coins.CATEGORIES.values() for c in v]
    assert len(univ) == 32 and len(coins.FINAL) == 7 and len(port) == 25
    assert not set(port) & set(coins.FINAL) and set(port) | set(coins.FINAL) == set(univ)
    assert all(sum(c in v for c in coins.FINAL) == 1 for v in coins.CATEGORIES.values())


def test_research_draw_is_fixed_by_the_run_name_and_covers_every_category():
    a = coins.research_draw("night10_example_run")
    assert a == coins.research_draw("night10_example_run") and len(a) == 8 == len(set(a))
    assert not set(a) & set(coins.FINAL)
    assert all(any(c in v for c in a) for v in coins.CATEGORIES.values())


def test_a_coins_first_90_days_are_not_usable():
    d = coins.first_usable_day("SUI")
    assert not coins.usable("SUI", d.replace(day=1) if d.day > 1 else d - __import__("datetime").timedelta(days=1))
    assert coins.usable("SUI", d)


def test_a_hole_longer_than_a_day_leaves_the_window_out():
    import datetime as dt
    days = [dt.date(2022, 1, 1) + dt.timedelta(days=i) for i in range(120) if i not in (10, 50, 51)]
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


def test_a_run_s_data_use():
    du = coins.new_data_use("night10_example_run")
    assert du == {"version": 2, "research_coins": coins.research_draw("night10_example_run"),
                  "windows": "04_backtest/windows/research_2016.json"}
    assert coins.data_use_file("x_run") == coins.STEPS / "orchestration" / "loop" / "x_run" / "data_use.json"
    assert coins.data_use("no_such_test_run") is None
