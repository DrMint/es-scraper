from urllib.parse import urlparse, parse_qsl

query = "gameid=3494&media=support-2D&hd=0®ion=jp&num=5&version=&maxwidth=338&maxheight=190"

parsedQuery = parse_qsl(query)

numPart = [e for e in parsedQuery if e[0] == "num"]
num = ""
if len(numPart) != 0:
    num = numPart[0][1]

print(num)

