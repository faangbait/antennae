from datetime import datetime, timedelta
import re
from typing import List, Tuple
import chess, chess.pgn

from django.forms.fields import FileField
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from positions.utils import fen_to_object

from .models import Match, Event, Move, Player
from positions.models import OpeningBook

class PGNImport:
    import_file = None
    filename = None
    url = None

    def __init__(self, file: FileField, folder="imported") -> None:
        self.import_file = file
        self.__import(folder=folder)
    
    def __import(self, folder):
        fs = FileSystemStorage(location=settings.CHESS_STORAGE, base_url="/raw/")
        self.filename = fs.save(f"{ folder }/{ self.import_file.name }", self.import_file)
        self.url = fs.url(self.filename)
    
class PGNExport:
    export_match = None

    def __init__(self, match: Match, folder="exported") -> None:
        self.export_match = match
        self.__export(folder)

    def __export(self, folder):
        fs = FileSystemStorage(location=settings.CHESS_STORAGE, base_url="/raw/")
        #fs.generate_filename(
        writer = fs.open(f"{ folder }/{ self.export_match.exportName }.pgn","w")
        exporter = chess.pgn.FileExporter(writer)

        game = chess.pgn.Game()

        game.headers = chess.pgn.Headers(
            Event=self.export_match.event.name,
            Site=self.export_match.event.location,
            Date=self.export_match.date_header,
            Round=self.export_match.round,
            White=self.export_match.white.name,
            Black=self.export_match.black.name,
            WhiteElo=str(self.export_match.white_elo),
            BlackElo=str(self.export_match.black_elo),
            Result=self.export_match.result_header,
        )
        if self.export_match.book:
            game.headers["ECO"] = self.export_match.book.eco
            game.headers["Opening"] = self.export_match.book.name
            game.headers["Variation"] = self.export_match.book.variation

        for move_obj in self.export_match.move_set.all():
            node = game.end()
            node.add_variation(chess.Move.from_uci(move_obj.move))
        
        game.accept(exporter)

def standardize_name(player_name: str) -> List[str]:
    roman_first = ""
    roman_last = ""
    
    # 1. Are we in Last, First?
    # name_regex = r"^([a-zA-Z\u00C0-\u00FF\'\-]+)[,]([a-zA-Z\u00C0-\u00FF ]+[a-zA-Z\u00C0-\u00FF]*)[.]?$"
    name_regex = r"^([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)[,][ ]?((?!.*([M|J|S]r\.?|III|IV|V))[a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)$"

    # Check (1) for matches
    result = re.match(name_regex, player_name)
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        res.reverse()
        return res

    # 2. Match Last, First Suffix
    name_regex = r"^([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)[,][ ]?([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+) ([M|J|S]r\.?|III|IV|V)$"
    
    # Check (2) for matches
    result = re.match(name_regex, player_name)
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res[1], res[0], res[2]
    
    # 3. Match (First Middle Last)
    name_regex = r"^((?!.*[@\_\d])[A-Za-z\u00C0-\u05F4\'\-\.][\.A-Za-z\u00C0-\u05F4\'\-\.]+)[ ]?([A-Za-z\u00C0-\u05F4\'\-\.][A-Za-z\u00C0-\u05F4\'\-\.]*)?[ ]?([A-Za-z\u00C0-\u05F4\'\-\.][A-Za-z\u00C0-\u05F4\'\-\.]+)*[,]?[ ]?([M|J|S]r\.?|III|IV|V)?$"
    
    # Check (3) for matches
    result = re.match(name_regex, player_name)
    
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res

    # 4. Elon named this player
    name_regex = r"^(.*)$"
    
    # Check (4) for matches
    result = re.match(name_regex, player_name)
    
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res
    return []

class PGNAdapter:
    headers = None
    mainline = None
    moves = None
    event = None
    site = None
    white = None
    black = None
    white_elo = None
    black_elo = None
    round = None
    board = None
    result = None
    date = None
    match = None
    
    def __init__(self, game: chess.pgn.Game) -> None:
        if not game.headers:
            return None
        
        self.headers = game.headers
        self.mainline = game.mainline()
        self.match = self.__parse_headers(create=True)
        self.moves = self.__parse_mainline(create=True)
        
    def __parse_headers(self, create=True) -> Match:
        
        event: str = self.headers.get("Event", "")
        site: str = self.headers.get("Site", "")
        date: str = self.headers.get("Date", "")
        round: str = self.headers.get("Round", "")
        board: str = self.headers.get("Board", "")
        white: str = self.headers.get("White", "")
        black: str = self.headers.get("Black", "")
        white_elo: str = self.headers.get("WhiteElo", "")
        black_elo: str = self.headers.get("BlackElo", "")
        result: str = self.headers.get("Result", "")
        eco: str = self.headers.get("ECO", "")
        opening: str = self.headers.get("Opening", "")
        variation: str = self.headers.get("Variation", "")
        
        # Fix date to November 11th if unknown
        date.replace("?", "1")
        
        year, month, day = date.split(".")
        self.date = datetime(int(year), int(month), int(day))

        # Process White Player Header
        self.white = self.__fetch_player(white)
        if white_elo and "?" not in white_elo:
            self.white_elo = int(white_elo)
            
        # Process Black Player Header
        self.black = self.__fetch_player(black)
        if black_elo and "?" not in black_elo:
            self.black_elo = int(black_elo)
       
        # Process Event Header
        if event and "?" not in event:
            try:
                self.event = Event.objects.get(
                    name=event,
                    location=site,
                    start_date__lte=self.date,
                    end_date__gte=self.date
                    )
            except ObjectDoesNotExist:
                if create:
                    self.event = Event.objects.create(
                        name=event,
                        location=site,
                        start_date=self.date - timedelta(days=14),
                        end_date=self.date + timedelta(days=14)
                    )
            except MultipleObjectsReturned:
                events = Event.objects.filter(
                    name=event,
                    location=site,
                    start_date__lte=self.date,
                    end_date__gte=self.date
                    )
                self.event = sorted(events, key=lambda event: event.end_date - event.start_date)[0]
                

        # Process Site Header
        if site and "?" not in site:
            self.site = site
                    
        # Process Round/Board Header
        if round and "?" not in round:
            self.round = round
        
        if board and "?" not in board:
            self.board = board

        # Process Result Header
        draw_regex = r"^(.*[/].*)$"
        white_regex = r"^(1.*0)$"
        black_regex = r"^(0.*1)$"
        
        if re.match(draw_regex, result):
            self.result = 0
        elif re.match(white_regex, result):
            self.result = 1
        elif re.match(black_regex, result):
            self.result = -1

        # Process ECO Header
        if eco and "?" not in eco:
            try:
                self.book = OpeningBook.objects.get(
                    eco=eco,
                    name=opening,
                    variation=variation
                )
            except ObjectDoesNotExist:
                if create:
                    self.book = OpeningBook.objects.create(
                        eco=eco,
                        name=opening,
                        variation=variation
                    )

        # Process Match
        try:
            self.match = Match.objects.get(
                date=self.date,
                round=self.round,
                board=self.board,
                event__id=self.event.id,
                white__id=self.white.id,
                black__id=self.black.id
            )
            if create and self.result != self.match.result:
                self.match.result = self.result
                self.match.save()
        except ObjectDoesNotExist:
            if create:
                self.match = Match.objects.create(
                    date=self.date,
                    round=self.round,
                    board=self.board,
                    event=self.event,
                    white=self.white,
                    black=self.black,
                    white_elo=self.white_elo,
                    black_elo=self.black_elo,
                    result=self.result,
                    book=self.book
                )

        return self.match

    def __fetch_player(self, player_name: str) -> Player:
        if not player_name or "?" in player_name:
            raise ValueError(f"Illegal character in { player_name }")
        
        player = None
        roman_first, roman_last = standardize_name(player_name)
        
        # Fuzzy match what we can
        player, created = Player.objects.get_or_create(
            name__contains=roman_last, 
            name__icontains=roman_first, 
            defaults={
                'name': f"{ roman_first } { roman_last }"
            }
        )
        return player

    def __parse_mainline(self, create=True) -> List[Move]:
        batch_move_objs = []
        
        for node in self.mainline:
            board = node.board()
            centipawns = None

            player = self.match.black
            if board.turn == chess.BLACK: # TODO: Is this backwards?
                player = self.match.white
            
            eval_regex = r"^[-]?[\d]+$"
            result = re.match(eval_regex, node.comment)
            if result:
                if board.turn == chess.BLACK:
                    centipawns = int(node.comment)
                else:
                    centipawns = int(node.comment) * -1

            position = fen_to_object(board.fen(), centipawns=centipawns)
            
            batch_move_objs.append(
                Move(match=self.match,
                     player=player,
                     move=node.move.uci(),
                     position=position
                )
            )
        return Move.objects.bulk_create(batch_move_objs, ignore_conflicts=True)
