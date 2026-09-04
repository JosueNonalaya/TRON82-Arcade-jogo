from game.board import Board

board = Board(10, 10)

print(board.esta_dentro((5,5)))
print(board.esta_dentro((15,5)))

board.ocupar((5, 5))

print(board.esta_ocupada((5,5)))
print(board.esta_ocupada((2,2)))

board.limpar()

print(board.esta_ocupada((5,5)))