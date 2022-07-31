# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Chicago has almost 2000 buses
# 150 bus routes
# 12,000 bus stops
# 10 train lines
# max 50 stops / bus
# 150 train stations
import sys
import cityplan
import paint
# city = cityplan.City(num_bus_routes=150, num_stops_each=50, stops_in_city=12000, max_stops=104)
# print(f"{city.test_city(100000)} success rate")

city = cityplan.City(num_bus_routes=2000, num_stops_each=15, stops_in_city=2000, max_bloom_elements=50)
print(f"{city.test_city(10000)} success rate")


sys.exit()

# Show bit array total for a bus.
# The last line has 27 leading 0's (final 5 good)
# 997 bytes
print('\n'.join((format(x, '#034b')[2:] for x in city.mybusses[-1].bloomstops.backend.array_)))
bitstring = ''.join((format(x, '#034b')[2:] for x in city.mybusses[-1].bloomstops.backend.array_))
#ending = bitstring[-5:]
#bitstring = bitstring[:-32] + ending
print(bitstring)
print(len(bitstring))

not_existing_route = list(city.validstops)[-1]
mynotstop = cityplan.Bus(route=[not_existing_route] , max_bloom_elements=40)
print("Not Looking for stop: ", mynotstop.liststops)
#num_stops_each=30, stops_in_city=500, max_bloom_elements=40)

existing_route = list(city.mybusses[-1].liststops)[-1]
mystop = cityplan.Bus(route=[existing_route] , max_bloom_elements=40)
print("Looking for stop: ", mystop.liststops)
print("in", city.mybusses[-1].liststops )


c = paint.Canvas()
c.visualizeByteString(''.join((format(x, '#034b')[2:] for x in mynotstop.bloomstops.backend.array_)))
c.visualizeByteString(''.join((format(x, '#034b')[2:] for x in mystop.bloomstops.backend.array_)))
c.visualizeByteString(bitstring, allLetters=True)