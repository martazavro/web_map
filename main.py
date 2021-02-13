'''
Module for task 2 lab 2
'''

import folium
from geopy.geocoders import Nominatim
import geopy.distance as geo
from geopy.extra.rate_limiter import RateLimiter


def inputed():
    '''
    Returns inputed by user information about year and coordinates
    '''
    year = input("Please enter a year you would like to have a map for: ")

    coordinates = input('Please enter your location (format: lat, long): ')
    coordinates = coordinates.split(', ')
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])

    print("Map is generating...")
    print('Please wait...')
    return (year, latitude, longitude)


def read_file(my_file, year):
    '''
    Reads file and return a dictionary of films, produced in current year
    '''
    this_file = open(my_file, "r")

    data = this_file.readlines()
    data = data[16:10000]
    content = []
    for row in data:
        row = row.split('"')
        row = row[1:]
        try:
            row[1] = list(row[1].split('\t'))
            row[1] = list(filter(lambda a: a != '', row[1]))
            row[1][0] = row[1][0][2:6]
            row[1][-1] = row[1][-1][:-1]

            if row[1][-1][0] == '(':
                row[1] = row[1][0:-1]
            if row[1][-1][0] == '(':
                row[1] = row[1][0:-1]

            if row[-1][0] == year:
                if '-' in row[1][-1]:
                    row[1][-1] = row[1][-1][row[1][-1].index('-')+2:]
                if 'Federal' not in row[-1][-1]:
                    content.append(row)
        except:
            IndexError

    dictionary = {}
    dictionary = dict(dictionary)
    for i in content:
        i[1].insert(0, i[0])
        dictionary[i[0]] = i[1]

    return dictionary


def get_coordinates(address):
    '''
    Returns coordinates of given address
    '''

    geolocator = Nominatim(user_agent="marta")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(address)

    coords = (location.latitude, location.longitude)

    return coords


def find_closest_coordinates(latitude, longitude, year):
    '''
    Returns information about 10 closest to user points
    '''

    my_coordinates = (latitude, longitude)
    dictionary = read_file('locations.list', year)
    addresses = dictionary.values()
    distances = []
    for address in addresses:
        try:
            coords = get_coordinates(address[-1])

            distance = geo.geodesic(my_coordinates, coords).km
            distances.append((distance, address))
        except:
            AttributeError
    coords_dict = {}
    for i in distances:
        coords_dict[i[0]] = i[1]

    coords_lst = sorted(coords_dict)
    coords_lst = coords_lst[0:10]

    listt = []
    # try:
    for i in coords_dict:
        if i in coords_lst:
            listt.append(coords_dict[i])

    return listt


def map(list_of_films, latitude, longitude, year):
    '''
    Creates a map with markers on film places, user's location and the best
    city
    '''

    map = folium.Map(location=[latitude, longitude], zoom_start=5)
    fg_films = folium.FeatureGroup(name='Films')
    for point in list_of_films:
        coordinates = get_coordinates(point[-1])
        text = 'Movie: '+point[0]+'\n Year: '+point[1]+'\n Place: '+point[2]
        fg_films.add_child(folium.Marker(
            location=[coordinates[0], coordinates[1]], popup=text,\
                 icon=folium.Icon()))
        map.add_child(fg_films)

    fg_city = folium.FeatureGroup(name='The best city!')
    fg_city.add_child(folium.Marker(
        location=[49.74510468600286, 25.61534401122421], popup='Best city!', \
            icon=folium.Icon(color='purple')))
    map.add_child(fg_city)

    fg_location = folium.FeatureGroup(name='Your location')
    fg_location.add_child(folium.Marker(
        location=[latitude, longitude], popup='You are here!',\
             icon=folium.Icon(color='red')))
    map.add_child(fg_location)
    map.add_child(folium.LayerControl())
    map.save(year+'_movies_map.html')

    return ''


def main():
    '''
    Unites all functions and starts the work of module
    '''
    data = inputed()
    year = data[0]
    latitude = data[1]
    longitude = data[2]
    list_of_points = find_closest_coordinates(latitude, longitude, year)
    map(list_of_points, latitude, longitude, year)

    return 'Finished. Please have look at the map '+year+'_movies_map.html'


if __name__ == "__main__":
    print(main())
