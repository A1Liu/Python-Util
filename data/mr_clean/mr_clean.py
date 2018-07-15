# -*- coding: utf-8 -*-
import pandas as pd
import mr_clean_functions as mcf

#This method takes in a DataFrame object, as well as a few parameters,
# and outputs a cleaned DataFrame. It operates under a few basic assumptions,
# so it can't do everything lol
def clean(df, 
             char_scrub = True, char_scrub_cutoff = .99, scrub_ignore = [],
             numeric_cutoff = .95, coerce_numeric = [], 
             dt_cutoff = .99, coerce_dt = [], dt_format = None,
             categorical_cutoff = .60,coerce_categorical = [],
             output_file = None,output_safe = True):
    
    # Error Trap inputs
    assert type(df) is pd.DataFrame
    column_dict = {}
    for element in coerce_numeric + coerce_dt + coerce_categorical: # these lists must be mutually exclusive
        assert type(element) is str
        assert not element in column_dict
        column_dict[element] = True
    del(column_dict)
    
    def memory_savings(task_name = None): # Returns a memory statement and resets memory
        nonlocal df_memory, df
        savings = df_memory - reset_mem()
        if savings > 0 and task_name is not None:
            return memory_statement(savings,task_name)+'\n'
    
    def memory(column = None):# Returns the memory of the dataframe
        nonlocal df
        if column is None:
            return df.memory_usage(deep=True)
        else:
            return df[column].memory_usage(deep=True)
    
    def reset_mem():# Resets memory value
        nonlocal df_memory
        df_memory = memory().sum()
        return df_memory

    # Make a copy of the inputted DataFrame
    df = df.copy()
    begin_df_memory = memory().sum()
    df_memory = begin_df_memory
    
    
    # ------TASK 1: CHANGE COLNAMES----------
    col_list = []
    print('Renaming columns...')
    for column in df:
        col_list.append(column.strip().lower().replace(' ','_'))
    df.columns = col_list
    del(col_list)
    
    # ------TASK 2: REMOVE WHITESPACE--------
    print('Checking for extra whitespace...')
    col_mem = memory()
    for savings,column in ((col_mem[column]-memory(column),column) for column in mcf.remove_whitespace(df) if col_mem[column]-memory(column) > 0):
        print( memory_statement(savings,
                                   "removing extra whitespace from column '{}'" \
                                   .format(column)))
    output = memory_savings('removing whitespace')
    print(output) if output is not None else None

    # ------TASK 3: REFORMAT INDEX-----------
    if mcf.rename_index(df):
        print('Changing unhelpful index and adding it as column')
        print("Size grew by " + memory_statement('adding a row')[8:])
    

    # Try to remove characters from beginning and end of columns
    # ------TASK 3: DEEP CLEAN---------------
    if char_scrub:
        print('Trying character scrub...')
        for result in ( mcf.scrub_str_cols( df,column, mcf.get_cutoff(column,char_scrub_cutoff) ) 
                                                for column in df if column not in scrub_ignore ):
            print("Scrubbed '{}' from the front and '{}' from the back of column '{}'" \
                 .format(*result)) if result is not None else None
        output = memory_savings('character scrubbing')
        print(output) if output is not None else None
                        
    
    # ------TASK 4: Coerce data types--------
    col_mem = memory()
    print('Trying to coerce column values...')
    for column in df:
        if mcf.coerce_col(df,column,
                    numeric_cutoff, coerce_numeric, 
                    dt_cutoff, coerce_dt, dt_format,
                    categorical_cutoff,coerce_categorical):
            print( memory_statement( col_mem[column]-memory(column),
                                    "coercing column '{}' to dtype '{}'" \
                                       .format(column,df[column].dtype) ) )
    output = memory_savings('coercing columns to specialized data-types')
    print(output) if output is not None else None

    # ------TASK 4:
    # ------TASK 5:
    # ------TASK 6:
    # ------TASK 7:
    # ------TASK 8:
    # ------TASK 9:
    # Handle missing values
    # Change data formats
    # Do melts and pivots (If necessary)
    
    
    # Print what was done
    print('Initial data size in memory: {}'.format( convert_memory(begin_df_memory) ) )
    print('  Final data size in memory: {}'.format( convert_memory(memory().sum()) ) )
    print('                     Change: {}'.format( convert_memory(memory().sum()-begin_df_memory) ) )
    
    if output_file is None:
        return df
    else:
        try:
            with open(output_file,'x' if output_safe else 'w') as file:
                    file.write(df)
        except FileExistsError:
            print("Nothing outputted: file '{}' already exists".format(output_file))
        

def memory_statement(savings,task_name):
    return 'Saved {} after {}' \
              .format( convert_memory(savings) ,task_name )
              
def convert_memory(memory_value):
    unit_list = ['KB','MB','GB','TB']
    index = 0
    memory = memory_value / 1024
    while memory > 1000 and index < 3:
        memory/=1024
        index+=1
    return '{} {}'.format(round( memory, 1),unit_list[index])
    
    

