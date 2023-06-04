import pandas as pd

def summarize_trip(df):
    df['Date'] = pd.to_datetime(df['Date'])

    sea_start = None
    summarized_data = []

    for index, row in df.iterrows():
        if row['Port'] != 'Sea':
            if sea_start is not None:
                # calculate the hours spent at sea
                sea_hours = (row['Date'] - sea_start).total_seconds() / 3600 - row['Arrive']
                sea_row = {'Date': sea_start, 'Time': df.loc[index-1, 'Depart'], 
                           'Hours': sea_hours, 'Day': 'Sea', 'Port': 'Sea', 'Country': 'Sea'}
                summarized_data.append(sea_row)
                sea_start = None

            # calculate the hours spent at the port
            port_hours = row['Depart'] - row['Arrive']
            port_row = {'Date': row['Date'], 'Time': row['Arrive'], 'Hours': port_hours, 
                        'Day': row['Day'], 'Port': row['Port'], 'Country': row['Country']}
            summarized_data.append(port_row)
        elif sea_start is None:
            sea_start = row['Date']

    summarized_df = pd.DataFrame(summarized_data)
    return summarized_df

# Load the csv file
df = pd.read_csv('life_at_sea.csv')

# Use the function
summarized_df = summarize_trip(df)
print(summarized_df)
