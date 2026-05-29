import tkinter as tk
from tkinter import messagebox

# Chess board setup
BOARD_SIZE = 8
SQUARE_SIZE = 80

# Unicode chess pieces
pieces = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
}

# Starting board
initial_board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

class ChessGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Chess Game")

        self.canvas = tk.Canvas(root, width=BOARD_SIZE*SQUARE_SIZE,
                                height=BOARD_SIZE*SQUARE_SIZE)
        self.canvas.pack()

        self.board = [row[:] for row in initial_board]

        self.selected_piece = None
        self.turn = 'white'

        self.draw_board()

        self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        self.canvas.delete("all")

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                x1 = col * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE

                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

                piece = self.board[row][col]
                if piece:
                    self.canvas.create_text(
                        x1 + SQUARE_SIZE//2,
                        y1 + SQUARE_SIZE//2,
                        text=pieces[piece],
                        font=("Arial", 36)
                    )

    def handle_click(self, event):
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if self.selected_piece:
            old_row, old_col = self.selected_piece
            self.move_piece(old_row, old_col, row, col)
            self.selected_piece = None
        else:
            piece = self.board[row][col]
            if piece:
                if self.turn == 'white' and piece.isupper():
                    self.selected_piece = (row, col)
                elif self.turn == 'black' and piece.islower():
                    self.selected_piece = (row, col)

    def move_piece(self, old_row, old_col, new_row, new_col):
        piece = self.board[old_row][old_col]

        if self.is_valid_move(piece, old_row, old_col, new_row, new_col):
            target = self.board[new_row][new_col]

            if target.lower() == 'k':
                winner = "White" if piece.isupper() else "Black"
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.root.destroy()
                return

            self.board[new_row][new_col] = piece
            self.board[old_row][old_col] = ''

            self.turn = 'black' if self.turn == 'white' else 'white'
            self.draw_board()

    def is_valid_move(self, piece, old_row, old_col, new_row, new_col):
        target = self.board[new_row][new_col]

        # Prevent capturing same color
        if target:
            if piece.isupper() and target.isupper():
                return False
            if piece.islower() and target.islower():
                return False

        direction = -1 if piece.isupper() else 1

        # Pawn movement
        if piece.lower() == 'p':
            if old_col == new_col and target == '':
                if new_row == old_row + direction:
                    return True

            if abs(new_col - old_col) == 1 and new_row == old_row + direction:
                if target != '':
                    return True

        # Rook movement
        elif piece.lower() == 'r':
            if old_row == new_row or old_col == new_col:
                return self.path_clear(old_row, old_col, new_row, new_col)

        # Bishop movement
        elif piece.lower() == 'b':
            if abs(new_row - old_row) == abs(new_col - old_col):
                return self.path_clear(old_row, old_col, new_row, new_col)

        # Queen movement
        elif piece.lower() == 'q':
            if (
                old_row == new_row or
                old_col == new_col or
                abs(new_row - old_row) == abs(new_col - old_col)
            ):
                return self.path_clear(old_row, old_col, new_row, new_col)

        # Knight movement
        elif piece.lower() == 'n':
            if (
                (abs(new_row - old_row) == 2 and abs(new_col - old_col) == 1) or
                (abs(new_row - old_row) == 1 and abs(new_col - old_col) == 2)
            ):
                return True

        # King movement
        elif piece.lower() == 'k':
            if abs(new_row - old_row) <= 1 and abs(new_col - old_col) <= 1:
                return True

        return False

    def path_clear(self, old_row, old_col, new_row, new_col):
        row_step = 0 if new_row == old_row else (1 if new_row > old_row else -1)
        col_step = 0 if new_col == old_col else (1 if new_col > old_col else -1)

        current_row = old_row + row_step
        current_col = old_col + col_step

        while (current_row, current_col) != (new_row, new_col):
            if self.board[current_row][current_col] != '':
                return False

            current_row += row_step
            current_col += col_step

        return True

# Run game
if __name__ == '__main__':
    root = tk.Tk()
    game = ChessGame(root)
    root.mainloop()
