from resources.fea_2D_truss import FeaTruss2D

if __name__ == '__main__':
    
    # ===== GEOMETRY =====
    nodesCoor_path = './test/nodesCoor.txt'                  # nodes coordonates
    elementsConnect_path = './test/elementsConnect.txt'      # connectivity of each element
    
    # init FEA
    fea = FeaTruss2D(nodesCoor_path, elementsConnect_path, show=True)
    
    # ===== BOUNDARY CONDITIONS =====
    restricted_dof = [0, 1, 9]
    loaded_dof = [3, 7, 11]
    values_load = [-50000, -100000, -50000]
    
    fea.set_BC(restricted_dof, loaded_dof, values_load, show_BC=True)
    
    # ===== STIFFNESS =====
    # paremeters
    E = 70000
    A = 300
    fea.eval_stiffness(E, A)
    
    # ===== SOLVE =====
    fea.solve()
    
    # ===== POST-PROCESSING =====
    fea.eval_reactions()
    fea.eval_stress()
    fea.show_deformed(compare_init=True, colored_stress=True)
    
    