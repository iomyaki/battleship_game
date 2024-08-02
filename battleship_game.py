import os
import sys
import random
import time


"""
O — empty
M — missed
H — hit
D — destroyed
S — ship
V — not allowed to hit
N — not allowed to place
"""


class Player:
    def __init__(self, name: str):
        self.name = name
        self.ships = 10

    def lose_ship(self):
        self.ships -= 1


class Ship:
    def __init__(self, owner: Player, hp: int):
        self.owner = owner
        self.hp = hp
        self.orient = None
        self.coords = []
        self.status = "online"

    def lose_hp(self):
        self.hp -= 1
        if self.hp <= 0:
            self.die()

    def die(self):
        self.status = "kia"
        self.owner.lose_ship()


class Board:
    def __init__(self):
        self.board_ships = [[None for _ in range(10)] for _ in range(10)]
        self.board_inner = [["O" for _ in range(10)] for _ in range(10)]
        self.board_outer = [["O" for _ in range(10)] for _ in range(10)]

    def place_ship(self, ship: Ship, row: int, col: int, orient: str):
        ship.orient = orient
        if orient == "v":
            a, b = 1, 0
        elif orient == "h":
            a, b = 0, 1
        elif orient == "n":
            a, b = 0, 0

        for i in range(ship.hp):
            row_coord, col_coord = row + i * a, col + i * b

            ship.coords.append((row_coord, col_coord))
            self.board_ships[row_coord][col_coord] = ship
            self.board_inner[row_coord][col_coord] = "W"

        # draw the "shade" of the ship
        around = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        for coord in ship.coords:
            for tile in around:
                if 0 <= coord[0] + tile[0] <= 9 and 0 <= coord[1] + tile[1] <= 9 and self.board_inner[coord[0] + tile[0]][coord[1] + tile[1]] == "O":
                    self.board_inner[coord[0] + tile[0]][coord[1] + tile[1]] = "V"

    def clear_shades(self):
        for i in range(10):
            for j in range(10):
                if self.board_inner[i][j] == "V":
                    self.board_inner[i][j] = "O"


class Game:
    def __init__(self):
        self.player_1 = Player("Human")
        self.player_2 = Player("AI")
        self.board_1 = Board()
        self.board_2 = Board()

    @staticmethod
    def ship_fits(row: int, col: int, board: Board, ship: Ship, orient: str):
        if orient == "v":
            a, b = 1, 0
        elif orient == "h":
            a, b = 0, 1
        elif orient == "n":
            a, b = 0, 0

        # is fully inside the map
        length = ship.hp
        if row + (length - 1) * a > 9 or col + (length - 1) * b > 9:
            return False

        # not overlaps with other ships
        for i in range(length):
            if board.board_inner[row + i * a][col + i * b] != "O":
                return False

        return True

    def cheat(self):
        ships_list = (
            self.p2_battleship,
            self.p2_cruiser_1,
            self.p2_cruiser_2,
            self.p2_destroyer_1,
            self.p2_destroyer_2,
            self.p2_destroyer_3,
            self.p2_submarine_1,
            self.p2_submarine_2,
            self.p2_submarine_3,
            self.p2_submarine_4
        )

        print("===========================================")
        print("============ C H E A T C O D E ============")
        print("===========================================")
        for ship in ships_list:
            print(*ship.coords)
        print("===========================================")

    def welcome_dialogue(self):
        print("Welcome to the Battleship game!")
        name = input("Please, introduce yourself: ")
        if name:
            self.player_1.name = name
        print("If you would like to fill your board manually, type A. If you choose a random layout, type B below")
        option = input("Your choice: ")

        if option == "A":
            self.player_manual_placement()
        elif not option or option == "B":
            self.random_ship_placement("human")

        # remove all Vs from the board
        self.board_1.clear_shades()

    def create_ships(self):
        self.p1_battleship = Ship(self.player_1, 4)
        self.p1_cruiser_1 = Ship(self.player_1, 3)
        self.p1_cruiser_2 = Ship(self.player_1, 3)
        self.p1_destroyer_1 = Ship(self.player_1, 2)
        self.p1_destroyer_2 = Ship(self.player_1, 2)
        self.p1_destroyer_3 = Ship(self.player_1, 2)
        self.p1_submarine_1 = Ship(self.player_1, 1)
        self.p1_submarine_2 = Ship(self.player_1, 1)
        self.p1_submarine_3 = Ship(self.player_1, 1)
        self.p1_submarine_4 = Ship(self.player_1, 1)

        self.p2_battleship = Ship(self.player_2, 4)
        self.p2_cruiser_1 = Ship(self.player_2, 3)
        self.p2_cruiser_2 = Ship(self.player_2, 3)
        self.p2_destroyer_1 = Ship(self.player_2, 2)
        self.p2_destroyer_2 = Ship(self.player_2, 2)
        self.p2_destroyer_3 = Ship(self.player_2, 2)
        self.p2_submarine_1 = Ship(self.player_2, 1)
        self.p2_submarine_2 = Ship(self.player_2, 1)
        self.p2_submarine_3 = Ship(self.player_2, 1)
        self.p2_submarine_4 = Ship(self.player_2, 1)

    def player_manual_placement(self):
        ships_list = (
            (self.p1_battleship, "battleship (len. 4)"),
            (self.p1_cruiser_1, "1st cruiser (len. 3)"),
            (self.p1_cruiser_2, "2nd cruiser (len. 3)"),
            (self.p1_destroyer_1, "1st destroyer (len. 2)"),
            (self.p1_destroyer_2, "2nd destroyer (len. 2)"),
            (self.p1_destroyer_3, "3rd destroyer (len. 2)"),
            (self.p1_submarine_1, "1st submarine (len. 1)"),
            (self.p1_submarine_2, "2nd submarine (len. 1)"),
            (self.p1_submarine_3, "3rd submarine (len. 1)"),
            (self.p1_submarine_4, "4th submarine (len. 1)"),
        )

        print(f"{self.player_1.name}, to place a ship, type its head's row and column, and its orientation (v/h), e.g.: 4 6 v")
        print("Your ships will be marked as W, and their vicinity will be marked as V")
        for ship in ships_list:
            print("Your field")
            print("  0 1 2 3 4 5 6 7 8 9")
            for i in range(10):
                print(i, end=" ")
                for c in self.board_1.board_inner[i]:
                    print(c, end=" ")
                print()

            row, col, orient = input(f"Place your {ship[1]}: ").split()
            while not self.ship_fits(int(row), int(col), self.board_1, ship[0], orient):
                row, col, orient = input(f"The placement is incorrect, please, try again: ").split()

            self.board_1.place_ship(ship[0], int(row), int(col), orient)

        # erase all V's from board_1.board_inner

    def random_ship_placement(self, player: str):
        if player == "human":
            ships_list = (
                self.p1_battleship,
                self.p1_cruiser_1,
                self.p1_cruiser_2,
                self.p1_destroyer_1,
                self.p1_destroyer_2,
                self.p1_destroyer_3,
                self.p1_submarine_1,
                self.p1_submarine_2,
                self.p1_submarine_3,
                self.p1_submarine_4
            )
            board = self.board_1
        elif player == "AI":
            ships_list = (
                self.p2_battleship,
                self.p2_cruiser_1,
                self.p2_cruiser_2,
                self.p2_destroyer_1,
                self.p2_destroyer_2,
                self.p2_destroyer_3,
                self.p2_submarine_1,
                self.p2_submarine_2,
                self.p2_submarine_3,
                self.p2_submarine_4
            )
            board = self.board_2

        for ship in ships_list:
            if ship != self.p2_submarine_1 and ship != self.p2_submarine_2 and ship != self.p2_submarine_3 and ship != self.p2_submarine_4:
                orient = random.choice(["v", "h"])
            else:
                orient = "n"

            row, col = random.randint(0, 9), random.randint(0, 9)
            while not self.ship_fits(row, col, board, ship, orient):
                row, col = random.randint(0, 9), random.randint(0, 9)

            board.place_ship(ship, row, col, orient)

    def place_player_ships_scripted(self):
        self.board_1.place_ship(self.p1_battleship, 4, 0, "v")
        self.board_1.place_ship(self.p1_cruiser_1, 1, 0, "h")
        self.board_1.place_ship(self.p1_cruiser_2, 1, 4, "h")
        self.board_1.place_ship(self.p1_destroyer_1, 3, 5, "h")
        self.board_1.place_ship(self.p1_destroyer_2, 1, 8, "v")
        self.board_1.place_ship(self.p1_destroyer_3, 4, 8, "v")
        self.board_1.place_ship(self.p1_submarine_1, 6, 3, "n")
        self.board_1.place_ship(self.p1_submarine_2, 6, 5, "n")
        self.board_1.place_ship(self.p1_submarine_3, 8, 7, "n")
        self.board_1.place_ship(self.p1_submarine_4, 9, 9, "n")

    def place_enemy_ships_scripted(self):
        self.board_2.place_ship(self.p2_battleship, 3, 3, "v")
        self.board_2.place_ship(self.p2_cruiser_1, 1, 5, "h")
        self.board_2.place_ship(self.p2_cruiser_2, 2, 9, "v")
        self.board_2.place_ship(self.p2_destroyer_1, 0, 0, "h")
        self.board_2.place_ship(self.p2_destroyer_2, 2, 1, "v")
        self.board_2.place_ship(self.p2_destroyer_3, 9, 0, "h")
        self.board_2.place_ship(self.p2_submarine_1, 0, 9, "n")
        self.board_2.place_ship(self.p2_submarine_2, 9, 3, "n")
        self.board_2.place_ship(self.p2_submarine_3, 8, 5, "n")
        self.board_2.place_ship(self.p2_submarine_4, 8, 7, "n")

    def play(self):
        def draw_fields():
            print("Your field              Enemy field")
            print("  0 1 2 3 4 5 6 7 8 9 \t  0 1 2 3 4 5 6 7 8 9")
            for i in range(10):
                print(i, end=" ")
                for c in self.board_1.board_inner[i]:
                    print(c, end=" ")
                print("\t", end="")

                print(i, end=" ")
                for c in self.board_2.board_outer[i]:
                    print(c, end=" ")
                print()

        def make_turn(order: list):
            if order[0][0] == self.player_1:
                row, col = map(int, input(f"{order[0][0].name}, make your turn: ").split())
                while not self.board_2.board_outer[row][col] == "O":
                    row, col = map(int, input(f"{order[0][0].name}, you can't hit this tile, try again: ").split())
            else:
                print(f"{order[0][0].name} makes their turn...")
                # time.sleep(2)

                row, col = random.randint(0, 9), random.randint(0, 9)
                while not self.board_1.board_outer[row][col] == "O":
                    row, col = random.randint(0, 9), random.randint(0, 9)

            ship = order[1][1].board_ships[row][col]
            if ship:
                print(f"{order[0][0].name} hit the ship!")
                order[1][1].board_ships[row][col].lose_hp()
                order[1][1].board_inner[row][col] = "H"
                order[1][1].board_outer[row][col] = "H"

                if ship.status == "kia":
                    print(f"{order[1][0].name}'s ship has been destroyed")
                    for r, c in ship.coords:
                        order[1][1].board_inner[r][c] = "D"
                        order[1][1].board_outer[r][c] = "D"

                    if ship.orient != "n":
                        head, tail = ship.coords[0], ship.coords[-1]

                        if ship.orient == "v":
                            a, b = 1, 0
                        elif ship.orient == "h":
                            a, b = 0, 1

                        if head[0] - a >= 0 and head[1] - b >= 0 and order[1][1].board_outer[head[0] - a][head[1] - b] == "O":
                            order[1][1].board_outer[head[0] - a][head[1] - b] = "V"
                        if tail[0] + a <= 9 and tail[1] + b <= 9 and order[1][1].board_outer[tail[0] + a][tail[1] + b] == "O":
                            order[1][1].board_outer[tail[0] + a][tail[1] + b] = "V"
                    else:
                        if ship.coords[0][0] - 1 >= 0 and order[1][1].board_outer[ship.coords[0][0] - 1][ship.coords[0][1]] == "O":
                            order[1][1].board_outer[ship.coords[0][0] - 1][ship.coords[0][1]] = "V"
                        if ship.coords[0][0] + 1 <= 9 and order[1][1].board_outer[ship.coords[0][0] + 1][ship.coords[0][1]] == "O":
                            order[1][1].board_outer[ship.coords[0][0] + 1][ship.coords[0][1]] = "V"
                        if ship.coords[0][1] - 1 >= 0 and order[1][1].board_outer[ship.coords[0][0]][ship.coords[0][1] - 1] == "O":
                            order[1][1].board_outer[ship.coords[0][0]][ship.coords[0][1] - 1] = "V"
                        if ship.coords[0][1] + 1 <= 9 and order[1][1].board_outer[ship.coords[0][0]][ship.coords[0][1] + 1] == "O":
                            order[1][1].board_outer[ship.coords[0][0]][ship.coords[0][1] + 1] = "V"

                if row - 1 >= 0 and col - 1 >= 0 and order[1][1].board_outer[row - 1][col - 1] == "O":
                    order[1][1].board_outer[row - 1][col - 1] = "V"
                if row - 1 >= 0 and col + 1 <= 9 and order[1][1].board_outer[row - 1][col + 1] == "O":
                    order[1][1].board_outer[row - 1][col + 1] = "V"
                if row + 1 <= 9 and col - 1 >= 0 and order[1][1].board_outer[row + 1][col - 1] == "O":
                    order[1][1].board_outer[row + 1][col - 1] = "V"
                if row + 1 <= 9 and col + 1 <= 9 and order[1][1].board_outer[row + 1][col + 1] == "O":
                    order[1][1].board_outer[row + 1][col + 1] = "V"

                if order[1][0].ships <= 0:
                    draw_fields()
                    print(f"{order[0][0].name} has won!")
                    sys.exit(0)

                return order

            else:
                print(f"{order[0][0].name} missed")
                order[1][1].board_inner[row][col] = "M"
                order[1][1].board_outer[row][col] = "M"

                order.reverse()

                return order

        # setup
        order = [(self.player_1, self.board_1), (self.player_2, self.board_2)]
        random.shuffle(order)
        while True:
            if order[0][0] == self.player_1:
                draw_fields()
            order = make_turn(order)


def main():
    game = Game()

    game.create_ships()
    game.random_ship_placement("AI")
    game.welcome_dialogue()
    #game.cheat()
    game.play()


if __name__ == "__main__":
    main()
