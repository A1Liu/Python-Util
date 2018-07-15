# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import io

#%% Cleaning utility

#This method takes in a DataFrame object, as well as a few parameters,
# and outputs a cleaned DataFrame. It operates under a few basic assumptions,
# so it can't do everything lol
def mr_clean(df, coerce_cols = [], categorical_cols = [], set_missing = {}, melt_cols = [], fill_missing = {}):
    assert type(df) is pd.DataFrame
    df = df.copy()



    for colname, missing_vals in set_missing:

    # Change missing values first (use set_missing as a dictionary of missing values for each column, where keys are column names)
    # Filling missing values
    # coerce columns (use coerce_cols)
    # create categorical columns (use categorical_cols)
    # try to melt a subset of columns
    pass

