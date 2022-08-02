import pytest
from Func_wheel_rate import RSF_wheel_rate

def test_wheel_rate_decreasing():
    rate=100
    ratio=2
    rate_mod=200
    ratio_mod=1.0000000001
    results = RSF_wheel_rate(rate, ratio, rate_mod, ratio_mod)
    assert results[0]<rate
    assert results[1]<rate_mod

def test_wheel_rate_increasing():
    rate=100
    ratio=0.5
    rate_mod=200
    ratio_mod=0.9999999999
    results = RSF_wheel_rate(rate, ratio, rate_mod, ratio_mod)
    assert results[0]>rate
    assert results[1]>rate_mod

#TODO: error handling tests
