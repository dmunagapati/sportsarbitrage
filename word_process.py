from fuzzywuzzy import process
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
def select_word(word_list, input_word):
    # Tokenize input word and remove stopwords
    input_tokens = set(word_tokenize(input_word.lower())) - set(stopwords.words("english"))

    # Custom scorer function based on word similarity
    def word_similarity(s1, s2):
        s1_tokens = set(word_tokenize(s1.lower())) - set(stopwords.words("english"))
        s2_tokens = set(word_tokenize(s2.lower())) - set(stopwords.words("english"))

        common_tokens = len(input_tokens.intersection(s1_tokens).union(input_tokens.intersection(s2_tokens)))
        total_tokens = len(input_tokens.union(s1_tokens).union(s2_tokens))

        similarity_ratio = common_tokens / total_tokens
        return int(similarity_ratio * 100)

    # Use the process module with the custom scorer
    ans = process.extractOne(input_word, word_list, scorer=word_similarity)
    if ans:
        best_match, score = ans
        return (best_match, score)
    
