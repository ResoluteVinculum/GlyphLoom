# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:28:39 2026

@author: trent
"""

from threading import Thread

import typer
import matplotlib.pyplot as plt

from glyphloom.data.fifth_edition import SpellData_5e
# from glyphloom.generation.geometry import Founts, Leylines, SAFE_MATH
# from glyphloom.generation.draw import Glyph


def wait_for_input(flag):
    input("Press Enter to continue...")
    flag['done'] = True


app = typer.Typer(no_args_is_help=True)


@app.command()
def draw(spell: str = typer.Argument(None),
         spell_opt: str = typer.Option("Modify Memory", "-s", "--spell"),
         source_opt: str = typer.Option("offline", "-o", "--origin"),
         ritual = typer.Option(None, "--ritual",
                               help="Ritual override for display, options are 0, 1, False, True, false, true"),
         fount_expression: str = typer.Option("polygon", "-f", "--founts",
                                              help="'founts' must be a semicolon (';') separated list of expressions with 'domain' as the input values of the function(s)"),
         fount_min=typer.Option("0", "--fount-min",
                                help="'fount-min' must be a number representing the minimum value of the 'founts' parametric equation"),
         fount_max=typer.Option("1", "--fount-max",
                                help="'fount-max' must be a number representing the minimum value of the 'founts' parametric equation"),
         leyline_expression: str = typer.Option("linear",
                                                "-p", "--path",
                                                help="'path' must be a semicolon (';') separated list of expressions with either 'domain' or 'P,Q' as the input values of the function(s)"),
         leyline_min=typer.Option("0", "--leyline-min",
                                  help="'leyline-min' must be a number representing the minimum value of the 'path' parametric equation, only affects functions with 'domain' as the input values."),
         leyline_max=typer.Option("1", "--leyline-max",
                                  help="'leyline-max' must be a number representing the minimum value of the 'path' parametric equation, only affects functions with 'domain' as the input values."),
         leyline_resolution=typer.Option("150", "--path-resolution",
                                         help="'path-resolution' must be an integer representing the number of samples to take along the leyline for shaping."),
         show_legend: bool = typer.Option(False, "-l", "--show-legend",
                                          help="Boolean to show legend"),
         save_file: str = typer.Option(None, "--save-file",
                                       help="Relative or Absolute filepath for png output.")
         ) -> None:
    
    from glyphloom.generation.geometry import Founts, Leylines, SAFE_MATH
    from glyphloom.generation.draw import Glyph

    done = {"done": False}
    t = Thread(target=wait_for_input, args=(done,), daemon=True)
    t.start()

    spell = spell or spell_opt

    plt.ion()
    data = SpellData_5e.get_spell(spell, source_opt)
    if ritual is not None:
        if isinstance(ritual, bool):
            ritual = ritual
        elif ritual in ["0", "1"]:
            ritual = bool(int(ritual))
        elif ritual.lower().capitalize() in ['True', 'False']:
            ritual = eval(ritual.lower().capitalize())
        data.ritual = ritual

    # Unpack founts
    shape = tuple(fount_expression.split(";"))
    if len(shape) == 1:
        shape = shape[0]

    fount_min = eval(fount_min, {}, SAFE_MATH)
    fount_max = eval(fount_max, {}, SAFE_MATH)
    founts = Founts(n_points=13,
                    expression=shape,
                    domain_min=(fount_min),
                    domain_max=(fount_max))

    # Unpack Leylines
    path = tuple(leyline_expression.split(";"))
    if len(path) == 1:
        path = path[0]
    leyline_min = eval(leyline_min, {}, SAFE_MATH)
    leyline_max = eval(leyline_max, {}, SAFE_MATH)
    leyline_resolution = int(eval(leyline_resolution, {}, SAFE_MATH))

    leylines = Leylines(founts=founts,
                        expression=path,
                        domain_min=leyline_min,
                        domain_max=leyline_max,
                        resolution=leyline_resolution)
    fig = Glyph(data,
                leylines).draw(legend=show_legend)
    if save_file is not None:
        plt.savefig(save_file, transparent=True, dpi='figure')
    plt.show()

    while not done['done'] and plt.fignum_exists(fig.number):
        plt.pause(0.1)


@app.command()
def custom(spell_name:str = typer.Argument(""),
           spell_name_opt:str = typer.Option("", "-n", "--spell-name",
                                             help="Spell Name for custom input"),
           level:int = typer.Argument(0),
           level_opt:int = typer.Option(0, "-v", "--level",
                                        help="Integer level of the spell from 0-20"),
           school:str = typer.Argument(None),
           school_opt:str = typer.Option(None, "-c", "--school",
                                       help=f"School of the spell: {tuple(SpellData_5e.school.options)}"),
           damage_type:str = typer.Argument(None),
           damage_type_opt:str = typer.Option(None, "-d", "--damage-type",
                                              help=f"Damage type of the spell: {tuple(SpellData_5e.damage_type.options)}"),
           area_of_effect:str = typer.Argument(None),
           area_of_effect_opt:str = typer.Option(None, "-aoe", "--area-of-effect",
                                                 help=f"Area of effect of the spell: {tuple(SpellData_5e.area_of_effect.options)}"),
           range:str = typer.Argument(None),
           range_opt:str = typer.Option(None, "-r", "--spell-range",
                                          help=f"Range of the spell as described by the SRD: {tuple(SpellData_5e.range.options)}"),
           duration:str = typer.Argument(None),
           duration_opt:str = typer.Option(None, "-t", "--spell-duration",
                                           help=f"Duration of the spell as described by the SRD: {tuple(SpellData_5e.duration.options)}"),
           ritual = typer.Option("0", "--ritual",
                                 help="Ritual override for display, options are 0, 1, False, True, false, true"),
           fount_expression: str = typer.Option("polygon", "-f", "--founts",
                                                help="'founts' must be a semicolon (';') separated list of expressions with 'domain' as the input values of the function(s)"),
           fount_min=typer.Option("0", "--fount-min",
                                  help="'fount-min' must be a number representing the minimum value of the 'founts' parametric equation"),
           fount_max=typer.Option("1", "--fount-max",
                                  help="'fount-max' must be a number representing the minimum value of the 'founts' parametric equation"),
           leyline_expression: str = typer.Option("linear",
                                                  "-p", "--path",
                                                  help="'path' must be a semicolon (';') separated list of expressions with either 'domain' or 'P,Q' as the input values of the function(s)"),
           leyline_min=typer.Option("0", "--leyline-min",
                                    help="'leyline-min' must be a number representing the minimum value of the 'path' parametric equation, only affects functions with 'domain' as the input values."),
           leyline_max=typer.Option("1", "--leyline-max",
                                    help="'leyline-max' must be a number representing the minimum value of the 'path' parametric equation, only affects functions with 'domain' as the input values."),
           leyline_resolution=typer.Option("150", "--path-resolution",
                                           help="'path-resolution' must be an integer representing the number of samples to take along the leyline for shaping."),
           show_legend: bool = typer.Option(False, "-l", "--show-legend",
                                            help="Boolean to show legend"),
           save_file: str = typer.Option(None, "--save-file",
                                         help="Relative or Absolute filepath for png output.")
           ) -> None:
    
    from glyphloom.generation.geometry import Founts, Leylines, SAFE_MATH
    from glyphloom.generation.draw import Glyph
    
    done = {"done": False}
    t = Thread(target=wait_for_input, args=(done,), daemon=True)
    t.start()
    plt.ion()
    
    # Create Data
    ritual = False
    if ritual is not None:
        if isinstance(ritual, bool):
            ritual = ritual
        elif ritual in ["0", "1"]:
            ritual = bool(int(ritual))
        elif ritual.lower().capitalize() in ['True', 'False']:
            ritual = eval(ritual.lower().capitalize())
    data = SpellData_5e(name = spell_name or spell_name_opt,
                        level = level or level_opt,
                        school = school or school_opt,
                        damage_type = damage_type or damage_type_opt,
                        area_of_effect = area_of_effect or area_of_effect_opt,
                        range = range or range_opt,
                        duration = duration or duration_opt,
                        ritual = ritual)
    

    # Unpack founts
    shape = tuple(fount_expression.split(";"))
    if len(shape) == 1:
        shape = shape[0]

    fount_min = eval(fount_min, {}, SAFE_MATH)
    fount_max = eval(fount_max, {}, SAFE_MATH)
    founts = Founts(n_points=13,
                    expression=shape,
                    domain_min=(fount_min),
                    domain_max=(fount_max))

    # Unpack Leylines
    path = tuple(leyline_expression.split(";"))
    if len(path) == 1:
        path = path[0]
    leyline_min = eval(leyline_min, {}, SAFE_MATH)
    leyline_max = eval(leyline_max, {}, SAFE_MATH)
    leyline_resolution = int(eval(leyline_resolution, {}, SAFE_MATH))

    leylines = Leylines(founts=founts,
                        expression=path,
                        domain_min=leyline_min,
                        domain_max=leyline_max,
                        resolution=leyline_resolution)
    fig = Glyph(data,
                    leylines).draw(legend=show_legend)
    if save_file is not None:
        plt.savefig(save_file, transparent=True, dpi='figure')
    plt.show()

    while not done['done'] and plt.fignum_exists(fig.number):
        plt.pause(0.1)
