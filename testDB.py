import deutschebahn
import pickle

with open('./pickles/allstations.pkl', 'rb') as F:
    allstations = pickle.load(F)

with open('./pickles/alltimetables.pkl', 'rb') as F:
    alltimetables = pickle.load(F)

with open('./pickles/alltrains.pkl', 'rb') as F:
    alltrains = pickle.load(F)

germany = deutschebahn.System(alltrains, allstations, alltimetables, max_bloom_elements=30, failure_rate=0.01)
germany.test_track_coherence(1000)
