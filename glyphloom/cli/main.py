# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:07:36 2026

@author: trent
"""

from threading import Thread

import typer
import matplotlib.pyplot as plt

app = typer.Typer(no_args_is_help=True)

from glyphloom.generation.draw import Glyph
from glyphloom.cli.commands import (fe)

app.add_typer(fe.app, name='5e')


def wait_for_input(flag):
    input("Press Enter to continue...")
    flag['done'] = True
    
    
@app.command()
def char(character_series: str = typer.Argument("The quick brown fox jumped over the lazy dog."),
        character_series_opt: str = typer.Option(None,
                                                 '-c',
                                                 '--characters',
                                                 help='Sentence or phrase you want represented, if using spaces wrap in double quotes "Hello World!"'),
        title: bool = typer.Option(True, '-t', '--hide-title', help="Flag to suppress the figure title")):
    
    done = {"done": False}
    t = Thread(target=wait_for_input, args=(done,), daemon=True)
    t.start()
    
    series = character_series or character_series_opt
    fig = Glyph.character_series(series=series,
                                 title=title)
    fig.show()
    
    while not done['done'] and plt.fignum_exists(fig.number):
        plt.pause(0.1)
        
if __name__ == "__main__":
    app()