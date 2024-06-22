import pandas as pd


class DataLoader:
    """Class for loading and validating data from CSV files.

    Attributes:
        required_columns (set): A set of columns required in the CSV data.
    """

    required_columns = {
        'order_id', 'customer_id', 'order_date', 'product_id',
        'product_name', 'product_price', 'quantity'
    }

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Loads data from a CSV file and validates it.
        :param file_path: The path to the CSV file.
        :return: The loaded data as a pandas DataFrame.
        :raises FileNotFoundError: If the file is not found at the specified path.
        :raises ValueError: If the file is empty, contains NaN values, duplicates, or missing columns.
        :raises Exception: If an unexpected error occurs while loading the data.
        """
        try:
            data = pd.read_csv(file_path)
            self.validate_data(data)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at {file_path}")
        except pd.errors.EmptyDataError:
            raise ValueError("File is empty or all data is NaN")
        except pd.errors.ParserError:
            raise ValueError("File could not be parsed")
        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"An unexpected error occurred while loading data: {e}")

    @classmethod
    def validate_data(cls, data: pd.DataFrame) -> bool:
        """
        Validates the loaded data to ensure it meets the required criteria.
        :param data: The loaded data as a pandas DataFrame.
        :return: True if the data is valid, False otherwise.
        :raises ValueError: If the data is missing required columns, contains NaN values, duplicates, or is empty.
        """
        if not cls.required_columns.issubset(data.columns):
            missing_cols = cls.required_columns - set(data.columns)
            raise ValueError(f"Missing required columns: {missing_cols}")
        if data.isnull().sum().sum() > 0:
            raise ValueError("Data contains missing values")
        if data.duplicated().sum() > 0:
            raise ValueError("Data contains duplicates")
        if data.shape[0] == 0:
            raise ValueError("Data is empty")
        return True
