from search import search

def test_number():
    numbers = [23,13,24,11,32,42,12]
    assert search(24,numbers) == 2
    #print(f"Assert statement: {A}")

def test_numberall():
    numbers = [23,13,24,11,32,42,12,23]
    assert search(23,numbers) == 0,7

def test_string():
    list = ["hest","femboy","Noah","cuddles","lilla",":3"]
    assert search("Noah",list) == 2

def test_stringall():
    list = ["hest","femboy","Noah","cuddles","lilla",":3","Noah"]
    assert search("Noah",list) == 2,6