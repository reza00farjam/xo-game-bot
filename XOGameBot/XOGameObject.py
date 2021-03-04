import json
import emojis
from pyrogram.types import InlineKeyboardButton


class XOGame:
    def __init__(self, game_id: str, player1: dict, player2: dict = None) -> None:
        self.game_id = game_id
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.winner_keys = []
        self.whose_turn = True  # True: Player1, False: Player2
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.board_keys = [
            [InlineKeyboardButton(
                ".",
                json.dumps({
                    "type": "K",
                    "coord": (i, j),
                    "end": False
                })
            ) for j in range(3)]
            for i in range(3)
        ]

    def is_draw(self) -> bool:
        for i in range(3):
            for j in range(3):
                if not self.board[i][j]:
                    return False

        new_board_keys = []

        for i in range(3):

            temp = []

            for j in range(3):
                if self.board[i][j] == 0:
                    temp.append(
                        InlineKeyboardButton(
                            ".",
                            json.dumps({
                                "type": "K",
                                "coord": (i, j),
                                "end": True
                            })
                        )
                    )
                elif self.board[i][j] == 1:
                    temp.append(
                        InlineKeyboardButton(
                            emojis.X_loser,
                            json.dumps({
                                "type": "K",
                                "coord": (i, j),
                                "end": True
                            })
                        )
                    )
                else:
                    temp.append(
                        InlineKeyboardButton(
                            emojis.O_loser,
                            json.dumps({
                                "type": "K",
                                "coord": (i, j),
                                "end": True
                            })
                        )
                    )

            new_board_keys.append(temp)

        new_board_keys.append(
            [InlineKeyboardButton(
                "Play again!",
                json.dumps({
                    "type": "R"
                })
            )]
        )

        self.board_keys = new_board_keys

        return True

    def fill_board(self, player_id: int, coord: tuple) -> bool:
        if self.board[coord[0]][coord[1]]:
            return False

        if player_id == self.player1["id"]:
            self.board[coord[0]][coord[1]] = 1
            self.board_keys[coord[0]][coord[1]] = InlineKeyboardButton(
                emojis.X,
                json.dumps({
                    "type": "K",
                    "coord": coord,
                    "end": False
                })
            )
        else:
            self.board[coord[0]][coord[1]] = 2
            self.board_keys[coord[0]][coord[1]] = InlineKeyboardButton(
                emojis.O,
                json.dumps({
                    "type": "K",
                    "coord": coord,
                    "end": False
                })
            )

        return True

    def check_winner(self) -> bool:
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != 0:
            self.winner = self.player1 if self.board[0][0] == 1 else self.player2
            self.winner_keys.extend([(0, 0), (0, 1), (0, 2)])
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] != 0:
            self.winner = self.player1 if self.board[0][0] == 1 else self.player2
            self.winner_keys.extend([(0, 0), (1, 0), (2, 0)])
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.player1 if self.board[0][0] == 1 else self.player2
            self.winner_keys.extend([(0, 0), (1, 1), (2, 2)])
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] != 0:
            self.winner = self.player1 if self.board[1][1] == 1 else self.player2
            self.winner_keys.extend([(1, 0), (1, 1), (1, 2)])
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] != 0:
            self.winner = self.player1 if self.board[1][1] == 1 else self.player2
            self.winner_keys.extend([(0, 1), (1, 1), (2, 1)])
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            self.winner = self.player1 if self.board[1][1] == 1 else self.player2
            self.winner_keys.extend([(0, 2), (1, 1), (2, 0)])
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] != 0:
            self.winner = self.player1 if self.board[2][2] == 1 else self.player2
            self.winner_keys.extend([(2, 0), (2, 1), (2, 2)])
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] != 0:
            self.winner = self.player1 if self.board[2][2] == 1 else self.player2
            self.winner_keys.extend([(0, 2), (1, 2), (2, 2)])

        if self.winner:
            new_board_keys = []

            for i in range(3):

                temp = []

                for j in range(3):
                    if self.board[i][j] == 0:
                        temp.append(
                            InlineKeyboardButton(
                                ".",
                                json.dumps({
                                    "type": "K",
                                    "coord": (i, j),
                                    "end": True
                                })
                            )
                        )
                    elif self.board[i][j] == 1:
                        temp.append(
                            InlineKeyboardButton(
                                emojis.X if self.player1["id"] == self.winner["id"] and (i, j) in self.winner_keys
                                else emojis.X_loser,
                                json.dumps({
                                    "type": "K",
                                    "coord": (i, j),
                                    "end": True
                                })
                            )
                        )
                    else:
                        temp.append(
                            InlineKeyboardButton(
                                emojis.O if self.player2["id"] == self.winner["id"] and (i, j) in self.winner_keys
                                else emojis.O_loser,
                                json.dumps({
                                    "type": "K",
                                    "coord": (i, j),
                                    "end": True
                                })
                            )
                        )

                new_board_keys.append(temp)

            new_board_keys.append(
                [InlineKeyboardButton(
                    "Play again!",
                    json.dumps({
                        "type": "R"
                    })
                )]
            )

            self.board_keys = new_board_keys

            return True

        return False