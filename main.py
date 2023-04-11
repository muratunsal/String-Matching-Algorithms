from collections import defaultdict
import time

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

file_path = 'test1.html'
pattern_path = 'pattern.txt'

text = read_file(file_path)
pattern = read_file(pattern_path)

## --------------------------- 1.Brute Force Algorithm ----------------------

def Brute_Force_String_Matching(text:str, pattern:str) -> list:
    ''' Brute Force Algorithm for String Matching Problem
    \n inputs : text -> list of string to search sended pattern 
    \n          pattern -> a string to search in the text
    \n outputs: highlighted_text -> same text with marked by found locations
    \n          occurence_count -> how many pattern occurences in the text 
    \n          comparison -> how many character compared during run
    '''

    text_length = len(text)
    pattern_length = len(pattern)

    occurence_count = 0
    comparisons = 0
    occurence_locations = [] #matching locations to mark

    for i in range(text_length - pattern_length + 1): 
        #Main loop to search all text via incrementing index one by one

        j = 0
        while(j < pattern_length):
            #loop checks if each character of the pattern matches the corresponding character in the text
            #j keeps track of position in pattern
            comparisons += 1
            if(text[i+j] != pattern[j]):
                #if they are not matching breaks the inner loop
                break

            j += 1

        if(j == pattern_length):
            #If j is equal to the pattern length, it means that a complete occurrence of the pattern has been found,
            #  so the occurence_count is incremented
            # and the current location i is appended to the occurence_locations list

            occurence_count+=1
            occurence_locations.append(i)

    highlighted_text = text
    previous_location = 0
    collapse = 0

    for i, location in enumerate(occurence_locations):
        #  The loop iterates over the occurence_locations list,
        #  and for each location, it checks if the previous location and the current location are adjacent.
        #  If they are, it means that the occurrences are consecutive,
        #  so the corresponding substring in highlighted_text is modified accordingly to add the appropriate tags.
        #  If the locations are not adjacent, it means that there is a gap between consecutive occurrences,
        #  so the code modifies highlighted_text accordingly to add the tags in the correct positions.
        
        if((location - previous_location) == (pattern_length-1)):
            highlighted_text = highlighted_text[:location + ((i-collapse) * 13) - 6] \
                + highlighted_text[location + ((i-collapse)*13) + 1 : location + ((i-collapse)*13) + pattern_length] \
                    + '</mark>' + highlighted_text[location + ((i-collapse)*13) + pattern_length:]
            collapse +=1
            

        else:
            highlighted_text = highlighted_text[:location + ((i-collapse)*13)] \
            + '<mark>' \
                + highlighted_text[location + ((i-collapse) * 13)  : location + pattern_length+((i-collapse)*13)] \
                    + '</mark>'  \
                        + highlighted_text[location + pattern_length+((i-collapse)*13):]
            
        previous_location = location

    return highlighted_text, comparisons, occurence_count     

start_time = time.time()
marked_text, comparison_count, occurences = Brute_Force_String_Matching(text, pattern)
end_time = time.time()

brute_force_time = (end_time - start_time)*1000

print("--------------------- 1.Brute Force Algorithm -------------------")
print('Comparison Count: ', comparison_count)
print('Occurences: ', occurences)
print('Running time :', brute_force_time)


write_file = open('output1.html', 'w')
write_file.write(marked_text)
write_file.close()

print()



## --------------------------- 2.Horspool's Algorithm -----------------------

def highlight_text(text, pattern):
    occurrences = 0         # initializing the values
    comparisons = 0
    highlighted_text = text     # getting text of html file

    pattern_length = len(pattern)   # getting length of the pattern
    if pattern_length == 0:
        return highlighted_text, occurrences    # if the pattern not exist text and 0 occurrence will return

    shift_table = {}
    for i in range(pattern_length - 1):
        shift_table[pattern[i]] = pattern_length - i - 1    # creating a shift table

    shift_table["*"] = pattern_length

    i = 0
    while i <= len(text) - pattern_length:  # search until reaching the final index
        j = pattern_length - 1
        comparisons += 1    # increase by 1 at each comparison

        while j >= 0 and pattern[j] == text[i + j]: # if pattern and text character match, compare previous index
            j -= 1
            comparisons += 1    # increase by 1 at each comparison

        if j == -1:     # if j value is -1 that means our pattern match with our text
            highlighted_text = highlighted_text[:i+(occurrences*13)] + '<mark>' + highlighted_text[i+(occurrences*13):i+pattern_length+(occurrences*13)] + '</mark>' + highlighted_text[i+pattern_length+(occurrences*13):]
            occurrences += 1
            i += pattern_length
        else:           # if j value is not -1 that means our pattern doesn't match with our text
            if text[i + pattern_length-1] in shift_table:
                i += shift_table[text[i + pattern_length-1]]
            else:
                i += pattern_length

    return highlighted_text, occurrences, shift_table, comparisons

print("--------------------------- 2.Horspool's Algorithm -----------------------")

print('Pattern:', pattern)
start_time = time.time()    # start the timer before the function call
highlighted_text, occurrences, shift_table, comparisons = highlight_text(text, pattern)
end_time = time.time()      # stop the timer after the function call
horspool_time = (end_time - start_time) * 1000
print('Number of Comparisons:', comparisons)
print('Running Time (ms):', horspool_time)
print('Occurrences:', occurrences)
print('Shift Table:', shift_table)
print()


try:
     with open('output2.html', 'w') as f:
        f.write(highlighted_text)
except FileNotFoundError:
    print("Error")




## --------------------------- 3.Boyer Moore Algorithm ----------------------

patternLen = len(pattern)
start_time = time.time()

#Function to set up bad symbol table.
def setBadSymbol(pattern):                                           
    badSymbolTable = defaultdict(lambda: patternLen) #Set a default value for characters not present in the pattern as the pattern length.
    for i in range(patternLen-1):
        badSymbolTable[pattern[i]] = patternLen - i - 1 #Set the values for the characters in the pattern.
    badSymbolTable["*"] = patternLen    
    return badSymbolTable

#Function to set up good suffix table.
def setGoodSuffix(pattern):
    d2 = [0] * patternLen
    
    for k in range (1,patternLen):
        precedingChar = pattern[patternLen -k-1]
        d2[k] = matchCount(pattern,k,precedingChar)
    return d2

#Function to determine d2 values for the good suffix table. That takes precedingChar as an argument and checks if there exists another substring with a different preceding char. 
def matchCount(pattern,k,precidingChar):
    temp = pattern
    suffix = pattern[patternLen -k : patternLen]
    
    index = pattern.rfind(suffix)
    if index != 0:
        while pattern[index - 1] == precidingChar and not(index < 0):
            #Finding the rightmost occurence of the substring that has different preceding char.
            pattern = pattern[: -1]                                     
            index = pattern.rfind(suffix)
            if index == -1:
                #If not found any, it checks if there exist a suffix prefix match. If there is no match it returns patternLen
                pattern = temp
                return patternLen - suffixPrefixMatch(pattern,k)        
    return patternLen - k - index

#Function that matches the longest part of the k character suffix with corresponding prefix
def suffixPrefixMatch(pattern,k):
    for i in range(k, 0, -1):
        if pattern[:i] == pattern[patternLen-i:]:
            return i
    return 0

#Function that makes comparisons.
def compare(pattern,text,totalShift,comparisons):
    k = 1
    while patternLen -k >= 0 and pattern[patternLen - k] == text[patternLen - k + totalShift] and patternLen - k + totalShift < len(text):
        k += 1
    comparisons += k
    if k-1 == patternLen:
        comparisons -= 1
    
    return k-1, text[patternLen - k + totalShift], comparisons

#Function for shifting. It shifts the pattern according to the badsymbol and goodSuffix tables. It takes markStarts list as an argument and it fills this list with the starting indexes of the occurrences.This list will be used for highlighting.


def shifting(markStarts, comparisons):
    occurrence = 0
    totalShift = 0
    while True :
        if totalShift > len(text) - patternLen: #if it exceeds the limits, it means no more occurences exist so break the while loop.
            break
        
        value = compare(pattern,text,totalShift, comparisons)
        k = value[0]
        mismatchChar = value[1]
        t1 = badSymbolTable[mismatchChar]
    
        if k == patternLen:
            #if k == patternLen it means there exist an occurrence, so it increments the occurence counter, add the starting index of the occurrence and shifts the pattern by pattern length.
            occurrence += 1
            markStarts.append(totalShift)
            totalShift += patternLen
        elif k == 0 :
            #if k ==0, it means there is no match, so it shifts according to the bad symbol table.
            totalShift += t1
        else:
            #else it shifts the pattern according to the good suffix table.
            t2 = goodSuffixTable[k]
            d1 = max(t1 - k, 1)
            totalShift += max(d1,t2)
        comparisons = value[2]
    return occurrence, comparisons


#Function that highlights the occurences, it takes occurence starting index as an argument and puts "<mark>" to that position.
def highlight(occurrence,markStarts):
    highlighted = text
    i = 0
    offset = 0
    while i < occurrence:
        markStart = markStarts[i] + offset
        markEnd = markStarts[i] + patternLen-1 + offset
        highlighted = highlighted[:markStart] + "<mark>" + highlighted[markStart:markEnd+1] + "</mark>" + highlighted[markEnd+1:]
        offset += 13  # 13 = len("<mark>") + len("</mark>"), when we put mark tags to the text it is shifted by 13.
        i +=1
    return highlighted    

goodSuffixTable = setGoodSuffix(pattern)
badSymbolTable = setBadSymbol(pattern)

comparisons = 0
markStarts = []
occ, comparisons = shifting(markStarts, comparisons)
highlighted = highlight(occ,markStarts)

end_time = time.time()

print("--------------------------- 3.Boyer Moore Algorithm ----------------------")

#Printing bad symbol table.
print("Bad Symbol Table")
printed = []
for i in range (patternLen - 1):
    if pattern[i] not in printed:
        printed.append(pattern[i])
        print(pattern[i],"|", badSymbolTable[pattern[i]])
    if i == patternLen - 2:
        print("* | " , badSymbolTable["*"])

#Printing good suffix table.
print("Good Suffix Table")
print("k | d")
print("--|--")
for i in range(1,patternLen):
    print(i , "|" , goodSuffixTable[i])

#Printing the results.
print(f"Character Comparisons : {comparisons}")
print(f"Occurence : {occ}")
boyer_moore_time = (end_time - start_time)*1000
print(f"Running time: {boyer_moore_time:.4f} ms")
print()

try:
     with open('output3.html', 'w') as f:
        f.write(highlighted)
except FileNotFoundError:
    print("Error")

print("---------------------------")


minimum_time = min(brute_force_time, horspool_time, boyer_moore_time)

if minimum_time == boyer_moore_time:
    print("Boyer Moore Algorithm is fastest")
elif minimum_time == horspool_time:
    print("Horspool's Algorithm is fastest")
elif minimum_time == brute_force_time:
    print("Brute Force Algorithm is fastest")


maximum_time = max(brute_force_time, horspool_time, boyer_moore_time)

if maximum_time == brute_force_time:
    print("Brute Force Algorithm is slowest")
elif maximum_time == horspool_time:
    print("Horspool's Algorithm is slowest")
elif maximum_time == boyer_moore_time:
    print("Boyer Moore Algorithm is slowest")

print()