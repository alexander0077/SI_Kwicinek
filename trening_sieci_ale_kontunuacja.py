import tensorflow as tf
import numpy as np
import random
import os


def check_if_done(observation):
    done = [False, 'No Winner Yet']

    if 0 not in observation[0]:
        done = [True, 'Draw']
    # horizontal check
    for i in range(6):
        for j in range(4):
            if observation[i][j] == observation[i][j + 1] == observation[i][j + 2] == observation[i][j + 3] == 1:
                done = [True, 'Player 1 Wins Horizontal']
            if observation[i][j] == observation[i][j + 1] == observation[i][j + 2] == observation[i][j + 3] == 2:
                done = [True, 'Player 2 Wins Horizontal']
    # vertical check
    for j in range(7):
        for i in range(3):
            if observation[i][j] == observation[i + 1][j] == observation[i + 2][j] == observation[i + 3][j] == 1:
                done = [True, 'Player 1 Wins Vertical']
            if observation[i][j] == observation[i + 1][j] == observation[i + 2][j] == observation[i + 3][j] == 2:
                done = [True, 'Player 2 Wins Vertical']
    # diagonal check top left to bottom right
    for row in range(3):
        for col in range(4):
            if observation[row][col] == observation[row + 1][col + 1] == observation[row + 2][col + 2] == \
                    observation[row + 3][col + 3] == 1:
                done = [True, 'Player 1 Wins Diagonal']
            if observation[row][col] == observation[row + 1][col + 1] == observation[row + 2][col + 2] == \
                    observation[row + 3][col + 3] == 2:
                done = [True, 'Player 2 Wins Diagonal']

    # diagonal check bottom left to top right
    for row in range(5, 2, -1):
        for col in range(3):
            if observation[row][col] == observation[row - 1][col + 1] == observation[row - 2][col + 2] == \
                    observation[row - 3][col + 3] == 1:
                done = [True, 'Player 1 Wins Diagonal']
            if observation[row][col] == observation[row - 1][col + 1] == observation[row - 2][col + 2] == \
                    observation[row - 3][col + 3] == 2:
                done = [True, 'Player 2 Wins Diagonal']
    return done


def testing(model, ile_treningu):
    wygrane = 0
    remisy = 0
    przegrane = 0
    invalids = 0
    v = 0
    h = 0
    d = 0
    for game_iterator in range(400):
        connect4_board = np.zeros((6, 7))
        done = [False, 'No Winner Yet']
        while done[0] == False:
            action = get_action(model, connect4_board, 0) # 0 to epsilon, nie zmieniac do testowania
            if connect4_board[0][action[0]] != 0: # jezeli agent wybral zly ruch to przegrywa
                przegrane += 1
                invalids += 1
                break
            connect4_board = make_move(connect4_board, action[0], 1)
            done = check_if_done(connect4_board)
            if done[0] == True:
                if 'Player 2' in done[1]:
                    przegrane += 1
                elif 'Player 1' in done[1]:
                    wygrane += 1
                    if 'Horizontal' in done[1]:
                        h += 1
                    elif 'Vertical' in done[1]:
                        v += 1
                    elif 'Diagonal' in done[1]:
                        d += 1
                elif 'Draw' in done[1]:
                    remisy += 1
                break
            random_move = returnRandomPossibleMove(connect4_board)
            connect4_board = make_move(connect4_board, random_move, 2)
            done = check_if_done(connect4_board)
            if done[0] == True:
                if 'Player 2' in done[1]:
                    przegrane += 1
                elif 'Player 1' in done[1]:
                    wygrane += 1
                elif 'Remis' in done[1]:
                    remisy += 1
                break
    raw_results = str(ile_treningu) + " " + str(wygrane) + " " + str(remisy) + " " + str(przegrane) + " "
    raw_results += str(invalids) + " " + str(v) + " " + str(h) + " " + str(d) + "\n"
    result_string = "Rezultat testu po " + str(ile_treningu) + " treningach:\n"
    result_string += "Wygrane: " + str(wygrane) + " Remisy: " + str(remisy) + " Przegrane: " + str(przegrane) + "\n"
    result_string += "Bledne ruchy: " + str(invalids) + " Pionowe: " + str(v) + " Poziome: " + str(h) + " Przekatne: " + str(d) + "\n\n"

    print(result_string)
    with open("tests_results/random_agent_results", 'a') as plik:
        plik.write(result_string)
    with open("tests_results/raw_results", 'a') as plik:
        plik.write(raw_results)



# Definicja architektury sieci
def create_model():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(50, activation='relu'))
    model.add(tf.keras.layers.Dense(7))

    return model


neutral_model = create_model()
neutral_model.load_weights("models/reinforced_model_v3.h5")

def compute_loss(logits, actions, rewards):
    neg_logprob = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=actions)
    loss = tf.reduce_mean(neg_logprob * rewards)
    return loss


def train_step(model, optimizer, observations, actions, rewards):
    with tf.GradientTape() as tape:
        # Forward propagate through the agent network

        logits = model(observations)
        loss = compute_loss(logits, actions, rewards)
        grads = tape.gradient(loss, model.trainable_variables)

        optimizer.apply_gradients(zip(grads, model.trainable_variables))


def get_action(model, observation, epsilon):
    # funkcja na podstawie epsilona wybiera czy podejmowac decyzje sama, czy losowo
    act = np.random.choice(['model', 'random'], 1, p=[1 - epsilon, epsilon])[0]
    observation = np.array(observation).reshape(1, 6, 7, 1)
    logits = model.predict(observation)
    prob_weights = tf.nn.softmax(logits).numpy()  # wektor prawdopodobienstw

    if act == 'model':
        action = list(prob_weights[0]).index(max(prob_weights[0]))
    else:
        action = np.random.choice(7)

    return action, prob_weights[0]


def check_if_action_valid(obs, action):
    if obs[0][action] == 0:
        valid = True
    else:
        valid = False
    return valid


def returnRandomPossibleMove(board):
    while True:
        choice = random.randint(0, 6)
        if check_if_action_valid(board, choice):
            return choice

def player_1_agent(observation, configuration):
    action, prob_weights = get_action(neutral_model, observation['board'], 0)
    if check_if_action_valid(observation['board'], action):
        return action
    else:
        while True: # jezeli model chce wybrac invalid ruch, to bierze inny
            previous_prob_weight = prob_weights[action]
            temp_prob = min(prob_weights)
            for prob in prob_weights:
                if prob < previous_prob_weight and prob > temp_prob:
                    temp_prob = prob
                    action = list(prob_weights).index(temp_prob)
            if check_if_action_valid(observation['board'], action):
                break

    return action

def make_move(board, action, player_num):
    the_row = None
    for row in range(5, -1, -1):
        if board[row][action] == 0:
            board[row][action] = player_num
            return board

def playingStep(obs, action, player_number):
    if not check_if_action_valid(obs, action):
        return obs, True
    else:
        new_board = obs.copy()
        new_board = make_move(new_board, action, player_number)
        return new_board, False

class Memory:
    def __init__(self):
        self.clear()

    # Resets/restarts the memory buffer
    def clear(self):
        self.observations = []
        self.actions = []
        self.rewards = []
        self.info = []

    def add_to_memory(self, new_observation, new_action, new_reward):
        self.observations.append(new_observation)
        self.actions.append(new_action)
        self.rewards.append(float(new_reward))


# train player 1 against random agent
tf.keras.backend.set_floatx('float64')
# LEARNING RATE
optimizer = tf.keras.optimizers.Adam(0.00001)

already_itered = 160000

connect4_board = np.zeros((6, 7))
memory = Memory()
epsilon = pow(.99985, already_itered)

win_count = 0
for i_episode in range(already_itered, 40000):

    connect4_board = np.zeros((6, 7))

    memory.clear()
    epsilon = epsilon * .99985
    overflow = False
    while True:
        action, _ = get_action(neutral_model, connect4_board, epsilon)
        board_before_move = connect4_board.copy()
        connect4_board, overflow = playingStep(connect4_board, action, 1)

        done = check_if_done(connect4_board)

        # tu customizujemy nagrody
        reward = 0
        if done[0] == False:
            reward = 0
        if done[0] == True:
            if 'Vertical' in done[1]:
                reward = 5
            elif 'Horizontal' in done[1]:
                reward = 40
            elif 'Diagonal' in done[1]:
                reward = 60

            if 'Player 2' in done[1]:
                reward = -1 * abs(reward)
            elif 'Player 1' in done[1]:
                win_count += 1

        if overflow == True and done[0] == False:
            reward = -999
            done[0] = True

        if done[0] == False:
            random_move = returnRandomPossibleMove(connect4_board)
            connect4_board = make_move(connect4_board, random_move, 2)
            done = check_if_done(connect4_board)

            if done[0] == True:
                if 'Vertical' in done[1]:
                    reward = 5
                elif 'Horizontal' in done[1]:
                    reward = 40
                elif 'Diagonal' in done[1]:
                    reward = 60

                if 'Player 2' in done[1]:
                    reward = -1 * abs(reward)
                elif 'Player 1' in done[1]:
                    win_count += 1

        memory.add_to_memory(np.array(board_before_move).reshape(6, 7), action, reward)

        if done[0]:
            # train after each game
            train_step(neutral_model, optimizer,
                       observations=np.array(memory.observations),
                       actions=np.array(memory.actions),
                       rewards=memory.rewards)

            if i_episode % 1000 == 0:
                testing(neutral_model, i_episode)

            if i_episode % 100 == 0:
                neutral_model.save('models/reinforced_model_v3.h5')
            break
