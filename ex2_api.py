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


def who_am_i():
    """Returns a ductionary with your name, id number and email. keys=['name', 'id','email']
        Make sure you return your own info!
    """
    return {'name': 'Tal Yitzhak', 'id': '204260533', 'email': 'talitz@post.bgu.ac.il'}
