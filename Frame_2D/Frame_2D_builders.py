from Frame_2D.Frame_2D import Frame_2D, Member_2D
import itertools

def Frame_builder(x_spacing: list, y_spacing:list) -> Frame_2D:
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

    columns = {}
    beams = {}

    member_number = 1

    
    for col in column_range:
        columns.update({'C' + str(col): Member_2D(member_number=member_number, area=0.18, elasticity=25_000, inertia=0.005, nodes={k: nodes[k] for k in (col, col + len(x_coordinates))})})
        member_number = member_number + 1

    beam = 1
    for k in range(len(x_coordinates), len(nodes) + 1):
        if k % len(x_coordinates) != 0:
            beams.update({'B' + str(beam): Member_2D(member_number=member_number, area=0.18, elasticity=25_000, inertia=0.005, nodes={k: nodes[k] for k in (k, k + 1)})})
            member_number = member_number + 1
            beam = beam + 1

    members_dict = columns | beams

    Frame = Frame_2D()
    Frame.Compile_Frame_Member_Properties(members_dict)
    Frame.supports = {k:[1,1,1] for k in range(1,len(x_coordinates)+1)}

    return Frame

def get_all_beams(Frame: Frame_2D):
    beams = [k for k in Frame.members if k.startswith('B')]
