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
