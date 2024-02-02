import numpy as np
import matplotlib.pyplot as plt

from . import utils as ut
from . import utils_plot as up

class FeaTruss2D():
    
    def __init__(self, NodesCoorPath: str, ElementsConnectPath: str, show: bool = False) -> None:
        """Finite Element Analysis -> init

        Args:
            NodesCoorPath (str): path towards nodes coordinates
            ElementsConnectPath (str): path towards elements connections
            show (bool, optional): plot the init truss
        """
        # input parameters
        self.nodes_path = NodesCoorPath
        self.elements_path = ElementsConnectPath
        
        # load all
        self.nodes_coor = ut.load_nodes_coor(self.nodes_path)
        self.elements_connect = ut.load_elements_connect(self.elements_path)
        
        self.nbNodes = self.nodes_coor.shape[0]
        self.nbElements = self.elements_connect.shape[0]
        self.dof = 2*self.nbNodes
        
        if show:
            _ = up.show_truss_init(self.nodes_coor, self.elements_connect)
            plt.show()
    
    def set_BC(self, restricted_dof: list, loaded_dof: list, values_load: list, show_BC: bool = True):
        """set parameters for the boundary conditions

        Args:
            restricted_dof (list): list of degree of freedom restricted to 0
            loaded_dof (list): list of dof with imposed load
            values_load (list): values of all imposed load
            show_BC (bool, optional): plot the init truss with restricted dof and imposed load. Defaults to True.
        """
        self.restricted_dof = restricted_dof
        
        self.loads = np.zeros([self.dof])
        for count, index in enumerate(loaded_dof):
            self.loads[index] = values_load[count]
        
        if show_BC:
            ax = up.show_truss_init(self.nodes_coor, self.elements_connect)
            _ = up.show_add_BC(ax, self.restricted_dof, self.nodes_coor, loaded_dof, values_load)
            plt.show()
        
    def eval_stiffness(self, Young: float, CrossSection: float) -> None:
        """evaluate the global stiffness matrix

        Args:
            Young (float): the Young's modulus
            CrossSection (float): the cross section area of all elements
        """
        self.young = Young
        self.area = CrossSection
        
        # get the stiffness matrix
        self.Kg = np.zeros([self.dof, self.dof])    

        # loop on each element
        for nodes_connected in self.elements_connect:
            cos, sin, Le = ut.get_cos_sin_Le(self.nodes_coor[nodes_connected])
            
            # Stiffness matrix for this element
            Ke = ut.stiffness_2D_truss(self.young, self.area, cos, sin, Le)
            
            # Placing Ke inside Kg to construct it
            elementDof = np.array([nodes_connected[0]*2, nodes_connected[0]*2+1, nodes_connected[1]*2, nodes_connected[1]*2+1])
            self.Kg[elementDof[:,np.newaxis],elementDof] += Ke
        
    def solve(self) -> None:
        """evaluate the nodal displacement using the relation Kg.U = F
        """
        not_restricted_dof = np.setdiff1d(np.arange(self.dof), self.restricted_dof)
        
        partial_displacements = np.linalg.solve(self.Kg[not_restricted_dof[:,np.newaxis],not_restricted_dof], self.loads[not_restricted_dof])
        self.nodal_displacements = np.zeros([self.dof])
        self.nodal_displacements[not_restricted_dof] = partial_displacements
        
        self.shaped_nodal_displacements = self.nodal_displacements.reshape((self.nbNodes,2))
        print('\nnodal dispalcements:')
        print(f'{self.shaped_nodal_displacements}\n')
        
    def eval_reactions(self) -> None:
        """evaluate nodal reactions
        """
        # self.reactions = np.matmul(self.Kg, self.nodal_displacements)
        self.reactions = self.Kg@self.nodal_displacements
        self.reactions[np.abs(self.reactions) < 1e-10] = 0
        
        self.shaped_reactions = self.reactions.reshape((self.nbNodes,2))
        print('\nnodal reactions:')
        print(f'{self.shaped_reactions}\n')
    
    def eval_stress(self, show_stress: bool = False) -> None:
        """evaluate the normal stress on each element
        
        Args:
            show_stress (bool, optional): showing illustration of stress values. Defaults to False
        """
        self.sigma = np.zeros(self.nbElements)
        for index, nodes_connected in enumerate(self.elements_connect):
            cos, sin, Le = ut.get_cos_sin_Le(self.nodes_coor[nodes_connected])
            # stress
            elementDof = np.array([nodes_connected[0]*2, nodes_connected[0]*2+1, nodes_connected[1]*2, nodes_connected[1]*2+1])[np.newaxis]
            self.sigma[index] = self.young/Le * np.array([[-cos, -sin, cos, sin]])@self.nodal_displacements[elementDof].T
        
        print('\nstress on each element:')
        print(f'{self.sigma[np.newaxis].T}\n')
        
    def show_deformed(self, compare_init: bool = True, colored_stress: bool = True) -> None:
        
        scaling = 10            # scaling factor to increase displayed deformation
        title = f'Deformed truss\nscaling factor: {scaling}'
        if compare_init:
            ax = up.show_truss_init(self.nodes_coor, self.elements_connect, title=title, color='gray')
        else:
            h = 5
            r = 4/3
            
            fig, ax = plt.subplots(figsize=(h*r, h))
            ax.grid()
            ax.axis('equal')
            ax.set_title(title)
        
        if colored_stress:
            ax = up.show_add_deformed(ax, self.nodes_coor, self.shaped_nodal_displacements, self.elements_connect, scaling, self.sigma)
        else:
            ax = up.show_add_deformed(ax, self.nodes_coor, self.shaped_nodal_displacements, self.elements_connect, scaling)
        
        plt.show()