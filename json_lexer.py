# File: json_lexer.py
# Author: Kent Morris
# Date: 10/7/22
# Description: Lexical analyzer for JSON files, returns different types of tokens from JSON files.

from multiprocessing.sharedctypes import Value
import string

class Token:
    def __init__(self, token_type, value = None):
        # Initialize the token
        self.token_type = token_type
        self.value = value
        #if self.value:
        #    # This forces Python to interpret escape sequences in a string.
        #    self.value = bytes(self.value, "utf-8").decode("unicode_escape")
    def __str__(self):
        # Return string representation of Token
        return f"{self.token_type}:{self.value}"

class JSON_lexer:
    def __init__(self, filename):
        # Initialize DFA
        self.f = open(filename)
        self.buffer = self.f.read()
        self.i = 0
        self.next_token_to_return = None
        self.start_state = 0
        self.accept_states = [8, 9, 11, 12, 14, 17, 18, 20, 21, 22, 23, 24, 25, 29, 34, 38]
        self.transitions = {} # the DFA transitions
        self.transitions[0] = {'"':1, '-':10, '0':12, '{':20, '}':21, '[':22, ']':23, ',':24, ':':25, 't':26, 'f':30, 'n':35}  
        self.transitions[1] = {" ":1, "\\": 2,'"':8, '(':1, ')':1, ':':1, '.':1, '-':1, ',':1}  
        self.transitions[2] = {'u':3,'\"':1, '\\':1,  "b":1, "f":1, "n":1, "r":1, "t":1, '"':1, '/':1}  
        self.transitions[3] = {}  
        self.transitions[4] = {}  
        self.transitions[5] = {}
        self.transitions[6] = {}
        self.transitions[7] = {'"':8, '\\':2}
        self.transitions[8] = {}
        self.transitions[9] = {'E':15, 'e':15, '.':14}
        self.transitions[10] = {'0':12}
        self.transitions[11] = {'E':15, 'e':15, '.':14}
        self.transitions[12] = {'.':14, 'E':13, 'e':13}
        self.transitions[13] = {'+':16, '-':16}
        self.transitions[14] = {'E':15, 'e':15}
        self.transitions[15] = {"+": 16, '-':16}
        self.transitions[16] = {}
        self.transitions[17] = {}
        self.transitions[18] = {}
        self.transitions[20] = {}
        self.transitions[21] = {}
        self.transitions[22] = {}
        self.transitions[23] = {}
        self.transitions[24] = {}
        self.transitions[25] = {}
        self.transitions[26] = {'r':27}
        self.transitions[27] = {'u':28}
        self.transitions[28] = {'e':29}
        self.transitions[29] = {}
        self.transitions[30] = {'a':31}
        self.transitions[31] = {'l':32}
        self.transitions[32] = {'s':33}
        self.transitions[33] = {'e':34}
        self.transitions[34] = {}
        self.transitions[35] = {'u':36}
        self.transitions[36] = {'l':37}
        self.transitions[37] = {'l':38}
        self.transitions[38] = {}
        

        # Add all transitions for letters
        for c in string.ascii_letters:
            self.transitions[1][c] = 1
            self.transitions[7][c] = 1

        # Add all transitions for hexadecimal digits
            
        for c in "0123456789abcdefABCDEF":
            self.transitions[3][c] = 4
            self.transitions[4][c] = 5
            self.transitions[5][c] = 6
            self.transitions[6][c] = 7
            
        # An add transitions for digits between one and nine    
            
        for c in "123456789":
            self.transitions[0][c] = 9
            self.transitions[10][c] = 11
            
        # And add transitions for digits
        for c in string.digits:
            self.transitions[1][c] = 1
            self.transitions[9][c] = 9
            self.transitions[11][c] = 11
            self.transitions[13][c] = 17
            self.transitions[14][c] = 14
            self.transitions[7][c] = 1
            self.transitions[15][c] = 17
            self.transitions[16][c] = 18
            self.transitions[17][c] = 17
            self.transitions[18][c] = 18

        # Add transition for special characters
        for c in ":-.":
            self.transitions[7][c] = 1
        # You will write this code, implementing a DFA to recognize
        # the tokens of  JSON file.
        # Define actions associated with accept states.
       
        self.actions = {}
        self.actions[8] = lambda value: Token("STRING", value.replace('"', ''))
        self.actions[9] = lambda value: Token("NUMBER", value)
        self.actions[11] = lambda value: Token("NUMBER", value)
        self.actions[12] = lambda value: Token("NUMBER", '{:,.0f}'.format(abs(float(value))))
        self.actions[14] = lambda value: Token("NUMBER", float(value))
        # Convert numbers from scientific notation to a floating point number
        self.actions[17] = lambda value: Token("NUMBER", value = float("{:.5f}".format(float(value))))
        self.actions[18] = lambda value: Token("NUMBER", value = float("{:.1f}".format(float(value))))
        self.actions[20] = lambda value = None: Token("LEFT_BRACE", )
        self.actions[21] = lambda value = None: Token("RIGHT_BRACE", )
        self.actions[22] = lambda value = None: Token("LEFT_BRACKET", )
        self.actions[23] = lambda value = None: Token("RIGHT_BRACKET", )
        self.actions[24] = lambda value = None: Token("COMMA", )
        self.actions[25] = lambda value = None: Token("COLON", )
        self.actions[29] = lambda value = True: Token("TRUE", value = True)
        self.actions[34] = lambda value = False: Token("FALSE", value= False)
        self.actions[38] = lambda value = None: Token("NULL", )
        
        



    def next_token(self):
        """
        Returns and consumes the next token.
        If no next token, returns None
        If next token is not valid, raises ValueError
        """
        #self.next_token_to_return = self.buffer[self.i]
        if self.next_token_to_return:
            retVal = self.next_token_to_return
            self.next_token_to_return = None
            return retVal
        else:
            retVal = self.peek_next_token()
            self.next_token_to_return = None
            return retVal

    def peek_next_token(self):
        # Returns next token in the input.
        # Returns None if no more tokens in input.
        # Raises ValueError if invalid token encountered.
        
        # You will write this code.  Just copy your next_token method
        # (and any supporting methods) from lexer2.py
        if self.next_token_to_return:  
            return self.next_token_to_return

        while self.i < len(self.buffer) and self.buffer[self.i].isspace():
            self.i+=1 
        state = self.start_state  
        token = ""
       

        #test why you dropped out of loop and return None
        if self.i == len(self.buffer):
            return None
        
        
        while self.i < len(self.buffer):#while the file is not empty
            if self.buffer[self.i] not in self.transitions[state]:
                break
            state = self.transitions[state][self.buffer[self.i]]
            token+=self.buffer[self.i]
            self.i+=1 
        
        if state in self.accept_states:  
            self.next_token_to_return = self.actions[state](token)
            return self.next_token_to_return
           
        elif state not in self.accept_states:
            self.i += 1
            raise ValueError
        
        
        
        
    

        
if __name__ == '__main__':
    # Test the JSON_lexer class.
    num_tested = 0
    num_correct = 0

    # Test the file json_lexer_testa.txt
    filename = "json_lexer_testa.txt"
    print(f"Testing file {filename}.  One of each token type.  Whitespace between them.")
    tokens = ["LEFT_BRACE:None", "RIGHT_BRACE:None", "LEFT_BRACKET:None", 
            "RIGHT_BRACKET:None", "COMMA:None", "COLON:None", "TRUE:None", 
            "FALSE:None", "NULL:None", "NUMBER:-123450000000000.0", 
            "STRING:a string example"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_testb.txt
    filename = "json_lexer_testb.txt"
    print(f"Testing file {filename}.  One of each token type.  No spaces between them.")
    tokens = ["LEFT_BRACE:None", "RIGHT_BRACE:None", "LEFT_BRACKET:None", 
            "RIGHT_BRACKET:None", "COMMA:None", "COLON:None", "TRUE:None", 
            "FALSE:None", "NULL:None", "NUMBER:-123450000000000.0", 
            "STRING:a string example"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_testc.txt
    filename = "json_lexer_testc.txt"
    print(f"Testing file {filename}")
    tokens = ["LEFT_BRACKET:None", "NUMBER:0", "COMMA:None", "NUMBER:0", 
            "COMMA:None", "NUMBER:-12", "COMMA:None", "NUMBER:3", "COMMA:None", 
            "NUMBER:3093", "COMMA:None", "NUMBER:619.0", "COMMA:None", "NUMBER:0.0", 
            "COMMA:None", "NUMBER:92.211", "COMMA:None", "NUMBER:0.234", "COMMA:None", 
            "NUMBER:23000000000.0", "COMMA:None", "NUMBER:12000000000000.0", 
            "COMMA:None", "NUMBER:0.0", "COMMA:None", "NUMBER:2120200000000000.0", 
            "COMMA:None", "NUMBER:-0.12", "COMMA:None", "NUMBER:9000000000.0", 
            "RIGHT_BRACKET:None"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_testd.txt
    filename = "json_lexer_testd.txt"
    print(f"Testing file {filename}.  String tokens, including escape sequences")
    tokens = ["LEFT_BRACKET:None", "STRING:", "COMMA:None", 
            "STRING:   here   is a string ", "COMMA:None", r"STRING:\\", 
            "COMMA:None", r"STRING:\/", "COMMA:None", r"STRING:\b", "COMMA:None", 
            r"STRING:\f", "COMMA:None", r"STRING:\n", "COMMA:None", r"STRING:\r", 
            "COMMA:None", r"STRING:\t", "COMMA:None", r"STRING:\u00AE", 
            "COMMA:None", r"STRING:\u00A2", "COMMA:None", 
            r"STRING:now\b\\\n\r\t\u00ae\u00a2other words", "RIGHT_BRACKET:None"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_teste.txt
    filename = "json_lexer_teste.txt"
    print(f"Testing file {filename}.  true, false, and null")
    tokens = ["LEFT_BRACKET:None", "TRUE:None", "COMMA:None", "FALSE:None", 
            "COMMA:None", "NULL:None", "RIGHT_BRACKET:None"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    filename = "json_lexer_testf.txt"
    print(f"Testing file '{filename}'.  A single invalid character after a single valid token.")
    tokens = ["NUMBER:123"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            try:
                token = lexer.next_token()
                print(f"Lexer did not raise ValueError.  It returned {token}  Incorrect")
            except ValueError:
                print("Lexer raised ValueError.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            except Exception as e:
                print(f"Lexer raised {e} instead of ValueError.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    filename = "json_lexer_testg.txt"
    print(f"Testing file '{filename}'.  A single invalid character after a single valid token - no spaces in betweem.")
    tokens = ["NUMBER:123"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            try:
                token = lexer.next_token()
                print(f"Lexer did not raise ValueError.  It returned {token}  Incorrect")
            except ValueError:
                print("Lexer raised ValueError.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            except Exception as e:
                print(f"Lexer raised {e} instead of ValueError.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    filename = "json_lexer_testh.txt"
    print(f"Testing file '{filename}'.  Invalid string token.")
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
       
        try:
            token = lexer.next_token()
            print(f"Lexer did not raise ValueError.  It returned {token}  Incorrect")
        except ValueError:
            print("Lexer raised ValueError.  Correct")
            print(f"File {filename} handled correctly.")
            num_correct += 1
        except Exception as e:
            print(f"Lexer raised {e} instead of ValueError.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    filename = "json_lexer_testi.txt"
    print(f"Testing file '{filename}'.  Invalid string token.")
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
       
        try:
            token = lexer.next_token()
            print(f"Lexer did not raise ValueError.  It returned {token}  Incorrect")
        except ValueError:
            print("Lexer raised ValueError.  Correct")
            print(f"File {filename} handled correctly.")
            num_correct += 1
        except Exception as e:
            print(f"Lexer raised {e} instead of ValueError.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_testj.json
    filename = "json_lexer_testj.json"
    print(f"Testing file {filename}.  A sample JSON file.")
    tokens = ["LEFT_BRACE:None", "STRING:menu", "COLON:None", "LEFT_BRACE:None", 
            "STRING:id", "COLON:None", "STRING:file", "COMMA:None", "STRING:value", 
            "COLON:None", "STRING:File", "COMMA:None", "STRING:popup", "COLON:None", 
            "LEFT_BRACE:None", "STRING:menuitem", "COLON:None", "LEFT_BRACKET:None", 
            "LEFT_BRACE:None", "STRING:value", "COLON:None", "STRING:New", 
            "COMMA:None", "STRING:onclick", "COLON:None", "STRING:CreateNewDoc()", 
            "RIGHT_BRACE:None", "COMMA:None", "LEFT_BRACE:None", "STRING:value", 
            "COLON:None", "STRING:Open", "COMMA:None", "STRING:onclick", "COLON:None", 
            "STRING:OpenDoc()", "RIGHT_BRACE:None", "COMMA:None", "LEFT_BRACE:None", 
            "STRING:value", "COLON:None", "STRING:Close", "COMMA:None", 
            "STRING:onclick", "COLON:None", "STRING:CloseDoc()", "RIGHT_BRACE:None", 
            "RIGHT_BRACKET:None", "RIGHT_BRACE:None", "RIGHT_BRACE:None", 
            "RIGHT_BRACE:None"]   
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    # Test the file json_lexer_testk.json
    filename = "json_lexer_testk.json"
    print(f"Testing file {filename}.  A sample JSON file.")
    tokens = ["LEFT_BRACE:None", "STRING:glossary", "COLON:None", 
                "LEFT_BRACE:None", "STRING:title", "COLON:None", 
                "STRING:example glossary", "COMMA:None", "STRING:GlossDiv", 
                "COLON:None", "LEFT_BRACE:None", "STRING:title", "COLON:None", 
                "STRING:S", "COMMA:None", "STRING:GlossList", "COLON:None", 
                "LEFT_BRACE:None", "STRING:GlossEntry", "COLON:None", 
                "LEFT_BRACE:None", "STRING:ID", "COLON:None", "STRING:SGML", 
                "COMMA:None", "STRING:SortAs", "COLON:None", "STRING:SGML", 
                "COMMA:None", "STRING:GlossTerm", "COLON:None", 
                "STRING:Standard Generalized Markup Language", "COMMA:None", 
                "STRING:Acronym", "COLON:None", "STRING:SGML", "COMMA:None", 
                "STRING:Abbrev", "COLON:None", "STRING:ISO 8879:1986", 
                "COMMA:None", "STRING:GlossDef", "COLON:None", "LEFT_BRACE:None", 
                "STRING:para", "COLON:None", 
                "STRING:A meta-markup language, used to create markup languages such as DocBook.", 
                "COMMA:None", "STRING:GlossSeeAlso", "COLON:None", "LEFT_BRACKET:None", 
                "STRING:GML", "COMMA:None", "STRING:XML", "RIGHT_BRACKET:None", "RIGHT_BRACE:None", 
                "COMMA:None", "STRING:GlossSee", "COLON:None", "STRING:markup", 
                "RIGHT_BRACE:None", "RIGHT_BRACE:None", "RIGHT_BRACE:None", "RIGHT_BRACE:None", 
                "RIGHT_BRACE:None"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()


    # Test the file json_lexer_testl.json
    filename = "json_lexer_testl.json"
    print(f"Testing file {filename}.  A sample JSON file.")
    tokens = ["LEFT_BRACE:None", "STRING:markers", "COLON:None", "LEFT_BRACKET:None", 
            "LEFT_BRACE:None", "STRING:name", "COLON:None", 
            "STRING:Rixos The Palm Dubai", "COMMA:None", "STRING:position", 
            "COLON:None", "LEFT_BRACKET:None", "NUMBER:25.1212", "COMMA:None", 
            "NUMBER:55.1535", "RIGHT_BRACKET:None", "COMMA:None", "RIGHT_BRACE:None", 
            "COMMA:None", "LEFT_BRACE:None", "STRING:name", "COLON:None", 
            "STRING:Shangri-La Hotel", "COMMA:None", "STRING:location", "COLON:None", 
            "LEFT_BRACKET:None", "NUMBER:25.2084", "COMMA:None", "NUMBER:55.2719", 
            "RIGHT_BRACKET:None", "RIGHT_BRACE:None", "COMMA:None", "LEFT_BRACE:None", 
            "STRING:name", "COLON:None", "STRING:Grand Hyatt", "COMMA:None", 
            "STRING:location", "COLON:None", "LEFT_BRACKET:None", "NUMBER:25.2285", 
            "COMMA:None", "NUMBER:55.3273", "RIGHT_BRACKET:None", "RIGHT_BRACE:None", 
            "RIGHT_BRACKET:None", "RIGHT_BRACE:None"]
    num_tested += 1
    try:
        lexer = JSON_lexer(filename)
        ok = True
        for i in range(len(tokens)):
            token = lexer.next_token()
            if isinstance(token, Token) and str(token) == tokens[i]:
                print(f"Token {i} returned is {token}.  Correct")
            else:
                print(f"Token {i} returned is {token}.  Incorrect.  Should be {tokens[i]}")
                ok = False
                break
        if ok:
            token = lexer.next_token()
            if not token:
                print("Lexer returns None as next token.  Correct")
                print(f"File {filename} handled correctly.")
                num_correct += 1
            else:
                print("Lexer did not return None at end of file.  Incorrect")
    except FileNotFoundError:
        print("Lexer did not open file.  Incorrect")
    except ValueError:
        print("Lexer raised ValueError when it should not have.  Incorrect")
    print()

    if num_correct == num_tested:
        print("All correct.  Nice job")
    else:
        print("Not all correct.  Keep working on it.") 