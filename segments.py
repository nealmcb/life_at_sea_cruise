import pandas as pd

def summarize_trip(df):
    df['Date'] = pd.to_datetime(df['Date'])

    summarized_data = []

    for index, row in df.iterrows():
        if row['Port'] != 'Sea':
            # calculate the hours spent at the port
            port_hours = row['Depart'] - row['Arrive']
            port_row = {'Date': row['Date'], 'Day': row['Day'], 'Port': row['Port'], 
                        'Country': row['Country'], 'Time': row['Arrive'], 'Hours': port_hours}
            summarized_data.append(port_row)

            if index < len(df) - 1:
                # calculate the hours spent at sea
                next_port_arrival = df.loc[index+1, 'Arrive']
                if df.loc[index+1, 'Date'] == row['Date']:
                    sea_hours = 24 - row['Depart'] + next_port_arrival
                else:
                    sea_days = (df.loc[index+1, 'Date'] - row['Date']).days
                    sea_hours = (sea_days - 1) * 24 + (24 - row['Depart']) + next_port_arrival

                sea_row = {'Date': row['Date'], 'Day': row['Day'], 'Port': 'Sea', 
                           'Country': 'Sea', 'Time': row['Depart'], 'Hours': sea_hours}
                summarized_data.append(sea_row)

    summarized_df = pd.DataFrame(summarized_data)
    return summarized_df

# Load the csv file
df = pd.read_csv('life_at_sea.csv')

# Use the function
summarized_df = summarize_trip(df)
print(summarized_df)
