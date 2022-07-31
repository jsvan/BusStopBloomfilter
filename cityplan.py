import random
from bloom_filter2 import BloomFilter


class City:

    def __init__(self, num_bus_routes=100, num_stops_each = 30, stops_in_city=500, max_bloom_elements=100):
        self.mybusses = []
        self.validstops = set()
        print(f"City:\nNum routes = {num_bus_routes}\nnum_stops_each = {num_stops_each}\ntotal stops = {stops_in_city}")

        for i in range(num_bus_routes):
            stops = random.sample(range(stops_in_city), num_stops_each)
            self.mybusses.append(Bus(stops, max_bloom_elements, 0.01))
            self.validstops.update(stops)

        self.validstops = list(self.validstops)
        arraysize = self.mybusses[-1].getarrayinfo()
        print(f"Busses have {max_bloom_elements} max elements of size {arraysize}, and a failure rate of 0.01\n")


    # Try catching a random bus, return TRUE if correct caught, FALSE if on wrong bus
    def catch_correct_bus(self):
        mydestination = random.choice(self.validstops)

        while True:
            nextbus = random.choice(self.mybusses)

            if nextbus.bloomhas(mydestination):
                return nextbus.listhas(mydestination)
            else:
                # wait for next bus
                pass


    def test_city(self, num_people):
        successes = 0

        for person in range(num_people):
            success = self.catch_correct_bus()
            successes += success

        return successes / num_people



class Bus:

    def __init__(self, route:list, max_bloom_elements:int = 12000, failure_rate:float = 0.01):
        # adds are deterministic, so two arrays of same definitions will add items to same indices.
        self.liststops = list(route)
        self.bloomstops = BloomFilter(max_elements = max_bloom_elements, error_rate=failure_rate)
        self.bloomstops.num_probes_k = 4
        for r in route:
            self.bloomstops.add(r)

    def bloomhas(self, stop):
        return stop in self.bloomstops

    def listhas(self, stop):
        return stop in self.liststops

    def getarrayinfo(self):
        return self.bloomstops.num_bits_m

    def paintbus(self):
        return 0