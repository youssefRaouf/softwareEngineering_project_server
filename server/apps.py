# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig
import tensorflow as tf
from transformers import DistilBertTokenizerFast, TFDistilBertModel


class ServerConfig(AppConfig):
    name = 'server'
    server_tokenizer = None
    server_model = None

    def pool_hidden_state(self, last_hidden_state):
        """
        Pool the output vectors into a single mean vector
        """
        last_hidden_state = last_hidden_state[0]
        mean_last_hidden_state = tf.reduce_mean(last_hidden_state, 1)

        return mean_last_hidden_state

    def create_model(self, model, max_len, pool=False):
        input_ids = tf.keras.Input(shape=(max_len,), dtype='int32')
        attention_masks = tf.keras.Input(shape=(max_len,), dtype='int32')

        output = model([input_ids, attention_masks])

        if(pool == True):
            output = self.pool_hidden_state(output)

        else:
            output = output[1]

        output = tf.keras.layers.Dense(7, activation='softmax')(output)
        model = tf.keras.models.Model(
            inputs=[input_ids, attention_masks], outputs=output)
        model.compile(tf.keras.optimizers.Adam(lr=1e-5),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        return model

    def ready(self):
        max_len = 40
        self.server_tokenizer = DistilBertTokenizerFast.from_pretrained(
            'distilbert-base-cased',
            add_special_tokens=True,
            max_length=max_len,
            pad_to_max_length=True)

        self.server_model = TFDistilBertModel.from_pretrained(
            'distilbert-base-cased')
        self.server_model = self.create_model(self.server_model, max_len, True)
        self.server_model.load_weights("saved_models/distilBert69.h5")
