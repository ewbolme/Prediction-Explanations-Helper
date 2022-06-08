from dataclasses import dataclass, Optional
from abc import ABC, abstractmethod
import pandas as pd


@dataclass
class DR_Connection():
    """Class which represents a REST API request to the DataRobot server."""
    api_endpoint: str
    api_key: str
    ssl_insecure: str

    def __post_init__(self) -> None:
        #TODO validate datatypes?
        pass

    def create_connection(self) -> None:
        #TODO code to create connection here
        pass

    def test_connection(self) -> None:
        #TODO code to create connection here
        pass

    def close_connection(self) -> None:
        #TODO code to close connection here - can we do this?
        pass

class Prediction_Explanations_Request(ABC):
    connection: DR_Connection
    input_filepath: str
    output_filepath: Optional[str]

    @abstractmethod
    def pull_data(self) -> None:
        """Pull the prediction explanations data"""

    @abstractmethod
    def generate_csv_predictions(self):
        """Generate the predictions augmented with the prediction explanations"""

    @abstractmethod
    def generate_json_predictions(self):
        """Generate the predictions augmented with the prediction explanations"""

class Deployment_Prediction_Request(Prediction_Explanations_Request):
    deployment_id: str

    def pull_data(self):
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.pya
        pass

    def generate_csv_predictions(self) -> None:
        if self.output_filepath is not None:
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.pya
            pass
        else:
            print("A output filepath is required to produce a csv output")
            pass

    def generate_json_predictions(self) -> None:
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.pya
        pass

    def __post_init__(self):
        #TODO validate datatypes?
        pass



@dataclass
class Model_Prediction_Request(Prediction_Explanations_Request):
    project_id: str
    model_id: str

    def pull_data(self) -> pd.DataFrame:
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.pya
        pass

    def generate_csv_predictions(self) -> None:
        if self.output_filepath is not None:
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.py
            data = self.pull_data(self)
            pass
        else:
            print("A output filepath is required to produce a csv output")
            pass

    def generate_json_predictions(self) -> None:
        data = self.pull_data(self)
        #TODO add code to pull from a deployment here maybe use make_deployment_predictions.pya
        pass

    def __post_init__(self):
        #TODO validate datatypes?
        pass
