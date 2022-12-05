import graph as graph

def create_butterfly_network():

    G = graph.DiGraph()

    G.add_vertex(1, is_source=True, pos=(0,0))
    G.add_vertex(2, pos=(1,1))
    G.add_vertex(3, pos=(1,-1))
    G.add_vertex(4, pos=(2,0))
    G.add_vertex(5, pos=(3,0))
    G.add_vertex(6, is_target=True, pos=(4,1))
    G.add_vertex(7, is_target=True, pos=(4,-1))

    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(2, 4)
    G.add_arc(2, 6)
    G.add_arc(3, 4)
    G.add_arc(3, 7)
    G.add_arc(4, 5)
    G.add_arc(5, 6)
    G.add_arc(5, 7)

    return G

def create_RIIS():

    G = graph.DiGraph()

    G.add_vertex(1, is_source=True, pos=(0,0))
    G.add_vertex(2, pos=(1,2))
    G.add_vertex(3, pos=(1,-2))
    G.add_vertex(4, pos=(3,1))
    G.add_vertex(5, pos=(3,-1))
    G.add_vertex(6, pos=(4,1))
    G.add_vertex(7, pos=(4,-1))
    G.add_vertex(8, is_target=True, pos=(5,2))
    G.add_vertex(9, is_target=True, pos=(5,1))
    G.add_vertex(10, is_target=True, pos=(5,0))
    G.add_vertex(11, is_target=True, pos=(5,-1))
    G.add_vertex(12, is_target=True, pos=(5,-2))

    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(2, 8)
    G.add_arc(2, 4)
    G.add_arc(2, 11)
    G.add_arc(2, 5)
    G.add_arc(3, 4)
    G.add_arc(3, 9)
    G.add_arc(3, 5)
    G.add_arc(3, 12)
    G.add_arc(4, 6)
    G.add_arc(5, 7)
    G.add_arc(6, 8)
    G.add_arc(6, 9)
    G.add_arc(6, 10)
    G.add_arc(7, 10)
    G.add_arc(7, 11)
    G.add_arc(7, 12)

    return G

def create_combination_5_3():

    G = graph.DiGraph()

    G.add_vertex(1, is_source=True, pos=(0,0))

    v2 = G.add_vertex(2, pos=(1,4))
    v3 = G.add_vertex(3, pos=(1,2))
    v4 = G.add_vertex(4, pos=(1,0))
    v5 = G.add_vertex(5, pos=(1,-2))
    v6 = G.add_vertex(6, pos=(1,-4))

    G.add_vertex(7, is_target=True, pos=(3,8))
    G.add_vertex(8, is_target=True, pos=(3,6))
    G.add_vertex(9, is_target=True, pos=(3,4))
    G.add_vertex(10, is_target=True, pos=(3,2))
    G.add_vertex(11, is_target=True, pos=(3,0))
    G.add_vertex(12, is_target=True, pos=(3,-2))
    G.add_vertex(13, is_target=True, pos=(3,-4))
    G.add_vertex(14, is_target=True, pos=(3,-6))
    G.add_vertex(15, is_target=True, pos=(3,-8))
    G.add_vertex(16, is_target=True, pos=(3,-10))

    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(1, 4)
    G.add_arc(1, 5)
    G.add_arc(1, 6)

    G.add_arc(2, 7)
    G.add_arc(3, 7)
    G.add_arc(4, 7)
    G.add_arc(2, 8)
    G.add_arc(3, 8)
    G.add_arc(5, 8)
    G.add_arc(2, 9)
    G.add_arc(3, 9)
    G.add_arc(6, 9)
    G.add_arc(2, 10)
    G.add_arc(4, 10)
    G.add_arc(5, 10)
    G.add_arc(2, 11)
    G.add_arc(4, 11)
    G.add_arc(6, 11)
    G.add_arc(2, 12)
    G.add_arc(5, 12)
    G.add_arc(6, 12)
    G.add_arc(3, 13)
    G.add_arc(4, 13)
    G.add_arc(5, 13)
    G.add_arc(3, 14)
    G.add_arc(4, 14)
    G.add_arc(6, 14)
    G.add_arc(3, 15)
    G.add_arc(5, 15)
    G.add_arc(6, 15)
    G.add_arc(4, 16)
    G.add_arc(5, 16)
    G.add_arc(6, 16)

    return G

def create_combination_5_2():

    G = graph.DiGraph()
    G.add_vertex(1, is_source=True, pos=(0,0))

    v2 = G.add_vertex(2, pos=(1,4))
    v3 = G.add_vertex(3, pos=(1,2))
    v4 = G.add_vertex(4, pos=(1,0))
    v5 = G.add_vertex(5, pos=(1,-2))
    v6 = G.add_vertex(6, pos=(1,-4))

    G.add_vertex(7, is_target=True, pos=(3,8))
    G.add_vertex(8, is_target=True, pos=(3,6))
    G.add_vertex(9, is_target=True, pos=(3,4))
    G.add_vertex(10, is_target=True, pos=(3,2))
    G.add_vertex(11, is_target=True, pos=(3,0))
    G.add_vertex(12, is_target=True, pos=(3,-2))
    G.add_vertex(13, is_target=True, pos=(3,-4))
    G.add_vertex(14, is_target=True, pos=(3,-6))
    G.add_vertex(15, is_target=True, pos=(3,-8))
    G.add_vertex(16, is_target=True, pos=(3,-10))

    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(1, 4)
    G.add_arc(1, 5)
    G.add_arc(1, 6)
    G.add_arc(2, 7)
    G.add_arc(3, 7)
    G.add_arc(2, 8)
    G.add_arc(4, 8)
    G.add_arc(2, 9)
    G.add_arc(5, 9)
    G.add_arc(2, 10)
    G.add_arc(6, 10)
    G.add_arc(3, 11)
    G.add_arc(4, 11)
    G.add_arc(3, 12)
    G.add_arc(5, 12)
    G.add_arc(3, 13)
    G.add_arc(6, 13)
    G.add_arc(4, 14)
    G.add_arc(5, 14)
    G.add_arc(4, 15)
    G.add_arc(6, 15)
    G.add_arc(5, 16)
    G.add_arc(6, 16)

    return G

def create_combination_5_2_mult():

    G = graph.DiGraph()

    G.add_vertex(0, is_source=True, pos=(-2,0))
    G.add_vertex(17, pos=(-1,0.5))
    G.add_vertex(18, pos=(-1,-0.5))
    
    G.add_vertex(1, pos=(0,0))

    v2 = G.add_vertex(2, pos=(1,4))
    v3 = G.add_vertex(3, pos=(1,2))
    v4 = G.add_vertex(4, pos=(1,0))
    v5 = G.add_vertex(5, pos=(1,-2))
    v6 = G.add_vertex(6, pos=(1,-4))

    G.add_vertex(7, is_target=True, pos=(3,8))
    G.add_vertex(8, is_target=True, pos=(3,6))
    G.add_vertex(9, is_target=True, pos=(3,4))
    G.add_vertex(10, is_target=True, pos=(3,2))
    G.add_vertex(11, is_target=True, pos=(3,0))
    G.add_vertex(12, is_target=True, pos=(3,-2))
    G.add_vertex(13, is_target=True, pos=(3,-4))
    G.add_vertex(14, is_target=True, pos=(3,-6))
    G.add_vertex(15, is_target=True, pos=(3,-8))
    G.add_vertex(16, is_target=True, pos=(3,-10))

    G.add_arc(0, 17)
    G.add_arc(0, 18)
    G.add_arc(17, 1)
    G.add_arc(18, 1)

    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(1, 4)
    G.add_arc(1, 5)
    G.add_arc(1, 6)
    G.add_arc(2, 7)
    G.add_arc(3, 7)
    G.add_arc(2, 8)
    G.add_arc(4, 8)
    G.add_arc(2, 9)
    G.add_arc(5, 9)
    G.add_arc(2, 10)
    G.add_arc(6, 10)
    G.add_arc(3, 11)
    G.add_arc(4, 11)
    G.add_arc(3, 12)
    G.add_arc(5, 12)
    G.add_arc(3, 13)
    G.add_arc(6, 13)
    G.add_arc(4, 14)
    G.add_arc(5, 14)
    G.add_arc(4, 15)
    G.add_arc(6, 15)
    G.add_arc(5, 16)
    G.add_arc(6, 16)

    return G

def create_4_2_mult():

    G = graph.DiGraph()

    G.add_vertex(0, is_source=True, pos=(-1,0))

    G.add_vertex(8, pos=(-0.5,0.5))
    G.add_vertex(9, pos=(-0.5,-0.5))

    G.add_vertex(1, pos=(0,0))
    G.add_vertex(2, pos=(1,2))
    G.add_vertex(3, pos=(1,-2))
    G.add_vertex(4, is_target=True, pos=(3,3))
    G.add_vertex(5, is_target=True, pos=(3,1))
    G.add_vertex(6, is_target=True, pos=(3,-1))
    G.add_vertex(7, is_target=True, pos=(3,-3))

    G.add_arc(0, 8)
    G.add_arc(0, 9)
    G.add_arc(8, 1)
    G.add_arc(9, 1)
    G.add_arc(1, 2)
    G.add_arc(1, 3)
    G.add_arc(2, 4)
    G.add_arc(2, 5)
    G.add_arc(2, 6)
    G.add_arc(2, 7)
    G.add_arc(3, 4)
    G.add_arc(3, 5)
    G.add_arc(3, 6)
    G.add_arc(3, 7)

    return G
    
def get_instance(instance_name):

    if instance_name == "butterfly":
        return create_butterfly_network()
    elif instance_name == "RIIS":
        return create_RIIS()
    elif instance_name == "comb5_3":
        return create_combination_5_3()
    elif instance_name == "comb5_2":
        return create_combination_5_2()
    elif instance_name == "comb5_2_mult":
        return create_combination_5_2_mult()
    elif instance_name == "comb4_2_mult":
        return create_4_2_mult()
    else:
         print("ERROR: unknown instance")
    return None
