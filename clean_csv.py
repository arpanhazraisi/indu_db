import os.path

import pandas as pd



CSV_PATH = './design_list_PT.csv'
signs_to_remove = ['!', '!!', '\n', '\t']
translation_table = str.maketrans('', '', ''.join(signs_to_remove))


def keyword_pp(raw_keyword):
    # updt_keyword = raw_keyword.lower()
    # updt_keyword = updt_keyword.replace('#', '')
    # Create a translation table
    updt_keyword = raw_keyword.translate(translation_table)
    updt_keyword = updt_keyword.strip()
    return updt_keyword


def clean_df():
    raw = pd.read_csv(os.path.abspath(CSV_PATH))
    cols = list(raw.columns)
    # print(cols)
    updt_cols = {col: keyword_pp(col) for col in cols}
    upd_df = raw.rename(columns=updt_cols)
    switch_list = [keyword_pp(col) for col in cols]
    # switch_list = list(upd_df.columns)
    object_columns = upd_df.select_dtypes(include=['object'])
    pp_df = upd_df.copy()
    for col in object_columns:
        upd_df[col] = upd_df[col].fillna(' ')
        pp_df[col] = upd_df[col].apply(preprocess_text)
    return pp_df


# Function to preprocess text in each cell
def preprocess_text(cell):
    # print(cell)
    return cell.strip()


if __name__=='__main__':
    pp_df = clean_df()
    path = CSV_PATH.split('.csv')[0] + '_cleaned.csv'
    pp_df.to_csv(os.path.abspath(path), index=False)
