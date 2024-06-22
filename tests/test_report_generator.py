import pandas as pd
import pytest
from app.report_generator import ReportGenerator
from unittest.mock import Mock


def test_generate_report_excel(mocker, tmp_path):
    # Create a temporary directory and file path
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "test.xlsx"

    report_gen = ReportGenerator(str(file_path))

    # Setup the mock for pandas.ExcelWriter with context manager support
    mocker.patch('pandas.ExcelWriter').return_value.__enter__.return_value = Mock(spec=pd.ExcelWriter)

    assert report_gen.generate_report({"Sheet1": pd.DataFrame([1, 2, 3])}, 'xlsx') is True


def test_generate_report_unsupported_type():
    report_gen = ReportGenerator("path/to/report.xlsx")
    with pytest.raises(ValueError) as e:
        report_gen.generate_report({}, 'csv')
    assert "Unsupported report type" in str(e.value)
