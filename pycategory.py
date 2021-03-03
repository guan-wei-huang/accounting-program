import sys

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """ 1. Initialize self._categories as a nested list. """
        self._categories = [ 'expense' , [ 'food' , [ 'meal' , 'snack' , 'drink' ] , \
                              'transportation' , [ 'bus' , 'railway' ]] , 'income' , [ 'salary' , 'bonus' ]]

    def view(self, L = None , n=0 ):
        """ 1. Define the formal parameters so that this method
        #    can be called recursively.
        # 2. Recursively print the categories with indentation.
        # 3. Alternatively, define an inner function to do the recursion."""
        if L == None:
            L = self._categories
        a = []
        for i in range(len(L)):
            if type( L[i] ) == str:
                s = '  '*n + '- ' + L[i]
                a = a + [s]
            else:
                a = a + self.view( L[i] , n+1 )
        return a 

    def is_category_valid(self, category , categories = None):
        """# 1. Define the formal parameters so that a category name can be
        #    passed in and the method can be called recursively.
        # 2. Recursively check if the category name is in self._categories.
        # 3. Alternatively, define an inner function to do the recursion."""
        if categories == None:
            categories = self._categories
        for i in range(len(categories)):
            if type(categories[i]) == str:
                if(categories[i] == category):
                    return True
            else:           # 如果不是 str 就使用遞迴進入該 list
                boo = self.is_category_valid(category , categories[i])
                if boo == 1:
                    return True
        return False
 
    def find_subcategories(self, category):
        def find_subcategories_gen(category , categories , found = False):
            if type(categories) == list:
                for index , child in enumerate(categories):
                    yield from find_subcategories_gen(category , child , found)
                    if child == category and index+1 < len(categories) and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category , categories[index+1] , True)
            else:
                if categories == category or found == True:
                    yield categories
    
        return [ i for i in find_subcategories_gen(category , self._categories) ]
