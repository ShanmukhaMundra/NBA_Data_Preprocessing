from Cleaning_Data import *
def feature_data(df):
    #Parsing as datetime object
    df['version'] = pd.to_datetime(['20'+i[5:]for i in df['version']])
    df['version'] = pd.to_datetime(df['version'])
    df['b_day'] = pd.to_datetime(df['b_day'])
    df['age'] = (df['version'] - df['b_day']).dt.days // 365 + 1
    df['experience'] = (df['version'] - df['draft_year']).dt.days // 365
    #Adding 'BMI-Body Mass Index" column (bmi = weight/height^2)
    df['bmi'] = df['weight'] / (df['height'] * df['height'])
    #Dropping unnecessary columns
    df.drop(['version', 'b_day', 'draft_year', 'weight', 'height'], axis=1, inplace=True)
    #Removing high Cardinality features
    categorical_cols = df.select_dtypes(include=['object']).columns
    threshold = 50
    high_cardinality_cols = [col for col in categorical_cols if df[col].nunique() > threshold]
    df = df.drop(columns=high_cardinality_cols)
    return df
df_cleaned = clean_data(path)
df = feature_data(df_cleaned)
print(df[['age', 'experience', 'bmi']].head())