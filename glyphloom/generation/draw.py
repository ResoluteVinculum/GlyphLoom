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
        fig = plt.figure()
        plt.rcParams.update({
            "figure.facecolor":  (0.0, 0.0, 0.0, 0.0),  # red   with alpha = 30%
            "axes.facecolor":    (0.0, 0.0, 0.0, 0.0),  # green with alpha = 50%
            "savefig.facecolor": (0.0, 0.0, 0.0, 0.0),  # blue  with alpha = 20%
        })
        plt.title(self.spelldata.name)
        
        if not self.leylines.founts.n_points:
            fig.show()
            return fig
        
        cmap = plt.get_cmap('tab10')
        for attr in self.spelldata.collect_attributes().values():
            if not attr.glyph: continue
            order = attr.order
            options = attr.options
            value = getattr(self.spelldata, attr.name)
            
            if value is None: continue
            index = list(options).index(value)
        
            binary = self.leylines.necklace[index]
            paths = self.leylines.default_curves[order, binary.astype(bool)]
            for i, path in enumerate(paths):
                if i:
                    plt.plot(*path, color=cmap.colors[order])
                else:
                    plt.plot(*path, color=cmap.colors[order], label=attr.name)
        plt.plot(*self.leylines.founts[:,1:], 'ok', fillstyle='full', markersize=8)
        plt.plot(*self.leylines.founts[:,0], 'ok', fillstyle='none', markersize=8)
        if legend:
            plt.legend(**legend_kwargs)
        plt.axis('off')
        
        return fig
            
if __name__ == '__main__':
    from glyphloom.data.fifth_edition import SpellData_5e
    
    spelldata = SpellData_5e.get_spell('Modify Memory', 
                                       'offline')
    leylines = geometry.Leylines(
        founts=geometry.Founts(
            n_points=13,
            expression=(
                'array([0,1,2,3,4,5,6,7,8,9,10,11,12])', 
                'random.randint(0,25,13)*domain')),
        expression='linear')
    Glyph(spelldata, leylines).draw()