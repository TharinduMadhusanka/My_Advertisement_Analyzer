import re
import multiprocessing
from fuzzywuzzy import fuzz
import nltk
from nltk.tokenize import sent_tokenize

# nltk.download('punkt')

town_set = {'Chilaw', 'Galigamuwa', 'Rideegama', 'Udubaddawa', 'Akkarepattu', 'Nachchadoowa', 'Hatton', 'Koralai Pattu North', 'Thamankaduwa', 'Kundasale', 'Colombo 14', 'Kadawatha', 'Badulla', 'Ratnapura', 'Mundalama', 'Kiriella', 'Pelmadulla', 'Sainthamaruthu', 'Kotapola', 'Wellawaya', 'Mahiyanganaya', 'Malabe', 'Udadumbara', 'Pallepola', 'Angoda', 'Kotte', 'Maritimepattu', 'Wattegama', 'Anamaduwa', 'Moneragala', 'Mulatiyana', 'Colombo 2', 'Ingiriya', 'Kekanadurra', 'Ella', 'Athurugiriya', 'Buttala', 'Rambewa', 'Galagedara', 'Manmunai North', 'Ampara', 'Galewela', 'Akmeemana', 'Wilgamuwa', 'Thawalama', 'Ganemulla', 'Valikamam West', 'Manmunai South and Eruvilpattu', 'Nochchiyagama', 'Kalutara', 'Marawila', 'Island South (Velanai)', 'Colombo 15', 'Thalawa', 'Colombo 6', 'Eravur Town', 'Colombo 4', 'Ambagamuwa', 'Batticaloa', 'Walapane', 'Veyangoda', 'Medawachchiya', 'Welimada', 'Mahara', 'Boralesgamuwa', 'Peradeniya', 'Eravur Pattu', 'Pathadumbara', 'Mount Lavinia', 'Godagama', 'Hikkaduwa', 'Matugama', 'Kohuwala', 'Akkaraipattu', 'Kalpitiya', 'Colombo 12', 'Pasbage Korale', 'Valikamam North', 'Kinniya', 'Thanamalvila', 'Mahakumbukkadawala', 'Alayadiwembu', 'Kobeigane', 'Kothmale', 'Welikanda', 'Kalmunai', 'Naula', 'Batapola', 'Dimbulagala', 'Kuchchaveli', 'Nugegoda', 'Valikamam South-West', 'Uva Paranagama', 'Rajagiriya', 'K.F.G. & G. Korale', 'Kekirawa', 'Colombo 3', 'Mannar Town', 'Udapalatha', 'Matale', 'Mahawewa', 'Ambalanthota', 'Tambuttegama', 'N. Palatha East', 'Weerambugedara', 'Beliatta', 'Narammala', 'Bope-Poddala', 'Jaffna', 'Karandeniya', 'Colombo 8', 'Walallawita', 'Bandaragama', 'Kalawana', 'Palapathwela', 'Madulla', 'Trincomalee', 'Minipe', 'Seeduwa', 'Passara', 'Niyagama', 'Tangalla', 'Galenbindunuwewa', 'Thambuttegama', 'Malimbada', 'Wellampitiya', 'Alutgama', 'Eheliyagoda', 'Polgahawela', 'Chavakachcheri', 'Beruwala', 'Negombo', 'Opanayaka', 'Baddegama', 'Mirigama', 'Hingurakgoda', 'Balangoda', 'Ganga Ihala Korale', 'Pannala', 'Vadamaradchi South-West', 'Kiribathgoda', 'Tissamaharama', 'Samanthurai', 'Sigiriya', 'Welivitiya-Divithura', 'Kamburupitiya', 'Madhu', 'Madawala Bazaar', 'Hanguranketha', 'Haputale', 'Dodangoda', 'Nagoda', 'Kamburugamuwa', 'Mathugama', 'Gandara', 'Katharagama', 'Gelioya', 'Colombo 5', 'Valikamam East', 'Battaramulla', 'Dehiowita', 'Dankotuwa', 'Hatharaliyadda', 'Kesbewa', 'Lunugala', 'Siyambalanduwa', 'Unawatuna', 'Meegahakivula', 'Anuradhapura', 'Mirissa', 'Dehiattakandiya', 'Wadduwa', 'Manthai West', 'Hambantota', 'Mullativu', 'Nanaddan', 'Mawanella', 'Sevanagala', 'Kandy', 'Kaduruwela', 'Thenmaradchy (Chavakachcheri)', 'Ambanganga Korale', 'Vavuniya North', 'Ahangama',
            'Karachchi', 'Damana', 'Akurana', 'Dompe', 'Bandarawela', 'Imbulpe', 'Colombo 11', 'Ninthavur', 'Kolonnawa', 'Lunugamvehera', 'Hanwella', 'Alawwa', 'Dikwella', 'Wariyapola', 'Kataragama', 'Maspotha', 'Homagama', 'Wattala', 'Sainthamarathu', 'N. Palatha Central', 'Karuwalagaswewa', 'Diyatalawa', 'Tangalle', 'Ratmalana', 'Yatawatta', 'Minuwangoda', 'Biyagama', 'Delthota', 'Pothuvil', 'Pachchilaipalli', 'Attanagalla', 'Puttalam', 'Ukuwela', 'Palugaswewa', 'Polpithigama', 'Matara', 'Monaragala', 'Colombo 10', 'Talawatugoda', 'Dambulla', 'Katuwana', 'Bulathsinhala', 'Piliyandala', 'Bentota', 'Digana', 'Laggala-Pallegama', 'Thissamaharama', 'Arachchikattuwa PS', 'Kegalle', 'Hali-Ela', 'Trincomalee Town and Gravets', 'Colombo 9', 'Millaniya', 'Ambalangoda', 'Kadugannawa', 'Divulapitiya', 'Padukka', 'Rambukkana', 'Madurawala', 'Soranathota', 'Welipitiya', 'Colombo 7', 'Ja-Ela', 'Imaduwa', 'Uhana', 'Ganewatta', 'Polonnaruwa', 'Nawalapitiya', 'Vavuniya', 'Mahawa', 'Palagala', 'Galgamuwa', 'Eppawala', 'Madampe', 'Ginigathhena', 'Rajanganaya', 'Colombo 1', 'Habaraduwa', 'Ambanpola', 'Moratuwa', 'Yatinuwara', 'Valikamam South', 'Katunayake', 'Addalachchenai', 'Gampaha', 'Pathahewaheta', 'Karapitiya', 'Horana', 'Weligepola', 'Vanathavilluwa', 'Galnewa', 'Udunuwara', 'Neluwa', 'Giribawa', 'Habarana', 'Kuruwita', 'Medirigiriya', 'Bulathkohupitiya', 'Kottawa', 'Ruwanwella', 'Kitulgala', 'Agalawatta', 'Ragama', 'Pallama', 'Colombo 13', 'Vadamaradchy North', 'Angunakolapelessa', 'Poojapitiya', 'Avissawella', 'Elpitiya', 'Palindanuwara', 'Balapitiya', 'Nattandiya', 'Pitabeddara', 'Sooriyawewa', 'Matara Four Gravets', 'Thirappane', 'Sri Jayawardanapura Kotte', 'Meegoda', 'Mihinthale', 'Warakapola', 'Godakawela', 'Mannar', 'Thumpane', 'Elahera', 'Nittambuwa', 'Gampola', 'Nallur', 'Weeraketiya', 'Mahaoya', 'Harispattuwa', 'Kahawatta', 'Nikaweratiya', 'Bibile', 'Delgoda', 'Panadura', 'Delft', 'Kolonna', 'Kilinochchi', 'Ampitiya', 'Rattota', 'Panvila', 'Ipalogama', 'Hali Ela', 'Colombo', 'Hakmana', 'Medadumbara', 'Ibbagamuwa', 'Pilimatalawa', 'Mihintale', 'Yatiyantota', 'Dehiovita', 'Deniyaya', 'Kaduwela', 'Hildummulla', 'Katugastota', 'Deraniyagala', 'Pannipitiya', 'Kandana', 'Nuwara Eliya', 'Thampalakamam', 'Nawala', 'Akuressa', 'Maharagama', 'Kurunegala', 'Lankapura', 'Nivithigala', 'Thihagoda', 'Lahugala', 'Talawa', 'Kuliyapitiya West', 'Wennappuwa', 'Ambalantota', 'Dehiwala', 'Galle', 'Embilipitiya', 'Dickwella', 'Devinuwara', 'Mallawapitiya', 'Kuruvita', 'Menikhinna', 'Yakkalamulla', 'Medagama', 'Ayagama', 'Koralai Pattu (Valachchenai)', 'Kelaniya', 'Doluwa', 'Weligama', 'Panduwasnuwara', 'Mawathagama', 'Yatiyanthota'}


def find_towns_in_chunk(chunk, town_set):
    found_towns = set()
    # Use regex to extract words from the chunk
    words = re.findall(r'\b\w+\b', chunk.lower())

    for word in words:
        # Exact matching
        if word in town_set and len(word) > 3:
            found_towns.add(word)
        # Fuzzy matching (using fuzzywuzzy library)
        elif any(fuzz.partial_ratio(word, town) >= 60 for town in town_set) and len(word) > 3:
            found_towns.add(word)

    return list(found_towns)


def find_towns_in_text_parallel(text, town_set=town_set, num_processes=2):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    if len(sentences) < num_processes:
        num_processes = 1

    chunk_size = len(sentences) // num_processes

    chunks = [sentences[i:i + chunk_size]
              for i in range(0, len(sentences), chunk_size)]

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.starmap(find_towns_in_chunk, [
            (' '.join(chunk), town_set) for chunk in chunks
        ])

    # Combine the results from all processes
    found_towns = set()
    for result in results:
        found_towns.update(result)

    return list(found_towns)

def find_towns_in_text_seriel(text, town_set=town_set):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)

    chunk_size = len(sentences)

    if chunk_size == 0:
        return []

    chunks = [sentences[i:i + chunk_size]
              for i in range(0, len(sentences), chunk_size)]

    found_towns = set()
    for chunk in chunks:
        found_towns.update(find_towns_in_chunk(' '.join(chunk), town_set))

    return list(found_towns)