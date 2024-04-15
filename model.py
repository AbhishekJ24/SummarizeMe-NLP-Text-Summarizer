from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import nltk
from collections import Counter
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud
import string

nltk.download('stopwords')
nltk.download('punkt')

class SummarizerModule:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
    
    def calculate_sentence_scores(self, sentences, word_frequencies):
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores:
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        return sentence_scores

    def generate_summary(self, text, num_sentences):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        word_frequencies = {}
        for word in words:
            if word not in stop_words:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequency = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word] / maximum_frequency

        sentences = sent_tokenize(text)
        sentence_scores = self.calculate_sentence_scores(sentences, word_frequencies)
        summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        return summary
    
    def extract_keywords(self, text, num_keywords=5):
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        filtered_words = [word for word in words if word not in stop_words and word not in string.punctuation]
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in filtered_words]
        word_freq = Counter(lemmatized_words)
        keywords = [word for word, _ in word_freq.most_common(num_keywords)]
        return keywords
    
    def save_word_cloud(self, keywords):
        keywords_str = ' '.join(keywords)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(keywords_str)
        wordcloud.to_file("/Users/gamingspectrum24/Documents/University Coursework/6th Semester/Natural Language Processing/SummarizeMe-NLP-Text-Summarizer/static/images/wordcloud.png")

