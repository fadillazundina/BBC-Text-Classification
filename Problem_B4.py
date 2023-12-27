# ===================================================================================================
# PROBLEM B4
#
# Build and train a classifier for the BBC-text dataset.
# This is a multiclass classification problem.
# Do not use lambda layers in your model.
#
# The dataset used in this problem is originally published in: http://mlg.ucd.ie/datasets/bbc.html.
#
# Desired accuracy and validation_accuracy > 91%
# ===================================================================================================

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd
import numpy as np


def solution_B4():
    bbc = pd.read_csv('https://github.com/dicodingacademy/assets/raw/main/Simulation/machine_learning/bbc-text.csv')

    # DO NOT CHANGE THIS CODE
    # Make sure you used all of these parameters or you can not pass this test
    vocab_size = 1000
    embedding_dim = 16
    max_length = 120
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = "<OOV>"
    training_portion = .8

    # YOUR CODE HERE
    # Using "shuffle=False"
    training_sentences, validation_sentences = train_test_split(
        bbc['text'], train_size=training_portion, shuffle=False
    )#YOUR CODE HERE
    training_labels, validation_labels = train_test_split(
        bbc['category'], train_size=training_portion, shuffle=False
    )#YOUR CODE HERE

    # Fit your tokenizer with training data
    tokenizer =  Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.fit_on_texts(training_sentences)
    word_index = tokenizer.word_index

    training_sequences = tokenizer.texts_to_sequences(training_sentences)
    validation_sequences = tokenizer.texts_to_sequences(validation_sentences)

    training_padded = pad_sequences(
        training_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
    )
    validation_padded = pad_sequences(
        validation_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type
    )
    # YOUR CODE HERE
    
    # You can also use Tokenizer to encode your label.
    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(bbc['category'])

    training_label_seq = np.array(
        label_tokenizer.texts_to_sequences(training_labels)
    )
    validation_label_seq = np.array(
        label_tokenizer.texts_to_sequences(validation_labels)
    )

    model = tf.keras.Sequential([
        # YOUR CODE HERE.
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        # YOUR CODE HERE. DO not change the last layer or test may fail
        tf.keras.layers.Dense(6, activation='softmax')
    ])

    optimizer = "adam"
    model.compile(
        loss="sparse_categorical_crossentropy", optimizer=optimizer, metrics=["accuracy"]
    )
    model.fit(
        training_padded, training_label_seq, epochs=100, validation_data=(validation_padded, validation_label_seq)
    )
    # Make sure you are using "sparse_categorical_crossentropy" as a loss fuction

    return model

    # The code below is to save your model as a .h5 file.
    # It will be saved automatically in your Submission folder.
if __name__ == '__main__':
    # DO NOT CHANGE THIS CODE
    model = solution_B4()
    model.save("model_B4.h5")
