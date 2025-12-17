import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from redwine.entity.config_entity import ModelEvaluationConfig 
from redwine.utils.common import save_json
from pathlib import Path
from redwine import logger

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    
    def eval_metrics(self,actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2
    


    def log_into_mlflow(self):
        
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        test_x = test_data.drop([self.config.target_column], axis=1)
        test_y = test_data[[self.config.target_column]]

        predicted_qualities = model.predict(test_x)
        (rmse, mae, r2) = self.eval_metrics(test_y, predicted_qualities)
        
        # Saving metrics as local
        scores = {"rmse": rmse, "mae": mae, "r2": r2}
        save_json(path=Path(self.config.metric_file_name), data=scores)
        logger.info(f"Metrics saved locally to: {self.config.metric_file_name}")
        
        logger.info(f"Model Evaluation Metrics:")
        logger.info(f"  RMSE: {rmse:.4f}")
        logger.info(f"  MAE: {mae:.4f}")
        logger.info(f"  R2 Score: {r2:.4f}")
        
        # Enable remote MLflow logging
        try:
            mlflow.set_tracking_uri(self.config.mlflow_uri)
            logger.info(f"MLflow tracking URI set to: {self.config.mlflow_uri}")
            
            mlflow.set_experiment("red_wine_quality_evaluation")
            
            with mlflow.start_run(run_name="model_evaluation_run"):
                logger.info("MLflow run started")
                
                # Convert all parameters to strings
                clean_params = {str(k): str(v) for k, v in self.config.all_params.items()}
                mlflow.log_params(clean_params)
                logger.info(f"Parameters logged: {clean_params}")
                
                # Log metrics
                mlflow.log_metric("rmse", float(rmse))
                mlflow.log_metric("mae", float(mae))
                mlflow.log_metric("r2", float(r2))
                logger.info("Metrics logged to MLflow")
                
                # Log model
                mlflow.sklearn.log_model(model, "model")
                logger.info("Model logged to MLflow")
                
                logger.info("✓ Remote MLflow logging completed successfully!")
                
        except Exception as mlflow_error:
            logger.warning(f"Remote MLflow logging failed: {mlflow_error}")
            logger.info("Continuing with local metrics only. Metrics saved in: artifacts/model_evaluation/metrics.json")