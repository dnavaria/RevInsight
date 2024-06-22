import pytest
import pandas as pd
from unittest.mock import Mock, patch
from app.core import RevInsightCore


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'order_date': ['2021-01-01'],
        'product_price': [100],
        'quantity': [2],
        'product_id': [101],
        'customer_id': [1]
    })


@pytest.fixture
def core_instance(tmp_path):
    fp = tmp_path / "data.csv"
    fp.write_text("order_date,product_price,quantity,product_id,customer_id\n2021-01-01,100,2,101,1")
    return RevInsightCore(str(fp))


def test_load_data(core_instance, mocker):
    mocker.patch('app.data_loader.DataLoader.load_data', return_value=pd.DataFrame())
    core_instance.load_data()
    assert core_instance.data is not None


def test_compute(core_instance, sample_data, mocker):
    mocker.patch('app.data_loader.DataLoader.load_data', return_value=sample_data)
    mocker.patch('app.revenue_calculator.RevenueCalculator.compute_monthly_revenue', return_value=pd.Series([200]))
    mocker.patch('app.revenue_calculator.RevenueCalculator.compute_product_revenue', return_value=pd.Series([200]))
    mocker.patch('app.revenue_calculator.RevenueCalculator.compute_customer_revenue', return_value=pd.Series([200]))
    mocker.patch('app.revenue_calculator.RevenueCalculator.top_n_customers', return_value=pd.Series([200]))
    core_instance.load_data()
    report = core_instance.compute()
    assert "Monthly Revenue" in report
    assert "Product Revenue" in report
    assert "Customer Revenue" in report
    assert "Top 10 Customers" in report


def test_export_report_invalid_path(core_instance, mocker):
    mocker.patch('app.report_generator.ReportGenerator.generate_report', return_value=True)
    with pytest.raises(ValueError) as e:
        core_instance.export_report({}, "")
    assert "Please provide a valid file path" in str(e.value)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'order_date': pd.to_datetime(['2021-01-01', '2021-01-01', '2021-02-01']),
        'product_price': [100, 200, 150],
        'quantity': [1, 2, 3],
        'product_id': [101, 102, 101],
        'customer_id': [1, 2, 1],
        'order_id': [1, 2, 3],
        'product_name': ['A', 'B', 'A'],

    })


def test_run_method_with_actual_values(sample_dataframe, tmp_path):
    # Setup the file path for testing
    data_file = tmp_path / "input_data.csv"
    export_file = tmp_path / "output_report.xlsx"

    # Save sample data to a CSV to mimic DataLoader functionality
    sample_dataframe.to_csv(data_file, index=False)

    # Create an instance of RevInsightCore
    core_instance = RevInsightCore(str(data_file))

    # Execute the run method
    result = core_instance.run('xlsx', str(export_file))
    assert result['Monthly Revenue'].loc[(2021, '01')] == 500
    assert result['Monthly Revenue'].loc[(2021, '02')] == 450
    assert result['Product Revenue'].loc[101] == 550
    assert result['Product Revenue'].loc[102] == 400
    assert result['Customer Revenue'].loc[1] == 550
    assert result['Customer Revenue'].loc[2] == 400
    assert result['Top 10 Customers'].iloc[0] == 550
    assert result['Top 10 Customers'].iloc[1] == 400
    assert export_file.exists()
