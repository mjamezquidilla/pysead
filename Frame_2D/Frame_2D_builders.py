from Frame_2D.Frame_2D import Member_2D
from typing import Type
import itertools
import inspect


def Frame_builder(x_spacing: list, 
                  y_spacing:list, 
                  cls_columns: Type[Member_2D], 
                  cls_beams: Type[Member_2D], 
                  cls_column_kwargs, 
                  cls_beams_kwargs) -> tuple:
    # For Columns
    params = inspect.signature(cls_columns.__init__).parameters
    valid_args_columns = {k: v for k, v in cls_column_kwargs.items() if k in params}
    
    # For Beams
    params = inspect.signature(cls_beams.__init__).parameters
    valid_args_beams = {k: v for k, v in cls_beams_kwargs.items() if k in params}
    
    x_coordinates = list(itertools.accumulate(x_spacing))
    y_coordinates = list(itertools.accumulate(y_spacing))

    x_coordinates.insert(0,0)
    y_coordinates.insert(0,0) 

    nodes = {i: [x, y]
            for i, (x, y) in enumerate(
                ((x, y) for y in y_coordinates for x in x_coordinates),
                start=1)}

    total_columns = len(y_spacing) * (len(x_spacing)+1)

    column_range = range(1, total_columns+1)

    columns: dict[str, Member_2D] = {}
    beams: dict[str, Member_2D] = {}

    member_number = 1
    
    for col in column_range:
        member = cls_columns(member_number=member_number, 
                             nodes={k: nodes[k] for k in (col, col + len(x_coordinates))}, 
                             **valid_args_columns)
        columns.update({'C' + str(col): member})
        member_number = member_number + 1

    beam = 1
    for k in range(len(x_coordinates), len(nodes) + 1):
        if k % len(x_coordinates) != 0:
            member = cls_beams(member_number=member_number, 
                               nodes={k: nodes[k] for k in (k, k + 1)},
                               **valid_args_beams)
            beams.update({'B' + str(beam): member})
            member_number = member_number + 1
            beam = beam + 1
            
    supports: dict[int, list[int]] = {k:[1,1,1] for k in range(1,len(x_coordinates)+1)}

    return columns, beams, supports

