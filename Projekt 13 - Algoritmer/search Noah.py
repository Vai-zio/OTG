# sorting algorithm would do "if i is bisgger than i-1, then:"

def search(key,L): # Searchterm, liste
    keys = []
    for i in range(len(L)):
        #print(f"i={i},L[i]={L[i]}")
        if L[i] == key:
            keys.append(i)
    if keys == []:
        return None
    elif keys != []:
        return keys
    
if __name__ == "__main__": # only works in this document, doesn't work when importing function
    numbers = [9,32,4,324,3,42,2,3,2,32,32,3,1,657763,46,346,7,62,2,523]
    num = int(input("Type a number to search for: "))
    idx = search(num,numbers)
    if idx is not None:
        print(f"{num} was found at {idx}.")
    else:
        print(f"{num} does not appear to be in the list.")
