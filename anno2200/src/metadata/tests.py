from multiprocessing.sharedctypes import Value
import os
import datetime
import chess, chess.pgn
import mock

from django.test import TestCase, Client
from django.conf import settings
from django.core.files import File
from django.urls import reverse
from django.contrib.auth.models import User

from metadata.forms import UploadPGNForm
from metadata.models import Event, Player, Match, Move
from metadata.utils import standardize_name, PGNAdapter, PGNExport, PGNImport
from positions.models import OpeningBook
from positions.utils import fen_to_object

from metadata.management.commands.load_annotated import Command as LoadAnnotatedCommand

class MetadataTestCase(TestCase):
    def setUp(self):
        for f in os.listdir(f"{ settings.CHESS_STORAGE }/test"):
            os.remove(os.path.join(f"{ settings.CHESS_STORAGE }/test", f))
      
        self.event, created = Event.objects.get_or_create(
            name="2200 World Championship",
            defaults={
                'location': 'Wijk aan Zee',
                'description': 'Lorem ipsum dolor sic amet'
                }
            )
        self.assertEquals(True, created)
        
        self.white, created = Player.objects.get_or_create(
            name="Player 1",
            defaults={
                'fide_number': 'abcdef',
                'chesscom_account': 'player1'
            }
        )
        self.assertEquals(True, created)
        
        self.black, created = Player.objects.get_or_create(
            name="Player 2",
            defaults={
                'fide_number': 'ghijkl',
                'chesscom_account': 'player2'
            }
        )
        self.assertEquals(True, created)

        self.book, created = OpeningBook.objects.get_or_create(
            eco="C23",
            name="Bishop's opening",
            variation="Philidor variation"
        )
        
        self.assertEquals(True, created)
        
        self.match, created = Match.objects.get_or_create(
            event=self.event,
            round='Finals',
            board='1',
            defaults={
                'date': datetime.date.today(),
                'white': self.white,
                'black': self.black,
                'white_elo': 2900,
                'black_elo': 3000,
                'result': -1,
                'book': self.book
            }
        )
        self.assertEquals(True, created)
        
        self.chess_moves = [
            chess.Move(from_square=chess.parse_square("e2"), to_square=chess.parse_square("e4")),
            chess.Move(from_square=chess.parse_square("e7"), to_square=chess.parse_square("e5")),
            chess.Move(from_square=chess.parse_square("f1"), to_square=chess.parse_square("c4")),
            chess.Move(from_square=chess.parse_square("b8"), to_square=chess.parse_square("c6")),
            chess.Move(from_square=chess.parse_square("d1"), to_square=chess.parse_square("h5")),
            chess.Move(from_square=chess.parse_square("g8"), to_square=chess.parse_square("f6")),
            chess.Move(from_square=chess.parse_square("h5"), to_square=chess.parse_square("f7")),
            ]

        self.move = Move.objects.create(
            match=self.match,
            player=self.white,
            move=self.chess_moves[0].uci(),
            position=fen_to_object("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", centipawns=50)
        )
        self.move2 = Move.objects.create(
            match=self.match,
            player=self.black,
            move=self.chess_moves[1].uci(),
            position=fen_to_object("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2", centipawns=25)
        )
        
        self.game = chess.pgn.Game()
        self.game.headers = chess.pgn.Headers(
            Event="World Championship",
            Site="Oslo, Norway",
            Date="2200.01.14",
            Round="1",
            White="Magnus Carlsen",
            Black="Ding, Liren",
            WhiteElo="2900",
            BlackElo="2850",
            Result="1-0",
            ECO="C23",
            Opening="Bishop's opening",
            Variation="Philidor variation"
        )

       
    def test_create_event(self):
        self.assertEquals(1, Event.objects.count())
        self.assertEquals("2200 World Championship", self.event.name)
        self.assertEquals("Wijk aan Zee", self.event.location)
        self.assertEquals("Lorem ipsum dolor sic amet", self.event.description)
    
    def test_create_player(self):
        self.assertEquals(2, Player.objects.count())
        self.assertEquals('Player 1', self.white.name)
        self.assertEquals('ghijkl', self.black.fide_number)
        self.assertEquals('player1', self.white.chesscom_account)
        
    def test_create_match(self):
        self.assertEquals(1, Match.objects.count())
        self.assertEquals('Wijk aan Zee', self.match.event.location)
        self.assertEquals('Player 1', self.match.white.name)

    def test_create_book(self):
        self.assertEquals("Philidor variation", self.match.book.variation)
        
    def test_create_move(self):
        self.assertEquals(2, Move.objects.count())
        self.assertEquals('e2e4', self.move.move)
        self.assertEquals('e7e5', self.move2.move)
        self.assertEquals('rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR', self.move.position.board_fen)
        self.assertEquals(chess.parse_square("e3"), self.move.position.ep_square)
        self.assertEquals('rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR', self.move2.position.board_fen)
        self.assertEquals(chess.parse_square("e6"), self.move2.position.ep_square)
        self.assertEquals(chess.WHITE, self.move.position.turn)
        self.assertEquals(chess.BLACK, self.move2.position.turn)
        self.assertEquals(50, self.move.position.centipawns)
        self.assertEquals(25, self.move2.position.centipawns)
        self.assertEquals("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR", self.move2.position.board.board_fen())

    def test_board_hashing(self):
        self.assertEquals("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3", f"{ self.move.position }")
        self.assertEquals("f0ab0262e6885e32", f"{ self.move.position.hash }")
        
    def test_name_parser(self):
        self.assertEquals("Magnus Carlsen", " ".join(standardize_name("Magnus Carlsen")))
        self.assertEquals("Jacob Aagaard", " ".join(standardize_name("Aagaard, Jacob")))
        self.assertEquals("Boško Abramović", " ".join(standardize_name("Abramović, Boško")))
        self.assertEquals("B. Adhiban", " ".join(standardize_name("B. Adhiban")))
        self.assertEquals("Ralf Åkesson", " ".join(standardize_name("Åkesson, Ralf")))
        self.assertEquals("Carlos Daniel Albornoz Cabrera", " ".join(standardize_name("Albornoz Cabrera, Carlos Daniel")))
        self.assertEquals("Ardiansyah", " ".join(standardize_name("Ardiansyah")))
        self.assertEquals("Rogelio Antonio Jr.", " ".join(standardize_name("Antonio, Rogelio Jr.")))
        self.assertEquals("Wei Yi", " ".join(standardize_name("Wei Yi")))
        self.assertEquals("D'Marcus Williums", " ".join(standardize_name("D'Marcus Williums")))
        self.assertEquals("T.J. Juckson", " ".join(standardize_name("T.J. Juckson")))
        self.assertEquals("T'variusness King", " ".join(standardize_name("King, T'variusness")))
        self.assertEquals("Tyroil Smoochie-Wallace", " ".join(standardize_name("Tyroil Smoochie-Wallace")))
        self.assertEquals("D'squarius Green Jr.", " ".join(standardize_name("D'squarius Green, Jr.")))
        self.assertEquals("Ibrahim Moizoos", " ".join(standardize_name("Moizoos, Ibrahim")))
        self.assertEquals("Jackmerius Tacktheritrix", " ".join(standardize_name("Jackmerius Tacktheritrix")))
        self.assertEquals("D'isiah T. Billings-Clyde", " ".join(standardize_name("D'isiah T. Billings-Clyde")))
        self.assertEquals("D'Jasper Probincrux III", " ".join(standardize_name("Probincrux, D'Jasper III")))
        self.assertEquals("Leoz Maxwell Jilliumz", " ".join(standardize_name("Leoz Maxwell Jilliumz")))
        self.assertEquals("Javaris Jamar Javarison-Lamar", " ".join(standardize_name("Javarison-Lamar, Javaris Jamar")))
        self.assertEquals("Davoin Shower-Handel", " ".join(standardize_name("Davoin Shower-Handel")))
        self.assertEquals("Hingle McCringleberry", " ".join(standardize_name("McCringleberry, Hingle")))
        self.assertEquals("L'Carpetron Dookmarriot", " ".join(standardize_name("L'Carpetron Dookmarriot")))
        self.assertEquals("J'Dinkalage Morgoone", " ".join(standardize_name("Morgoone, J'Dinkalage")))
        self.assertEquals("Xmus Jackson Flaxon Waxon", " ".join(standardize_name("Xmus Jackson Flaxon Waxon")))
        self.assertEquals("Swirvithan L'Goodling-Splatt", " ".join(standardize_name("L'Goodling-Splatt, Swirvithan")))
        self.assertEquals("Shakiraquan T.G.I.F Carter", " ".join(standardize_name("Carter, Shakiraquan T.G.I.F")))
        self.assertEquals("X-Wing @Aliciousness", " ".join(standardize_name("X-Wing @Aliciousness")))
        self.assertEquals("T.J. A.J. R.J. Backslashinfourth V", " ".join(standardize_name("Backslashinfourth, T.J. A.J. R.J. V")))


    def test_pgn_adapter(self):
        adapter = PGNAdapter(self.game)
        self.assertEquals("World Championship", adapter.match.event.name)
        self.assertEquals("Liren Ding", adapter.black.name)
        self.assertEquals("Magnus Carlsen", adapter.white.name)
        
    def test_pgn_export(self):
        pgn_export = PGNExport(self.match, folder="test")
        self.assertEquals(self.match, pgn_export.export_match)
    
    def test_upload_form(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = f"{ self.match.exportName }.pgn"
        upload_form = UploadPGNForm(data={},files={'pgn': file_mock})
        self.assertEquals(1,len(upload_form.files.items()))
        
    def test_upload_view(self):
        user, created = User.objects.get_or_create(username='admin', password='pass', is_staff=True)
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = f"{ self.match.exportName }.pgn"
        client = Client()

        client.force_login(user)
        response = client.get(reverse("upload"))
        self.assertEquals(200,response.status_code)

        response = client.post(reverse("upload"), data={'pgn': file_mock})
        self.assertEquals(200,response.status_code)
        
    def test_pgn_import(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = f"{ self.match.exportName }.pgn"
        
        pgn_import = PGNImport(file_mock, folder="test")
        self.assertEquals(f"test/{ self.match.exportName }.pgn", pgn_import.filename)

    def test_load_annotated(self):
        cmd = LoadAnnotatedCommand()
        self.assertEquals(True, cmd.handle())

    def test_match_fallbacks(self):
        match = Match(
            date=None,
            event=self.event,
            white=self.white,
            black=self.black,
            )
        
        self.assertEquals("????.??.??", match.date_header)
        
        self.assertEquals("*", match.result_header)
        self.assertEquals("No Result", match.result_human)
        match.result=0
        self.assertEquals("1/2-1/2", match.result_header)
        self.assertEquals("Draw", match.result_human)
        match.result=-1
        self.assertEquals("0-1", match.result_header)
        self.assertEquals("Black", match.result_human)
        match.result=1
        self.assertEquals("1-0", match.result_header)
        self.assertEquals("White", match.result_human)
