Main Features
=============

In this section we will describe the main features of Augmentext with example code and output.

Augmentext is a software package for text augmentation with an emphasis on providing operations that are typically used in the generation of text data for machine learning or NLP problems.

In principle, Augmentext consists of a number of classes for standard text manipulation functions, such as the ``RandomTypo`` class or the ``SynChecker`` class. You interact and use these classes using a large number of convenience functions, which cover most of the functions you might require when augmenting text datasets for machine learning or NLP problems.

Augmentext uses a **pipeline**-based approach, where **operations** are added sequentially in order to generate a pipeline. Text files are then passed through this pipeline, where each operation is applied to a text element (word or sentence) as it passes through.

Also, Augmentext applies operations to text **stochastically** as it passes through the pipeline, according to a user-defined probability value for each operation.

Therefore every operation has at minimum a probability parameter, which controls how likely the operation will be applied to each word/sentence that is seen as the text passes through the pipeline. Take for example a letter-skip operation, which is defined as follows:

.. code-block:: python
    
    letter_skip(p=0.05)

The ``probability`` parameter controls how often the operation is applied.

Therefore, Augmentext allows you to create an augmentation pipeline, which chains together operations that are applied stochastically, where the parameters of each of these operations are also chosen at random, within a range specified by the user. This means that each time text is passed through the pipeline, a different text corpus is returned. Depending on the number of operations in the pipeline, and the range of values that each operation has available, a very large amount of new text data can be created in this way.

All functions described in this section are made available by the Pipeline object. To begin using Augmentext, you always create a new Pipeline object by instantiating it with a path to a set of text-files or text that you wish to augment:

.. code-block:: python

    >>> import Augmentext
    >>> pipe = Augmentext.Pipes("/path/to/text")

You can now add operations to this pipeline using the ``pipe`` Pipeline object. For example, to add a key distance typo operation:

.. code-block:: python

    >>> pipe.keydist_typo(p=0.1)

All pipeline operations have at least a probability parameter.

Full documentation of all functions and operations can be found in the auto-generated documentation. Below you find a list of the (current) features of Augmentext.


Character-based
---------------
* Letter-Flip
* Letter-Skip
* Random Typo
* Keyboard Distance Typo
* Random Space Inserter

Word-based
----------
* Synonym-Replacer

Furthermore, it is possible to generate a random pipeline with a certain amount of operations.
