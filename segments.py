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
                first_day_hours = 24 - ongoing_port['Arrive'] if ongoing_port['Arrive'] else 24
                last_day_hours = ongoing_port['Depart'] if ongoing_port['Depart'] else 24
                extra_days = (row['Date'] - ongoing_port['Date']).days - 1
                hours = first_day_hours + last_day_hours + extra_days * 24
                port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                            'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
                summarized_data.append(port_row)
                # start a new port visit
                ongoing_port = row.copy()
        elif ongoing_port is not None:
            # finalize the ongoing port visit
            first_day_hours = 24 - ongoing_port['Arrive'] if ongoing_port['Arrive'] else 24
            last_day_hours = ongoing_port['Depart'] if ongoing_port['Depart'] else 24
            extra_days = (row['Date'] - ongoing_port['Date']).days - 1
            hours = first_day_hours + last_day_hours + extra_days * 24
            port_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': ongoing_port['Port'], 
                        'Country': ongoing_port['Country'], 'Time': ongoing_port['Arrive'], 'Hours': hours}
            summarized_data.append(port_row)
            ongoing_port = None
        
        if row['Port'] == 'Sea' and (ongoing_port is None or ongoing_port['Port'] != 'Sea'):
            ongoing_port = row.copy()
        elif row['Port'] == 'Sea' and ongoing_port['Port'] == 'Sea':
            ongoing_port['Depart'] = row['Depart']
        elif ongoing_port is not None and ongoing_port['Port'] == 'Sea':
            # finalize the ongoing sea trip
            first_day_hours = 24 - ongoing_port['Arrive'] if ongoing_port['Arrive'] else 24
            last_day_hours = ongoing_port['Depart'] if ongoing_port['Depart'] else 24
            extra_days = (row['Date'] - ongoing_port['Date']).days - 1
            hours = first_day_hours + last_day_hours + extra_days * 24
            sea_row = {'Date': ongoing_port['Date'], 'Day': ongoing_port['Day'], 'Port': 'Sea', 
                       'Country': 'Sea', 'Time': ongoing_port['Arrive'], 'Hours': hours}
            summarized_data.append(sea_row)
            ongoing_port = None

    if ongoing_port is not None:
        first_day_hours = 24
