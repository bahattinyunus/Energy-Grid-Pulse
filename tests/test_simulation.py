import sys
import os
import pytest

# Add the project root to the python path to allow importing simulation_core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation_core.src.grid_manager import GridManager
from simulation_core.src.node import EnergyNode

def test_grid_initialization():
    grid = GridManager()
    assert grid.grid_frequency == 50.0
    assert len(grid.nodes) == 0

def test_add_node():
    grid = GridManager()
    node = EnergyNode(node_id="test_node", node_type="URETICI", capacity=100.0)
    grid.add_node(node)
    assert len(grid.nodes) == 1
    assert grid.nodes[0] == node

def test_stability_analysis_stable():
    grid = GridManager()
    # Balanced production and load
    prod = EnergyNode("gen", "URETICI", 100)
    prod.current_generation = 50
    cons = EnergyNode("load", "TUKETICI", 50)
    cons.current_load = 50
    
    grid.add_node(prod)
    grid.add_node(cons)
    
    status = grid.analyze_stability()
    assert status['durum'] == "STABIL"
    assert status['frekans'] == 50.0

def test_stability_analysis_unstable():
    grid = GridManager()
    # Over production -> Frequency increase
    prod = EnergyNode("gen", "URETICI", 100)
    prod.current_generation = 60
    cons = EnergyNode("load", "TUKETICI", 50)
    cons.current_load = 50
    
    grid.add_node(prod)
    grid.add_node(cons)
    
    status = grid.analyze_stability()
    # 50.0 + (10 * 0.01) = 50.1
    assert status['frekans'] > 50.0
