import pandas as pd
from sklearn.cluster import KMeans
import mpu
import statistics
import time
from itertools import permutations
from itertools import chain
import keyboard  # using module keyboard
from django.contrib.admin.utils import flatten

# remove individual location
def remove_location(idx):
    df.drop(idx, inplace=True)


# get time covering between two location
def distance_time(lat1, long1, lat2, long2):
    def cal_time(dist, speed):
        return dist / speed

    # Point one
    lat1 = lat1
    lon1 = long1

    # Point two 
    lat2 = lat2
    lon2 = long2

    # What you were looking for
    dist = mpu.haversine_distance((lat1, lon1), (lat2, lon2))
    speed = 10  # 10 km per hour
    outcome = cal_time(round(dist, 3), speed)
    return round(outcome * 60)


def Add_emergency_case(df, label_list, query_lat=28.615595, query_long=77.070784):
    dct1 = {}
    for cluster in label_list:
        rows = df.loc[df['label'] == cluster]
        lat = rows.latitude
        log = rows.longitude
        time_list = []
        for i, j in zip([query_lat], [query_long]):
            for k, l in zip(lat, log):
                time_list.append(distance_time(i, j, k, l))
        avg_time = statistics.mean(time_list)
        dct1[cluster] = avg_time
    result = {k: v for k, v in sorted(dct1.items(), key=lambda item: item[1])}
    result = list(result.keys())[0]
    return result


def routing(df, final_list):
    print("Press Spacebar for Emergency")
    print("Press q to stop the loop before 10 hours are complete")
    terminate = True  # variable to check end of loop
    # print(final_list)
    current_loc = {}
    no_of_hours = 0
    tech_id = ""  # technician id
    while terminate:
        x = 0
        for dictionary in final_list:  # traversing final dictionary
            x += 1
            # print(list(dictionary))
            for dictionary2 in list(dictionary.values())[0].values():  # accessing specific location
                if len(dictionary2) > 0:
                    if flatten(dictionary.keys())[0] == tech_id:  # checking if emergency case was resolved
                        print("Your emergency was resolved")
                        time.sleep(1)
                        tech_id = ""
                    print(f"worker no.{x} is at:")
                    print(get_area(df, [dictionary2[0], dictionary2[1]]))
                    if keyboard.is_pressed('q'):  # if key 'q' is pressed and kept
                        terminate = False
                        print("All jobs completed")
                    # print(dictionary2[0], ",", dictionary2[1])
                    time.sleep(1)
                    current_loc[flatten(dictionary.keys())[0]] = [dictionary2[0], dictionary2[
                        1]]  # appending the current location of each technician
                    del dictionary2[0]
                    del dictionary2[0]
            # making a loop
            if keyboard.is_pressed('space'):  # if key 'space' is pressed and kept
                print('Enter your Emergency:')
                lat2 = float(input("enter the latitude of the emergency"))  # taking emergency input from user
                long2 = float(input("enter the longtitude of the emergency"))  # taking emergency input from user
                time.sleep(1)
                print("We will resolve the emergency case found at:")
                print(get_area(df, [lat2, long2]))  # getting location of emergency
                time.sleep(1)
                dist_from_emergency = []
                for location in (list(current_loc.values())):
                    lat1 = float(location[0])
                    long1 = float(location[1])
                    dist_from_emergency.append(distance_time(lat1, long1, lat2,
                                                             long2))  # calculating distance of each technician from emergency point
                closest = min(dist_from_emergency)  # finding closest technician to emergency
                index = dist_from_emergency.index(closest)
                tech_id = (flatten(current_loc.keys())[index])
                print(
                    f"Your problem lies in {tech_id}, Technican {index + 1} is heading to the location")  # assigning technician to emergency at needed Area
                time.sleep(1)
                for arr in final_list:
                    if flatten(arr.keys())[0] == tech_id:
                        key = flatten(flatten(arr.values())[0].keys())[0]
                        initial_list = flatten(arr.values())[0][key]
                        if len(initial_list) == 0:  # checking if all jobs are completed for closest technician
                            initial_list.insert(0, lat2)  # adding emergency latitude
                            initial_list.insert(1, long2)  # adding emeregency longtitude
                            flatten(arr.values())[0][key] = initial_list
                        else:
                            initial_list.insert(2, lat2)  # adding emergency latitude
                            initial_list.insert(3, long2)  # adding emeregency longtitude
                            flatten(arr.values())[0][key] = initial_list
                        # print(initial_list)
                continue
        # finishing  the loop
        time.sleep(2)
        no_of_hours += 1  # appending number of hours completed
        # print(final_list)
        print(f"{no_of_hours} hours passed")
        print("Jobs completed for these hours")
        if keyboard.is_pressed('q'):  # if key 'q' is pressed and kept
            terminate = False
            print("All jobs completed")
        if no_of_hours > 9:  # if all jobs are completed
            terminate = False
            print("All jobs completed")


def get_area(df, list_of_ids):
    place_id = ''
    for lt, lg, place in zip(df.latitude, df.longitude, df.Venue):
        if place_id == '':
            place_id = f'{list_of_ids[0]},{list_of_ids[1]}'
        if list_of_ids[0] == lt and list_of_ids[1] == lg:
            place_id = place
    return place_id


if __name__ == '__main__':
    # load dataset
    df = pd.read_excel("final.xlsx")  # reading dataset
    # drop duplicates
    df.drop_duplicates(subset=['latitude', 'longitude'], inplace=True, ignore_index=True)  # dropping duplicate values
    df = df.loc[df.latitude > 28.45]  # Removing outlier

    # get the clusters area for each technician using kmean
    coor = df[["latitude", "longitude"]].values
    kmeans = KMeans(n_clusters=round(len(df) / 10))  # number of working hours for per technician #default 10 hour a day working time
    label = kmeans.fit_predict(coor)
    df['label'] = label

    # get list of lables
    df.label = df.label.apply(lambda x: "Area_" + str(x))

    # list of unique clusters
    label_list = list(df.label.unique())

    # make list for storing final data
    location_list = []
    time_list = []
    time_taken = {}
    possible_routes = []
    count = 0
    final_list = []
    # main function
    location_list = []
    time_list = []
    time_taken = {}
    possible_routes = []
    count = 0 
    final_list = []
    for label in label_list:
        df1 = df.loc[df['label'] == f'{label}']
        list_of_lat = df1['latitude'].to_list()  # converting latitude to list
        list_of_long = df1['longitude'].to_list()  # converting longtitude to list
        if len(list_of_long) < 7:  # limiting maximum number of hours to 10
            for i, j in zip(list_of_lat, list_of_long):
                location_list.append([i, j])
                possible_routes1 = list(permutations(location_list))#finding all permutations for the routes for each technician
            for value in possible_routes1:
                possible_routes.append(list(chain(*value)))
            for routes in possible_routes:
                route_time = 0
                for i in range(0, len(routes), 2):
                    if i + 3 <= (len(routes) - 1):
                        pt1 = [routes[i], routes[i + 1]]
                        pt2 = [routes[i + 2], routes[i + 3]]
                        time_d = distance_time(pt1[0], pt1[1], pt2[0], pt2[1])#finding the time for each permutation of each technician
                        time_list.append(time_d)
                time_taken[f"{sum(time_list)}"] = routes#summing up the total time for each technician route
                # print(time_taken)
                time_list = []
                # print(time_taken)
                # print(time_taken.keys())
            min_time = min(time_taken.keys())#finding the minimum time for each technicain to complete their route
            dict = {f"{label}": {min_time: time_taken[min_time]}}#creating a dict to store all values of each technicain along with their shortest route
            final_list.append(dict)#adding the dictionary of each technicain along with their shortest route to a list
            # possible_routes=[]
            # location_list=[]
            time_taken = {}
            # print(dict)
            possible_routes = []
            location_list = []

    routing(df, final_list)#running the routing and emergency function inside it
