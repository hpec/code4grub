import urllib
import re
from collections import Counter
from collections import defaultdict

allInfo = defaultdict(Counter)
allFlag = defaultdict(Counter)

mindictKey = ["diff", "para", "number", "exclaim", "comment"]
mindictTemp = dict()
for ky in mindictKey:
    mindictTemp[ky] = float('inf')
getTokens = lambda text: map(lambda x: x[0]+x[1], re.findall("(\w+)(['-]\w+)?", text))
getAvg = lambda lst: sum(lst)*1.0/len(lst) if len(lst) > 0 else 0.0
getMed = lambda lst: sorted(lst)[len(lst)/2] if len(lst) > 0 else 0.0

for i in range(1, 31):
    txtfile = urllib.urlopen("http://www.cs.berkeley.edu/~jrs/coding4grub/"+str(i)+".txt")
    alltext = txtfile.read()
    
    allword = getTokens(alltext)
    allInfo[i] = Counter(allword)
    
    allword2 = []   # Get all pair of words.
    for k in range(len(allword)-1):
        allword2 += [allword[k] + allword[k+1]]
    allInfo[i] += Counter(allword2)
    
    allParaLength = map(lambda line: len(getTokens(line)), alltext.split("\n"))
    allFlag[i]["para"] = getAvg(allParaLength)
    allFlag[i]["comment"] = len(re.findall("\(", alltext))
    allFlag[i]["number"] = len(re.findall("[0-9]\)", alltext))
    allFlag[i]["exclaim"] = len(re.findall("!", alltext))
    
    
    
pairedUp = []
pairs = dict()

output = open("OUTPUT.txt","wb");

for i in range(1, 31):
    if i in pairedUp:
        continue
    mindict = mindictTemp.copy()
    mindictIndex = -1
    for j in range(1, 31):
        if j == i or j in pairedUp:
            continue
        testdict = mindictTemp.copy()

        diffCounter = (allInfo[i] - allInfo[j]) + (allInfo[j] - allInfo[i])
        testdict["diff"] = getAvg(diffCounter.values())
        testdict["para"] = abs(allFlag[i]["para"] - allFlag[j]["para"])
        testdict["number"] = abs(allFlag[i]["number"] - allFlag[j]["number"])
        testdict["exclaim"] = abs(allFlag[i]["exclaim"] - allFlag[j]["exclaim"])
        testdict["comment"] = abs(allFlag[i]["comment"] - allFlag[j]["comment"])
        
        if getAvg(testdict.values()) < getAvg(mindict.values()):
            mindict = testdict
            mindictIndex = j
            
    print(str(i)+".txt"+","+str(mindictIndex)+".txt");
    output.write(str(i)+".txt"+","+str(mindictIndex)+".txt"+"\n");
    pairs[i] = mindictIndex
    pairs[mindictIndex] = i
    pairedUp += [i, mindictIndex]







