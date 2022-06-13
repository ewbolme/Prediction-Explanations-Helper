import datarobot as dr
import pandas as pd


def submit_csv_batch(
    deployment_id, input_file, output_file, max_explanations_returned, max_wait
) -> pd.DataFrame:
    job = dr.BatchPredictionJob.score(
        deployment=deployment_id,
        intake_settings={
            "type": "localFile",
            "file": input_file,
        },
        output_settings={
            "type": "localFile",
            "path": output_file,
        },
        # If explanations are required, uncomment the line below
        max_explanations=max_explanations_returned,
        download_timeout=max_wait
        # Uncomment this for Prediction Warnings, if enabled for your deployment.
        # prediction_warning_enabled=True
    )

    job.wait_for_completion()

    return pd.read_csv(output_file)
