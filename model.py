from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import nltk

nltk.download('stopwords')
nltk.download('punkt')

class SummarizerModule:
    def __init__(self):
        pass
    
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