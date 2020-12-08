import numpy as np
import nltk
import re


class Features:
    """
    The class :class:`Features` represents the base class for all
    feature extractions.
    """
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_list = []
        self.tokens = []
        self.documents = self.corpus.keys()

        self.word_tree = None
        self.feature_matrix = None
        self.binary_feature_matrix = None

        self.initialize()

    def initialize(self):
        self.feature_matrix = self.generate()
        self.binary_feature_matrix = self.generate(binary=True)

    def generate_tree_representation(self):
        """
        This helper function returns a tree like representation of a given
        corpus by generating a nested dictionary.

        :return: Nested dictionary, with the token as first key,
                the document as 2nd key
                and the token count as value of the 2nd key.

                Structure:
                    {Token: {Doc_ID: value_count}
                Example:
                    {"This": {0: 1}}
        """

        token_dict = {}

        # Necessary to avoid multiple appends with multiple function calls
        self.corpus_list = []

        for idx_doc, (doc, val_list) in enumerate(self.corpus.items()):
            doc_text = val_list[0][0]
            self.corpus_list.append(doc_text)
            tokens = nltk.word_tokenize(doc_text)
            self.corpus[doc][1] = tokens

            for tok in tokens:
                token_count = tokens.count(tok)

                if tok not in token_dict:
                    token_dict[tok] = {}

                token_dict[tok][idx_doc] = token_count

        return token_dict

    def generate(self, binary=False):
        """
        This function creates a matrix (np.array), which contains the numbers
        of every token. The x-axis represents the token, the y-axis represents
        the document ID so the value shows the frequency of a specific token in
        a document.

        :return: matrix as np.array of the Corpus object.
        """

        # Create word tree
        self.word_tree = self.generate_tree_representation()

        # get token
        self.tokens = list(self.word_tree.keys())

        # Create empty sparse matrix
        feature_matrix = np.zeros((len(self.corpus), len(self.word_tree.keys())))

        for index, (tok, doc) in enumerate(self.word_tree.items()):
            for doc2, val in doc.items():

                # Fill sparse matrix
                if binary:
                    if val > 0:
                        val = 1
                    feature_matrix[doc2, index] = val
                else:
                    feature_matrix[doc2, index] = val

        return feature_matrix

    @ property
    def average_word_length(self):
        """
        Calculates the average word length per document.

        :return: Number of the average word length
        """

        token_list = map(lambda x: nltk.word_tokenize(x), self.corpus_list)

        average_word_length = list(map(
            lambda x: round(sum(map(len, x)) / len(x)), token_list))

        return np.asarray(average_word_length)

    @ property
    def text_contains_numbers(self):
        """
        Finds ALL numbers per document, regardless of whether they
        stand alone or appear in a string.
        Multi-digit numbers and floats are not separated.

        :return: List with Lists per document, which contain the
                 specific document id and another list with
                 the occurring numbers.
        """

        doc_numbers = np.empty(shape=(0, 1))

        for txt in self.corpus_list:
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", txt)
            numbers = list(map(float, numbers))

            if len(numbers) < 1:
                numbers = [0]

            doc_numbers = np.append(doc_numbers, numbers)

        return doc_numbers

    @ property
    def text_begins_with_capital_letter(self):
        """
        Checks, if a document starts with a capital letter and
        stores the boolean result.

        :return: np.array with boolean values:
                 True: Text begins with capital letter
                 False: Text does not begin with capital letter
        """
        capital_letter = np.empty(shape=(0, 1))

        for doc in self.corpus_list:
            if doc[0].isupper():
                capital_letter = np.append(capital_letter, True)
            else:
                capital_letter = np.append(capital_letter, False)

        return capital_letter

    @ property
    def number_of_words(self):
        """
        Calculates the number of words per document, therefore the text
        is split in token, any token without any letters is excluded.

        :return: np.array with number of tokens per document
        """

        token_list = list(map(
            lambda x: nltk.word_tokenize(x), self.corpus_list))

        # Filter strings without any letters
        token_list = [[tok for tok in inner if re.search('[a-zA-Z]', tok)]
                      for inner in token_list]
        # Count tokens
        token_count = list(map(lambda x: len(x), token_list))

        return np.asarray(token_count)

    def number_of_characters(self, incl_whitespace=True) -> np.array:
    # TODO: Define character
        """
        All characters per document are counted, either with or without
        whitespaces.


        :param incl_whitespace: If True, whitespaces are also counted as
                                characters
        :type incl_whitespace:  Boolean
        :return: np.array with the number of characters per document
        """

        # Count characters
        if incl_whitespace:
            char_count = list(map(lambda x: len(x), self.corpus_list))
        else:
            char_count = list(map(lambda x: len(x.replace(" ", "")),
                                  self.corpus_list))

        return np.asarray(char_count)

    def number_of_stopwords(self):

        stopwords_list = []
        stop_words = set(nltk.corpus.stopwords.words('english'))
        count_stopwords = 0
        for idx, (doc_name, txt) in enumerate(self.corpus.items()):
            tokens = txt[1]
            for token in tokens:
                if token in stop_words:
                    count_stopwords += 1
            stopwords_list.append(count_stopwords)

        return stopwords_list

    @ property
    def number_of_special_characters(self):
        """
        Counts all special characters per document, excluding whitespaces.

        :return: np.array with the number of special characters per document
        """

        # Remove non-special characters
        spec_char_count = [[tok for tok in inner if not re.sub('\W+','', tok)]
                           for inner in self.corpus_list]

        # Remove whitespaces and empty strings
        spec_char_count = [[tok for tok in inner if tok.strip()]
                            for inner in spec_char_count]

        # Count special characters
        spec_char_count = list(map(lambda x: len(x), spec_char_count))

        return np.asarray(spec_char_count)

    @ property
    def number_of_numerical_items(self) -> np.array:
        # TODO: Multi-Digits count as one?
        """
        Counts all numerical items. Elements of multi-digits will be counted
        separately. E.g.:
            "t2his":    1
            "42first":  2

        :return: np.array with the number of numerical items per document.
        """

        # Remove non special characters
        num_count = [[tok for tok in inner if re.findall(r'[0-9]+', tok)]
                           for inner in self.corpus_list]

        # Remove whitespaces and empty strings
        num_count = [[tok for tok in inner if tok.strip()]
                            for inner in num_count]

        # Count special characters
        num_count = list(map(lambda x: len(x), num_count))

        return np.asarray(num_count)

    @ property
    def term_frequency(self):
        # TODO: Sentence?
        """
        Term frequency is simply the ratio of the count of a word present in a
        sentence, to the length of the sentence.

        Therefore, we can generalize term frequency as:

        .. math::

            \\text{TF} = \\frac{t_N}{n}

        TF = (Number of times term T appears in the particular row) /
             (number of terms in that row)


        :return: Nested np.array with the tf per token and document
        """

        tf = list(map(
            lambda doc_list: list(map(
                lambda val: round(
                    val/len(doc_list), 3), doc_list)), self.feature_matrix))

        return np.asarray(tf)

    def inverse_document_frequency(self, smooth=True):
        """
        The inverse document frequency, IDF, of a word is the log of the ratio
        of the total number of rows to the number of rows in which that word is
        present.

        The inverse document frequency is defined as:

        .. math::

            \\text{IDF} = log\\Big(\\frac{N}{n}\\Big)

        Where :math:`N` is the number of rows and :math:`n` is the number of
        rows where the word is present.

        :param smooth: True, if the smoothing shall be added to the formula.
        :type smooth:  Boolean
        :return:       np.array with the inverse document frequency per token.
        """

        n = len(self.documents)
        tr_mat = np.transpose(self.feature_matrix)

        # Smoothing added here
        if smooth:
            n += 1

        idf = list(map(lambda x: round(
            np.log(n/np.count_nonzero(x, axis=0)) + 1, 3), tr_mat))

        return np.asarray(idf)

    def term_frequency_inverse_document_frequency(self, smooth=True):
        """
        The Term Frequency-Inverse Document Frequency (TF-IDF) is the TF times
        the IDF:

        .. math::

            \\text{TF-IDF} = \\text{TF(t,d)} \\times \\text{IDF}(t)

        :param smooth: True, if the smoothing shall be added to the formula.
        :type smooth:  Boolean
        :return: Nested np.array with the calculated tf-idf per token and
                 document
        """
        tf_list = self.term_frequency

        if not smooth:
            idf_list = self.inverse_document_frequency(smooth=False)
        else:
            idf_list = self.inverse_document_frequency(smooth=True)

        tf_idf = list(map(
            lambda tf_doc: list(map(
                lambda tf, idf: round(tf*idf, 3), tf_doc, idf_list)), tf_list))

        return np.asarray(tf_idf)

    def n_grams(self, n=2):
        """
        Uses the tokens of the documents to create N-token sequences
        of words.

        Example with n = 2:
            Text:   According to a recent  American study food allergies ...
            Sequences: "According to", "to a", "a recent", "recent American",..


        :param n: Length of the sequences/number of characters
        :type n:  Integer

        :return: List with lists per document, containing the sequences
        """

        n_grams = []

        for idx, (doc_name, txt) in enumerate(self.corpus.items()):
            tokens = txt[1]
            grams_doc = []

            for idx_tok, tok in enumerate(tokens):
                end = idx_tok + n
                grams = tokens[idx_tok:end]

                # comparison needed to avoid last smaller grams of the end
                if len(grams) == n:
                    grams = " ".join(grams)

                grams_doc.append(grams)
            n_grams.append(grams_doc)

        return n_grams

