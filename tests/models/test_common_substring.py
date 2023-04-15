from instances import instances_g1
from pytest import mark

from models.common_substring import CommonSubstring


@mark.parametrize(
        'S1,S2,optval', instances_g1
)
def test_common_substring(S1, S2, optval):
    m = CommonSubstring(S1, S2)
    r = m.solve('CPLEX', 1800000)
    val = r[0]
    assert val == optval