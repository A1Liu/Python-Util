# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import mr_clean_utils as mcu

def validate(df,coerce_numeric,coerce_dt,coerce_categorical): # validates input
    assert type(df) is pd.DataFrame
    column_dict = {}
    for element in coerce_numeric + coerce_dt + coerce_categorical: # these lists must be mutually exclusive
        assert type(element) is str
        assert not element in column_dict
        column_dict[element] = True

def rename_cols(df, col_names): # renames columns
    if col_names is not None:
        col_list = [*col_names]
        col_gen = get_colname_gen(df)
        for col_name in col_gen():
            if len(col_list) >= len(df.columns):
                break
            else:
                col_list.append(col_name)
    else:
        col_list = [*df.columns]
    for index,col_name in enumerate(col_list):
        col_list[index] = col_name.strip().lower().replace(' ','_')
    df.columns = col_list

def remove_whitespace(df): # removes whitespace from string columns
    for column in (column for column in df if not mcu.is_num( df[column] )  ):
        df[column] = df[column].str.strip()
        yield column

def rename_index(df):
    if not (type(df.index) is pd.RangeIndex or type(df.index) is pd.DatetimeIndex):
        df.reset_index() # reset the index
        return True

def scrub_str_cols(df,column,char_scrub_cutoff): 
    # Tries to remove common characters from the front of the strings in df[column]
    if not mcu.is_num(df[column]): # if it's not a numeric
        char_scrub_cutoff = get_cutoff(column, char_scrub_cutoff)
        from_front = ""
        from_back = ""
        flag1 = True
        flag2 = True
        while flag1 or flag2:
            valcounts = df[column].str[0].value_counts()
            flag1 = valcounts[0] > char_scrub_cutoff * df.shape[0]
            if flag1:
                from_front+=valcounts.index[0]
                df[column] = df[column].str[1:]
            valcounts = df[column].str[-1].value_counts()
            flag2 = valcounts[0] > char_scrub_cutoff * df.shape[0]
            if flag2:
                from_back=valcounts.index[0]+from_back
                df[column] = df[column].str[:-1]
        if len(from_front) > 0 or len(from_back) > 0:
           return (from_front, from_back, column)

def coerce_col(df, column,
               numeric_cutoff, coerce_numeric, 
               dt_cutoff, coerce_dt, dt_format,
               categorical_cutoff,coerce_categorical):
    success = True
    if column in coerce_numeric:
            mcu.coerce(df, column, 
                    pd.to_numeric(df[column], errors = 'coerce'))
    elif column in coerce_dt:
        if dt_format is None:
            mcu.coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True))
        else:
            mcu.coerce(df, column, 
                    pd.to_datetime(df[column],errors = 'coerce',format = dt_format))
    elif column in coerce_categorical:
        mcu.coerce(df, column, df[column].astype('category'))
    else:
        success = infer_coerce(df, column,
               get_cutoff( column,numeric_cutoff ),
               get_cutoff( column,dt_cutoff ),
               get_cutoff( column,categorical_cutoff ) )
    return success

def infer_coerce(df, column,
               numeric_cutoff,dt_cutoff,categorical_cutoff):
    
    num_coerced = pd.to_numeric(df[column], errors = 'coerce')
    dt_coerced = pd.to_datetime(df[column],errors = 'coerce',infer_datetime_format = True)
    cat_coerced = df[column].astype('category')
    
    all_cutoffs = [numeric_cutoff,dt_cutoff,categorical_cutoff]
    all_coerced = [num_coerced,dt_coerced, cat_coerced]
    all_counts = [coerced.count() for coerced in all_coerced]
    all_counts[2] = mcu.rows(df)-len(all_coerced[2].value_counts())
    high_count = max(*all_counts)
    for index in range(3):
        if all_counts[index] == high_count and \
            all_counts[index] > mcu.row_req(df,all_cutoffs[index]):
            mcu.coerce(df, column, all_coerced[index])
            return True
    return False

def get_cutoff(column, cutoff):
    if type(cutoff) is dict:
        return cutoff[column] if column in cutoff else 1
    return cutoff

def get_colname_gen(df):
    def colname_gen(row_name = 'mrClean'):
        assert type(df) is pd.DataFrame
        id_number = 0
        while True:
            id_string = row_name + str(id_number)
            if id_string in df.keys():
                id_number+=1
            else:
                yield id_string
    return colname_gen

def preview(df,preview_rows = 5,preview_max_cols = 0):
    """ Returns a preview of a dataframe, which contains both header
    rows and tail rows.
    """
    assert type(df) is pd.DataFrame
    if preview_rows <= 0:
        preview_rows = 1
    initial_max_cols = pd.get_option('display.max_columns')
    pd.set_option('display.max_columns', preview_max_cols)
    data = df.iloc[np.r_[0:preview_rows,-preview_rows:0]]
    pd.set_option('display.max_columns', initial_max_cols)
    return str(data)