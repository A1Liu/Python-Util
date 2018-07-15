# MR CLEAN
With Mr. Clean, no dataset is safe! (Unless it's clean, or in a format other than DataFrame.)

## Plan

0. Make a copy of the inputted DataFrame
1. Diagnose problems with underlying data format
2. Handle missing values
3. Change data formats
4. Do melts and pivots (If necessary)
5. Print what was done

#### Diagnose underlying problems

These are problems that hinder every other operation that could be done, and include:

- All entries contain characters that prevent the dataframe from being read in correctly.
- Rows are labeled with names that make it harder to do analysis
- Data is corrupted
- No entries 
- Entries are encoded wrong

#### Handling missing values

1. Change missing values to NaN, using some logic to do this.
2. Fill missing values, using logic and some user inputs

#### Changing data formats

1. Coerce columns to numerics and datetimes
2. Change columns to categorical
3. Handle missing values again

#### Melts and pivots

1. Infer columns that need to be melted or pivoted
2. Do it.
3. If a melt was performed, convert the 'variable' column to a categorical column

#### Print what was done

Print exactly what was done, and a (useful) summary of the dataset, after each action.
