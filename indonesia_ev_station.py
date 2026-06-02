# Import Libraries
import duckdb
from tabulate import tabulate
import s2cell
import geocoder
from geopy import distance
from geopy.geocoders import Nominatim
import webbrowser

# ------------------------------------------------------------------------------------------------------ #

# Data Preparation

# Import Data
duckdb.sql('INSTALL httpfs; LOAD httpfs;')
ev_station_df = duckdb.read_parquet('https://github.com/dzakwantaufiq/indonesia_ev_station_crud_project/raw/35a3d6570e7466645f87cc579c6ec7a02de0aba3/data/indonesia_ev_station.parquet').to_df()
ev_station_dict = ev_station_df.set_index('id').T.to_dict()

# Convert dictionary to list of dictionary
ev_station_list = []
for key,value in ev_station_dict.items():
    row = {'id': key}
    row.update(value)
    ev_station_list.append(row)

# ------------------------------------------------------------------------------------------------------ #

# Function

def show_menu():
    return input("""
Welcome to Indonesia's EV Station Directory\n

Available Menu:
1. Show EV Station Distribution in Indonesia
2. Add New EV Station
3. Update Current EV Station Information
4. Remove Inactive EV Station
5. Route to the Surrounding EV Station
6. Exit\n
                        
Please choose the menu by entering the corresponding number (1-6): """)

def show_distribution_menu():
    return input("""
Please Input the City Name (format: 'Kota/Kab <city_name>'; special for Jakarta, please follow this example 'Kota ADM Jakarta Pusat'): """)

def show_ev_information(dict_list):
    keys_to_show = ["id", "name", "highest_power", "total_chargers", "city", "province"]
    filtered = [{k: d[k] for k in keys_to_show} for d in dict_list]
    return tabulate(filtered, headers='keys', tablefmt="mixed_outline", showindex=False)

def show_ev_information_update(dict_list):
    keys_to_show = ["id", "name", "address", "provider", "highest_power", "total_chargers"]
    filtered = [{k: d[k] for k in keys_to_show} for d in dict_list]
    return tabulate(filtered, headers='keys', tablefmt="mixed_outline", showindex=False)

def return_to_menu():
    return input(f"\nDo you want to return to the previous menu? (y/n): ")

def show_id_menu():
    return input("""
Please Input the EV Station ID: """)

def integer_checker(user_input):
    while True:
        try:
            int_value = input(user_input)
            return int(int_value)
        except ValueError:
            print(f'\nInvalid input. Please input a proper number. You have entered: {int_value}')
        
def coordinate_checker(user_input):
    while True:
        try:
            float_value = input(user_input)
            return float(float_value)
        except ValueError:
            print(f'\nInvalid input for location. Please input a proper coordinate. You have entered: {float_value}')

def geocoder_user_ip_location():
    g = geocoder.ip('me')
    loc = g.latlng
    return loc

def nearby_ev_station(list_of_dictionary):
    total_data = 0
    for i in list_of_dictionary:
        total_data += 1
    return total_data

def coordinate_checker_input():
    while True:
        try:
            input_coordinate = input('\nPlease input the coordinates: ')
            lat_input, lon_input = input_coordinate.strip().split(',')
            latitude = float(lat_input)
            longitude = float(lon_input)
            return latitude, longitude
        except:
            print(f'\nInvalid input for coordinates. Please input in the correct coordinate (format: latitude,longitude). You have entered: {input_coordinate}')
            continue

def geocoding():
    while True:
        try:
            geolocator = Nominatim(user_agent="my_app")
            location = geolocator.geocode(input("\nPlease input the POI name: "))
            poi_name = location.raw['name']
            poi_latitude = location.latitude
            poi_longitude = location.longitude
            return poi_name, poi_latitude, poi_longitude
        except AttributeError:
            print('\nLocation not found. Try using a more specific or well-known landmark/POI.')


# ------------------------------------------------------------------------------------------------------ #

# CRUD Menu

while True:

    menu_option = show_menu()

    # Menu 1 - READ
    if menu_option == '1':
        while True:
            print("---"*30)
            menu_1_option = input("""
Available show options:
1. Based on City
2. Based on EV Station's ID
3. Back to Main Menu
                                  
Please choose one option (1-3): """)
            print("---"*30)
        
            if menu_1_option == '1':
                while True:
                    choosen_city = show_distribution_menu()

                    selected_city = []
                    for i in ev_station_list:
                        if i['city'].lower() == choosen_city.lower():
                            selected_city.append(i)
                    
                    if selected_city != []:
                        print(f'\nEV Station Distribution in {choosen_city.title()}:')
                        print(show_ev_information(selected_city))
                    
                        back_menu_read = return_to_menu()
                        
                        if back_menu_read.lower() == 'y':
                            break
                        elif back_menu_read.lower() == 'n':
                            print("\nDo you want to select another city?")
                        else:
                            print("\nInvalid input, automatically returning to previous menu.")
                            break
                    else:
                        print(f'\nNo EV stations found in {choosen_city}, if you wrote incorrectly, please follow the format and try again.')
                        continue

            elif menu_1_option == '2':
                while True:
                    try:
                        choosen_id_input = show_id_menu()
                        choosen_id = int(choosen_id_input)
                        
                        selected_id = []
                        for i in ev_station_list:
                            if i['id'] == choosen_id:
                                selected_id.append(i)

                        if selected_id != []:
                            print(f'\nEV Station Information with ID {choosen_id}:')
                            print(show_ev_information(selected_id))
                        
                            back_menu_read = return_to_menu()
                            
                            if back_menu_read.lower() == 'y':
                                break
                            elif back_menu_read.lower() == 'n':
                                print("\nDo you want to select another EV Station ID?")
                            else:
                                print("\nInvalid input, automatically returning to previous menu.")
                                break
                        else:
                            print(f'\nEV stations with ID {choosen_id} does not exist. Please try again.')
                            continue
                    except ValueError:
                        print(f'\nInvalid input for EV Station ID. Please input numbers. You have entered: {choosen_id_input}')

            elif menu_1_option == '3':
                break
            
            else:
                print(f'\nPlease input the proper menu option (1-3). You have entered: {menu_1_option}')
    

    # Menu 2 - CREATE
    elif menu_option == '2':
        add_ev_station = []
        while True:
            print("---"*30)
            menu_2_option = input("""
Available add options:
1. Add a new EV Station
2. Back to Main Menu
                                  
Please choose one option (1-2): """)
            print("---"*30)

            if menu_2_option == '1':
                while True:
                    try:
                        add_ev_id = input("\nPlease input the new EV Station's ID: ")
                        value = int(add_ev_id)

                        id_exists = False
                        for id in ev_station_list:
                            if id['id'] == value:
                                id_exists = True
                                break 

                        if id_exists == True:
                            print(f"\nID {add_ev_id} already exists. Please input a different EV Station's ID")
                            continue

                        elif id_exists == False:
                            print('\nPlease input the necessary information below to add the new EV Station')
                            add_ev_name = input("Name: ")
                            add_ev_provider = input("Provider: ")
                            add_ev_address = input("Address: ")

                            add_ev_highest_power = integer_checker("Highest Power (in kW): ")
                            add_ev_total_chargers = integer_checker("Total Chargers: ")

                            add_ev_city = input("City: ")
                            add_ev_province = input("Province: ")
                            
                            add_ev_latitude = coordinate_checker("Latitude: ")
                            add_ev_longitude = coordinate_checker("Longitude: ")

                            add_ev_s2cell_id_12 = s2cell.lat_lon_to_cell_id(add_ev_latitude, add_ev_longitude, 12)

                    except ValueError:
                        print(f"\nInvalid input for EV Station's ID. Please input numbers. You have entered: {add_ev_id}")
                        continue

                # append the list + show the added data in the same city
                    new_ev_station = [{
                        'id': value,
                        'name': add_ev_name.title(),
                        'provider': add_ev_provider.upper(),
                        'address': add_ev_address.capitalize(),
                        'highest_power': str(int(add_ev_highest_power)) + " kW",
                        'total_chargers': int(add_ev_total_chargers),
                        'city': add_ev_city.title(),
                        'province': add_ev_province.title(),
                        'latitude': float(add_ev_latitude),
                        'longitude': float(add_ev_longitude),
                        's2cell_id_12': int(add_ev_s2cell_id_12)
                    }]

                    add_ev_station.extend(new_ev_station)
                    print('\nThe new EV Station that will be added into database:')
                    print(tabulate(add_ev_station, headers='keys', tablefmt="mixed_outline", showindex=False))
                    
                    checker_add = input("\nDo you want to save the new EV Station? (y/n): ")
                    if checker_add.lower() == 'y':
                        ev_station_list.extend(add_ev_station)
                        print("\nThe New EV Station has been saved.")

                        back_menu_read = return_to_menu()
                        if back_menu_read.lower() == 'y':
                            break
                        elif back_menu_read.lower() == 'n':
                            print("\nDo you want to add another EV Station?")
                        else:
                            print("\nInvalid input, automatically returning to previous menu.")
                            break      
                    elif checker_add.lower() == 'n':
                        print("\nThe New EV Station will not be saved.")
                        break
                    else:
                        print("\nInvalid input, the new EV Station will not be saved.")
                        break

            elif menu_2_option == '2':
                break
            else:
                print(f'\nPlease input the proper menu option (1-2). You have entered: {menu_2_option}')


    # Menu 3 - UPDATE
    elif menu_option == '3':
        while True:
            print("---"*30)
            menu_3_option = input("""
Available update options:
1. Update information from an existing EV Station
2. Back to Main Menu
                                  
Please choose one option (1-2): """)
            print("---"*30)

            if menu_3_option == '1':
                while True:
                    try:
                        update_ev_id_input = input("\nPlease input the EV Station's ID that you want to update: ")
                        update_ev_id = int(update_ev_id_input)
                        
                        id_exists = False
                        for id in ev_station_list:
                            if id['id'] == int(update_ev_id):
                                id_exists = True
                                break
                        
                        if id_exists == False:
                            print(f"\nID {update_ev_id} does not exist. Please input a different EV Station's ID")
                            continue
                        else:
                            print(f'\nEV Station Information with ID {update_ev_id}:')
                            selected_updated_id = []
                            for i in ev_station_list:
                                if i['id'] == int(update_ev_id):
                                    selected_updated_id.append(i)
                            print(show_ev_information_update(selected_updated_id))


                            checker_update = input("\nDo you want to update this EV Station information? (y/n): ")
                            if checker_update.lower() == 'y':
                                while True:
                                    updated_column = input("\nWrite the column name that you want to update: ").lower()
                                    if updated_column not in ev_station_list[0].keys():
                                        print(f"\nColumn name {updated_column} does not exist. Please write the column name based on the shown information and try again")
                                        continue
                                    updated_value = input(f"\nWrite the new value for the {updated_column} column: ")
                                    ev_station_list_copy = ev_station_list.copy()
                                    for i in ev_station_list_copy:
                                        if i['id'] == int(update_ev_id):
                                            i[updated_column] = updated_value

                                    print('\nBelow is the updated information for this EV Station:')
                                    selected_updated_id = []
                                    for i in ev_station_list:
                                        if i['id'] == int(update_ev_id):
                                            selected_updated_id.append(i)
                                    print(show_ev_information_update(selected_updated_id))

                                    checker_update_confirm = input("\nDo you want to save this updated information? (y/n): ")
                                    if checker_update_confirm.lower() == 'y':
                                        for i in ev_station_list:
                                            if i['id'] == int(update_ev_id):
                                                i[updated_column] = updated_value
                                        print("\nThis EV Station information has been updated.")
                                        break
                                    elif checker_update_confirm.lower() == 'n':
                                        print("\nThe update request is cancelled.")
                                        break
                                    else:
                                        print("\nInvalid input, automatically returning to previous menu.")
                                        break
                            elif checker_update.lower() == 'n':
                                print("\nThe update request is cancelled.")
                                break
                            else:
                                print("\nInvalid input, automatically returning to previous menu.")
                                break
                        break
                    except ValueError:
                        print("\nInvalid input. Please enter a valid EV Station ID.")
                        
            elif menu_3_option == '2':
                break
            else:
                print(f'\nPlease input the proper menu option (1-2). You have entered: {menu_3_option}')


    # Menu 4 - DELETE
    elif menu_option == '4':
        while True:
            print("---"*30)
            menu_4_option = input("""
Available delete options:
1. Delete an existing EV Station
2. Back to Main Menu
                                  
Please choose one option (1-2): """)
            print("---"*30)

            if menu_4_option == '1':
                while True:
                    try:
                        delete_ev_id_input = input("\nPlease input the EV Station's ID that you want to delete: ")
                        delete_ev_id = int(delete_ev_id_input)

                        id_exists = False
                        for id in ev_station_list:
                            if id['id'] == int(delete_ev_id):
                                id_exists = True
                                break
                        
                        if id_exists == False:
                            print(f"\nID {delete_ev_id} does not exist. Please input a different EV Station's ID")
                            continue

                        else:
                            print(f'\nEV Station Information with ID {delete_ev_id}:')
                            selected_deleted_id = []
                            for i in ev_station_list:
                                if i['id'] == int(delete_ev_id):
                                    selected_deleted_id.append(i)
                            print(show_ev_information_update(selected_deleted_id))

                            checker_delete = input("\nDo you want to delete this EV Station information? (y/n): ")
                            if checker_delete.lower() == 'y':
                                for i in ev_station_list:
                                    if i['id'] == int(delete_ev_id):
                                        ev_station_list.remove(i)
                                print("\nThis EV Station information has been deleted.")
                                break
                            elif checker_delete.lower() == 'n':
                                print("\nThe delete request is cancelled.")
                                break
                            else:
                                print("\nInvalid input, automatically returning to previous menu.")
                                continue
                    except ValueError:
                        print("\nInvalid input. Please enter a valid EV Station ID.")

            elif menu_4_option == '2':
                break
            else:
                print(f'\nPlease input the proper menu option (1-2). You have entered: {menu_4_option}')

# ------------------------------------------------------------------------------------------------------ #

# Geospatial Menu

    # Menu 5 - EXTRA FUNCTION
    elif menu_option == '5':
        while True:
            print("---"*30)
            menu_5_option = input("""
Available options to find the surrounding EV Station:
1. My Current Location (based on IP Geolocation)
2. Based on the coordinates
3. Based on the the POI (Point of Interest)
4. Back to Main Menu
                                  
Please choose one option (1-4): """)
            print("---"*30)

            if menu_5_option == '1':
                latitude, longitude = geocoder_user_ip_location()

                user_s2cell_id_12 = s2cell.lat_lon_to_cell_id(latitude, longitude, 12)
                user_s2cell_id_12_neighbors = s2cell.cell_id_to_neighbor_cell_ids(user_s2cell_id_12, edge=True, corner=True)
                user_s2cell_id_12_neighbors.append(user_s2cell_id_12)

                user_ip_location = {
                    'latitude': latitude,
                    'longitude': longitude,
                    's2cell_id_12_neighbors': user_s2cell_id_12_neighbors
                    }
                
                surrounding_ev_stations = []
                for i in ev_station_list:
                    if i['s2cell_id_12'] in user_ip_location['s2cell_id_12_neighbors']:
                        surrounding_ev_stations.append(i)

                total_nearby_ev_station = nearby_ev_station(surrounding_ev_stations)

                if total_nearby_ev_station == 0:
                    print("\nNo EV Station found in your surrounding area.")
                    continue
                elif total_nearby_ev_station > 0:
                    distance_to_surrounding_ev_stations = []
                    for station in surrounding_ev_stations:
                        distance_m = round(distance.distance((latitude, longitude), (station['latitude'], station['longitude'])).km, 3)
                        distance_to_surrounding_ev_stations.append({
                            'id': station['id'],
                            'name': station['name'],
                            # 'address': station['address'],
                            'highest_power': station['highest_power'],
                            'total_chargers': station['total_chargers'],
                            # 'highest_charger_types': station['highest_charger_types'],
                            'latitude': station['latitude'],
                            'longitude': station['longitude'],
                            'distance_km': distance_m
                        }) 

                    distance_to_surrounding_ev_stations.sort(key=lambda x: x['distance_km'])
                    print(f'\n{total_nearby_ev_station} EV Station(s) has been detected from this coordinates: {latitude},{longitude}')
                    print(tabulate(distance_to_surrounding_ev_stations, headers='keys', tablefmt="mixed_outline", showindex=False))

                    while True:
                        try:
                            selected_station_id_input = input("\nPlease input the EV Station's ID that you want to visit: ")
                            selected_station_id = int(selected_station_id_input)

                            surrounding_ev_station_id_list = []
                            for station in surrounding_ev_stations:
                                surrounding_ev_station_id_list.append(station['id'])

                            if selected_station_id in surrounding_ev_station_id_list:
                                for ev_station in ev_station_list:
                                    if ev_station['id'] == selected_station_id:
                                        try:
                                            url = f"https://www.google.com/maps/dir/{latitude},{longitude}/{ev_station['latitude']},{ev_station['longitude']}"
                                            webbrowser.open(url)
                                            print('The route has been generated in your browser.\nReturning to previous menu.')
                                        except:
                                            print('The route is failed to be generated. Please try again.')
                                break
                            else:
                                print(f"\nID {selected_station_id} is not in the surrounding EV Station list. Please input a different EV Station's ID")
                                continue
                        except ValueError:
                            print("\nInvalid input. Please enter a valid EV Station ID.")
                else:
                    print("\nAn error occurred while finding the surrounding EV Stations. Please try again.")
                    continue

            elif menu_5_option == '2':
                latitude, longitude = coordinate_checker_input()

                user_s2cell_id_12 = s2cell.lat_lon_to_cell_id(latitude, longitude, 12)
                user_s2cell_id_12_neighbors = s2cell.cell_id_to_neighbor_cell_ids(user_s2cell_id_12, edge=True, corner=True)
                user_s2cell_id_12_neighbors.append(user_s2cell_id_12)

                manual_location = {
                    'latitude': latitude,
                    'longitude': longitude,
                    's2cell_id_12_neighbors': user_s2cell_id_12_neighbors
                    }
                
                surrounding_ev_stations = []
                for i in ev_station_list:
                    if i['s2cell_id_12'] in manual_location['s2cell_id_12_neighbors']:
                        surrounding_ev_stations.append(i)

                total_nearby_ev_station = nearby_ev_station(surrounding_ev_stations)

                if total_nearby_ev_station == 0:
                    print("\nNo EV Station found around this area.")
                    continue
                elif total_nearby_ev_station > 0:
                    distance_to_surrounding_ev_stations = []
                    for station in surrounding_ev_stations:
                        distance_m = round(distance.distance((latitude, longitude), (station['latitude'], station['longitude'])).km, 3)
                        distance_to_surrounding_ev_stations.append({
                            'id': station['id'],
                            'name': station['name'],
                            # 'address': station['address'],
                            'highest_power': station['highest_power'],
                            'total_chargers': station['total_chargers'],
                            # 'highest_charger_types': station['highest_charger_types'],
                            'latitude': station['latitude'],
                            'longitude': station['longitude'],
                            'distance_km': distance_m
                        })

                    distance_to_surrounding_ev_stations.sort(key=lambda x: x['distance_km'])
                    print(f'\n{total_nearby_ev_station} EV Station(s) has been detected')
                    print(tabulate(distance_to_surrounding_ev_stations, headers='keys', tablefmt="mixed_outline", showindex=False))

                    while True:
                        try:
                            selected_station_id_input = input("\nPlease input the EV Station's ID that you want to visit: ")
                            selected_station_id = int(selected_station_id_input)

                            surrounding_ev_station_id_list = []
                            for station in surrounding_ev_stations:
                                surrounding_ev_station_id_list.append(station['id'])

                            if selected_station_id in surrounding_ev_station_id_list:
                                for ev_station in ev_station_list:
                                    if ev_station['id'] == selected_station_id:
                                        try:
                                            url = f"https://www.google.com/maps/dir/{latitude},{longitude}/{ev_station['latitude']},{ev_station['longitude']}"
                                            webbrowser.open(url)
                                            print('The route has been generated in your browser.\nReturning to previous menu.')
                                        except:
                                            print('The route is failed to be generated. Please try again.')
                                break
                            else:
                                print(f"\nID {selected_station_id} is not in the surrounding EV Station list. Please input a different EV Station's ID")
                                continue
                        except ValueError:
                            print("\nInvalid input. Please enter a valid EV Station ID.")
                else:
                    print("\nAn error occurred while finding the surrounding EV Stations. Please try again.")
                    continue
                
            elif menu_5_option == '3':
                poi_name, poi_latitude, poi_longitude = geocoding()

                user_s2cell_id_12 = s2cell.lat_lon_to_cell_id(poi_latitude, poi_longitude, 12)
                user_s2cell_id_12_neighbors = s2cell.cell_id_to_neighbor_cell_ids(user_s2cell_id_12, edge=True, corner=True)
                user_s2cell_id_12_neighbors.append(user_s2cell_id_12)

                poi_geocode_location = {
                    'latitude': poi_latitude,
                    'longitude': poi_longitude,
                    's2cell_id_12_neighbors': user_s2cell_id_12_neighbors
                            }
                
                surrounding_ev_stations = []
                for i in ev_station_list:
                    if i['s2cell_id_12'] in poi_geocode_location['s2cell_id_12_neighbors']:
                        surrounding_ev_stations.append(i)

                total_nearby_ev_station = nearby_ev_station(surrounding_ev_stations)

                if total_nearby_ev_station == 0:
                    print("\nNo EV Station found around this area.")
                    continue
                elif total_nearby_ev_station > 0:
                    distance_to_surrounding_ev_stations = []
                    for station in surrounding_ev_stations:
                        distance_m = round(distance.distance((poi_latitude, poi_longitude), (station['latitude'], station['longitude'])).km, 3)
                        distance_to_surrounding_ev_stations.append({
                            'id': station['id'],
                            'name': station['name'],
                            # 'address': station['address'],
                            'highest_power': station['highest_power'],
                            'total_chargers': station['total_chargers'],
                            # 'highest_charger_types': station['highest_charger_types'],
                            'latitude': station['latitude'],
                            'longitude': station['longitude'],
                            'distance_km': distance_m
                        })

                    distance_to_surrounding_ev_stations.sort(key=lambda x: x['distance_km'])
                    print(f'\n{total_nearby_ev_station} EV Station(s) has been detected')
                    print(tabulate(distance_to_surrounding_ev_stations, headers='keys', tablefmt="mixed_outline", showindex=False))

                    while True:
                        try:
                            selected_station_id_input = input("\nPlease input the EV Station's ID that you want to visit: ")
                            selected_station_id = int(selected_station_id_input)

                            surrounding_ev_station_id_list = []
                            for station in surrounding_ev_stations:
                                surrounding_ev_station_id_list.append(station['id'])

                            if selected_station_id in surrounding_ev_station_id_list:
                                for ev_station in ev_station_list:
                                    if ev_station['id'] == selected_station_id:
                                        try:
                                            url = f"https://www.google.com/maps/dir/{poi_latitude},{poi_longitude}/{ev_station['latitude']},{ev_station['longitude']}"
                                            webbrowser.open(url)
                                            print(f'The route from {poi_name} has been generated in your browser.\nReturning to previous menu.')
                                        except:
                                            print('The route is failed to be generated. Please try again.')
                                break
                            else:
                                print(f"\nID {selected_station_id} is not in the surrounding EV Station list. Please input a different EV Station's ID")
                                continue
                        except ValueError:
                            print("\nInvalid input. Please enter a valid EV Station ID.")
                else:
                    print("\nAn error occurred while finding the surrounding EV Stations. Please try again.")
                    continue
                
            elif menu_5_option == '4':
                break
            else:
                print(f'\nPlease input the proper menu option (1-4). You have entered: {menu_5_option}')


    # Menu 6 - EXIT
    elif menu_option == '6':
        while True:
            exit_confirm = input("\nAre you sure you want to exit the program? (y/n): ")
            if exit_confirm.lower() == 'y':
                print("\nClosing the program. Goodbye!\n")
                exit()
            elif exit_confirm.lower() == 'n':
                print("\nReturning to main menu.")
                print("---"*30)
                break
            else:
                print(f"\nInvalid input. you have entered: {exit_confirm}")
                continue

    # Others - INCORRECT INPUT
    else:
        print(f'\nPlease input the proper menu option (1-6). You have entered: {menu_option}')
        print("---"*30)