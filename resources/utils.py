import numpy as np

def load_nodes_coor(nodes_path: str) -> np.ndarray:
    """load coordinates of all nodes

    Args:
        nodes_path (str): path towards the file

    Returns:
        nodes_coor (np.ndarray): a 2D ndarray with first column the x coordinate and the second column the y coordinate
    """
    nodes_coor = np.loadtxt(nodes_path, dtype=float, delimiter=' ', skiprows=1)
    return nodes_coor

def load_elements_connect(elements_path: str) -> np.ndarray:
    """load elements connectivity (from nodeA to nodeB)

    Args:
        elements_path (str): path towards the file

    Returns:
        elements_connect (np.ndarray): a 2D ndarray with first column the first node connected to the element and the second the second node
    """
    elements_connect = np.loadtxt(elements_path, dtype=int, delimiter=' ', skiprows=1)
    return elements_connect

def get_cos_sin_Le(nodes: np.ndarray) -> tuple[float, float, float]:
    """get info for element connected to 'nodes'

    Args:
        nodes (np.ndarray): 2D ndarray of the nodes coordinates connected to the element

    Returns:
        tuple[float, float, float]: cosinus, sinus and element length
    """
    dx = nodes[1, 0]-nodes[0, 0]
    dy = nodes[1, 1]-nodes[0, 1]
    
    Le = np.sqrt(dx**2+dy**2)
    cos = dx/Le
    sin = dy/Le
    return cos, sin, Le

def stiffness_2D_truss(young: float, cross_section: float, cos: float, sin: float, Le: float) -> np.ndarray:
    """generate the stiffness matrix for one element

    Args:
        young (float): Young's modulus
        cross_section (float): section of the beam
        cos (float): cosinus of the angle
        sin (float): sinus of the angle
        Le (float): length of the beam

    Returns:
        np.ndarray: the stiffness matrix of the element
    """
    Ke = (young*cross_section)/Le * np.array([[cos**2, cos*sin, -cos**2, -cos*sin], [cos*sin, sin**2, -cos*sin, -sin**2],
                               [-cos**2, -cos*sin, cos**2, cos*sin], [-cos*sin, -sin**2, cos*sin, sin**2]])
    return Ke
