import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()

        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbours = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if (i, j) in self.safes:
                    continue
                if (i, j) in self.mines:
                    count -= 1
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        new_sentence = Sentence(neighbours, count)
        self.knowledge.append(new_sentence)

        self.update_knowledge()

    def update_knowledge(self):
        """
        Updates the AI's knowledge base, inferring new safe and mine cells.
        """
        updated = True
        while updated:
            updated = False
            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes |= sentence.known_safes()
                mines |= sentence.known_mines()

            if safes:
                updated = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                updated = True
                for mine in mines:
                    self.mark_mine(mine)

            new_inferences = []
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 == sentence2:
                        continue
                    if sentence1.cells.issubset(sentence2.cells):
                        inferred_cells = sentence2.cells - sentence1.cells
                        inferred_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(inferred_cells, inferred_count)
                        if new_sentence not in self.knowledge and new_sentence not in new_inferences:
                            new_inferences.append(new_sentence)

            if new_inferences:
                updated = True
                self.knowledge.extend(new_inferences)

        # Clean up empty sentences
        self.knowledge = [sentence for sentence in self.knowledge if sentence.cells]

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        available_moves = [
            (i, j) for i in range(self.height) for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]
        if available_moves:
            return random.choice(available_moves)
        return None
