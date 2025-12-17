import os
from redwine import logger
import pandas as pd
from redwine.entity.config_entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            data = pd.read_csv(self.config.unzip_data_dir)

            dataset_columns = set(data.columns)
            schema_columns = set(self.config.all_schema.keys())

            # Check for extra or missing columns
            validation_status = dataset_columns == schema_columns

            with open(self.config.STATUS_FILE, "w") as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise e
