import pandas as pd
import pytest
from app.revenue_calculator import RevenueCalculator


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'order_date': pd.to_datetime(['2021-01-01', '2021-01-02', '2021-02-01']),
        'product_price': [100, 200, 150],
        'quantity': [1, 3, 2],
        'product_id': [101, 102, 101],
        'customer_id': [1, 2, 1]
    })


def test_compute_monthly_revenue(sample_data):
    result = RevenueCalculator.compute_monthly_revenue(sample_data)
    assert result.loc[(2021, '01')] == 700  # 100*1 + 200*3
    assert result.loc[(2021, '02')] == 300  # 150*2


def test_compute_product_revenue(sample_data):
    result = RevenueCalculator.compute_product_revenue(sample_data)
    assert result.loc[101] == 400  # 100*1 + 150*2
    assert result.loc[102] == 600  # 200*3


def test_compute_customer_revenue(sample_data):
    result = RevenueCalculator.compute_customer_revenue(sample_data)
    assert result.loc[1] == 400  # 100*1 + 150*2
    assert result.loc[2] == 600  # 200*3


def test_top_n_customers(sample_data):
    result = RevenueCalculator.top_n_customers(sample_data, number_of_customers=1)
    assert len(result) == 1
    assert result.iloc[0] == 600
