"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import math
import poc_wrangler_provided as provided
codeskulptor.set_timeout(60)
WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
#http://www.codeskulptor.org/#user36_t1wZgIXXNQ_55.py

def binary_search(L,l,r,k):
    if l>=r:
        return false
    mid=math.floor((l+r)/2)
    if k==L[mid]:
        return true
    elif k<L[mid]:
        binary_search(L,l,mid-1,k)
    elif k>L[mid]:
        binary_search(L,mid+1,r,k)

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    temp_list=[]
    temp=''
    for item in list1:
        if temp!=item:
            temp_list.append(item)
            temp=item
    return temp_list        
            

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    list1=remove_duplicates(list1)
    list2=remove_duplicates(list2)
    sect_list=[]
    looper1=0
    looper2=0
    while looper1<len(list1) and looper2<len(list2):
        if list1[looper1]==list2[looper2]:
            sect_list.append(list1[looper1])
            looper1+=1
            looper2+=1
        elif list1[looper1]<list2[looper2]:
            looper1+=1
        else:
            looper2+=1
    """
    if len(list1)==0 or len(list2)==0:
        return []
    for item in list1:
        print "item in list1 "+str(item)
        print looper
        if item<list2[looper]:
            continue
        while looper<len(list2):            
            if list2[looper]==item:       
                sect_list.append(item)
                break
            else:
                looper+=1
        if looper==len(list2):
            break
    """
    return sect_list
# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    list_all=[]
    looper1=0
    looper2=0
    while looper1<len(list1)and looper2<len(list2):
        if list1[looper1]<list2[looper2]:
            list_all.append(list1[looper1])
            looper1+=1
        elif list1[looper1]==list2[looper2]:
            list_all.append(list1[looper1])
            list_all.append(list2[looper2])
            looper1+=1
            looper2+=1
        else:
            list_all.append(list2[looper2])
            looper2+=1
    list_all.extend(list1[looper1:])
    list_all.extend(list2[looper2:])
    return list_all

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1)<=1:
        return list1
    else:
        half_len=len(list1)/2
        list_half1=list1[:half_len]
        list_half2=list1[half_len:]
        list_half1=merge_sort(list_half1)
        list_half2=merge_sort(list_half2)
        list_all=merge(list_half1,list_half2)   
        return list_all

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word)==0:
        return ['']
    
    first=word[0]
    rest=word[1:]
    rest_strings=gen_all_strings(rest)
    all_strings=rest_strings[:]#this is the point!!!!!!!

    for item in rest_strings:
        for looper in range(len(item)+1):
            all_strings.append(item[0:looper]+first+item[looper:len(item)])
            
    return all_strings

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    words=[]
    url=codeskulptor.file2url(filename)
    netfile=urllib2.urlopen(url)
    for line in netfile.readlines():
        words.append(line[:-1])   
    return words
    
def run():
    """
    Run game.
    """
    
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    
    
