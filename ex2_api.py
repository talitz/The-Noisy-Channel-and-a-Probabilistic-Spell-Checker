import csv
import re
from collections import Counter
from IPython.core.debugger import set_trace

class Spell_Checker:
    """The class implements a context sensitive spell checker. The corrections
        are done in the Noisy Channel framework, based on a language model and
        an error distribution model.
    """

    def __init__(self,lm=None):
        """Initializing a spell checker object with a language model as an
        instance  variable. The language model should suppport the evaluate()
        and the get_model() functions as defined in assignment #1.

        Args:
            lm: a language model object. Defaults to None
        """
        self.lm = lm

    def build_model(self, text, n=3):
        """Returns a language model object built on the specified text. The language
            model should support evaluate() the get_model() functions as defined
            in assignment #1.

            Args:
                text (str): the text to construct the model from.
                n (int): the order of the n-gram model (defaults to 3).

            Returns:
                A language model object
        """
        self.lm.build_mode(text)

    def add_language_model(self, lm):
        """Adds the specified language model as an instance variable.
            (Replaces an older LM disctionary if set)

            Args:
                ls: a language model object
        """
        self.lm = lm

    def learn_error_distribution(self, errors_file):
        """Returns a dictionary {str:dict} where str is in:
            <'deletion', 'insertion', 'transposition', 'substitution'> and the
            inner dict {tupple: float} represents the confution matrix of the
            specific errors, where tupple is (err, corr) and the float is the
            probability of such an error.
            Examples of such tupples are ('t', 's'), for deletion of a 't'
            after an 's', insertion of a 't' after an 's'  and substitution
            of 's' by a 't'; and example of a transposition tupple is ('ac','ca').
            In the case of insersion, the tuppe (i,j) reads as "i was mistakingly
            added after j". In the case of deletion, the tupple reads as
            "i was mistakingly ommitted after j"

            Notes:
                1. The error distributions could be represented in more efficient ways.
                    We ask you to keep it simple and straight forward for clarity.
                2. Ultimately, one can use only 'deletion' and 'insertion' and have
                    'substitution' and 'transposition' derived. Again,  we use all
                    four types explicitly in order to keep things simple.
            Args:
                errors_file (str): full path to the errors file. File format, TSV:
                                    <error>    <correct>
            Returns:
                A dictionary of error distributions by error type (dict).
        """
        ret_dict = {
            "deletion" : {},
            "insertion" : {},
            "transposition" : {},
            "substitution" : {}
        }
        
        WORDS = Counter(words(open(errors_file).read()))
        with open(errors_file) as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                err = row[0]
                corr = row[1]
                print("-------------------")                  
                print("Error = {}".format(err))
                print("Correction = {}".format(corr))
                
                return_inserts = edits1(err,WORDS,False,False,False,True,corr)
                return_deletes = edits1(err,WORDS,True,False,False,False,corr) 
                return_transposes = edits1(err,WORDS,False,True,False,False,corr)                
                return_replaces = edits1(err,WORDS,False,False,True,False,corr)
                print("return_inserts = {}".format(return_inserts))
                print("return_deletes = {}".format(return_deletes))
                print("return_transposes = {}".format(return_transposes))
                print("return_replaces = {}".format(return_replaces))                
                
                deletion_dict = ret_dict["deletion"]              
                substitution_dict = ret_dict["substitution"]
                transposition_dict = ret_dict["transposition"]         
                insertion_dict = ret_dict["insertion"]   
                
                if(return_deletes):
                    for i in range(len(err)):
                        curr_char = err[i]
                        first_part = err[0:i]
                        second_part = err[i+1:]
                        print("current char = {}".format(err[i]))
                        print("first part = {}".format(first_part))
                        print("second part = {}".format(second_part))
                        if(first_part + second_part == corr):
                            tupple = (curr_char,err[i-1])
                            print("added tupple = {}".format(tupple))
                            
                            if tupple in deletion_dict.keys(): 
                                print("deletion_dict is not empty. adding 1 to it's value")
                                deletion_dict[tupple] += 1
                            else:
                                print("deletion_dict is empty. default value is 1 now")
                                deletion_dict[tupple] = 1
                            break    
                elif(return_replaces):
                    for i in range(len(corr)):
                        print("err[i] = {}".format(err[i]))
                        print("corr[i] = {}".format(corr[i]))
                        if(err[i] != corr[i]):
                            tupple = (corr[i],corr[i-1])
                            print("added tupple = {}".format(tupple))

                            if tupple in substitution_dict.keys(): 
                                print("substitution_dict is not empty. adding 1 to it's value")
                                substitution_dict[tupple] += 1
                            else:
                                print("substitution_dict is empty. default value is 1 now")
                                substitution_dict[tupple] = 1
                            break   
                elif(return_transposes): 
                    for i in range(len(corr)):
                        print("err[i] = {}".format(err[i]))
                        print("corr[i] = {}".format(corr[i]))
                        if(err[i] != corr[i]):
                            for j in range(i+1, len(corr)):
                                if(err[j] == corr[j]):
                                    tupple = (err[i:j],corr[i:j])
                                    print("added tupple = {}".format(tupple))

                                    if tupple in transposition_dict.keys(): 
                                        print("transposition_dict is not empty. adding 1 to it's value")
                                        transposition_dict[tupple] += 1
                                    else:
                                        print("substitution_dict is empty. default value is 1 now")
                                        transposition_dict[tupple] = 1
                                    break
                            break                 
                elif(return_inserts): 
                    for i in range(len(err)):
                        print("err[i] = {}".format(err[i]))
                        print("corr[i] = {}".format(corr[i]))
                        if(err[i] != corr[i]):
                            print("--")
                            print("err[0:i] = {}".format(err[0:i]))
                            print("corr[i] = {}".format(corr[i]))
                            print("err[i+1:] = {}".format(err[i+1:]))                                        
                            print(corr)
                            print("--")
                            if(err[0:i] + corr[i] + err[i:] == corr):
                                tupple = (corr[i],err[i-1])
                                print("added tupple = {}".format(tupple))

                                if tupple in insertion_dict.keys(): 
                                    print("insertion_dict is not empty. adding 1 to it's value")
                                    insertion_dict[tupple] += 1
                                else:
                                    print("insertion_dict is empty. default value is 1 now")
                                    insertion_dict[tupple] = 1
                                break 
                else:
                    print("all return types are null!")                 
                print("-------------------")  
        return ret_dict
                                
    def add_error_tables(self, error_tables):
        """ Adds the speficied dictionary of error tables as an instance variable.
            (Replaces an older value disctionary if set)

            Args:
                error_tables (dict): a dictionary of error tables in the format
                returned by  learn_error_distribution()
        """


    def evaluate(self,text):
        """Returns the log-likelihod of the specified text given the language
            model in use. Smoothing is applied on texts containing OOV words

           Args:
               text (str): Text to evaluate.

           Returns:
               Float. The float should reflect the (log) probability.
        """

    def spell_check(self, text, alpha):
        """ Returns the most probable fix for the specified text. Use a simple
            noisy channel model is the number of tokens in the specified text is
            smaller than the length (n) of the language model.

            Args:
                text (str): the text to spell check.
                alpha (float): the probability of keeping a lexical word as is.

            Return:
                A modified string (or a copy of the original if no corrections are made.)
        """

def edits1(word, WORDS, return_deletes, return_transposes, return_replaces, return_inserts,correct):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnop qrstu-\'vwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    ret        = []
    
    if(return_deletes):
        ret = set(deletes)
    
    if(return_transposes):
        ret = set(transposes)
        
    if(return_replaces):
        ret = set(replaces)
    
    if(return_inserts):
        ret = set(inserts)
    
    ret = known(ret,WORDS)
        
    if(correct.lower() in ret): 
        return True
    else:
        return False

def known(words,WORDS):
    agg = []
    lower_words = [x.lower() for x in words]
    
    for w in lower_words:
        if w in WORDS:
            agg.append(w)
        else:
            ans = []
            if(" " in w):
                ans = w.split(" ")
            elif("-" in w):
                ans = w.split("-")
                
            is_all_exist = True
            for e in ans:
                if e not in WORDS:
                    is_all_exist = False
            if(is_all_exist): 
                agg.append(w)    
    agg_as_set = set(agg)
    return agg_as_set

def get_all_correct_words(error_file):
    agg = []
    with open(error_file) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            agg.append(row[1])
    return Counter(agg)

def words(text): return re.findall(r'\w+', text.lower())

def who_am_i():
    """Returns a ductionary with your name, id number and email. keys=['name', 'id','email']
        Make sure you return your own info!
    """
    return {'name': 'Tal Yitzhak', 'id': '204260533', 'email': 'talitz@post.bgu.ac.il'}
