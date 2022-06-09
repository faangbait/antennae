import xxhash
import chess
import re

from .models import FenPosition

def fen_to_object(fen: str, centipawns=None, annotations=None) -> FenPosition:
    board_fen, turn, castling_fen, ep_square, halfmove_clock, fullmove_number = fen.split(" ")
    
    board_regex = r"^[rnbqkpRNBQKP/1-9]+$"
    if not re.match(board_regex, board_fen):
        raise ValueError(f"Invalid Board FEN (expected { board_regex }, got { board_fen })")
    
    if turn not in ['w','b']:
        raise ValueError(f"Invalid Turn (expected [w,b], got {turn})")
    
    castling_regex = r"^(?:[KQkq]{1,4}|-)$"
    if not re.match(castling_regex, castling_fen):
        raise ValueError(f"Invalid Castling FEN (expected { castling_regex }, got { castling_fen })")
    
    board_fen_hash = xxhash.xxh64(f"{ board_fen } { turn } { castling_fen } { ep_square }").hexdigest()
    
    obj, created = FenPosition.objects.get_or_create(
        id=board_fen_hash,
        board_fen=board_fen,
        _turn = True if turn == 'w' else False,
        castling_fen=castling_fen,
        ep_square=None if ep_square == '-' else chess.parse_square(ep_square),
        defaults={
            'halfmove_clock': int(halfmove_clock),
            'fullmove_number': int(fullmove_number),
            'centipawns': centipawns,
            'annotations': annotations
            }
    )
    
    return obj
