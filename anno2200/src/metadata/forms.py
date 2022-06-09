from unicodedata import name
from django import forms

class UploadPGNForm(forms.Form):
    pgn = forms.FileField(label="PGN File")
