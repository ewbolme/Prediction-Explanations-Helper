import datarobot as dr
import pandas as pd

def submit_request_to_model(data: pd.DataFrame, project_id: str, model_id: str, max_explantions: int) -> pd.DataFrame:

    dataset = dr.Dataset.create_from_in_memory_data(data)
    project = dr.Project.get(project_id=project_id)
    dataset = project.upload_dataset_from_catalog(dataset_id=dataset.id)

    model = dr.Model.get(project=project_id, model_id=model_id)
    feature_impacts = model.get_or_request_feature_impact()
    pred_job = model.request_predictions(dataset.id)
    pred_job.wait_for_completion()

    pei_job =dr.PredictionExplanationsInitialization.create(project_id, model_id)
    pei_job.wait_for_completion()

    # Compute prediction explanations with default parameters
    pe_job = dr.PredictionExplanations.create(project_id, model_id, dataset.id, max_explantions=max_explantions)
    pe = pe_job.get_result_when_complete()
    pe_df = pe.get_all_as_dataframe()

    return pe_df

