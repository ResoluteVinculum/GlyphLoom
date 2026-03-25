# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 16:07:36 2026

@author: trent
"""

import typer

app = typer.Typer(no_args_is_help=True)

from glyphloom.cli.commands import (draw)

app.add_typer(draw.app, name='draw')