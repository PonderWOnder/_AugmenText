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

        Parameters
        ----------

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

        :return: Sparse matrix of the Corpus object.
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
    def average_word_length(self) -> List[int]:
        # TODO: If input should be possible, type check needs to be added
        """
        Calculates the average word length per document.

        :return: Number of the average word length
        """

        token_list = map(lambda x: nltk.word_tokenize(x), self.corpus_list)

        average_word_length = list(map(
            lambda x: round(sum(map(len, x)) / len(x)), token_list))

        return average_word_length

    @ property
    def text_contains_numbers(self) -> np.array(List[int]):
        """
        Finds ALL numbers per document, regardless of whether they stand alone
        or appear in a string. Multi-digit numbers are not separated.

        :return: List with Lists per document, which contain the
        specific document id and another list with the occuring numbers.
        """
        doc_numbers = []

        for txt in self.corpus_list:
            ints = re.findall(r'\d+', txt)
            ints = list(map(int, ints))

            if len(ints) < 1:
                ints = [0]

            doc_numbers.append(ints)

        return doc_numbers

    @ property
    def text_begins_with_capital_letter(self) -> List[bool]:
        """
        Checks, if a document starts with a capital letter and
        stores the boolean result.

        :return: Boolean value:
                    True: Text begins with capital letter
                    False: Text does not begin with capital letter
        """
        capital_letter = []

        for doc in self.corpus_list:
            if doc[0].isupper():
                capital_letter.append(True)
            else:
                capital_letter.append(False)

        return capital_letter

    @ property
    def number_of_words(self) -> List[int]:
        """
        Calculates the number of words per document, therefore the text
        is split in token, any token without any letters is excluded.

        :return: Number of tokens per document
        """

        token_list = list(map(
            lambda x: nltk.word_tokenize(x), self.corpus_list))

        # Filter strings without any letters
        token_list = [[tok for tok in inner if re.search('[a-zA-Z]', tok)]
                      for inner in token_list]
        # Count tokens
        token_count = list(map(lambda x: len(x), token_list))

        return token_count

    def number_of_characters(self, incl_whitespace=True) -> List[int]:
    # TODO: Define character
        """
        All characters per document are counted, either with or without
        whitespaces.

        :param incl_whitespace: If True, whitespaces are also counted as
                                characters
        :return:                Number of characters per document
        """

        # Count characters
        if incl_whitespace:
            char_count = list(map(lambda x: len(x), self.corpus_list))
        else:
            char_count = list(map(lambda x: len(x.replace(" ", "")),
                                  self.corpus_list))

        return char_count

    def number_of_stopwords(self):
        # TODO: stopwords define by nltk, tf-idf or both?
        return 0

    @ property
    def number_of_special_characters(self) -> List[int]:
        """
        Counts all special characters per document, excluding whitespaces.

        :return: Number of special characters per document
        """

        # Remove non-special characters
        spec_char_count = [[tok for tok in inner if not re.sub('\W+','', tok)]
                           for inner in self.corpus_list]

        # Remove whitespaces and empty strings
        spec_char_count = [[tok for tok in inner if tok.strip()]
                            for inner in spec_char_count]

        # Count special characters
        spec_char_count = list(map(lambda x: len(x), spec_char_count))

        return spec_char_count

    @ property
    def number_of_numerical_items(self) -> List[int]:
        # TODO: Multi-Digits count as one?
        """
        Counts all numerical items. Elements of multi-digits will be counted
        separately. E.g.:
            "t2his":    1
            "42first":  2

        :return: Number of numerical items per document.
        """

        # Remove non special characters
        num_count = [[tok for tok in inner if re.findall(r'[0-9]+', tok)]
                           for inner in self.corpus_list]

        # Remove whitespaces and empty strings
        num_count = [[tok for tok in inner if tok.strip()]
                            for inner in num_count]

        # Count special characters
        num_count = list(map(lambda x: len(x), num_count))

        return num_count

    @ property
    def term_frequency(self) -> List[List[float]]:
        # TODO: Sentence?
        """
        Term frequency is simply the ratio of the count of a word present in a
        sentence, to the length of the sentence.

        Therefore, we can generalize term frequency as:

        .. math::

            \\text{TF} = \\frac{t_N}{n}

        TF = (Number of times term T appears in the particular row) / (number of terms in that row)

        :param:
        :return:
        """

        tf = list(map(
            lambda doc_list: list(map(
                lambda val: round(
                    val/len(doc_list), 3), doc_list)), self.sparse_matrix))

        return tf

    @ property
    def inverse_document_frequency(self) -> List[float]:
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
        :return: The inverse document frequency.
        """

        n = len(self.documents)
        tr_sparse_mat = np.transpose(self.sparse_matrix)
        idf = list(map(lambda x: round(
            np.log(n/np.count_nonzero(x, axis=0)), 3), tr_sparse_mat))

        return idf

    @ property
    def term_frequency_inverse_document_frequency(self):
        """
        The Term Frequency-Inverse Document Frequency (TF-IDF) is the TF times the
        IDF:

        .. math::

            \\text{TF-IDF} = \\text{TF(t,d)} \\times \\text{IDF}(t)

        :param corpus:
        :return:
        """

        tf_list = self.term_frequency
        idf_list = self.inverse_document_frequency
#        tf_idf = list(map(
#            lambda tf: list(map(
#                lambda idf_doc: list(map(
#                    lambda idf: round(tf*idf, 3), idf_doc)), idf_list)), tf_list))

        tf_idf = list(map(
            lambda tf_doc: list(map(
                lambda tf, idf: round(tf*idf, 3), tf_doc, idf_list)), tf_list))

        return tf_idf


if __name__ == '__main__':
    corpus1 = [
        'This is the 4first document.',
        'This document is the second document.',
        'and t2his is the th6ird one.',
        'Is this the first document?',
    ]

    corpus2 = {"dok1": [["This ? is the 42first document."], [""], [""], [""]],
               "dok2": [["This document is the second document."], [""], [""], [""]],
               "dok3": [["and t2his is the th6ird one."], [""], [""], [""]],
               "dok4": [["Is this the first document?"], [""], [""], [""]]}

    corp = GenerateSparseMatrix(corpus2)

    print(f'Tokens: {corp.tokens}')
    print(corp.sparse_matrix)
    print(f'Average word length: {corp.average_word_length}')
    print(f'Integers in corpus: {corp.text_contains_numbers}')
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





