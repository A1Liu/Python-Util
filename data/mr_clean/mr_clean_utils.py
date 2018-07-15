# -*- coding: utf-8 -*-
import numpy as np

def coerce(df,column, coerce):
    df[column] = coerce

def row_req(df,cutoff):
    return rows(df) * cutoff

def rows(df):
    return df.shape[0]

def is_num(series):
    if (series.dtype == np.float64 or series.dtype == np.int64):
        return True
    return False