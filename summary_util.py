import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

class SummaryUtil:

    def __init__(self):
        self.stopwords = list(STOP_WORDS)
        self.punctuation = punctuation + '\n'

    
    # lower the cut off, shorter the result
    def start_summarization(self, content, size_percent):
        processed_text = self.__nlp_process(content)
        get_normalized_word_freq = self.__normalize_word_frequency(processed_text)
        sentence_importance_scores = self.__sentence_importance_scores(get_normalized_word_freq,processed_text)

        final_summary = self.__get_summary(sentence_importance_scores,size_percent)
        return final_summary

    #the content pass through spacy nlp pipeline 
    #
    def __nlp_process(self,content):
        nlp = spacy.load('en_core_web_sm')
        processed_text = nlp(content)
        
        return processed_text

    # each word frequency is recorded
    # normalize by dividing each word freq with max freq
    def __normalize_word_frequency(self,processed_text):
        word_freq = {}
        
        for word in processed_text:
            if word.text.lower() not in self.stopwords:
                if word.text.lower() not in self.punctuation:
                    if word.text not in word_freq.keys():
                        word_freq[word.text] = 1

                    else:
                        word_freq[word.text] += 1

        max_freq = max(word_freq.values())

        #normalze each word frequency based on max freq
        for word in word_freq.keys():
            word_freq[word] = word_freq[word]/max_freq

        return word_freq


    #for each sentence, for each word in the sentence, 
    # sum the total normalized values per word freq.
    # result is the score to each sentence importance.
    # higher the score, more impt the sentence
    def __sentence_importance_scores(self,word_freq, processed_text):
        sentence_tokens = [sentence for sentence in processed_text.sents]
        sentence_scores = {}

        for sentence in sentence_tokens:
            for word in sentence:
                if word.text.lower() in word_freq.keys():
                    if sentence not in sentence_scores.keys():
                        sentence_scores[sentence] = word_freq[word.text.lower()]
                    else:
                        sentence_scores[sentence] += word_freq[word.text.lower()]

        return sentence_scores


    def __get_summary(self,sentence_scores,size_percent):
        cut_off = int(len(sentence_scores)*size_percent) # get the top size_percent. 
        impt_content = nlargest(cut_off,sentence_scores, key=sentence_scores.get)

        final_summary = [sentence.text for sentence in impt_content]
        final_summary = ''.join(final_summary)

        return final_summary