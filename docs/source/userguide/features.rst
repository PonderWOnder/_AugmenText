Features
========

This section will describe the main features of Augmentext with example code and output.

Augmentext is a software package for various text augmentation techniques such as character based and word based operations.

Augmentext consists of a number of classes for several text manipulation functions, for instance the ``spell_mistake`` class. You interact and use these classes using a large number of convenience functions which cover most of the functions you might require when augmenting your text corpus for your machine learning problems.

Spell-mistake
---------------
* Letter-Flip
* Letter-Skip
* Random Typo
* Realistic Typo
* Random Space

Word-based
----------
* Synonym-Replacer
* Change word order (still in Progress)
* Filter out useless words (still in Progress)

Medicine-related
----------------
* Change units (still in Progress)
* Drug name swaps (still in Progress)

Because text augmentation is often a multi-stage process, Augmentext uses a **pipeline**-based approach, where **operations** are added sequentially in order to generate a pipeline. Images are then passed through this pipeline, where each operation is applied to the text as it passes through.

Also, Augmentext applies operations to text elements (i.e. letters, words, sentences) **stochastically** as they pass through the pipeline, according to a user-defined probability value for each operation. 

Therefore every operation has at minimum a probability parameter, which controls how likely the operation will be applied to each text element that is seen as the text corpus passes through the pipeline. Take for example a random spell mistake generator, which is defined as follows:

.. code-block:: python
    
    sometest.random_spell_mistake(p=0.02).token_list

The ``probalility`` parameter controls how often the operation is applied.

Therefore, Augmentext allows you to create an augmentation pipeline, which chains operations together. This means every time text is passed through the self-made pipeline, a different text is returned. Depending on the number of operations, and the probabilities chosen by the user, a large amount of new text can be created in this way.

To begin using Augmentext, you have to load your text corpus:

.. code-block:: python
   
    >>> import Augmentext
    >>> sometest = Augmentext.loader.aug_loader('path_to_file')




