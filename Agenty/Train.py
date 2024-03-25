class GameLoop:
    def __init__(self, agent1, agent2, game):
        self.agent1 = agent1
        self.agent2 = agent2
        self.game = game

    def generate_training_data(self, num_games):
        training_data = []

        for _ in range(num_games):
            self.game.reset()
            game_history = []
            board_full = False
            while self.game.wining_player == -1 and not board_full:

                game_history.append((self.game.getArr(), self.game.current_Player))
                self.game.dodajKrazek(self.agent1.decide(self.game))

                moves = self.game.possible_drops()
                if not moves:
                    board_full = True
                if self.game.wining_player != -1 or board_full:
                    break

                game_history.append((self.game.getArr(), self.game.current_Player))
                self.game.dodajKrazek(self.agent2.decide(self.game))

                moves = self.game.possible_drops()
                if not moves:
                    board_full = True

            game_result = self.game.wining_player
            for state, player in game_history:
                target = 1 if player == game_result else -1
                training_data.append((state, target))

        return training_data
