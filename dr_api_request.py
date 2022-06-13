from dataclasses import dataclass, field
import pandas as pd
import datarobot as dr
import os
from typing import List, Optional
from deployment_predictions import submit_csv_batch
from make_project_predictions import submit_request_to_model
from data_sources import get_from_csv


@dataclass
class DR_Connection:
    """Class which represents a REST API request to the DataRobot server."""

    api_endpoint: str
    api_key: str
    ssl_insecure: str

    def create_connection(self) -> None:
        dr.Client(
            endpoint=self.api_endpoint,
            token=self.api_key,
            ssl_verify=not self.ssl_insecure,
            user_agent_suffix="IntegrationSnippet-ApiClient",
        )

    def test_connection(self) -> None:
        # TODO code to create connection here
        pass

    def close_connection(self) -> None:
        # TODO code to close connection here - can we do this?
        pass


@dataclass
class DR_Pred_Explan_Pipeline:
    connection: Optional[DR_Connection] = field(repr=False)
    data: Optional[pd.DataFrame] = field(repr=False)
    temp_input: str = "temp_file_input.csv"
    temp_output: str = "temp_file_output.csv"
    max_explanations: int = 50
    shap_bool: bool = False

    def load_data_from_csv(self, input_filename: str) -> None:
        self.data = get_from_csv(input_filename)

    def deployment_request(self, deployment_id, max_wait=300) -> None:
        """Makes a batch prediction request to a DataRobot deployment - returns a dataframe with predictions and max_explanation prediction explanations"""

        self.data.to_csv(self.temp_input, sep=",")
        self.data = submit_csv_batch(
            deployment_id,
            self.temp_input,
            self.temp_output,
            self.max_explanations,
            max_wait,
        )

        # TODO do this anyway even if above steps fail
        os.remove(self.temp_input)
        os.remove(self.temp_output)

    def project_request(self, project_id, model_id) -> None:
        """Makes a prediction request (along with prediction explanations) to a DataRobot model in a project returns a new pandas dataframe with the predictions and prediction explanations"""
        self.data = submit_request_to_model(
            data=self.data,
            project_id=project_id,
            model_id=model_id,
            max_explanations=self.max_explanations,
            shap_bool=self.shap_bool,
        )

        pass

    def process_explanations(self, project_id) -> None:
        """processes the prediction explanations"""
        pass

    def output_explanations_as_json(self, project_id):
        """Makes a prediction request (along with prediction explanations) to a DataRobot model in a project"""
        pass
