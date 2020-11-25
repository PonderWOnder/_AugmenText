import numpy as np
from typing import Dict, List, Union
import nltk
import re


class GenerateSparseMatrix:
    def __init__(self, corpus):
        self.corpus = corpus
        self.corpus_list = []
        self.tokens = []
        self.documents = self.corpus.keys()

        self.sparse_tree = None
        self.sparse_matrix = None

        self.initialize()

    def initialize(self):
        self.sparse_matrix = self.generate()

    def generate_tree_representation(self) -> Dict[str, Dict[int, int]]:
        """
        This helper function returns a tree like representation of a given corpus
        by generating a nested dictionary.

        Returns
        -------
        token_dict: Nested dictionary, with the token as first key,
                the document as 2nd key
                and the token count as value of the 2nd key.

                Structure:
                    {Token: {Doc_ID: value_count}
                Example:
                    {"This": {0: 1}}
        """

        token_dict = {}

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

    def generate(self) -> np.ndarray:
        """
        This function creates a sparse matrix, which contains the numbers of
        every token. The x-axis represents the token, the y-axis represents
        the document ID so the value shows the frequency of a specific token in
        a document.

        Returns
        ------
        sparse_matrix: Sparse matrix of the Corpus object.
        """

        # Create sparse tree
        self.sparse_tree = self.generate_tree_representation()

        # get token
        self.tokens = list(self.sparse_tree.keys())

        # Create empty sparse matrix
        sparse_matrix = np.zeros((len(self.corpus), len(self.sparse_tree.keys())))

        for index, (tok, doc) in enumerate(self.sparse_tree.items()):
            for doc2, val in doc.items():

                # Fill sparse matrix
                sparse_matrix[doc2, index] = val

        return sparse_matrix

    @ property
    def average_word_length(self) -> np.ndarray:
        """
        Calculates the average word length per document.

        Returns
        -------
        average_word_length: Number of the average word length
        """

        token_list = map(lambda x: nltk.word_tokenize(x), self.corpus_list)

        average_word_length = list(map(
            lambda x: round(sum(map(len, x)) / len(x)), token_list))

        return np.asarray(average_word_length)

    @ property
    def text_contains_numbers(self) -> np.array(List[float]):
        """
        Finds ALL numbers per document, regardless of whether they
        stand alone or appear in a string.
        Multi-digit numbers and floats are not separated.

        Returns
        -------
        doc_numbers: List with Lists per document, which contain the
        specific document id and another list with the occuring numbers.
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
    def text_begins_with_capital_letter(self) -> np.array:
        """
        Checks, if a document starts with a capital letter and
        stores the boolean result.

        Returns
        -------
        capital_letter:
                    Boolean value:
                    True: Text begins with capital letter
                    False: Text does not begin with capital letter
        """
        capital_letter = np.empty(shape=(0, 1))
#        capital_letter = []

        for doc in self.corpus_list:
            if doc[0].isupper():
                capital_letter = np.append(capital_letter, True)
            else:
                capital_letter = np.append(capital_letter, False)

        return capital_letter

    @ property
    def number_of_words(self) -> np.array:
        """
        Calculates the number of words per document, therefore the text
        is split in token, any token without any letters is excluded.

        Returns
        -------
        token_count: Number of tokens per document
        """

        token_list = list(map(
            lambda x: nltk.word_tokenize(x), self.corpus_list))

        # Filter strings without any letters
        token_list = [[tok for tok in inner if re.search('[a-zA-Z]', tok)]
                      for inner in token_list]
        # Count tokens
        token_count = list(map(lambda x: len(x), token_list))

        return np.asarray(token_count)

    def number_of_characters(self, incl_whitespace: bool = True) -> np.array:
    # TODO: Define character
        """
        All characters per document are counted, either with or without
        whitespaces.

        Parameters
        ----------
        incl_whitespace: If True, whitespaces are also
                    counted as characters
        Returns
        -------
        char_count:      Number of characters per document
        """

        # Count characters
        if incl_whitespace:
            char_count = list(map(lambda x: len(x), self.corpus_list))
        else:
            char_count = list(map(lambda x: len(x.replace(" ", "")),
                                  self.corpus_list))

        return np.asarray(char_count)

    def number_of_stopwords(self):
        # TODO: stopwords define by nltk, tf-idf or both?
        return 0

    @ property
    def number_of_special_characters(self) -> np.array:
        """
        Counts all special characters per document, excluding whitespaces.

        Returns
        -------
        spec_char_count: Number of special characters per document
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

        Returns
        -------
        num_count: Number of numerical items per document.
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
    def term_frequency(self) -> np.array:
        # TODO: Sentence?
        """
        Term frequency is simply the ratio of the count of a word present in a
        sentence, to the length of the sentence.

        Therefore, we can generalize term frequency as:

        .. math::

            \\text{TF} = \\frac{t_N}{n}

        TF = (Number of times term T appears in the particular row) / (number of terms in that row)


        Returns
        -------
        tf:
        """

        tf = list(map(
            lambda doc_list: list(map(
                lambda val: round(
                    val/len(doc_list), 3), doc_list)), self.sparse_matrix))

        return np.asarray(tf)

    @ property
    def inverse_document_frequency(self) -> np.array:
        """
        The inverse document frequency, IDF, of a word is the log of the ratio
        of the total number of rows to the number of rows in which that word is
        present.

        The inverse document frequency is defined as:

        .. math::

            \\text{IDF} = log\\Big(\\frac{N}{n}\\Big)

        Where :math:`N` is the number of rows and :math:`n` is the number of rows
        where the word is present.

        :param corpus: The corpus to analyse.

        Returns
        -------
        idf: The inverse document frequency.
        """

        n = len(self.documents)
        tr_sparse_mat = np.transpose(self.sparse_matrix)
        idf = list(map(lambda x: round(
            np.log(n/np.count_nonzero(x, axis=0)), 3), tr_sparse_mat))

        return np.asarray(idf)

    @ property
    def term_frequency_inverse_document_frequency(self) -> np.array:
        """
        The Term Frequency-Inverse Document Frequency (TF-IDF) is the TF times the
        IDF:

        .. math::

            \\text{TF-IDF} = \\text{TF(t,d)} \\times \\text{IDF}(t)

        Returns
        -------
        tf_idf:
        """

        tf_list = self.term_frequency
        idf_list = self.inverse_document_frequency

        tf_idf = list(map(
            lambda tf_doc: list(map(
                lambda tf, idf: round(tf*idf, 3), tf_doc, idf_list)), tf_list))

        return np.asarray(tf_idf)

    def n_grams(self, n: int = 2):
        """

        :param n:
        :return:
        """

#        n_grams = np.empty(shape=(0, 1))
        n_grams = []

        for idx, (doc_name, txt) in enumerate(self.corpus.items()):
            tokens = txt[1]
#            grams_doc = np.empty(shape=(0, 1))
            grams_doc = []
            for idx_tok, tok in enumerate(tokens):
                end = idx_tok + n
                grams = tokens[idx_tok:end]
                print(idx_tok)
                print(end)
                print(grams)
                grams = " ".join(grams)
#                print(grams)
#                grams_doc = np.append(grams_doc, grams)
                grams_doc.append(grams)
#               n = idx_tok + n
#            n_grams = np.append(n_grams, grams_doc)
            n_grams.append(grams_doc)
        return n_grams


    def word_embedding(corpus):
        # Research Method with good performance, less power
        return 0


if __name__ == '__main__':
    corpus1 = [
        'This is the 4first document.',
        'This document is the second document.',
        'and t2his is the th6ird one.',
        'Is this the first document?',
    ]

    corpus2 = {"dok1": [["This ? is the 42first document."], [""], [""], [""]],
               "dok2": [["This document is 1.9 the second document."], [""], [""], [""]],
               "dok3": [["and t2his is the th6ird one."], [""], [""], [""]],
               "dok4": [["Is this the first document?"], [""], [""], [""]]}

    import os
    directory = r'C:\Users\Jacky\PycharmProjects\_AugmenText\test'
    corpus3 = {}
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        text = open(file_path, "r").read()
        filename = os.path.splitext(file)[0]
        corpus3[filename] = [[text], [""], [""], [""]]
        print(filename)
        print(text)
    corp = GenerateSparseMatrix(corpus3)

    print(f'Tokens: {corp.tokens}')
    print(corp.sparse_matrix)
    print(f'Average word length: {corp.average_word_length}')
    print(f'Numbers in corpus: {corp.text_contains_numbers}')
    print(f'Capital Letters: {corp.text_begins_with_capital_letter}')
    print(f'Number of Words: {corp.number_of_words}')
    print(f'Number of Characters: {corp.number_of_characters()}')
    print(f'Number of Characters without whitespaces: {corp.number_of_characters(incl_whitespace=False)}')
    print(f'Number of special Characters: {corp.number_of_special_characters}')
    print(f'Number of numerical Characters: {corp.number_of_numerical_items}')
    print(f'Corpus List: {corp.corpus_list}')
    print(f'TF: {corp.term_frequency}')
    print(f'IDF: {corp.inverse_document_frequency}')
    print(f'TF-IDF: {corp.term_frequency_inverse_document_frequency}')
    print(f'N-grams: {corp.n_grams(n=3)}')


