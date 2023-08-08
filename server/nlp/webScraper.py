from newspaper import Article

from nlp.findlocations import extract_addresses_with_geocoding
from nlp.findcatogory import identify_catogory
from nlp.findprice import identify_price
from nlp.findcontacts import extract_contacts

import spacy

# spacy.cli.download("en_core_web_sm")

# ____________________nlp = spacy.load('en_core_web_sm')

# import nltk
# nltk.download('vader_lexicon')


def extract_article_info(url):
    # Create an Article object
    article = Article(url, language="en")  # en for English

    # To download the article
    article.download()

    # To parse the article
    article.parse()

    # To perform natural language processing (NLP)
    article.nlp()

    # Extract title
    title = article.title

    # Extract text
    text = article.text

    # Extract summary
    summary = article.summary

    # Extract keywords
    keywords = article.keywords

    # ent_list = []
    # doc = nlp(text)
    # for ent in doc.ents:
    #     if (ent.label_ == 'PERSON' or ent.label_ == 'DATE') and ent.text not in [item[0] for item in ent_list]:
    #         ent_list.append((ent.text, ent.label_))

    locations = extract_addresses_with_geocoding(text)
    catogory = identify_catogory(text)
    price = identify_price(text)
    contact = extract_contacts(text)

    return title, text, summary, keywords, catogory, price, contact, locations
    return summary, title, text, keywords, ent_list, locations, catogory, price, contact
