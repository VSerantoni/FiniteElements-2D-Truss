import numpy as np
import matplotlib.pyplot as plt

def plot_bc_xy(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y = coor
    s2 = 0.5*s
    ax.plot([x-s2, x+s2, x+s2, x-s2, x-s2], [y-s2, y-s2, y+s2, y+s2, y-s2], 'g', lw=2)
    return ax

def plot_bc_x(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y = coor
    s2 = 0.5*s
    s3 = 0.5*s2
    ax.plot([x-s3, x+s3, x+s3, x-s3, x-s3], [y-s2, y-s2, y+s2, y+s2, y-s2], 'g', lw=2)
    return ax

def plot_bc_y(ax: plt.axes, coor: np.ndarray, s: float) -> plt.axes:
    """plot square box around the node in coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y = coor
    s2 = 0.5*s
    s3 = 0.5*s2
    ax.plot([x-s2, x+s2, x+s2, x-s2, x-s2], [y-s3, y-s3, y+s3, y+s3, y-s3], 'g', lw=2)
    return ax

def plot_load_x(ax: plt.axes, coor: np.ndarray, load: float, s: float) -> plt.axes:
    """plot arrow in the node coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        load (float): load value with sign indicating the direction
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y = coor
    if load < 0:
        arrowstyle='-|>'
    else:
        arrowstyle='<|-'
        
    ax.annotate('', xy=(x, y), xytext=(x+s, y), arrowprops=dict(arrowstyle=arrowstyle, color='r', mutation_scale=20))
    return ax

def plot_load_y(ax: plt.axes, coor: np.ndarray, load: float, s: float) -> plt.axes:
    """plot arrow in the node coor

    Args:
        ax (plt.axes): ax to complete
        coor (np.ndarray): coordinates where to draw
        load (float): load value with sign indicating the direction
        s (float): size of the box

    Returns:
        ax (plt.axes): ax to return
    """
    x, y = coor
    if load < 0:
        arrowstyle='-|>'
    else:
        arrowstyle='<|-'
    
    ax.annotate('', xy=(x, y), xytext=(x, y+s), arrowprops=dict(arrowstyle=arrowstyle, color='r', mutation_scale=20))
    return ax