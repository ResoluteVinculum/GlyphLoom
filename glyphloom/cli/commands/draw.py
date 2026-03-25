# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:22:30 2026

@author: trent
"""

import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def test(arg:str = 'Hello World'):
    print(arg)