# File: json_parser.py
# Author: Kent Morris 
# Date: Novemeber 22nd 2022
# Description: This program runs a JSON_Parser that parses Arrays and Objects and checks if they are valid or Not


from pickle import TRUE
from json_lexer import Token # Copy your working json_lexer.py file from PSA1
from json_lexer import JSON_lexer
import json


class JSON_parser:
    def __init__(self, filename):
        """
        Initializes the parser to read from the file with filename 'filename'
        """

        # Create a lexer tied to the input file named filename. 
        
        self.lexer = JSON_lexer(filename)

    def parse(self):
        """
        Parse the JSON file that this parser was initialized with.
        Returns the Python data structure represented by the JSON file.
        Raises ValueError if the file has incorrect format.        
        """

        # Start with a call to the self.element() method, and
        # return what that method returns.  Make sure there are no
        # tokens following the single element.

        
        lst = self.element()
        
        # if next_token is not None
        if self.lexer.next_token() != None:
            raise ValueError
        
        return lst

    def element(self):
        """
        Reads from the current position in the input file an
        element, and returns that element.
        Raises ValueError if the element is invalid.        
        """

        # Peek at the next token.  If it is a base case
        # element, then read the token, and return its value.
        # If its a recursive element (object or array),
        # then call the appropriate method, and return the 
        # element returned by that method.

        
        '''Our Comment: In this function we first peek_next_token so that every time this function is recursively called we can,
        always store the value we want to later read once we find what kind of element/Token we are reading.'''
        
        
        token = self.lexer.peek_next_token()
        if token == None:
            raise ValueError

        if token.token_type == "STRING" or token.token_type == "NUMBER" or token.token_type == "TRUE" or token.token_type == "FALSE" or token.token_type == "NULL":
            return self.lexer.next_token().value


        if token.token_type == "LEFT_BRACKET":
            return self.array()
            

        if token.token_type == "LEFT_BRACE":
            return self.object()
            
        else:
            raise ValueError


    def object(self):
        """
        Reads from the current position in the input file an
        object (in Python, a dictionary), and returns that object
        as a Python dictionary.
        Raises ValueError if the object is invalid.
        """

        # Read the { token.  If the token following
        # that is either None (no more tokens), or RIGHT_BRACE,
        # then the object has no key/value pairs.
        # Otherwise, call member() to get the first key/value pair,
        # and remaining_members() to get the remaining key/value pairs.
        # Finally, read the } token, and return the dictionary formed
        # from what is returned by member() and remaining members() 

        '''Our Comment: This function reads the first token of a dictionary checking if its a left_Brace and if not raises ValueError.
        We then call our member function to return the first key-object pair, then remaining member to get the rest.
        we then read in the final token to make sure its a Right_Brace so that it is a valid dictionary and if not raises ValueError.
        The we combine the members of our self.member and self.remaining_members into one dictionary and return it'''
        
        r_token = self.lexer.next_token()
        if r_token == None or r_token.token_type == "RIGHT_BRACE":
            raise ValueError

        member = self.member()
        rem_members = self.remaining_members()
        
        r_token = self.lexer.next_token()
        if r_token == None or  r_token.token_type != "RIGHT_BRACE":
            raise ValueError
        
        for i in rem_members.keys():
            member[i] = rem_members[i]
            
        return member
        



    def member(self):
        """
        Reads from the current position in the input file a
        member (in Python, a dictionary), and returns that member
        as a Python dictionary.
        Raises ValueError if the member is invalid.
        """
        
        '''Our Comment:This function first checks if the key in the first member is valid and if not then the dictionary is empty so we return a empty dictionary.
         we then read the key value that we peeked and store it as a key variable to later set to our dictionary that we return.
         then we call peek to see if a colon is called to separate key-value pair and if not raise ValueError. We then read the colon and
         call self.member to get the element of our first member value. Now that we know the first member is a dictionary we return that member.'''
        
        token = self.lexer.peek_next_token()
        if token == None or token.token_type != "STRING":
            return {}
        
        r_token = self.lexer.next_token()
        key = r_token.value
        
        token = self.lexer.peek_next_token()
        if token.token_type != "COLON":
            raise ValueError
        
        r_token = self.lexer.next_token()
        value = self.element()
        
        element = {key:value}
        return element
        


    def remaining_members(self):
        """
        Reads from the current position in the input file
        the remaining members of an object (in Python, a dictionary), 
        and returns those members as a Python dictionary.
        Raises ValueError if the remaining members are invalid.
        """
        
        # Peek at the next token. If the peeked token
        # is a COMMA, then read the token (the COMMA),
        # the next member, and the remaining members.
        # Return the next member and remaining members
        # as a single Python dictionary.
        
        '''Our Comment: In this function we return all the remaing members in the dictionary and if there are more than one we
        merge them together to be later added to our first member dictionary. We peek first to make sure their is a comma separating
        memeber and if not then the remaining dictionary is empty.'''
        
        token = self.lexer.peek_next_token()
        if token == None or token.token_type != "COMMA":
            return {}

        else:
            self.lexer.next_token()
            mem = self.member()
            rem_mem = self.remaining_members()
            for i in rem_mem.keys():
                mem[i] = rem_mem[i]
            return mem


    def array(self):
        """
        Reads from the current position in the input file an
        array (in Python, a list), and returns that array
        as a Python list.
        Raises ValueError if the array is invalid.
        """
        # Read the [ token.  If the token following
        # that is either None (no more tokens), or RIGHT_BRACKET,
        # then the array has no elements.
        # Otherwise, call element() to get the first element,
        # and remaining_elements() to get the remaining elements.
        # Finally, read the ] token, and return the single list
        # formed from what is returned by element() and 
        # remaining_elements().

        '''Our Comment: This function reads the first token of a array making sure it starts with a left_bracket so that its a valid array.
        If not raises ValueError,then checks to make sure it has a token after if not raises value error and if next token is a right_bracket then
        returns a empty list. Then once all those are passes there are elements inside the array so we call self.element to get the first element of
        the array and self.remaining_elements to get the rest and merge them into one list to return. Also check that the last element read is a Right Bracket
        so its a valid list, if not raises ValueError'''
        
        r_token = self.lexer.next_token()
        if r_token == None or r_token.token_type != "LEFT_BRACKET":
            raise ValueError
                
        token = self.lexer.peek_next_token()
        if token == None:
            raise ValueError
            
        if token.token_type == "RIGHT_BRACKET":
            self.lexer.next_token()
            return []

        
        
        element = [self.element()]
        element.extend(self.remaining_elements())
                
        r_token = self.lexer.next_token()

        if r_token == None or r_token.token_type != "RIGHT_BRACKET":
            raise ValueError
        
        return element
        

        
        

        



    def remaining_elements(self):
        """
        Reads from the current position in the input file
        the remaining elements of an array (in Python, a list), 
        and returns those elements as a Python list.
        Raises ValueError if the remaining elements are invalid.
        """

        # Peek at the next token. If the peeked token
        # is a COMMA, then read the token (the COMMA),
        # the next element, and the remaining elements.
        # Return the next element and remaining elements
        # as a single Python list.

        '''Our Comment: This function recursively iterates over each nested list collecting the elements and adding them to the other 
        remaing elements,eventually returning the final list to self.array. We peek the next token at the beggining of the function
        to make sure a comma separates the element or if nested list is empty we return a empty list. '''
        
        token = self.lexer.peek_next_token()
        if token == None or token.token_type != "COMMA":
            return []

        self.lexer.next_token()
        element = [self.element()]
        element.extend(self.remaining_elements())
        
        return element


if __name__ == '__main__':
    # Test the JSON_parser class.
    num_tested = 0
    num_correct = 0

    num_tests = 26
            
    # Test the files
    for i in range(1, num_tests + 1):
        filename = f"test{i}.json"
        print(f"Testing file {filename}.")
        num_tested += 1  
        try:
            f = open(filename)
            json_str = f.read()
            json_element_correct = json.loads(json_str)
            try:
                
                # Get our data structure
                parser = JSON_parser(filename)
                json_element_test = parser.parse()

                # Compare
                if json_element_correct == json_element_test:
                    print("Correct.  Nice job!")
                    print(json_element_test)
                    num_correct += 1
                else:
                    print("Not correct")
                    print(json_element_correct)
                    print(json_element_test)
            except ValueError:
                print("Parser raised value error when it should not have.  Incorrect.")
        
        except json.decoder.JSONDecodeError:
            try:
                # Get our data structure
                parser = JSON_parser(filename)
                json_element_test = parser.parse()
                print("Parser did not raise value error when it should have.  Incorrect.")
            except ValueError:
                print("Parser raised value error.  Correct.")
                num_correct += 1

        except FileNotFoundError:
            print("Parser could not open file.  Incorrect")
        print()

    print(f"Num tested = {num_tested}")    
    print(f"Num correct = {num_correct}")
    if num_tested == num_correct:
        print("All correct.  Nice job")
    else:
        print("Not all correct.  Keep working on it.")