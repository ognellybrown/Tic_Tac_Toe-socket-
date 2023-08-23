
import socket
import threading

class TicTacToe:
    def __init__(self):
        self.board = [[" "]*3 for _ in range(3)]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False
        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()

        self.you = 'X'
        self.opponent = 'O'
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = "O"
        self.opponent = "X"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row,column): ")
                if self.move_is_valid(move.split(',')):
                    self.apply_move(move.split(','), self.you)
                    self.turn = self.opponent
                    client.send(move.encode('utf-8'))
                else:
                    print('This is an invalid move!')
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You win!")
            elif self.winner == self.opponent:
                print('You lose!')
            else:
                if self.counter == 9:
                    print ('It\'s a draw!')
            self.game_over = True

    def move_is_valid(self, move):
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0] 
                return True 
        
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                return True
            
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            return True
        
        return False
        
    def print_board(self):
        for row in range(3):
            print (" | ".join(self.board[row]))
            if row != 2:
                print("----------")

game = TicTacToe()
game.connect_to_game("localhost", 9999)




































