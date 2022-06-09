import io
from pathlib import Path
import chess, chess.pgn
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.core.files.storage import FileSystemStorage

from django.conf import settings
from metadata.models import Match, Event, Move
from positions.models import FenPosition
from metadata.utils import PGNAdapter

class Command(BaseCommand):
    help = 'Loads annotated files and creates matches'

    def handle(self, *args, **options):

        fs = FileSystemStorage(location=settings.CHESS_STORAGE)
        directories, files = fs.listdir("annotated")
        
        for filename in files:
            with fs.open(f"annotated/{ filename }", "r") as pgn_file:
                while True:
                    game = chess.pgn.read_game(pgn_file)
                    if game:
                        adapter = PGNAdapter(game)
                    else:
                        break
            self.stdout.write(self.style.SUCCESS(f"Successfully imported { filename }"))
        
        return True
