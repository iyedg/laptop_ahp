import pytest

from ahppy import AHP
from anytree import Node, AsciiStyle, RenderTree


@pytest.fixture()
def jones_problem():
    return AHP(criteria=[
        "cost",
        "cost.purchase_price",
        "cost.fuel_costs",
        "cost.maintenance_costs",
        "cost.resale_value",
        "cost.resale_value.cash",
        "cost.resale_value.wait",
        "safety",
        "style",
        "capacity",
        "capacity.cargo_capacity",
        "capacity.passenger_capacity"
    ], alternatives=[], goal="best_car")


def test_model_tree(jones_problem):
    goal = Node("best_car")

    cost = Node("cost", parent=goal)
    safety = Node("safety", parent=goal)
    style = Node("style", parent=goal)
    capacity = Node("capacity", parent=goal)

    purchase_price = Node("purchase_price", parent=cost)
    fuel_costs = Node("fuel_costs", parent=cost)
    maintenance_costs = Node("maintenance_costs", parent=cost)
    resale_value = Node("resale_value", parent=cost)

    cash = Node("cash", parent=resale_value)
    wait = Node("wait", parent=resale_value)

    cargo_capacity = Node("cargo_capacity", parent=capacity)
    passenger_capacity = Node("passenger_capacity", parent=capacity)

    assert goal.depth == jones_problem.tree.depth
    assert str(RenderTree(goal, style=AsciiStyle())) == str(RenderTree(
        jones_problem.tree, style=AsciiStyle()))
