import chess

from django.test import TestCase

from metadata.models import Move

from .models import FenPosition, OpeningBook
from .utils import fen_to_object

class PositionTestCase(TestCase):
    def test_create_fen_position(self):
        # Create New Object
        fen_string="rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R b KQkq - 3 3"
        obj = fen_to_object(fen_string)
        self.assertIsNotNone(obj)
        self.assertEquals("rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R", obj.board_fen)
        self.assertEquals(False, obj._turn)
        self.assertEquals("KQkq", obj.castling_fen)
        self.assertIsNone(obj.ep_square)
        self.assertEquals(3, obj.halfmove_clock)
        self.assertEquals(3, obj.fullmove_number)
        self.assertEqual(1, FenPosition.objects.count())
        
        # Duplicate Object - Get, not Create
        fen_string="rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R b KQkq - 3 3"
        obj = fen_to_object(fen_string)
        self.assertIsNotNone(obj)
        self.assertEquals("rnbqkb1r/ppp1pppp/5n2/3p4/3P1B2/5N2/PPP1PPPP/RN1QKB1R", obj.board_fen)
        self.assertEquals(False, obj._turn)
        self.assertEquals("KQkq", obj.castling_fen)
        self.assertIsNone(obj.ep_square)
        self.assertEquals(3, obj.halfmove_clock)
        self.assertEquals(3, obj.fullmove_number)
        self.assertEqual(1, FenPosition.objects.count())

        # Create New Object
        fen_string="rnbqkb1r/pp2pppp/5n2/2pp4/3P1B2/5N2/PPP1PPPP/RN1QKB1R w KQkq c6 0 4"
        obj = fen_to_object(fen_string)
        self.assertIsNotNone(obj)
        self.assertEquals("rnbqkb1r/pp2pppp/5n2/2pp4/3P1B2/5N2/PPP1PPPP/RN1QKB1R", obj.board_fen)
        self.assertEquals(True, obj._turn)
        self.assertEquals("KQkq", obj.castling_fen)
        self.assertEquals(chess.parse_square("c6"), obj.ep_square)
        self.assertEquals(0, obj.halfmove_clock)
        self.assertEquals(4, obj.fullmove_number)
        self.assertEqual(2, FenPosition.objects.count())
        
    def test_create_opening_book(self):
        book, created = OpeningBook.objects.get_or_create(
            eco="X99",
            name="Faang's opening",
            variation="Baited counter-gambit"
        )
        
        self.assertEquals(True, created)
        self.assertEquals("X99", book.eco)

    def test_invalid_fen(self):
        with self.assertRaises(ValueError):
            fen_to_object("tooshort")
        
        with self.assertRaises(ValueError): # Invalid Board FEN
            fen_to_object("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNT w KQkq - 0 0")

        with self.assertRaises(ValueError): # Invalid Turn
            fen_to_object("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR x KQkq - 0 0")

        with self.assertRaises(ValueError): # Invalid castling FEN
            fen_to_object("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w XQkq - 0 0")
