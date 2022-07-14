"""
Unit tests
"""

import unittest


class test_deployment(unittest.TestCase):
    def setUp(self):
        # TODO use this to load in connection information
        pass

    def test_project_pull_xemp(self):
        pass

    def test_deployment_shap_melted(self):
        from dr_api_request import DR_Connection

        dr_connection = DR_Connection(
            api_endpoint="https://app.datarobot.com/api/v2",
            api_key="NjJjZGFhNzJkZDQyODRmM2ViYTNiMDRmOmtOZ0JCdEI4ZzFLdHQrL1UwZEpmUmsxbXRSZVRBbCtNdmVUVEk3WkhMUms9",
            ssl_insecure=True,
        )
        dr_connection.create_connection()
        from dr_api_request import DR_Pred_Explan_Pipeline

        pred_explan_pipe = DR_Pred_Explan_Pipeline(
            connection=dr_connection, data="", shap_bool=True
        )
        pred_explan_pipe.load_data_from_csv("./data/LendingClub.csv")
        pred_explan_pipe.deployment_request(
            deployment_id="62a7803def0aec264517a955", max_wait=600
        )
        pred_explan_pipe.process_deployment_explanations_melted()
        pred_explan_pipe.data.to_csv("./data/test_data_output_deployment_melt.csv")


unittest.main()
