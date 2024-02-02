import numpy as np
import matplotlib.pyplot as plt

from . import sub_utils_plot as su

def show_truss_init(nodes_coor: np.ndarray, elements_connect: np.ndarray, title: str = 'Initial truss\nClose to continue', color: str='k') -> plt.axes:
    """show the loaded truss

    Args:
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        elements_connect (np.ndarray): 2D ndarray of elements connectivities
        title (str, optional): title of the plot. Defaults to 'Initial truss\nClose to continue'
        color (str, optional): color of the truss
        
    Return:
        ax (plt.axes): used axis
    """
    h = 5
    r = 4/3
    
    fig, ax = plt.subplots(figsize=(h*r, h))
    ax.grid()
    ax.axis('equal')
    for nodes_connected in elements_connect:
        x_plot = nodes_coor[nodes_connected, 0]
        y_plot = nodes_coor[nodes_connected, 1]
        ax.plot(x_plot, y_plot, '-o', lw=2, markersize=10, color=color)

    ax.set_title(title)
    return ax

def show_add_BC(ax:plt.axes, restricted_dof: list, nodes_coor: np.ndarray, loaded_dof: list, values_load:list) -> plt.axes:
    """illustrate all Boundary Conditions by completing axis 'ax'

    Args:
        ax (plt.axes): axis with init truss to complete
        restricted_dof (list): list of degree of freedom restricted to 0
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        loaded_dof (list): list of dof with imposed load
        values_load (list): values of all imposed load

    Returns:
        ax (plt.axes): used axis
    """
    # get main dimension
    height = np.max(nodes_coor[:,1])-np.min(nodes_coor[:,1])
    length = np.max(nodes_coor[:,0])-np.min(nodes_coor[:,0])
    s = np.min([height, length])/10         # box drawing parameter
    
    count = 0
    while count < len(restricted_dof):
        nb_dof = restricted_dof[count]
        nb_node = int(nb_dof/2)
        coor = nodes_coor[nb_node, :]
        
        if nb_dof % 2 == 0:
            if nb_dof+1 in restricted_dof:
                ax = su.plot_bc_xy(ax, coor, s)
            else:
                ax = su.plot_bc_x(ax, coor, s)
            count += 2
        else:
            ax = su.plot_bc_y(ax, coor, s)
            count += 1
    
    s = 3*s         # arrow drawing parameter
    
    for count, load in enumerate(values_load):
        nb_dof = loaded_dof[count]
        nb_node = int(nb_dof/2)
        coor = nodes_coor[nb_node, :]
        
        if nb_dof % 2 == 0:
            ax = su.plot_load_x(ax, coor, load, s)
        else:
            ax = su.plot_load_y(ax, coor, load, s)
    
    return ax

def show_add_deformed(ax: plt.axes, nodes_coor: np.ndarray, shaped_nodal_displacements: np.ndarray, elements_connect: np.ndarray, scaling: float = 10, stress: np.ndarray = None) -> plt.axes:
    """Add to axe 'ax' the deformed truss

    Args:
        ax (plt.axes): axis to complete
        nodes_coor (np.ndarray): 2D ndarray of nodes coordinates
        shaped_nodal_displacements (np.ndarray): 2D ndarray of all nodal displacements
        elements_connect (np.ndarray): 2D ndarray of elements connectivities
        scaling (float, optinal): scaling of nodal displacements. Defaults to 10.
        stress (np.ndarray, optional): stress value for each element. Defaults to None

    Returns:
        plt.axes: used axis
    """
    deformed_truss = nodes_coor + scaling*shaped_nodal_displacements
    if stress is not None:
        norm_stress = 3*stress/np.max(np.abs(stress))
        for index, nodes_connected in enumerate(elements_connect):
            x_plot = deformed_truss[nodes_connected, 0]
            y_plot = deformed_truss[nodes_connected, 1]
            if stress[index] > 0:
                ax.plot(x_plot, y_plot, color='g', lw=norm_stress[index], marker='o', markersize=7)
            else:
                ax.plot(x_plot, y_plot, color='r', lw=norm_stress[index], marker='o', markersize=7)
        print('\nColor code:')
        print('    |- red -> compression')
        print('    |- green -> tension\n')
    else:
        for nodes_connected in elements_connect:
            x_plot = deformed_truss[nodes_connected, 0]
            y_plot = deformed_truss[nodes_connected, 1]
            ax.plot(x_plot, y_plot, '--ok', lw=1, markersize=7)
    
    return ax