import spacy
import pyap
from geopy.geocoders import Nominatim
from nlp.locationlist import find_towns_in_text_seriel
import nltk
from nltk.corpus import words, brown

# nltk.download('words')
# nltk.download('brown')


# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Initialize the geocoder
geolocator = Nominatim(user_agent="myGeocoder")


def extract_addresses_with_geocoding(text):
    # Use spaCy to find entities in the text
    doc = nlp(text)

    # Extract addresses using the pyap library with the country set to "US"
    addresses = pyap.parse(text, country="US")

    # Extract addresses from spaCy entities
    for entity in doc.ents:
        if entity.label_ == "GPE" or entity.label_ == "ORG":
            addresses.append(entity.text)

    # Remove duplicates from the address list
    new_addresses = find_towns_in_text_seriel(text)

    # print("new_addresses------------------", new_addresses)

    # print("addresses------------------", addresses)

    addresses.extend(new_addresses)

    addresses = [address.lower() for address in addresses]

    addresses = list(set(addresses))
    addresses = remove_known_words(addresses)

    # print("addresses------------------", addresses)

    # Geocode the addresses
    geocoded_addresses = {}
    for address in addresses:
        try:
            location = geolocator.geocode(address)
            if location:
                geocoded_addresses[address] = (
                    location.latitude, location.longitude)
        except Exception as e:
            print(f"Error geocoding address '{address}': {e}")

    return geocoded_addresses

# sample_text = """The White House is located at 1600 Pennsylvania Avenue NW, Washington, DC, 20500"""
# print(extract_addresses_with_geocoding(sample_text))


def remove_known_words(input_list):
    english_words = set(words.words())
    common_nouns = set(brown.words(categories='news'))
    all_known_words = english_words.union(common_nouns)
    filtered_list = [word for word in input_list if word.lower()
                     not in all_known_words]
    return filtered_list
