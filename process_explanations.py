import re
import numpy as np
import pandas as pd
from tqdm import tqdm


def id_explan_columns(data: pd.DataFrame) -> pd.DataFrame:
    number_of_rows = data.shape[0]
    pattern_base = re.compile("EXPLANATION_(.*?)")
    explanation_columns = [col for col in data.columns if pattern_base.match(col)]
    pattern = re.compile("EXPLANATION_(.*?)_FEATURE_NAME")

    populated_explanation_col_numbers = [
        pattern.match(col)[1]
        for col in explanation_columns
        if pattern.match(col) and data[col].isna().sum() != number_of_rows
    ]
    return explanation_columns, populated_explanation_col_numbers


def return_explanations_flat(data: pd.DataFrame) -> pd.DataFrame:
    explanation_columns, populated_explanation_col_numbers = id_explan_columns(data)

    for i, row in tqdm(data.iterrows()):
        for col_num in populated_explanation_col_numbers:
            feature_name = row[f"EXPLANATION_{str(col_num)}_FEATURE_NAME"]
            # TODO does this work on a copy or a window
            if f"{feature_name}_EXPLANATION_STRENGTH" in row.keys():
                data.at[i, f"{feature_name}_EXPLANATION_STRENGTH"] = row[
                    f"EXPLANATION_{str(col_num)}_STRENGTH"
                ]
            elif np.isnan(f"EXPLANATION_{str(col_num)}_FEATURE_NAME"):
                pass
            else:
                data[f"{feature_name}_EXPLANATION_STRENGTH"] = np.nan
                data.at[i, f"{feature_name}_EXPLANATION_STRENGTH"] = row[
                    f"EXPLANATION_{str(col_num)}_STRENGTH"
                ]

    return data.drop(explanation_columns, axis=1)


def return_melted_dataframe(data: pd.DataFrame) -> pd.DataFrame:
    # TODO make part below something that can be called by both functions
    explanation_columns, populated_explanation_col_numbers = id_explan_columns(data)

    explan_feature_name_cols = []
    explan_feature_str_cols = []

    for col_num in populated_explanation_col_numbers:
        explan_feature_name_cols.append(f"EXPLANATION_{str(col_num)}_FEATURE_NAME")
        explan_feature_str_cols.append(f"EXPLANATION_{str(col_num)}_STRENGTH")

    data["orig_row_num"] = data.index
    pattern = re.compile("[0-9]+")
    def_trim_function = lambda x: pattern.findall(x)[0]

    data_melted_feat_name = data.melt(
        id_vars=["orig_row_num"],
        value_vars=explan_feature_name_cols,
        value_name="feature_name",
        var_name="variable_number",
    )

    data_melted_feat_str = data.melt(
        id_vars=["orig_row_num"],
        value_vars=explan_feature_str_cols,
        value_name="feature_strength",
        var_name="variable_number",
    )

    data_melted_feat_name["variable_number"] = data_melted_feat_name[
        "variable_number"
    ].map(def_trim_function)
    data_melted_feat_str["variable_number"] = data_melted_feat_str[
        "variable_number"
    ].map(def_trim_function)

    return data_melted_feat_name.merge(
        data_melted_feat_str, on=["orig_row_num", "variable_number"]
    )
