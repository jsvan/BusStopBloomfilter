import random
from bloom_filter2 import BloomFilter
import statistics
import paint
VISUALIZE = True
NUM_PROBES_K = 3

"""
I Want 2 things here:

-- 1> fingerprints on every train

-- 2> fingerprints on every station platform

---- 1.5> metrics on how small to make the trains fingerprints before more than 1% FP

---- 2.5> probability to get FP for standing at the wrong platform


Only 1) and 2) can be engineered for in this class. 

"""


class System:

    def __init__(self, alltrains, allstations, alltimetables, max_bloom_elements=30, failure_rate=0.05):
        self.alltrains = alltrains
        self.allstations = allstations
        self.alltimetables = alltimetables
        self.max_bloom_elements = max_bloom_elements
        self.failure_rate = failure_rate
        # Will be train name : bloom filter
        self.trains = dict()
        # Will be station, track : bloom filter
        self.stationtracks = dict()
        self.canvas = paint.Canvas()

        print(f"City:\nNum routes = {len(alltrains)}\nnum_stops_each = {statistics.mean( (len(x) for x in alltrains.values()))}\ntotal stops = {len(allstations)}")

        # Every Bloom filter must have the same instantiation params
        # But each track on each platform has its own Bloom Filter
        # Along with each train.
        # Each track is the collection of each train.
        # Each train is the collection of each of its stops.
        # Use BF.union(otherBF)

        #{'ICE 618': [8000013, 8000050, 8000080, 8000085, 8000105, 8096021, 8070003, 8000281, 8004158, 8000271, 8000294, 8000096, 8005556, 8000170],
        # 'ICE 616': [8000013, 8004158, 8000294,
        for name, stops in alltrains.items():
            self.trains[name] = self.Train(name, stops, max_bloom_elements=max_bloom_elements, failure_rate=failure_rate)

        #Just grab one for array info
        arraysize, probe_rate = self.trains[name].bloomstops.num_bits_m, self.trains[name].bloomstops.num_probes_k
        print(f"Blooms have {max_bloom_elements} max elements of size {arraysize}, \nand a failure rate of {failure_rate} and {probe_rate} probes\n")
        # {8000013: {'1': ['ICE 618', 'ICE 616', 'ICE 614', 'IC 2366', 'ICE 692', 'TGV 9576', 'ICE 802', 'ICE 612',
        # 'IC 1296', 'ICE 690', 'IC 1298', 'ICE 610'], '4': ['ICE 619', 'NJ 40491', 'NJ 421', 'RJX 63', 'ICE 511'],
        for station, tracks in alltimetables.items():
            self.stationtracks[station] = dict()

            for track, trains in tracks.items():
                self.stationtracks[station][track] = self.Train(f"{allstations[station]} {track}", [], max_bloom_elements=max_bloom_elements, failure_rate=failure_rate)

                # These are all trains arriving to this track
                for trainname in trains:
                    self.stationtracks[station][track].bloomstops.union( self.trains[trainname].bloomstops )


    def bf_has(self, key, bloomfilter):
        for bitno in bloomfilter.probe_bitnoer(bloomfilter, key):
            if not bloomfilter.backend.is_set(bitno):
                return False
        return True


    def test_track_coherence(self, trials):
        passengers = self.passenger(trials, alltrains=self.alltrains)
        passstops = passengers.next()

        for startstation, endstation in passstops:
            waitingtrack = None

            if VISUALIZE:
                passbf = BloomFilter(max_elements=self.max_bloom_elements, error_rate=self.failure_rate)
                passbf.num_probes_k = NUM_PROBES_K
                passbf.add(endstation)
                print("\nPASSENGER TICKET")
                self.canvas.visualizeByteString(passbf, title=f"Passenger Ticket \nfrom \"{self.allstations[startstation]}\" to \"{self.allstations[endstation]}\"")
            showtrack = True
            # Passenger starts at station
            for trackname, trackbloom in random.sample(self.stationtracks[startstation].items(), len(self.stationtracks[startstation])): #jenky shuffle
                if self.bf_has(endstation, trackbloom.bloomstops):
                    #passenger chooses this track to wait
                    waitingtrack = trackname
                    if VISUALIZE:
                        print("\tCORRECT TRACK FILTER")
                        self.canvas.visualizeByteString(trackbloom.bloomstops, title=f"Correct track, which will have the correct train")
                    break
                else:
                    if VISUALIZE and showtrack:
                        print("\tWRONG TRACK FILTER")
                        self.canvas.visualizeByteString(trackbloom.bloomstops, title=f"Wrong track, which will not have the right train")
                        showtrack = False

            if waitingtrack:
                showtrain = True
                for arrivingtrain in self.alltimetables[startstation][waitingtrack]:

                    #if the train has the right fingerprint
                    if self.bf_has(endstation, self.trains[arrivingtrain].bloomstops):
                        if endstation in self.trains[arrivingtrain].liststops:
                            passengers.success()
                            if VISUALIZE:
                                print("\t\tCORRECT TRAIN FILTER")
                                self.canvas.visualizeByteString(self.trains[arrivingtrain].bloomstops, title=f"Correct train, which is going to {self.allstations[endstation]}. Stoplist:\n{', '.join([self.allstations[x] for x in self.trains[arrivingtrain].liststops])}")
                        break
                    else:
                        # WRong train
                        if VISUALIZE and showtrain:
                            print("\t\tWRONG TRAIN FILTER")
                            self.canvas.visualizeByteString(self.trains[arrivingtrain].bloomstops, title=f"Wrong train, which is NOT going to {self.allstations[endstation]}. Stoplist:\n{', '.join([self.allstations[x] for x in self.trains[arrivingtrain].liststops])}")
                            showtrain = False

        print(passengers.accuracy())




        # Passenger finds correct track

        # Passenger finds correct train

        # Passenger sees if train actually takes them to their destination



    def test_train_coherence(self, trials):
        pass #TODO

    def test_trains(self, num_people):
        successes = 0

        for person in range(num_people):
            #success = self.catch_correct_bus()
            successes += 1#success

        return successes / num_people


    class passenger:
        def __init__(self, count, alltrains):
            self.count = count
            self.trials = 0
            self.successes = 0
            self.alltrains = alltrains
            self.trainnames = list(self.alltrains.keys())


        def next(self):
            for p in range(self.count):
                self.trials += 1
                train = random.choice(self.trainnames)

                while len(self.alltrains[train]) < 2:
                    train = random.choice(self.trainnames)

                stops = random.sample(self.alltrains[train], 2)
                yield (stops[0], stops[1])

        def __next__(self):
            return self.next()

        def success(self):
            self.successes += 1

        def accuracy(self):
            print(f"Trials: {self.trials}, Successes: {self.successes}, Accuracy: {self.successes/self.trials}")
            return self.successes / self.trials


    class Train:
        def __init__(self, name, route:list, max_bloom_elements: int, failure_rate: float):
            # adds are deterministic, so two arrays of same definitions will add items to same indices.
            self.liststops = list(route)
            self.name = name
            self.bloomstops = BloomFilter(max_elements = max_bloom_elements, error_rate=failure_rate)
            self.bloomstops.num_probes_k = NUM_PROBES_K
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