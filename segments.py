import pandas as pd
import argparse
import os

def summarize_trip(df):
    df['Date'] = pd.to_datetime(df['Date'])

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
                hours = ongoing_port['Depart'] - ongoing_port['Arrive']
                port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                            'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
                summarized_data.append(port_row)
                # start a new port visit
                ongoing_port = row.copy()

        if ongoing_port is not None and (row['Port'] == 'Sea' or index == len(df) - 1):
            # finalize the ongoing port visit
            hours = ongoing_port['Depart'] - ongoing_port['Arrive']
            port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                        'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
            summarized_data.append(port_row)
            ongoing_port = None

        if row['Port'] == 'Sea' and index < len(df) - 1:
            # calculate the hours spent at sea
            next_row = df.loc[index+1]
            sea_hours = (next_row['Arrive'] if next_row['Port'] != 'Sea' else 24) - row['Depart']
            sea_row = {'Date': row['Date'], 'Day': row['Day'], 'Port': 'Sea', 
                       'Country': 'Sea', 'Time': row['Depart'], 'Hours': sea_hours}
            summarized_data.append(sea_row)

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
    parser = argparse.ArgumentParser(description='Process a trip itinerary CSV file.')
    parser.add_argument('input_file', help='The CSV file to process.')
    args = parser.parse_args()

    main(args.input_file)
