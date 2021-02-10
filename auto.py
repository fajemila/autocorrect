import re
from collections import Counter
import numpy as np
from flask import Flask , render_template,request,redirect,Response,url_for
import pandas as pd
app = Flask(__name__)
def process_data(file_name):
    words = []

    with open(file_name,encoding="utf8") as f:
        file_name_data = f.read()
    file_name_data=file_name_data.lower()
    words = re.findall('\w+',file_name_data)
    
    return words
word_l = process_data('ogboju_ode.txt')

vocab = set(word_l)
def get_count(word_l):
    word_count_dict = {}  # fill this with word counts
    word_count_dict = Counter(word_l)
    return word_count_dict
word_count_dict = get_count(word_l)
def get_probs(word_count_dict):
    probs = {} 

    m = sum(word_count_dict.values())
    for key in word_count_dict.keys():
        probs[key] = word_count_dict[key] / m
    return probs
probs = get_probs(word_count_dict)

def delete_letter(word, verbose=False):
    delete_l = []
    split_l = []
    
    ### START CODE HERE ###
    for c in range(len(word)):
        split_l.append((word[:c],word[c:]))
    for a,b in split_l:
        delete_l.append(a+b[1:])          
    if verbose: print(f"input word {word}, \nsplit_l = {split_l}, \ndelete_l = {delete_l}")

    return delete_l
def switch_letter(word, verbose=False):
    def swap(c, i, j):
        c = list(c)
        c[i], c[j] = c[j], c[i]
        return ''.join(c)
    
    switch_l = []
    split_l = []
    len_word=len(word)
    for c in range(len_word):
        split_l.append((word[:c],word[c:]))
    switch_l = [a + b[1] + b[0] + b[2:] for a,b in split_l if len(b) >= 2]          
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nswitch_l = {switch_l}") 

    return switch_l
def replace_letter(word, verbose=False):
   
    
    letters = 'abdeẹfggbhijklmnoọprsṣtuwy'
    replace_l = []
    split_l = []
    
    
    for c in range(len(word)):
        split_l.append((word[0:c],word[c:]))
    replace_l = [a + l + (b[1:] if len(b)> 1 else '') for a,b in split_l if b for l in letters]
    replace_set=set(replace_l)    
    replace_set.remove(word)    
    # turn the set back into a list and sort it, for easier viewing
    replace_l = sorted(list(replace_set))
    
    if verbose: print(f"Input word = {word} \nsplit_l = {split_l} \nreplace_l {replace_l}")   
    
    return replace_l
def insert_letter(word, verbose=False):
 
    letters = 'abdeẹfggbhijklmnoọprsṣtuwy'
    insert_l = []
    split_l = []
    
    for c in range(len(word)+1):
        split_l.append((word[0:c],word[c:]))
    insert_l = [ a + l + b for a,b in split_l for l in letters]

    if verbose: print(f"Input word {word} \nsplit_l = {split_l} \ninsert_l = {insert_l}")
    
    return insert_l
def edit_one_letter(word, allow_switches = True):    
    edit_one_set = set()
        
    edit_one_set.update(delete_letter(word))
    if allow_switches:
        edit_one_set.update(switch_letter(word))
    edit_one_set.update(replace_letter(word))
    edit_one_set.update(insert_letter(word))

    return edit_one_set
def edit_two_letters(word, allow_switches = True):

    edit_two_set = set()
    edit_one = edit_one_letter(word,allow_switches=allow_switches)
    for w in edit_one:
        if w:
            edit_two = edit_one_letter(w,allow_switches=allow_switches)
            edit_two_set.update(edit_two)
    return edit_two_set
def get_corrections(word, probs, vocab, n=2, verbose = False):
   
    suggestions = []
    n_best = []
    
    suggestions = list((word in vocab and word) or edit_one_letter(word).intersection(vocab) or edit_two_letters(word).intersection(vocab))
    n_best = [[s,probs[s]] for s in list(reversed(suggestions))]    
    # if verbose: print("suggestions = ", suggestions)

    return suggestions
# # Test your implementation - feel free to try other words in my word
# my_word = 'iws' 
# tmp_corrections = get_corrections(my_word, probs, vocab, 2, verbose=True) # keep verbose=True
# for i, word_prob in enumerate(tmp_corrections):
#     print(f"word {i}: {word_prob[0]}, probability {word_prob[1]:.6f}")

# # CODE REVIEW COMMENT: using "tmp_corrections" insteads of "cors". "cors" is not defined
# print(f"data type of corrections {type(tmp_corrections)}")

@app.route('/',methods=['GET','POST'])
@app.route('/correct',methods=['GET','POST'])
def correct():
    if request.method=='POST':
        word = request.form['text']
        tmp_corrections = get_corrections(word, probs, vocab, 2, verbose=True) # keep verbose=True
        return render_template('correct.html',tmp_corrections = tmp_corrections)
    return render_template('correct.html')
if __name__=="__main__":
    app.run(debug=True)