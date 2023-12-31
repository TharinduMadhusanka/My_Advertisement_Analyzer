import ahocorasick
import pickle

# Generator function to read cities from the file one by one
def cities_generator(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()

# Initialize Aho-Corasick automaton and save it if not already saved
def initialize_automaton(filename, save_filename):
    if not hasattr(initialize_automaton, 'automaton'):
        try:
            with open(save_filename, 'rb') as f:
                automaton = pickle.load(f)
        except (FileNotFoundError, pickle.UnpicklingError):
            automaton = ahocorasick.Automaton()
            for city in cities_generator(filename):
                automaton.add_word(city, city)
            automaton.make_automaton()
            with open(save_filename, 'wb') as f:
                pickle.dump(automaton, f)
        initialize_automaton.automaton = automaton
    return initialize_automaton.automaton

# Given text
given_text = "This is a text containing some city names like Ampara, Kalmunai, etc."

# Get the automaton (initialize if not already initialized)
automaton = initialize_automaton('cities.txt', 'automaton.pkl')

# Find matching cities using the Aho-Corasick automaton
matching_cities = set()
for _, city in automaton.iter(given_text):
    matching_cities.add(city)

# Print the matching cities
print("Cities found in the given text:")
for city in matching_cities:
    print(city)
