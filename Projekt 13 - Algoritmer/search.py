# sorting algorithm would do "if i is bigger than i-1, then:"
def search(key,L): # Searchterm, liste
    for i in range(len(L)):
        #print(f"i={i},L[i]={L[i]}")
        if L[i] == key:
            return i

def searchall(key,L): # Searchterm, liste
    idx = []
    for i in range(len(L)):
        #print(f"i={i},L[i]={L[i]}")
        if L[i] == key:
            idx.append(i)
    return idx
    
if __name__ == "__main__": # only works in this document, doesn't work when importing function
    from numbers import numberlist
    numbers = numberlist
    num = int(input("Type a number to search for: "))
    idx = search(num,numbers)
    if idx is not None:
        print(f"{num} was found at {idx}.")
    else:
        print(f"{num} does not appear to be in the list.")
