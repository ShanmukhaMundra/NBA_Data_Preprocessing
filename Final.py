import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
def clean_data(path):
    df = pd.read_csv(path)
    df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
    df['draft_year'] = pd.to_datetime(df['draft_year'].astype(str) + '-01-01', errors='coerce')
    df['team'] = df['team'].fillna('No Team')
    df['height'] = df['height'].str.extract(r'/\s*([\d.]+)').astype(float)
    df['weight'] = df['weight'].str.extract(r'/\s*([\d.]+)').astype(float)
    df['salary'] = df['salary'].str.replace('$', '', regex=False).astype(float)
    df['country'] = df['country'].apply(lambda x: 'USA' if x == 'USA' else 'Not-USA')
    df['draft_round'] = df['draft_round'].replace("Undrafted", "0").astype(str)
    return df
def feature_data(df):
    df['version'] = df['version'].str.extract(r'(\d{2})$')[0].astype(int) + 2000
    df['version'] = pd.to_datetime(df['version'].astype(str) + '-01-01')
    df['age'] = (df['version'] - df['b_day']).dt.days // 365
    df['experience'] = (df['version'] - df['draft_year']).dt.days // 365
    df['bmi'] = df['weight'] / (df['height'] ** 2)
    df.drop(['version', 'b_day', 'draft_year', 'weight', 'height', 'full_name', 'jersey'], axis=1, inplace=True)
    categorical_cols = df.select_dtypes(include=['object']).columns
    high_cardinality_cols = [col for col in categorical_cols if df[col].nunique() > 50]
    df.drop(columns=high_cardinality_cols, inplace=True)
    return df
def multicol_data(df):
    df_combined = df.select_dtypes(include=['number', 'object'])
    df_numeric = df_combined.select_dtypes(include=['number'])
    corr_matrix = df_numeric.corr()
    correlated_features = set()
    for col in corr_matrix.columns:
        for idx in corr_matrix.index:
            if col != idx and abs(corr_matrix.loc[col, idx]) > 0.5:
                correlated_features.add((col, idx))
    target_corr = corr_matrix['salary'].dropna()
    features_to_drop = set()
    for feat1, feat2 in correlated_features:
        if (feat1 in ['age', 'rating', 'experience', 'salary', 'draft_round']
                or feat2 in ['age', 'rating', 'experience', 'salary', 'draft_round']):
            continue
        if feat1 in target_corr and feat2 in target_corr:
            if abs(target_corr[feat1]) < abs(target_corr[feat2]):
                features_to_drop.add(feat1)
            else:
                features_to_drop.add(feat2)
    df_combined.drop(columns=features_to_drop, errors='ignore', inplace=True)
    return df_combined
def transform_data(df):
    #target_column = 'salary'
    y = df['salary']
    feature_cols = df.drop(columns=['salary'])
    numerical_cols = feature_cols.select_dtypes(include=['number']).columns
    categorical_cols = feature_cols.select_dtypes(include=['object']).columns
    scaler = StandardScaler()
    scaled_numerical = scaler.fit_transform(feature_cols[numerical_cols])
    scaled_numerical_df = pd.DataFrame(scaled_numerical, columns=numerical_cols)
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_categorical = encoder.fit_transform(feature_cols[categorical_cols])
    encoded_columns = [val for col, vals in zip(categorical_cols, encoder.categories_) for val in vals]
    encoded_categorical_df = pd.DataFrame(encoded_categorical, columns=encoded_columns)
    X = pd.concat([scaled_numerical_df, encoded_categorical_df], axis=1)
    X = X.drop(columns=['age'], errors='ignore')
    return X, y
path = "/Users/shanmukhamundra/Desktop/NBA_Data/nba2k-full.csv"
df_cleaned = clean_data(path)
df_featured = feature_data(df_cleaned)
df_filtered = multicol_data(df_featured)
X, y = transform_data(df_filtered)
print(X.shape, y)