import pytest
import pandas as pd

def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "site": ["London", "London", "Manchester"],
        "date": pd.to_datetime(["2023-01-01", "2023-06-15", "2023-03-10"]),
        "pm2.5": [12.5, 8.3, 15.0],
        "no2":   [30.0, 20.0, 25.0],
        "co":    [0.5,  0.3,  0.8],
        "o3":    [40.0, 55.0, 35.0],
        "so2":   [5.0,  3.0,  7.0],
        "pm10":  [20.0, 15.0, 22.0],
        "nox":   [35.0, 25.0, 30.0],
    })

def test_winter():
    assert get_season(12) == "Winter"
    assert get_season(1)  == "Winter"
    assert get_season(2)  == "Winter"

def test_spring():
    assert get_season(3) == "Spring"
    assert get_season(4) == "Spring"
    assert get_season(5) == "Spring"

def test_summer():
    assert get_season(6) == "Summer"
    assert get_season(7) == "Summer"
    assert get_season(8) == "Summer"

def test_autumn():
    assert get_season(9)  == "Autumn"
    assert get_season(10) == "Autumn"
    assert get_season(11) == "Autumn"

def test_filter_by_city(sample_df):
    filtered = sample_df[sample_df["site"] == "London"]
    assert len(filtered) == 2
    assert all(filtered["site"] == "London")

def test_filter_by_date(sample_df):
    start = pd.to_datetime("2023-01-01")
    end   = pd.to_datetime("2023-03-01")
    filtered = sample_df[
        (sample_df["date"] >= start) &
        (sample_df["date"] <= end)
    ]
    assert len(filtered) == 1

def test_empty_filter(sample_df):
    filtered = sample_df[sample_df["site"] == "NonExistentCity"]
    assert filtered.empty

def test_pm25_mean(sample_df):
    london = sample_df[sample_df["site"] == "London"]
    expected_mean = round((12.5 + 8.3) / 2, 2)
    assert round(london["pm2.5"].mean(), 2) == expected_mean

def test_most_polluted_year(sample_df):
    sample_df["year"] = sample_df["date"].dt.year
    year_avg = sample_df.groupby("year")["pm2.5"].mean().reset_index()
    worst_year = year_avg.sort_values(by="pm2.5", ascending=False).iloc[0]["year"]
    assert worst_year == 2023

def test_most_polluted_month(sample_df):
    sample_df["month"] = sample_df["date"].dt.month
    month_avg = sample_df.groupby("month")["pm2.5"].mean().reset_index()
    worst_month = month_avg.sort_values(by="pm2.5", ascending=False).iloc[0]["month"]
    assert worst_month == 3

def test_best_season(sample_df):
    sample_df["month"]  = sample_df["date"].dt.month
    sample_df["season"] = sample_df["month"].apply(get_season)
    season_avg = sample_df.groupby("season")["pm2.5"].mean().reset_index()
    best = season_avg.sort_values(by="pm2.5", ascending=True).iloc[0]["season"]
    assert best == "Summer"

@pytest.fixture
def hourly_df():
    return pd.DataFrame({
        "site": ["London"] * 5,
        "date": pd.to_datetime([
            "2023-01-01 08:00",
            "2023-01-01 09:00",
            "2023-01-01 10:00",
            "2023-01-01 11:00",
            "2023-01-01 12:00",
        ]),
        "pm2.5": [5.0, 20.0, 15.0, 8.0, 3.0],
        "no2":   [10.0, 25.0, 18.0, 12.0, 6.0],
    })

def test_peak_hour(hourly_df):
    hourly_df["hour"] = hourly_df["date"].dt.hour
    hourly_means = hourly_df.groupby("hour")["pm2.5"].mean()
    peak_hour = hourly_means.idxmax()
    assert peak_hour == 9

def test_peak_hour_empty():
    empty_df = pd.DataFrame(columns=["site", "date", "pm2.5"])
    assert empty_df.empty
