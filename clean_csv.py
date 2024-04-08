import os.path

import pandas as pd
import numpy as np


CSV_PATH = 'design_list_PT.csv'
signs_to_remove = ['!', '!!', '\n', '\t']
translation_table = str.maketrans('', '', ''.join(signs_to_remove))

int_columns = ['cores_ref', 'cores_test','mem_ref', 'mem_test', 'scratch']
int_columns = [name.upper() for name in int_columns]
boolean_columns = ['is_stp?']
boolean_columns = [name.upper() for name in boolean_columns]
def keyword_pp(raw_keyword):
    raw_keyword = raw_keyword.upper()
    # updt_keyword = updt_keyword.replace('#', '')
    # Create a translation table
    updt_keyword = raw_keyword.translate(translation_table)
    updt_keyword = updt_keyword.strip()
    return updt_keyword


def clean_df():
    input_path = os.path.abspath(CSV_PATH)
    raw = pd.read_csv(input_path)
    cols = list(raw.columns)
    # print(cols)
    updt_cols = {col: keyword_pp(col) for col in cols}
    upd_df = raw.rename(columns=updt_cols)
    object_columns = upd_df.select_dtypes(include=['object']).columns
    object_columns = list(set(object_columns) - set(int_columns + boolean_columns))
    pp_df = upd_df.copy()
    for col in object_columns:
        upd_df[col] = upd_df[col].fillna(' ')
        pp_df[col] = upd_df[col].apply(preprocess_text)

    pp_df[int_columns] = pp_df[int_columns].replace(' ', np.nan).fillna(np.nan)
    pp_df[int_columns] = pp_df[int_columns].astype('float').astype('Int64')

    return pp_df


# Function to preprocess text in each cell
def preprocess_text(cell):
    return cell.strip()


if __name__=='__main__':
    pp_df = clean_df()
    path = CSV_PATH.split('.csv')[0] + '_cleaned.csv'
    path = os.path.abspath(path)
    pp_df.to_csv(path, index=False)
