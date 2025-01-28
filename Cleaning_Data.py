import pandas as pd
def clean_data(path):
        df = pd.read_csv(path)
        # Parsing the b_day features as datetime objects
        df['b_day'] = pd.to_datetime(df['b_day'], format='%m/%d/%y')
        # Parsing the draft_year features as datetime objects
        df['draft_year'] = pd.to_datetime(df['draft_year'].astype(str) + '-01-01')
        # Replace the missing values in team feature with "No Team"
        df['team'] = df['team'].fillna('No Team')
        # Taking the height feature in meters.
        df['height'] = df['height'].str.split('/').str[1].str.strip()  # Extracting the metric value using string operations
        # Take the weight feature in kg.
        df['weight'] = df['weight'].str.split('/').str[1].str.replace('kg.', '', regex=False).str.strip()  # Extracting the metric value using string operations
        # Removing the extraneous $ character from the salary column
        df['salary'] = df['salary'].str.replace('$', '', regex=False)
        # Parsing the height, weight, and salary features as floats;
        df = df.astype({'height':float, 'weight':float, 'salary':float})
        # Categorizing the country column as "USA" and "Not-USA";
        df['country'] = df['country'].map(lambda x: 'USA' if x == 'USA' else 'Not-USA')
        # Replacing the cells containing "Undrafted" in the draft_round column with the string "0"
        df['draft_round'] = df['draft_round'].map(lambda x: "1" if x == '1' else "0")
        return df
path = '/Users/shanmukhamundra/Desktop/NBA_Data/nba2k-full.csv'
df = clean_data(path)
print(df.head())