class Score:
    def __init__(self, player_score = 0, computer_score=0):
        self.player_score = player_score
        self.computer_score = computer_score

    def increase_player_score(self):
        self.player_score += 1
        return f"Player score has increased to {self.player_score}."
    
    def increase_computer_score(self):
        self.computer_score += 1
        return f"Computer score has increased to {self.computer_score}"
    
    def get_score(self):
        return f"Player score = {self.player_score} and computer score = {self.computer_score}"

