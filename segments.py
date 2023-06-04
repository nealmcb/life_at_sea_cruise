import pandas as pd
import argparse
import os
import numpy as np

def summarize_trip(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    summarized_data = []
    ongoing_port = None

    for index, row in df.iterrows():
        if row['Port'] != 'Sea':
            if ongoing_port is None:
                # start a new port visit
                ongoing_port = row.copy()
            elif ongoing_port['Port'] == row['Port']:
                # update the ongoing port visit
                ongoing_port['Depart'] = row['Depart']
            else:
                # finalize the ongoing port visit
                first_day_hours = 24 - ongoing_port['Arrive'] 
                last_day_hours = ongoing_port['Depart']
                extra_days = (row['Date'] - ongoing_port['Date']).days - 1
                hours = first_day_hours + last_day_hours + extra_days * 24
                port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                            'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
                summarized_data.append(port_row)
                # start a new port visit
                ongoing_port = row.copy()

        elif row['Port'] == 'Sea' and (ongoing_port is None or ongoing_port['Port'] != 'Sea'):
            if ongoing_port is not None:
                # finalize the ongoing port visit
                first_day_hours = 24 - ongoing_port['Arrive'] 
                last_day_hours = ongoing_port['Depart']
                extra_days = (row['Date'] - ongoing_port['Date']).days - 1
                hours = first_day_hours + last_day_hours + extra_days * 24
                port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                            'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
                summarized_data.append(port_row)
            ongoing_port = row.copy()

        elif row['Port'] == 'Sea' and ongoing_port['Port'] == 'Sea':
            ongoing_port['Depart'] = row['Depart']

    if ongoing_port is not None:
        first_day_hours = 24 - ongoing_port['Arrive'] 
        last_day_hours = ongoing_port['Depart']
        extra_days = (row['Date'] - ongoing_port['Date']).days
        hours = first_day_hours + last_day_hours + extra_days * 24
        row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                    'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
        summarized_data.append(row)

    summarized_df = pd.DataFrame(summarized_data)
    return summarized_df

def main(input_file):
    # Load the csv file
    df = pd.read_csv(input_file)

    # Process the data
    summarized_df = summarize_trip(df)
    
    # Create output filename and save the dataframe
    base, ext = os.path.splitext(input_file)
    output_file = base + "_segments" + ext
    summarized_df.to_csv(output_file, index=False)
    print(f"Saved the processed data to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='
    parser.add_argument('input_file', help='The CSV file to process.')
    args = parser.parse_args()

    main(args.input_file)
