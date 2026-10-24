from collections import defaultdict


def file_rank_to_xy(fr):
    if fr == "-":
        return -1, -1
    x = ord(fr[0]) - ord('a')
    y = int(fr[1]) - 1
    return x, y


def xy_to_file_rank(x, y):
    if 0 <= x <= 7 and 0 <= y <= 7:
        file = chr(ord('a') + x)
        rank = y + 1
        return file + str(rank)
    return "-"


class Board:
    pieces = []
    turn = "w"
    castles = "KQkq"
    en_passant = "-"
    half_moves = 0
    full_moves = 1
    fen_dict = defaultdict(int)
    move_history = []

    class Piece:
        symbol = "-"
        pos = "-"

        def __init__(self, s, p):
            self.symbol = s
            self.pos = p

        def __repr__(self):
            return self.symbol + self.pos

        def white(self):
            return self.symbol in ['P', 'R', 'N', 'B', 'Q', 'K']

        def tile_by_vector(self, v):
            x, y = file_rank_to_xy(self.pos)
            x += v[0]
            y += v[1]
            return xy_to_file_rank(x, y)

        def reachable_tiles_and_attackable_pieces(self, board):
            moves = []
            attacks = []
            if self.symbol == 'P':
                test_tile = self.tile_by_vector([0, 1])
                test_piece = board.piece_type_on_tile(test_tile)
                if test_piece == "-":
                    moves.append(test_tile)
                    if self.pos[1] == "2":
                        test_tile = self.tile_by_vector([0, 2])
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                for v in [[1, 1], [-1, 1]]:
                    test_tile = self.tile_by_vector(v)
                    if test_tile != "-" and test_tile == board.en_passant:
                        moves.append(test_tile)
                    else:
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece in ['p', 'r', 'n', 'b', 'q', 'k']:
                            attacks.append(board.piece_object_on_tile(test_tile))
            elif self.symbol == 'p':
                test_tile = self.tile_by_vector([0, -1])
                test_piece = board.piece_type_on_tile(test_tile)
                if test_piece == "-":
                    moves.append(test_tile)
                    if self.pos[1] == "7":
                        test_tile = self.tile_by_vector([0, -2])
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                for v in [[1, -1], [-1, -1]]:
                    test_tile = self.tile_by_vector(v)
                    if test_tile != "-" and test_tile == board.en_passant:
                        moves.append(test_tile)
                    else:
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece in ['P', 'R', 'N', 'B', 'Q', 'K']:
                            attacks.append(board.piece_object_on_tile(test_tile))
            elif self.symbol in ['n', 'N']:
                for v in [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]:
                    test_tile = self.tile_by_vector(v)
                    if test_tile != "-":
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                        else:
                            test_piece = board.piece_object_on_tile(test_tile)
                            if test_piece.white() != self.white():
                                attacks.append(test_piece)
            elif self.symbol in ['k', 'K']:
                for v in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
                    test_tile = self.tile_by_vector(v)
                    if test_tile != "-":
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                        else:
                            test_piece = board.piece_object_on_tile(test_tile)
                            if test_piece.white() != self.white():
                                attacks.append(test_piece)
                if self.symbol == 'K' and 'K' in board.castles:
                    if board.piece_type_on_tile("e2") != 'p' and board.piece_type_on_tile(
                            "g2") != 'p' and board.piece_type_on_tile("f1") == "-" and board.piece_type_on_tile(
                            "g1") == "-":
                        for piece in board.pieces:
                            if piece.white() != self.white():
                                [r, a] = piece.reachable_tiles_and_attackable_pieces(board)
                                if "f1" in r or self in a:
                                    break
                        else:
                            moves.append("g1")
                if self.symbol == 'K' and 'Q' in board.castles:
                    if board.piece_type_on_tile("c2") != 'p' and board.piece_type_on_tile(
                            "e2") != 'p' and board.piece_type_on_tile("c1") == "-" and board.piece_type_on_tile(
                            "d1") == "-":
                        for piece in board.pieces:
                            if piece.white() != self.white():
                                [r, a] = piece.reachable_tiles_and_attackable_pieces(board)
                                if "d1" in r or self in a:
                                    break
                        else:
                            moves.append("c1")
                if self.symbol == 'k' and 'k' in board.castles:
                    if board.piece_type_on_tile("e7") != 'P' and board.piece_type_on_tile(
                            "g7") != 'P' and board.piece_type_on_tile("f8") == "-" and board.piece_type_on_tile(
                            "g8") == "-":
                        for piece in board.pieces:
                            if piece.white() != self.white():
                                [r, a] = piece.reachable_tiles_and_attackable_pieces(board)
                                if "f8" in r or self in a:
                                    break
                        else:
                            moves.append("g8")
                if self.symbol == 'k' and 'q' in board.castles:
                    if board.piece_type_on_tile("c7") != 'P' and board.piece_type_on_tile(
                            "e7") != 'P' and board.piece_type_on_tile("c8") == "-" and board.piece_type_on_tile(
                            "d8") == "-":
                        for piece in board.pieces:
                            if piece.white() != self.white():
                                [r, a] = piece.reachable_tiles_and_attackable_pieces(board)
                                if "d8" in r or self in a:
                                    break
                        else:
                            moves.append("c8")
            elif self.symbol in ['r', 'R']:
                for [v1, v2] in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                    for i in range(1, 8):
                        test_tile = self.tile_by_vector([v1 * i, v2 * i])
                        if test_tile == "-":
                            break
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                        else:
                            test_piece = board.piece_object_on_tile(test_tile)
                            if test_piece.white() != self.white():
                                attacks.append(test_piece)
                            break
            elif self.symbol in ['b', 'B']:
                for [v1, v2] in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
                    for i in range(1, 8):
                        test_tile = self.tile_by_vector([v1 * i, v2 * i])
                        if test_tile == "-":
                            break
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                        else:
                            test_piece = board.piece_object_on_tile(test_tile)
                            if test_piece.white() != self.white():
                                attacks.append(test_piece)
                            break
            elif self.symbol in ['q', 'Q']:
                for [v1, v2] in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
                    for i in range(1, 8):
                        test_tile = self.tile_by_vector([v1 * i, v2 * i])
                        if test_tile == "-":
                            break
                        test_piece = board.piece_type_on_tile(test_tile)
                        if test_piece == "-":
                            moves.append(test_tile)
                        else:
                            test_piece = board.piece_object_on_tile(test_tile)
                            if test_piece.white() != self.white():
                                attacks.append(test_piece)
                            break
            else:
                return [[], []]
            return [moves, attacks]

    class Move:
        text = ""
        piece = ""
        begin = ""
        end = ""
        castle = ""
        en_passant = ""
        white = True
        takes = False
        check = False
        checkmate = False
        promotion = ""

        def __str__(self):
            return self.begin + "-" + self.piece + "->" + self.end

        def __init__(self, move, board):
            self.text = move
            self.white = board.turn == "w"  # turn
            if board.en_passant != "-":  # en passant
                if board.en_passant[1] == "3":
                    self.en_passant = board.en_passant[0] + "4"
                else:
                    self.en_passant = board.en_passant[0] + "5"
            if move[-1] == "#":  # checkmate
                self.checkmate = True
                move = move[:-1]
            elif move[-1] == "+":  # check
                self.check = True
                move = move[:-1]
            if move[-2] == "=":  # promotion
                self.promotion = move[-1]
                move = move[-2]
            if move == "O-O" or move == "O-O-O":  # castle
                self.piece = "K"
                if board.turn == "w":
                    if move == "O-O":
                        self.castle = "K"
                    else:
                        self.castle = "Q"
                elif move == "O-O":
                    self.castle = "k"
                else:
                    self.castle = "q"
            self.end = move[-2:]
            move = move[:-2]
            if move != "" and move[0] in ['R', 'N', 'B', 'Q', 'K']:
                self.piece = move[0]
                move = move[1:]
            else:
                self.piece = 'P'
            if move != "" and move[-1] == "x":
                self.takes = True
                move = move[:-1]
            if len(move) > 0:
                self.begin = move
            for piece in board.pieces:
                [r, a] = piece.reachable_tiles_and_attackable_pieces(board)
                a_pos = [pc.pos for pc in a]
                if piece.white() == self.white and piece.symbol.upper() == self.piece:
                    if self.takes:
                        if self.end in a_pos and (
                                len(move) == 0 or piece.pos == move or piece.pos[0] == move or piece.pos[
                                1] == move or (self.end == self.en_passant and self.piece == "P" and self.takes)):
                            self.begin = piece.pos
                            break
                    else:
                        if self.end in r and (
                                len(move) == 0 or piece.pos == move or piece.pos[0] == move or piece.pos[1] == move):
                            self.begin = piece.pos
                            break

    def realize_move(self, move):
        p = move.piece
        if not move.white:
            p = p.lower()
        if p == 'r':
            if move.begin == "a8":
                self.castles = self.castles.replace('q', '')
            elif move.begin == "h8":
                self.castles = self.castles.replace('k', '')
        elif p == 'R':
            if move.begin == "a1":
                self.castles = self.castles.replace('Q', '')
            elif move.begin == "h1":
                self.castles = self.castles.replace('K', '')
        elif p == 'k':
            self.castles = self.castles.replace('q', '')
            self.castles = self.castles.replace('k', '')
        elif p == 'K':
            self.castles = self.castles.replace('Q', '')
            self.castles = self.castles.replace('K', '')
        if move.castle != "":
            if move.castle == 'q':
                for piece in self.pieces:
                    if piece.symbol == 'k':
                        piece.pos = 'c8'
                    if piece.symbol == 'r' and piece.pos == 'a8':
                        piece.pos = 'd8'
                self.castles = self.castles.replace('q', '')
                self.castles = self.castles.replace('k', '')
            elif move.castle == 'k':
                for piece in self.pieces:
                    if piece.symbol == 'k':
                        piece.pos = 'g8'
                    if piece.symbol == 'r' and piece.pos == 'h8':
                        piece.pos = 'f8'
                self.castles = self.castles.replace('q', '')
                self.castles = self.castles.replace('k', '')
            elif move.castle == 'Q':
                for piece in self.pieces:
                    if piece.symbol == 'K':
                        piece.pos = 'c1'
                    if piece.symbol == 'r' and piece.pos == 'a1':
                        piece.pos = 'd1'
                self.castles = self.castles.replace('Q', '')
                self.castles = self.castles.replace('Q', '')
            elif move.castle == 'K':
                for piece in self.pieces:
                    if piece.symbol == 'K':
                        piece.pos = 'g1'
                    if piece.symbol == 'r' and piece.pos == 'h1':
                        piece.pos = 'f1'
                self.castles = self.castles.replace('Q', '')
                self.castles = self.castles.replace('K', '')
        else:
            to_del = -1
            if move.takes:                                      # taking...
                if move.piece == "P" and move.end == self.en_passant:   # ...with en passant
                    for i, piece in enumerate(self.pieces):
                        if piece.pos == move.en_passant:
                            to_del = i
                            break
                else:                                                   # ...normally
                    for i, piece in enumerate(self.pieces):
                        if piece.pos == move.end:
                            if piece.symbol in ['r', 'R']:
                                if self.turn == 'w':
                                    self.castles = self.castles.replace('q', '')
                                    self.castles = self.castles.replace('k', '')
                                else:
                                    self.castles = self.castles.replace('Q', '')
                                    self.castles = self.castles.replace('K', '')
                            to_del = i
                            break
                if to_del != -1:
                    del self.pieces[to_del]
            for piece in self.pieces:       # move the piece
                if piece.symbol == p and (piece.pos == move.begin or piece.pos[0] == move.begin):
                    piece.pos = move.end
        if self.turn == "b":
            self.full_moves += 1
            self.turn = "w"
        else:
            self.turn = "b"
        if not move.takes and move.piece not in ['p', 'P']:
            self.half_moves += 1
        else:
            self.half_moves = 0
        self.en_passant = "-"

    def readFEN(self, fen):
        self.fen_dict[fen[:-4]] += 1
        fen = fen.split(" ")
        self.turn = fen[1]
        self.castles = fen[2]
        self.en_passant = fen[3]
        self.half_moves = int(fen[4])
        self.full_moves = int(fen[5])
        fen = fen[0].split("/")
        for r, rank in enumerate(fen):
            f = 0
            for p in rank:
                if p in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    f += int(p)
                else:
                    self.pieces.append(Board.Piece(p, xy_to_file_rank(f, 7 - r)))
                    f += 1

    def __init__(self):
        self.readFEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # self.readFEN("rnbqkbnr/pppp1ppp/8/4p3/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2")
        # self.readFEN("r3k1nr/1p1bq1p1/2Pp3p/p3pn2/P1B5/2N2N2/1PPQ1PPP/R4RK1 b kq - 0 14")

    def piece_type_on_tile(self, tile):
        if tile == "-":
            return None
        for piece in self.pieces:
            if piece.pos == tile:
                return piece.symbol
        return "-"

    def piece_object_on_tile(self, tile):
        if tile == "-":
            return None
        for piece in self.pieces:
            if piece.pos == tile:
                return piece
        return None

    def __str__(self) -> str:
        res = ""
        for y in range(7, -1, -1):
            for x in range(8):
                res += self.piece_type_on_tile(xy_to_file_rank(x, y)) + " "
            res += "\n"
        return res


if __name__ == '__main__':
    b = Board()
    print(b)
    while True:
        # for p in b.pieces:
        #     print(p, p.reachable_tiles_and_attackable_pieces(b))
        m = Board.Move(input("Move: "), b)
        # m = Board.Move("fxe6", b)
        b.realize_move(m)
        print(m, b, sep="\n\n")
