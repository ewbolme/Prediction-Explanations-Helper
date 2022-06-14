import re
import numpy as np
import pandas as pd


def processs_deployment_explanations_flat(data: pd.DataFrame):
    number_of_rows = data.shape[0]
    pattern_base = re.compile("EXPLANATION_(.*?)")
    explanation_columns = [col for col in data.columns if pattern_base.match(col)]
    pattern = re.compile("EXPLANATION_(.*?)_FEATURE_NAME")
    populated_explanation_col_numbers = [
        pattern.match(col)[1]
        for col in explanation_columns
        if pattern.match(col) and data[col].isna().sum() != number_of_rows
    ]

    for i, row in data.iterrows():
        for col_num in populated_explanation_col_numbers:
            feature_name = row[f"EXPLANATION_{str(col_num)}_FEATURE_NAME"]
            if f"{feature_name}_EXPLANATION_STRENGTH" in row.keys():
                data.at[i, f"{feature_name}_EXPLANATION_STRENGTH"] = row[
                    f"EXPLANATION_{str(col_num)}_STRENGTH"
                ]
            else:
                data[f"{feature_name}_EXPLANATION_STRENGTH"] = np.nan
                data.at[i, f"{feature_name}_EXPLANATION_STRENGTH"] = row[
                    f"EXPLANATION_{str(col_num)}_STRENGTH"
                ]
        print(f"row {str(i)} processed")

    return data.drop(explanation_columns, axis=1)


def processs_deployment_explanations_bi_tool(data: pd.DataFrame) -> pd.DataFrame:
    # TODO edit lukes code to fit in here
    return data
