import pandas as pd


class ReportGenerator:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def generate_report(self, df_map: dict, export_format: str) -> bool:
        """
        Generate a report based on the data frames provided in the input dictionary.
        :param df_map:
        :param export_format:
        :return: True if the report was successfully generated, False otherwise.
        :raises: ValueError if the export format is not supported.
        """
        if export_format == 'xlsx':
            return self.export_report_excel(df_map)
        else:
            raise ValueError(f"Unsupported report type: {export_format}")

    def export_report_excel(self, data_frames):
        """
        Export the data frames to an Excel file.
        :param data_frames:
        :return: True if the export was successful, False otherwise.
        :raises: Exception if an error occurs during the export process.
        """
        try:
            with pd.ExcelWriter(self.file_path, engine='xlsxwriter') as writer:
                for sheet_name, df in data_frames.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=True)
            return True
        except Exception as e:
            print(f"An error occurred while generating the Excel report: {e}")
            return False
