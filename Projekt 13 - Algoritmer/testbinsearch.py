from binsearch import binsearch

#pip install pytest
#pytest test_binsearch.py


def test_number():
    assert binsearch(5,[5]) == 0

def test_negative_number():
    assert binsearch(-7,[-10,-7,3,7,8,9,10,11]) == 1

def test_no_number():
    assert binsearch(7,[0,1,2,3,4,5,6,8]) == None

def test_no_sorted_list():
    assert binsearch(6,[6,1,2,3,4,5,7]) == None

def test_passes_but_bad_style():
    try:
        binsearch(6,[])
    except ValueError as e:
        print(e)
        assert True

"""
with pytest.raises(ValueError, match='must be 0 or None'):
    raise ValueError('value must be 0 or None')"""