# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 14:23:40 2026

@author: trent
"""
import typing

if __name__ != "__main__":
    import matplotlib
    matplotlib.use("TkAgg")
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
                 leylines: geometry.Leylines = None) -> typing.Self:
    
        self.spelldata = spelldata
        if leylines:
            self.leylines = leylines
        else:
            self.leylines = geometry.Leylines(
                geometry.Founts(n=len(spelldata.collect_attributes())))
        
    
    def draw(self, legend: bool = False, legend_kwargs: dict = {}):
        # TODO: Add thematic colors
        fig = plt.figure(constrained_layout=True)
        ax = fig.add_subplot(111)
        ax.set_aspect('equal', adjustable='box')
        plt.title(self.spelldata.name)
        
        if not self.leylines.founts.n_points:
            fig.show()
            return fig, ax
        
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
                    plt.plot(0,0, 'o', **kwargs)
                elif value:
                    kwargs = dict(markersize=15, color='#991B1E')
                    plt.plot(0,0, 'o', **kwargs)
                
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
                    plt.plot(*path, color=colors[order])
                else:
                    plt.plot(*path, color=colors[order], label=attr.name)
        plt.plot(*self.leylines.founts[:,1:], 'ok', fillstyle='full', markersize=8)
        plt.plot(*self.leylines.founts[:,0], 'ok', fillstyle='none', markersize=8)
        if legend and legend_kwargs:
            plt.legend(**legend_kwargs)
        elif legend:
            ax.legend(loc='upper left',
                      bbox_to_anchor=(1.02, 0.8))

        plt.axis('off')
        
        return fig, ax
            
if __name__ == '__main__':
    from glyphloom.data.fifth_edition import SpellData_5e
    
    spelldata = SpellData_5e.get_spell('Flame Strike5', 
                                       'offline')
    leylines = geometry.Leylines(
        founts=geometry.Founts(
            n_points=13,
            expression=None),
        expression='linear')
    Glyph(spelldata, leylines).draw(legend=True)