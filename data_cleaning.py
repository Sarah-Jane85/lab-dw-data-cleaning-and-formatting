import pandas as pd
import numpy as np

def clean_column_names(df):
    df_columns = [ 'customer', 'state', 'gender', 'education', 'customer_lifetime_value', 'income', 'monthly_premium', 'number_open_complaints', 'policy_type', 'vehicle_class', 'total_claim_amount']
    df.columns = df_columns
    return df

def extract_middle_value(df):
    
    def get_middle_value(value):
   
        if isinstance(value, str):
            parts = value.split('/')  # Split the string by '/'
            return int(parts[1]) if len(parts) > 1 else 0  # Return the middle value if it exists, otherwise return 0.
        else:
            return 0
    # Apply the function to convert the entire column.
    df['number_open_complaints'] = df['number_open_complaints'].apply(get_middle_value)
    return df

def fill_missing_values(df):
    df['state'] = df['state'].fillna('Unknown')
    df['customer'] = df['customer'].fillna('Invalid')
    df['gender'] = df['gender'].fillna('Divers')
    df['education'] = df['education'].fillna('Unknown')
    df['policy_type'] = df['policy_type'].fillna('Invalid')
    return df

#def replace_zero_with_nan(df, column_name):
 #   mask_all_null_except = df.drop(columns=[column_name]).isnull().all(axis=1)
  #  df.loc[mask_all_null_except, column_name] = df.loc[mask_all_null_except, column_name].replace(0, np.nan)
   # return df
#make function (nested if statements)


def fill_missing_income(df):
    vehicle_classes = ['Luxury', 'Four-Door Car', 'Two-Door Car', 'SUV']
    mean_incomes = {}
    #calculate mean incomes
    for vehicle_class in vehicle_classes:
        class_df = df[df['vehicle_class'] == vehicle_class]
        mean_incomes[vehicle_class] = class_df['income'].mean()
    #define row wise function
    def fill_value(row):
        if pd.isnull(row['income']):
            return mean_incomes.get(row['vehicle_class'], row['income'])
        return row['income']
    
    df['income'] = df.apply(fill_value, axis=1)
    return df

def fill_missing_customer_life_value(df):
 #convert to float
    df['customer_lifetime_value'] = df['customer_lifetime_value'].str.replace('%', '').astype(float)

    #calculate mean incomes based on vehicle class
    vehicle_classes = ['Luxury', 'Four-Door Car', 'Two-Door Car', 'SUV']

    mean_incomes = {}
    for vehicle_class in vehicle_classes:
        class_df = df[df['vehicle_class'] == vehicle_class]
        mean_incomes[vehicle_class] = class_df['customer_lifetime_value'].mean()
    
    #define row-wise function
    def fill_value(row):
        if pd.isnull(row['customer_lifetime_value']):
            return mean_incomes.get(row['vehicle_class'], row['customer_lifetime_value'])
        return row['customer_lifetime_value']
    
    df['customer_lifetime_value'] = df.apply(fill_value, axis = 1)
    return df


def drop_duplicate_rows(df, subset=None):
    return df.drop_duplicates(subset=subset)

# Main function to perform all cleaning steps
def clean_data(df):
    df = clean_column_names(df)
    df = extract_middle_value(df)
    df = fill_missing_values(df)
    df = fill_missing_income(df)
    df = fill_missing_customer_life_value(df)
    #df = replace_zero_with_nan(df, 'Number of Open Complaints')
    df = drop_duplicate_rows(df)
    return df