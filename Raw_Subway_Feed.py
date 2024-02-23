
import time
while True:
    # pip install gtfs-realtime-bindings
    # pip install protobuf3-to-dict
    # pip install requests

    Station_1_S = "D17S"
    Station_1_N = "D17N"
    Station_2_S = "R17S" # If not needed, use ""
    Station_2_N = "R17N" # If not needed, use ""
    Station_3_S = "" # If not needed, use ""
    Station_3_N = "" # If not needed, use ""

    t1 = "D"
    t2 = "D"
    t3 = "N" # If not needed, use ""
    t4 = "N" # If not needed, use ""
    t5 = "" # If not needed, use ""
    t6 = "" # If not needed, use ""

    # This app supports up to 6 different subway feeds. Each station requires a north and a south bound station. 
    # You only need to add one train that is found in a feed. Ex: The "D" train will pull all B/D/F/M trains.
    # If you need require more, you will need to add the appropriate code above, and below starting at line 620.


    # URLs for each of the MTA's feeds
    NQRWfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw' # N,Q,R,W
    BDFMfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm' # B,D,F,M
    S1234567feed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs' # GS,1,2,3,4,5,6,7
    ACEHfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace' # A,C,E,H,FS
    Lfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l' # L
    Gfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g' # G
    JZfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz' # JZ
    #Sevenfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-7' # 7 OLD FEED
    SIRfeed = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-si' # SIR



    # Function to get feed URL based on first character
    def get_feed_url(station_code):
        first_char = station_code
        if first_char in '1234567GS':
            return S1234567feed
        elif first_char in 'NQRW':
            return NQRWfeed
        elif first_char in 'BDFM':
            return BDFMfeed
        elif first_char in 'ACEHFS':
            return ACEHfeed
        elif first_char == 'L':
            return Lfeed
        elif first_char in 'JZ':
            return JZfeed
        elif first_char == 'G':
            return Gfeed
        else:
            return "No feed available for this code"

    # Assigning feeds to variables
    feed1 = get_feed_url(t1)
    feed2 = get_feed_url(t2)
    feed3 = get_feed_url(t3)
    feed4 = get_feed_url(t4)
    feed5 = get_feed_url(t5)
    feed6 = get_feed_url(t6)

    feed1, feed2, feed3, feed4, feed5, feed6

    

    from google.transit import gtfs_realtime_pb2
    from protobuf_to_dict import protobuf_to_dict
    import requests
    import datetime
    import time
    import sys
    from datetime import datetime
    import json

    # Get our API key from file
    APIKey = 'YOUR_API_KEY'

    # List of feeds (in order) that we'll check for arrival times.
    # The order of this list will be optimized based on the
    # feeds most likely to have the trains in which we are interested
    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    # Dictionary of feed "scores." The score will simply be the number of times
    # that our desired station was found in a given feed. This will then be used
    # to optimize the order of 'feedsToCheck'
    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed1, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_1_n = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_1_N:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_1_n[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_1_n_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_1_n.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_1_n_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "due"
            }

        counter += 1  # Increment the counter

    ############################
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name
    stations_df = pd.read_csv('/YOUR/FILE/PATH//stations.csv')
    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_1_n_time_diff with station names
    for trip_data in station_1_n_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

# STATION 2 #

    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed2, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_1_s = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_1_S:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_1_s[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_1_s_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_1_s.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_1_s_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "due"
            }

        counter += 1  # Increment the counter


    ############################
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_1_n_time_diff with station names
    for trip_data in station_1_s_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    station_1_s_time_diff

# FEED 3 #



    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed3, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_2_n = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_2_N:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_2_n[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_2_n_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_2_n.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_2_n_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "due"
            }

        counter += 1  # Increment the counter

    ############################
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_2_n_time_diff with station names
    for trip_data in station_2_n_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    station_2_n_time_diff

    #### FEED 4 ####

    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    # Dictionary of feed "scores." The score will simply be the number of times
    # that our desired station was found in a given feed. This will then be used
    # to optimize the order of 'feedsToCheck'
    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed4, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_2_s = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_2_S:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_2_s[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_2_s_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_2_s.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_2_s_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "Due"
            }

        counter += 1  # Increment the counter
        ############################
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_1_n_time_diff with station names
    for trip_data in station_2_s_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    station_2_s_time_diff


    #### FEED 5 ####

    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed5, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_3_s = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_3_S:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_3_s[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_3_s_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_3_s.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_3_s_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "due"
            }

        counter += 1  # Increment the counter
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_1_n_time_diff with station names
    for trip_data in station_3_s_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    station_1_s_time_diff

    ###### FEED 6 #######
        
    feedsToCheck = [NQRWfeed, BDFMfeed, S1234567feed, ACEHfeed,
                    Lfeed, Gfeed, JZfeed, SIRfeed]

    feedScores = dict.fromkeys(feedsToCheck,0)



    uptownTimes = []
    downtownTimes = []
    uptownTrainIDs = []
    downtownTrainIDs = []
    route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(feed6, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list
    ####################

    station_3_n = {}

    for entity in subway_feed.get('entity', []):
        if 'trip_update' in entity and 'stop_time_update' in entity['trip_update']:
            trip_info = entity['trip_update'].get('trip', {})
            stop_time_updates = entity['trip_update']['stop_time_update']

            for stop in stop_time_updates:
                if stop.get('stop_id') == Station_3_N:
                    trip_id = entity['id']
                    last_stop_id = stop_time_updates[-1].get('stop_id', 'No stop_id found')
                    route_id = trip_info.get('route_id', 'No route_id found')
                    arrival_time = stop.get('arrival', {}).get('time', 'No arrival time found')
                    station_3_n[trip_id] = {
                        'route_id': route_id,
                        'last_stop_id': last_stop_id,
                        'arrival_time': arrival_time
                    }

    import datetime
    # Converting arrival times to a time difference from the current time in minutes
    current_time = datetime.datetime.now()
    station_3_n_time_diff = {}

    counter = 0  # Counter for the number of entries

    for trip_id, trip_data in station_3_n.items():
        if counter >= 30:  # Break the loop if 30 entries are already processed
            break

        arrival_time_unix = trip_data['arrival_time']
        if isinstance(arrival_time_unix, int):
            arrival_time = datetime.datetime.fromtimestamp(arrival_time_unix)
            time_diff = (arrival_time - current_time).total_seconds() / 60.0
            station_3_n_time_diff[trip_id] = {
                'route_id': trip_data['route_id'],
                'last_stop_id': trip_data['last_stop_id'],
                'arrival_time': int(round(time_diff)) if time_diff > 0 else "due"
            }

        counter += 1  # Increment the counter
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_1_n_time_diff with station names
    for trip_data in station_3_n_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    station_3_n_time_diff
        

    ############################ STATION MAPPING ########################
    import pandas as pd

    # Load the stations.csv file and create a mapping from stop_id to station name

    stop_id_to_name_csv = {row['stop_id']: row['name'] for _, row in stations_df.iterrows()}

    # Update station_2_s_time_diff with station names
    for trip_data in station_3_s_time_diff.values():
        last_stop_id = trip_data['last_stop_id']
        # Remove the last character from last_stop_id for the lookup
        last_stop_id_lookup = last_stop_id[:-1] if last_stop_id else last_stop_id
        trip_data['last_stop_name'] = stop_id_to_name_csv.get(last_stop_id_lookup, 'Unknown Station')

    # # Display the final data
    # station_2_s_time_diff

    combined_dict = {**station_1_n_time_diff, **station_1_s_time_diff, **station_2_n_time_diff, **station_2_s_time_diff, **station_3_n_time_diff, **station_3_s_time_diff}


    # Convert the list to JSON format
    json_data = json.dumps(combined_dict, indent=4)

    # Some 'arrival_time' values are not convertible to integers. 
    # Let's handle these cases by treating non-integer values differently in the sorting process.
    # Non-integer values like 'Departed' will be placed at the end of the sorted list.

    def sort_key(entry):
        try:
            # Attempt to convert 'arrival_time' to integer
            return int(entry['arrival_time'])
        except ValueError:
            # If conversion fails, return a large number to sort these entries last
            return float('inf')

    # Sorting the data with the new sort_key function
    sorted_data = sorted(combined_dict.values(), key=sort_key)

    sorted_data1 = json.dumps(sorted_data, indent=4)


    #print(sorted_data1)

    # Convert the combined dictionary to JSON format
    #json_data = json.dumps(combined_dict, indent=4)

    # Path to save the JSON file
    json_file_path = '/YOUR/FILE/PATH//output1.json'  # Update with your path

    # Writing the JSON data to a file
    with open(json_file_path, 'w') as json_file:
        json_file.write(sorted_data1)



    ############################ SERVICE STATUS GATHERING #####################################################

    from google.transit import gtfs_realtime_pb2
    from protobuf_to_dict import protobuf_to_dict
    import requests
    import datetime
    import time
    import sys
    from datetime import datetime
    import json

    # Get our API key from file
    APIKey = 'YOUR_API_KEY'

    # URLs for each of the MTA's feeds
    servalerts = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts'

    # List of feeds (in order) that we'll check for arrival times.
    # The order of this list will be optimized based on the
    # feeds most likely to have the trains in which we are interested
    feedsToCheck = [servalerts]

    # Dictionary of feed "scores." The score will simply be the number of times
    # that our desired station was found in a given feed. This will then be used
    # to optimize the order of 'feedsToCheck'
    feedScores = dict.fromkeys(feedsToCheck,0)



    # uptownTimes = []
    # downtownTimes = []
    # uptownTrainIDs = []
    # downtownTrainIDs = []
    # route_id = ""

    # Request parameters
    headers = {'x-api-key': APIKey}

    # Get the train data from the MTA
    response = requests.get(servalerts, headers=headers, timeout=30)

    # Parse the protocol buffer that is returned
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # Get a list of all the train data
    subway_feed = protobuf_to_dict(feed) # subway_feed is a dictionary
    realtime_data = subway_feed['entity'] # train_data is a list

    #subway_feed

    json_data_servstatus = json.dumps(subway_feed, indent=4)

    #print(json_data_servstatus)

    # Path to save the JSON file
    json_file_path1 = '/YOUR/FILE/PATH//status.json'  # Update with your path

    # Writing the JSON data to a file
    with open(json_file_path1, 'w') as json_file:
        json_file.write(json_data_servstatus)       

    # Load and parse the JSON file again with the correct approach
    with open('/YOUR/FILE/PATH//status.json', 'r') as file:
        data = json.load(file)['entity']


        # Define the list of possible route_ids
    route_ids = ["1", "2", "3", "4", "5", "6", "6X", "7", "7X", "A", "B", "C", "D", "E", "F", "G", "J", "L", "M", "N", "Q", "R", "S", "W", "Z","GS","FS","H", "FX"]

    # Initialize a dictionary to store the service status for each route_id
    service_status_dict = {route_id: "Good Srvice" for route_id in route_ids}

    for entity in data:
        if 'alert' in entity and 'informed_entity' in entity['alert']:
            for informed_entity in entity['alert']['informed_entity']:
                route_id = informed_entity.get('route_id')
                if route_id in route_ids:
                    # Check for service change (lmm:alert) and update the status
                    if 'lmm:alert' in entity['id']:
                        service_status_dict[route_id] = "Serv. Chng."

    service_status_dict

    # Load the newly uploaded JSON file
    new_file_path = '/YOUR/FILE/PATH//output1.json'

    # Read the file
    with open(new_file_path, 'r') as file:
        new_data = json.load(file)

    # Add the service status to each route_id in the new_data
    for item in new_data:
        route_id = item.get('route_id')
        if route_id in service_status_dict:
            item['service_status'] = service_status_dict[route_id]
        else:
            item['service_status'] = "Unknown"


    output_path = '/YOUR/FILE/PATH//output.json'
    # Save the updated data back to the file
    with open(output_path, 'w') as file:
        json.dump(new_data, file, indent=4)   


    time.sleep(15)

