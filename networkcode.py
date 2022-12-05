import gurobipy as gp
import graph as graph
import itertools as it
from itertools import chain, combinations
import re

def create_strings(alpha, size):
    '''
    creates all strings of length size for a given alphabet
    alpha - the alphabet
    size  - length of the strings to be generated
    '''

    return [elem for elem in it.product(*[alpha for i in range(size)])]

def string_name(string):
    '''
    replaces special characters such as whitespaces and % in strings by #
    string - string to be processed
    '''

    name, n = re.subn('[(\|)\| ]', '', string.replace(',','#'))
    if name.endswith('#'):
        return name[:-1]
    return name

def powerset(iterable):
    '''
    creates the powerset of an iterable object
    iterable - object to compute powerset of
    '''
    
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def create_variables(m, G, alpha, code):
    '''
    creates the variables of the unambiguous code model
    m     - Gurobi model for which variables are created
    G     - graph for which we want to compute the code
    alpha - the alphabet
    code  - indices of code words
    '''

    vertices = G.get_vertices()

    # variables to indicate the input at a vertex
    var_input_at_node = {}
    for c in code:
        for v in vertices:

            # sources have no input
            if v.is_source:
                continue

            vl = v.get_label()
            in_arcs = G.get_in_arcs(vl)
            assert not in_arcs is None

            in_strings = create_strings(alpha, len(in_arcs))
            for in_str in in_strings:
                varname = "varinCode{}Node{}Str{}".format(c,vl,string_name(str(in_str)))
                var_input_at_node[c,v,in_str] = m.addVar(vtype=gp.GRB.BINARY, name=varname)

    # variables to indicate output at vertex
    var_output_at_node = {}
    for c in code:
        for v in vertices:

            # targets have no output
            if v.is_target:
                continue

            vl = v.get_label()
            out_arcs = G.get_out_arcs(vl)
            assert not out_arcs is None

            out_strings = create_strings(alpha, len(out_arcs))
            for out_str in out_strings:
                varname = "varoutCode{}Node{}Str{}".format(c,vl,string_name(str(out_str)))
                var_output_at_node[c,v,out_str] = m.addVar(vtype=gp.GRB.BINARY, name=varname)

    # variables to indicate maps
    var_map_at_node = {}
    for v in vertices:

        # sources and targets don't require a map
        if v.is_source or v.is_target:
            continue

        vl = v.get_label()
        in_arcs = G.get_in_arcs(vl)
        out_arcs = G.get_out_arcs(vl)
        assert not in_arcs is None
        assert not out_arcs is None

        in_strings = create_strings(alpha, len(in_arcs))
        out_strings = create_strings(alpha, len(out_arcs))
        for in_str in in_strings:
            for out_str in out_strings:
                inname = string_name(str(in_str))
                outname = string_name(str(out_str))
                varname = "mapNode{}In{}Out{}".format(v,inname,outname)
                var_map_at_node[v,in_str,out_str] = m.addVar(vtype=gp.GRB.BINARY, name=varname)

    return var_input_at_node, var_output_at_node, var_map_at_node

def create_constraints(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node):
    '''
    creates the basic constraints of the unambiguous code model
    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    code               - indices of code words
    var_input_at_node  - variables modeling the input at vertices
    var_output_at_node - variables modeling the output at vertices
    var_map_at_node    - variables modeling the maps at vertices
    '''

    vertices = G.get_vertices()

    # every vertex has exactly one input per code word
    for c in code:
        for v in vertices:
            if v.is_source:
                continue

            vl = v.get_label()
            in_arcs = G.get_in_arcs(vl)
            assert not in_arcs is None

            in_strings = create_strings(alpha, len(in_arcs))

            consname = "oneinputCode{}Node{}".format(c,vl)
            m.addConstr(gp.quicksum(var_input_at_node[c,v,in_str] for in_str in in_strings) == 1,
                        name=consname)

    # every vertex has exactly one output per code word
    for c in code:
        for v in vertices:
            if v.is_target:
                continue

            vl = v.get_label()
            out_arcs = G.get_out_arcs(vl)
            assert not out_arcs is None

            out_strings = create_strings(alpha, len(out_arcs))

            consname = "oneoutputCode{}Node{}".format(c,vl)
            m.addConstr(gp.quicksum(var_output_at_node[c,v,out_str] for out_str in out_strings) == 1,
                        name=consname)

    # construct maps at vertices
    for v in vertices:
        if v.is_source or v.is_target:
            continue
        
        vl = v.get_label()
        in_arcs = G.get_in_arcs(vl)
        out_arcs = G.get_out_arcs(vl)
        assert not in_arcs is None
        assert not out_arcs is None

        in_strings = create_strings(alpha, len(in_arcs))
        out_strings = create_strings(alpha, len(out_arcs))
        
        # every vertex sends an input string to at most one output string
        for in_str in in_strings:
            consname = "mapatmost#{}#{}".format(vl,string_name(str(in_str)))
            m.addConstr(gp.quicksum(var_map_at_node[v,in_str,out_str] for out_str in out_strings) <= 1,
                        name=consname)

        # every vertex has at least one output string when it receives an input
        for in_str in in_strings:
            for c in code:
                consame = "mapsatleast#{}#{}#{}".format(vl,string_name(str(in_str)),c)
                m.addConstr(var_input_at_node[c,v,in_str] <=
                            gp.quicksum(var_map_at_node[v,in_str,out_str] for out_str in out_strings),
                            name=consname)

        # relation between input, maps, and output
        for c in code:
            for out_str in out_strings:
                consname = "maps#{}#{}#{}".format(vl,out_str,c)
                m.addConstr(var_output_at_node[c,v,out_str] ==
                            gp.quicksum(var_input_at_node[c,v,in_str]*var_map_at_node[v,in_str,out_str]
                                        for in_str in in_strings),
                            name=consname)

    # there are no ambiguities
    for v in vertices:
        if not v.is_target:
            continue

        vl = v.get_label()
        in_arcs = G.get_in_arcs(vl)
        assert not in_arcs is None

        in_strings = create_strings(alpha, len(in_arcs))
        for in_str in in_strings:
            consname = "noambig#{}#{}".format(vl,string_name(str(in_str)))
            m.addConstr(gp.quicksum(var_input_at_node[c,v,in_str] for c in code) <= 1,
                        name=consname)
        
    # input and output need to be compatible
    arcs = G.get_arcs();
    for arc in arcs:

        u = arc.get_tail()
        v = arc.get_head()
        ul = u.get_label()
        vl = v.get_label()
        
        in_arcs = G.get_in_arcs(vl)
        out_arcs = G.get_out_arcs(ul)
        assert not in_arcs is None
        assert not out_arcs is None

        pos_in_arcs = [i for i in range(len(in_arcs))
                       if in_arcs[i].get_tail() == u and in_arcs[i].get_head() == v]
        pos_out_arcs = [i for i in range(len(out_arcs))
                        if out_arcs[i].get_tail() == u and out_arcs[i].get_head() == v]
        assert len(pos_in_arcs) >= 1
        assert len(pos_out_arcs) >= 1

        in_strings = create_strings(alpha, len(in_arcs))
        out_strings = create_strings(alpha, len(out_arcs))

        for c in code:
            for i in pos_in_arcs:
                for j in pos_out_arcs:
                    for in_str in in_strings:
                        consname = "compatible{}#{}#{}#{}#{}".format(arc,c,i,j,string_name(str(in_str)))
                        m.addConstr(var_input_at_node[c,v,in_str] +\
                                    gp.quicksum(var_output_at_node[c,u,out_str]
                                                for out_str in out_strings
                                                if in_str[i] != out_str[j])
                                    <= 1, name=consname
                                    )

def symmetry_handling(m, G, alpha, code, var_output_at_node):
    '''
    handles symmetries, currently implemented methods:
       1) so-called column inequalities are used to enforce that the
          different output strings of the first source are assigned
          in lexicographic order

    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    code               - indices of code words
    var_output_at_node - variables modeling the output at vertices
    '''

    print("APPLY SYMMETRY HANDLING: sort code words at first source")

    # sort the output of the first source non-increasingly
    vertices = G.get_vertices()
    for v in vertices:
        if not v.is_source:
            continue

        vl = v.get_label()
        out_arcs = G.get_out_arcs(vl)
        assert not out_arcs is None

        out_strings = create_strings(alpha, len(out_arcs))

        # the first code word takes the first out_string
        var_output_at_node[0,v,out_strings[0]].lb = 1

        # sort the remaining code words
        for c in range(1, len(code)):
            for j in range(len(out_strings)):
                m.addConstr(var_output_at_node[c,v,out_strings[j]] <=\
                            gp.quicksum(var_output_at_node[c-1,v,out_strings[i]] for i in range(j)),
                            name="symAtNode{}#{}#{}".format(vl,c,j))

        break

def preprocessing(m, G, alpha, var_map_at_node):
    '''
    preprocesses the model, currently implemented methods:
       1) if an intermediate vertex has in-degree 1, then the map
          at this vertex is w.l.o.g. the identity
    
    m               - Gurobi model for which variables are created
    G               - graph for which we want to compute the code
    alpha           - the alphabet
    code            - indices of code words
    var_map_at_node - variables modeling the maps at vertices
    '''

    print("APPLY PREPROCESSING: intermediate vertices with in-degree 1 have identity map")
    # maps of non-sink and non-target vertices with in-degree are the identity map
    for v in G.get_vertices():
        # skip vertices which are sources or targets or have the wrong in-degree
        if v.is_source or v.is_target:
            continue

        vl = v.get_label()

        if G.in_degree(vl) != 1:
            continue

        in_arcs = G.get_in_arcs(vl)
        out_arcs = G.get_out_arcs(vl)
        assert not in_arcs is None and len(in_arcs) == 1
        assert not out_arcs is None and len(out_arcs) > 0

        in_strings = create_strings(alpha, len(in_arcs))
        out_strings = create_strings(alpha, len(out_arcs))

        for in_str in in_strings:
            id_str = tuple(len(out_arcs) * [in_str[0]])
            for out_str in out_strings:
                # fix the identity map and forbid all others
                if out_str == id_str:
                    var_map_at_node[v,in_str,out_str].lb = 1.0
                else:
                    var_map_at_node[v,in_str,out_str].ub = 0.0
        

def add_cutting_planes(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node):
    '''
    adds cutting planes to the model, currently implemented methods:
       1) Inequalities derived from linearizing the expression
          var_output[c,v,out_str] = sum_{in_str} var_input[c,v,in_str] * map[v,in_str,out_str]
          and the fact that each code word sends at most one input to a vertex

    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    code               - indices of code words
    var_input_at_node  - variables modeling the input at vertices
    var_output_at_node - variables modeling the output at vertices
    var_map_at_node    - variables modeling the maps at vertices    
    '''

    # add cutting planes based on linearization and partitioning condition
    for c in code:
        for v in G.get_vertices():
            # skip vertices which are sources or targets
            if v.is_source or v.is_target:
                continue

            vl = v.get_label()
            out_arcs = G.get_out_arcs(vl)
            in_arcs = G.get_in_arcs(vl)
            assert not out_arcs is None
            assert not in_arcs is None

            out_strings = create_strings(alpha, len(out_arcs))
            in_strings = create_strings(alpha, len(in_arcs))
            ###
            # we add three classes of inequalities
            ###
            for out_str in out_strings:
                # NOTE: in principle correct, but too many for most applications
                # for I subset of input strings: input[I] + map[I^c,out_str] >= output[out_str]
                # for I in powerset(in_strings):
                #     m.addConstr(gp.quicksum(var_input_at_node[c,v,in_str] for in_str in I) +\
                #                 gp.quicksum(var_map_at_node[v,in_str,out_str] for in_str in in_strings if not in_str in I)
                #                 >= var_output_at_node[c,v,out_str])

                # for i in input strings: map[I\setminus{i},out_str] <= |input strings| - 2 + output[out_str] + input[i]
                for in_str in in_strings:
                    m.addConstr(gp.quicksum(var_map_at_node[v,i,out_str] for i in in_strings if i != in_str)
                                <= len(in_strings) - 2 + var_input_at_node[c,v,in_str] + var_output_at_node[c,v,out_str])

                # map[in_strings] <= |in_strings| = 1 + output[out_str]
                m.addConstr(gp.quicksum(var_map_at_node[v,in_str,out_str] for in_str in in_strings)
                            <= len(in_strings) - 1 + var_output_at_node[c,v,out_str])
            

def display_solution(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node):
    '''
    prints the solution to the screen
    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    code               - indices of code words
    var_input_at_node  - variables modeling the input at vertices
    var_output_at_node - variables modeling the output at vertices
    var_map_at_node    - variables modeling the maps at vertices    
    '''

    if m.Status == gp.GRB.INFEASIBLE or m.Status == gp.GRB.INF_OR_UNBD:
        print("there does not exist an unambiguous code")
        return

    if m.SolCount == 0:
        print("WARNING: cannot display solution, no solution found yet")
        return

    vertices = G.get_vertices()

    # display maps at vertices
    print("MAPS")
    for v in vertices:
        vl = v.get_label()
        print("map at {}".format(vl))

        if v.is_source:
            print("\tno map since {} is source".format(vl))
        elif v.is_target:
            print("\tno map since {} is target".format(vl))
        else:
            in_arcs = G.get_in_arcs(vl)
            out_arcs = G.get_out_arcs(vl)
            assert not in_arcs is None
            assert not out_arcs is None

            out_neighbors = [arc.get_head().get_label() for arc in out_arcs]
            print("\tarcs pointing to neighbors in order {}".format(out_neighbors))

            in_strings = create_strings(alpha, len(in_arcs))
            out_strings = create_strings(alpha, len(out_arcs))
            for in_str in in_strings:
                result = "?"
                for out_str in out_strings:
                    if var_map_at_node[v,in_str,out_str].X > 0.5:
                        result = string_name(str(out_str))
                        break

                print("\t{} -> {}".format(string_name(str(in_str)), result))
            
    print("\nCODE WORDS")
    for c in code:
        print("\tword %d" % c)
        for v in vertices:
            if v.is_target:
                continue

            vl = v.get_label()
            out_arcs = G.get_out_arcs(vl)
            assert not out_arcs is None

            out_strings = create_strings(alpha, len(out_arcs))

            out_neighbors = [arc.get_head().get_label() for arc in out_arcs]
            for out_str in out_strings:
                if var_output_at_node[c,v,out_str].X > 0.5:
                    print("\t\t{} -> {} arcs pointing to neighbors in order {}".format(vl, string_name(str(out_str)),out_neighbors))

def verify_solution(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node):
    '''
    verifies whether solution of Gurobi model indead models an unambiguous network code
    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    code               - indices of code words
    var_input_at_node  - variables modeling the input at vertices
    var_output_at_node - variables modeling the output at vertices
    var_map_at_node    - variables modeling the maps at vertices    
    '''    

    # infeasible models cannot be verified
    if m.Status == gp.GRB.INFEASIBLE or m.Status == gp.GRB.INF_OR_UNBD:
        return

    if m.SolCount == 0:
        print("WARNING: cannot verify solution, no solution found yet")
        return

    vertices = G.get_vertices()

    # check whether each code word is propagated correctly
    for c in code:
        for v in vertices:

            if v.is_source or v.is_target:
                continue

            vl = v.get_label()
            in_arcs = G.get_in_arcs(vl)
            out_arcs = G.get_out_arcs(vl)
            assert not in_arcs is None
            assert not out_arcs is None

            in_strings = create_strings(alpha, len(in_arcs))
            out_strings = create_strings(alpha, len(out_arcs))

            # find input at vertex
            nodeinput = None
            for in_str in in_strings:
                if var_input_at_node[c,v,in_str].X > 0.5:
                    nodeinput = in_str
                    break

            # find output at vertex
            nodeoutput = None
            for out_str in out_strings:
                if var_output_at_node[c,v,out_str].X > 0.5:
                    nodeoutput = out_str
                    break

            if var_map_at_node[v,nodeinput,nodeoutput].X < 0.5:
                print("ERROR: code is not propagated correctly")

    print("everything fine, code has been propagated correctly")

def fix_maps(maps, var_map_at_node):
    '''
    fixes the maps at specified vertices
    maps               - dictonary modeling the maps at some vertices
    var_map_at_node    - variables modeling the maps at vertices    
    '''

    for (v, in_str) in maps:
        var_map_at_node[v,in_str,maps[v,in_str]].lb = 1.0

def fix_code(init_code, var_output_at_node):

    nodes_fixed_code = set()
    # fix used code words
    for (c,v) in init_code:        
        var_output_at_node[c,v,init_code[c,v]].lb = 1.0
        nodes_fixed_code.add(v)

    # forbid other code words
    # for (c,v,out_str) in var_output_at_node:
    #     if v in nodes_fixed_code and not (c,v,out_str) in init_code:
    #         var_output_at_node[c,v,out_str].ub = 0.0
    
def create_maps_from_solution(m, G, alpha, var_map_at_node):
    '''
    extracts maps at each vertex from a solution of the Gurobi model,
    returns None in case of an infeasible model
    m                  - Gurobi model for which variables are created
    G                  - graph for which we want to compute the code
    alpha              - the alphabet
    var_map_at_node    - variables modeling the maps at vertices    
    
    '''

    # only apply method for feasible models
    if m.Status == gp.GRB.INFEASIBLE or m.Status == gp.GRB.INF_OR_UNBD:
        return None

    if m.SolCount == 0:
        print("WARNING: cannot create maps, no solution found yet")
        return

    maps = {}
    for v in G.get_vertices():
        
        if v.is_source or v.is_target:
            continue

        vl = v.get_label()
        in_arcs = G.get_in_arcs(vl)
        out_arcs = G.get_out_arcs(vl)
        assert not in_arcs is None
        assert not out_arcs is None

        in_strings = create_strings(alpha, len(in_arcs))
        out_strings = create_strings(alpha, len(out_arcs))

        for in_str in in_strings:
            for out_str in out_strings:
                if var_map_at_node[v,in_str,out_str].X > 0.5:
                    maps[v,in_str] = out_str

    return maps
    
def create_code_from_solution(m, G, alpha, var_output_at_node):

    # only apply method for feasible models
    if m.Status == gp.GRB.INFEASIBLE or m.Status == gp.GRB.INF_OR_UNBD:
        return None

    code_words = {}
    for v in G.get_vertices():
        if not v.is_source:
            continue

        for (c,w,out_str) in var_output_at_node:
            if w != v or var_output_at_node[c,w,out_str].X < 0.5:
                continue
            code_words[c,w] = out_str

    return code_words
    
def find_unambiguous_code2(G, size_alpha, size_code, handle_symmetries=True, add_cuts=True,
                           apply_preprocessing=True, init_maps=None, init_code=None):
    '''
    finds an unambigious network code or proves that none exists
    G          - network to be used
    size_alpha - size of the underlying alphabet
    size_code  - size of code to be found

    optional input:
    handle_symmetries   - whether symmetry handling methods are applied
    add_cuts            - whether cutting planes are added
    apply_preprocessing - whether preprocessing is applied
    init_maps           - dictionary with keys (v,in_str) modeling how in_str is transformed
                          at vertex v
    init_code           - dictionary with keys (c,v) modeling the code word c on the out-arcs
                          of vertex v
    '''

    alpha = range(size_alpha)
    code = range(size_code)

    m = gp.Model()

    # create variables and constraints
    var_input_at_node, var_output_at_node, var_map_at_node = create_variables(m, G, alpha, code)
    create_constraints(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node)

    # handle options    
    if handle_symmetries:
        if not init_maps is None:
            print("WARNING: symmetric handling is active and initial maps are provided, which can be conflicting")
        symmetry_handling(m, G, alpha, code, var_output_at_node)

    if add_cuts:
        add_cutting_planes(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node)

    if apply_preprocessing:
        if not init_maps is None:
            print("WARNING: preprocessing is active and initial maps are provided, which can be conflicting")
        preprocessing(m, G, alpha, var_map_at_node)

    if not init_maps is None:
        fix_maps(init_maps, var_map_at_node)

    if not init_code is None:
        fix_code(init_code, var_output_at_node)

    m.Params.Heuristics = 0.9
    m.optimize()

    display_solution(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node)
    verify_solution(m, G, alpha, code, var_input_at_node, var_output_at_node, var_map_at_node)

    # create maps
    maps = create_maps_from_solution(m, G, alpha, var_map_at_node)

    # create code for sources
    code_words = create_code_from_solution(m, G, alpha, var_output_at_node)    

    return maps, code_words

