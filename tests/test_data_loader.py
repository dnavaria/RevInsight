import pandas as pd
import pytest
from app.data_loader import DataLoader


def test_load_data_valid(mocker):
    # Mock pandas read_csv to return a valid DataFrame
    mock_data = pd.DataFrame({
        'order_id': [1], 'customer_id': [1], 'order_date': ['2021-01-01'],
        'product_id': [101], 'product_name': ['Widget'], 'product_price': [100], 'quantity': [1]
    })
    mocker.patch('pandas.read_csv', return_value=mock_data)

    # Instance of DataLoader and load data
    loader = DataLoader()
    data = loader.load_data("fake_path.csv")
    assert not data.empty
    assert list(data.columns) == [
        'order_id',
        'customer_id',
        'order_date',
        'product_id',
        'product_name',
        'product_price',
        'quantity'
    ]


def test_load_data_missing_columns(mocker):
    # Mock pandas read_csv to return DataFrame with missing columns
    mock_data = pd.DataFrame({
        'order_id': [1], 'customer_id': [1]
    })
    mocker.patch('pandas.read_csv', return_value=mock_data)

    loader = DataLoader()
    with pytest.raises(ValueError) as e:
        loader.load_data("fake_path.csv")
    assert "Missing required columns" in str(e.value)


def test_load_data_file_not_found(mocker):
    mocker.patch('pandas.read_csv', side_effect=FileNotFoundError)
    loader = DataLoader()
    with pytest.raises(FileNotFoundError) as e:
        loader.load_data("nonexistent_path.csv")
    assert "File not found" in str(e.value)


def test_validate_data_missing_values():
    # Create a DataFrame with missing values
    data = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': [1, None, 3],
        'order_date': ['2021-01-01', '2021-01-02', '2021-01-03'],
        'product_id': [101, 102, 103],
        'product_name': ['A', 'B', 'C'],
        'product_price': [100, 200, 300],
        'quantity': [1, 2, 3]
    })

    loader = DataLoader()
    with pytest.raises(ValueError) as e:
        loader.validate_data(data)
    assert "Data contains missing values" in str(e.value)
