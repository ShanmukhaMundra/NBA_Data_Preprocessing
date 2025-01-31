from future_engineering import *
def multicol_data(feature_data):
    df = feature_data
    df = df.select_dtypes(include=['number'])
    corr_matrix = df.corr()
    correlated_features = set()
    for col in corr_matrix.columns:
        for idx in corr_matrix.index:
            if col != idx and abs(corr_matrix.loc[col, idx]) > 0.5:
                correlated_features.add((col, idx))
    target_corr = corr_matrix['salary'].drop('salary')
    features_to_drop = set()
    for feat1, feat2 in correlated_features:
        if feat1 in target_corr and feat2 in target_corr:
            if abs(target_corr[feat1]) < abs(target_corr[feat2]):
                features_to_drop.add(feat1)
            else:
                features_to_drop.add(feat2)
    df = df.drop(columns=features_to_drop, errors='ignore')
    return df
path = path
df_cleaned = clean_data(path)
df_featured = feature_data(df_cleaned)
df = multicol_data(df_featured)
print(list(df.select_dtypes('number').drop(columns='salary')))