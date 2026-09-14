L = [2323,2,43,5,65,7,4,14,4,75,24,26,57,6,3,367,76,745,653,543,45,34,24,4646,5,2,346,4,3,25346,475,735754,292,2000000]

def find_max(L):
    cur_max = L[0]
    for i in range(1,len(L)):
        print("i:",i,"L[i]:", L[i])
        if cur_max < L[i]:
            cur_max = L[i]
    return cur_max

m = find_max(L) 
print("Max should be:", m)


# Definering af funktion (find maks integer):
#   nuværende maksimum sætter vi til at være lig med listens første integer
#   for hver ting i længden af listen, starter fra det næste tal:
#       Hvis nuværende maksimum er mindre end næste tal:
#           Sæt nuværende maksimum til det nye tal
#   retuner nuværende maksimum

alle_videoer = ["lang liste af video id's"]
def anbefal_video(bruger):
    relevante_videoer = []
    for video in alle_videoer:
        score = 0
        if video.hashtag in bruger.interesser:
            score += 3
        if video.type in bruger.tidligere_likes:
            score += 5
        if video.varighed_set > 0.8:
            score += 7
        relevante_videoer.append((video, score))
    
    sorterede = find_max(relevante_videoer) #sort_by_score kan være ligesom maks algoritmen
    return sorterede[:10]  # returnér top 10 videoer
