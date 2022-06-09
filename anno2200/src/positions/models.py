from multiprocessing.sharedctypes import Value
from django.db import models

import chess
import xxhash

class PositionManager(models.Manager):
    pass

class FenPosition(models.Model):
    """
        A Model that can be directly converted into a python-chess board.
    """
    objects = PositionManager()
    id = models.CharField(max_length=64, primary_key=True)
    board_fen = models.CharField(max_length=39, help_text="String representation of the board part of a fen.")
    _turn = models.BooleanField(help_text="True if black created this position, else false.")
    castling_fen = models.CharField(max_length=4, help_text="FEN representation of castling rights (e.g. KQkq).")
    ep_square = models.IntegerField(blank=True, null=True, help_text="None, or a valid en passant capture square.")
    halfmove_clock = models.IntegerField(help_text="The number of half-moves in the game so far.")
    fullmove_number = models.IntegerField(help_text="The number of full moves in the game so far.")
    centipawns = models.IntegerField(blank=True, null=True, help_text="Centipawn eval from white's perspective.")
    annotations = models.TextField(blank=True, null=True, help_text="Notes about this position.")

    @property
    def turn(self) -> chess.Color:
        """ Returns the color of the next player to move.

        Returns:
            chess.Color: chess.WHITE or chess.BLACK
        """
        if self._turn:
            return chess.BLACK
        return chess.WHITE
    
    @property
    def board(self) -> chess.Board:
        """The python-chess board of this position.

        Returns:
            chess.Board: See python-chess
        """
        return chess.Board(fen=self.full_fen)
            
    @property
    def hash(self) -> str:
        """Creates a hash of the important parts of the fen to become the primary id

        Returns:
            str: xxh64 hex digest
        """
        return xxhash.xxh64(self.__str__()).hexdigest()

    @property
    def full_fen(self) -> str:
        return f"{ self.board_fen } { 'w' if self._turn else 'b' } { self.castling_fen } { chess.square_name(self.ep_square) if self.ep_square else '-' } { self.halfmove_clock } { self.fullmove_number }"

    def __str__(self) -> str:
        return f"{ self.board_fen } { 'w' if self._turn else 'b' } { self.castling_fen } { chess.square_name(self.ep_square) if self.ep_square else '-' }"

    def save(self, *args, **kwargs) -> None:
        if not self.id:
            self.id = self.hash
        return super().save(*args, **kwargs)

class OpeningBook(models.Model):
    eco = models.CharField(max_length=6)
    name = models.CharField(max_length=64)
    variation = models.CharField(max_length=256)
    positions = models.ManyToManyField('FenPosition', blank=True)

    class Meta:
        unique_together = ('eco', 'name', 'variation')
