# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:23:40 2026

@author: trent
"""
import typing


import matplotlib
try:
    matplotlib.use('TkAgg')
except:
    pass
import matplotlib.pyplot as plt
plt.rcParams.update({
    "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),
    "axes.facecolor":    (1.0, 1.0, 1.0, 0.0),
    "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),
})
from numpy import linspace

from glyphloom.generation import data, geometry


class Glyph:
    
    def __init__(self,
                 spelldata: data.SpellData = None,
                 leylines: geometry.Leylines = None):
    
        self.spelldata = spelldata
        if leylines:
            self.leylines = leylines
        else:
            self.leylines = geometry.Leylines(
                geometry.Founts(n=len(spelldata.collect_attributes())))
        
    
    def draw(self, 
             title: bool = True, 
             title_kwargs: dict = {}, 
             legend: bool = False, 
             legend_kwargs: dict = {}, 
             ax = None) -> None:
        # TODO: Add thematic colors        
        
        if not ax:
            fig = plt.figure(constrained_layout=True)
            ax = fig.add_subplot(111)
        elif ax:
            fig = plt.gcf()
        ax.set_aspect('equal', adjustable='box')
        
        if title and not title_kwargs:
            ax.set_title(self.spelldata.name, fontdict=dict(family='Consolas'))
        elif title:
            ax.set_title(self.spelldata.name, **title_kwargs)
        
        if not self.leylines.founts.n_points:
            return fig
        
        attrs = self.spelldata.collect_attributes().values()
        cmap = plt.get_cmap('cubehelix')
        colors = cmap(linspace(0.1, 0.8, len(attrs)))
        non_glyph = 0
        for attr in attrs:
            value = getattr(self.spelldata, attr.name)
            if isinstance(value, typing.Iterable) and not isinstance(value, str):
                value = tuple(value)
            if not attr.glyph:
                if value and non_glyph:
                    kwargs = dict(fillstyle='none', 
                                  markersize=20+10*non_glyph,
                                  color='#991B1E')
                    ax.plot(0,0, 'o', **kwargs)
                elif value:
                    kwargs = dict(markersize=15, color='#991B1E')
                    ax.plot(0,0, 'o', **kwargs)
                
                non_glyph+=1
                continue
            order = attr.order
            options = attr.options
            
            if value is None: continue
            index = list(options).index(value)
            binary = self.leylines.necklace[index]
            paths = self.leylines.default_curves[order, binary.astype(bool)]
            for i, path in enumerate(paths):
                if i:
                    ax.plot(*path, color=colors[order])
                else:
                    ax.plot(*path, color=colors[order], label=f'{attr.name: <15}- {value}')
        ax.plot(*self.leylines.founts[:,1:], 'ok', fillstyle='full', markersize=6)
        ax.plot(*self.leylines.founts[:,0], 'ok', fillstyle='none', markersize=6)
        if legend and legend_kwargs:
            ax.legend(**legend_kwargs)
        elif legend:
            ax.legend(loc='lower center',
                      bbox_to_anchor=(0.5, -0.4),
                      prop={'family':'monospace'})

        ax.axis('off')
        
        return fig
    
    
    @staticmethod
    def character_series(series:str,
                         options:typing.Iterable[str] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnoqprstuvwxyz.!?,;:\"'"),
                         leyline_expression:str|tuple[str] = 'non-centre-circle',
                         title:bool = True) -> None:
        
        figure, axes = plt.subplots(nrows=1,ncols=len(series.split()),
                                    figsize=(max(1.5*len(series.split()),5), 2))
        if title:
            figure.suptitle(series, fontdict=dict(family='Consolas'))
        if not isinstance(axes, typing.Iterable):
            axes = [axes]
        for i, word in enumerate(series.split()):
            # l_word = word.lower()
            l = len(word)
            Data = type(f"Word_{l}", (data.SpellData,), 
                        {f'letter{j}' : data.SpellAttribute(
                            j, 
                            options, 
                            default=None)
                        for j in range(l)})
            spelldata = Data(word, *word)
            
            points = l
            while True:
                try:
                    Glyph(spelldata, 
                          geometry.Leylines(
                              founts=geometry.Founts(n_points=points*2+1),
                              expression=leyline_expression
                              )
                          ).draw(title=False, ax=axes[i], legend=False)
                    break
                except IndexError:
                    points += 1
        plt.show()
        return figure
                    
if __name__ == '__main__':
    # from glyphloom.data.fifth_edition import SpellData_5e
    
    # spelldata = SpellData_5e.get_spell('Magic Stone', 
    #                                    'offline')
    # leylines = geometry.Leylines(
    #     founts=geometry.Founts(
    #         n_points=13,
    #         expression=None),
    #     expression='linear')
    # Glyph(spelldata, leylines).draw(title=False,legend=False)
    
    Glyph.character_series("The quick brown fox jumped over the lazy dog")