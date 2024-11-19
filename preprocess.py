import nltk # type: ignore
from nltk.corpus import stopwords # type: ignore
from nltk.tokenize import word_tokenize # type: ignore
from nltk.stem import WordNetLemmatizer # type: ignore
from nltk import pos_tag, ne_chunk # type: ignore
import openai # type: ignore
import numpy as np
from dotenv import load_dotenv # type: ignore
import os
import py3langid # type: ignore

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def preprocess_text(text, language):
    words = word_tokenize(text)
    
    if language == "en":
        stop_words = set(stopwords.words("english"))
    elif language == "fr":
        stop_words = set(stopwords.words("french"))
    else:
        stop_words = set()
    
    filtered_words = [word for word in words if word.lower() not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
    
    return ' '.join(lemmatized_words)

def extract_entities(text):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    
    chunks = ne_chunk(pos_tags)
    
    entities = []
    for chunk in chunks:
        if hasattr(chunk, 'label'):
            entity = ' '.join(c[0] for c in chunk)
            entity_label = chunk.label()
            entities.append({
                "entity": entity_label,
                "value": entity
            })
    return entities

def get_openai_embedding(text, language):
    if language == "fr":
        prompt = f"Please respond in French: {text}"
    else:
        prompt = f"Please respond in English: {text}"
    
    response = openai.Embedding.create(
        input=prompt,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_most_similar_intent(input_text, training_data, language):
    input_embedding = get_openai_embedding(preprocess_text(input_text, language), language)
    similarities = []
    for example in training_data.training_examples:
        intent = example.get("intent")
        text = example.get("text")
        text_embedding = get_openai_embedding(preprocess_text(text, language), language)
        similarity = cosine_similarity(input_embedding, text_embedding)
        similarities.append((intent, similarity))
    most_similar_intent, max_similarity = max(similarities, key=lambda x: x[1])
    return most_similar_intent, max_similarity

def detect_language(text):
    lang, _ = py3langid.classify(text)
    return lang