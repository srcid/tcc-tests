from instances import instances_g1
from pytest import mark

from models.common_blocks import CommonBlocks


@mark.parametrize(
        'S1,S2,optval', instances_g1
)
def test_common_blocks(S1, S2, optval):
    m = CommonBlocks(S1, S2)
    r = m.solve('CPLEX', 1800000)
    val = r[0]
    assert val == optval