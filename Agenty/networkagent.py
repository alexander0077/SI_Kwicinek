import copy
import numpy as np
import tensorflow as tf


class NetworkAgent:
    def __init__(self, my_token=1):
        self.my_token = my_token
        self.opponent_token = 3 - my_token
        if my_token == 1 :
            self.neutral_model = tf.keras.models.load_model('models/reinforced_model_v7.h5')
        else:
            self.neutral_model = tf.keras.models.load_model('models/gracz2_random_v2.h5')

    def toString(self):
        return "Model sieci neuronowej"

    def get_action(self, observation):
        observation = np.array(observation).reshape(1, 6, 7, 1)
        logits = self.neutral_model.predict(observation)
        prob_weights = tf.nn.softmax(logits).numpy()

        action = list(prob_weights[0]).index(max(prob_weights[0]))

        return action, prob_weights[0]
    def decide(self, game):
        arr = game.getArr()
        action, prob = self.get_action(arr)
        if action in game.possible_drops():
            return action
        else:
            return np.random.choice(7)