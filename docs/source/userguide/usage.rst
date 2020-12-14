Usage
=====

Here we describe the general usage of Augmentext. 

Getting Started
---------------

To use Augmentext, the following general procedure is followed:

1. You instantiate a :class:`~Augmentext.Pipeline.Pipes` object pointing to a directory containing your initial text data set.
2. You define a number of operations to perform on this data set using your :class:`~Augmentext.Pipeline.Pipes` object.
3. You execute these operations by calling the :class:`~Augmentext.Pipeline.Pipes`'s :func:`~Augmentext.Pipeline.Pipes.run` method.

We will go through each of these steps in order in the proceeding 3 sub-sections.

Step 1: Create a New Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Let us first create an empty pipeline. In other words, to begin any augmentation task, you must first initialise a :class:`~Augmentext.Pipeline.Pipes` object, that points to a directory where your original text dataset is stored:

.. code-block:: python

    >>> import Augmentext
    >>> pipe = Augmentext.Pipes("/path/to/text")

The variable ``pipe`` now contains a :class:`~Augmentext.Pipeline.Pipes` object, and has been initialised with a (list of) text file(s) found in the source directory.

Step 2: Add Operations to the Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created a :class:`~Augmentor.Pipeline.Pipeline`, ``pipe``, we can begin by adding operations to ``pipe``. For example, we shall begin by adding a :func:`~Augmentext.Pipeline.Pipes.space_inserter` operation:

.. code-block:: python

    >>> pipe.space_inserter(p=0.01)

In this case, we have added a :func:`~Augmentor.Pipeline.Pipes.space_inserter` operation, that will execute with a probability of 1%.

Next, we add a further operation, in this case a :func:`~Augmentext.Pipeline.Pipes.random_typo` operation:

.. code-block:: python

    >>> pipe.random_typo(p=0.03)

This time, we have specified that we wish the operation to be applied with a probability of 3%.

Step 3: Execute and Sample From the Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have added the operations that you require, you can generate new, augmented data by using the :func:`~Augmentext.Pipeline.Pipes.run` function:

.. code-block:: python

    >>> pipe.run()

.. hint::

    A full list of operations can be found in the :mod:`~Augmentext.Operations` module documentation.