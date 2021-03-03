import sys
from datetime import date

class Record:
    """Represent a record."""
    def __init__(self , _date , _category , _description , _amount):
        self._category = _category
        self._description = _description
        self._amount = _amount
        self._date = _date
    @property
    def category(self):
        return self._category
    @property
    def description(self):
        return self._description
    @property
    def amount(self):
        return self._amount
    @property
    def date(self):
        return self._date

#-------------------------------------------------------------------------------------
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """ 1. Read from 'records.txt' or prompt for initial amount of money.
        # 2. Initialize the attributes (self._records and self._initial_money)
        #    from the file or user input."""
        self._records = []
        try:
            with open('records.txt' , 'r') as fh:
                #print('Welcome back!')
                try:
                    self._initial_money = int(fh.readline())      # 檔案中的第一行為初始錢包裡的錢
                except ValueError:
                    sys.stderr.write('The record is wrong. Set to 0 by default.\n')
                    self._initial_money = 0
        
                for line in fh.readlines():
                    line_s = line.split(' ')
                    record = Record( line_s[0] , line_s[1] , line_s[2] , int(line_s[3]) )
                    self._records.append( record )
        except FileNotFoundError:    # 尚未建檔 , 詢問一開始有多少錢
            '''try:
                self._initial_money = int(input('How much money do you have? '))
            except:
                sys.stderr.write('Invalid value for money. Set to 0 by default.\n')
                self._initial_money = 0'''
            self._initial_money = 0
    
    @property
    def initial_money(self):
        return self._initial_money

    @property
    def records(self):
        return self._records

    def add(self , record , categories):
        """ 1. Define the formal parameter so that a string input by the user
        #    representing a record can be passed in.
        # 2. Convert the string in to a Record instance.
        # 3. Check if the category is valid. For this step, the predefined
        #    categories have to be passed in through the parameter.
        # 4. Add the Record into self._records if the category is valid."""
        record = record.split(' ')
        try:
            if len(record) == 3:
                boo = categories.is_category_valid(record[0])     # 判斷是否有這個 categories
            else:
                boo = categories.is_category_valid(record[1])

            if boo == False:
                sys.stderr.write('The specified category is not in the category list.')
                sys.stderr.write('You can check the category list by command "view categories".')
                sys.stderr.write('Fail to add a record.')
                return

            if len(record) == 3:
                today = date.today()
                new_record = Record( str(today) , record[0] , record[1] , int(record[2]) )
                self._records.append( new_record )
            else:
                try:
                    date.fromisoformat(str(record[0]))
                except:
                    sys.stderr.write('The format of date should be YYYY-MM-DD.\nFail to add a record.\n')
                    return
                new_record = Record( str(record[0]) , record[1] , record[2] , int(record[3]) )
                self._records.append( new_record )
        except IndexError:      # 無法分成3個
            sys.stderr.write('The format of a record should be like this: breakfast -50. \nFail to add a record.\n')
        except ValueError:      # 日期格式錯誤
            sys.stderr.write('Value of input is wrong\nFail to add\n')

    def view(self):
        """ 1. Print all the records and report the balance."""
        surplus = self._initial_money
        print('Date        Category     Description     Amount')
        print('=========== ============ =============== ========')
        for i in range(len(self._records)):
            print("{:<12s}{:<13s}{:<16s}{:<10d}".format( self._records[i].date , self._records[i].category , self._records[i].description , self._records[i].amount ))
            surplus = surplus + self._records[i].amount      # 錢包剩餘的錢
        print('=================================================')
        print('Now you have %d dollars.' %surplus)    


    def delete(self):
        """ 1. Define the formal parameter.
        # 2. Delete the specified record from self._records."""
        item = len( self._records )    # 有多少筆資料
        if item == 0:   # 沒有任何資料
            print('There is nothing to delete.')
            return

        i = 1
        print('No. Date        Description     Amount')      # 輸入編號來選擇要刪哪一個
        print('=== =========== =============== =========')        
        for i in range(item):
            print("{:02d}  {:<12s}{:<16s}{:<10d}".format( i+1 , self._records[i].date , self._records[i].description , self._records[i].amount))

        print('Which record do you want to delete (Enter number)?',end=' ')

        try:
            delete_record = int(input())
            del self._records[ delete_record-1 ]
        except ValueError:  # 無法轉成數字
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
        except IndexError:  # 輸入的數字超出範圍
            sys.stderr.write('There\'s no record with number{delete}. Fail to delete a record.\n')

    def find(self, target_categories):
        """ 1. Define the formal parameter to accept a non-nested list
        #    (returned from find_subcategories)
        # 2. Print the records whose category is in the list passed in
        #    and report the total amount of money of the listed records."""

        L = list( filter(lambda n: n.category in target_categories , self._records))
        return L

        '''print('Category    Date            Description     Amount')
        print('=========== =============== =============== ========')
        for i in range(len(L)):
            print("{:<13s}{:<12s}{:<16s}{:<10d}".format( L[i].category , L[i].date ,L[i].description , L[i].amount ))
            surplus = surplus + L[i].amount      # 錢包剩餘的錢
        print('==================================================')
        print('The total amount above is %d.' %surplus)'''


    def save(self):
        """ 1. Write the initial money and all the records to 'records.txt'. """
        store = []
        for i in range(len( self._records)):           # 每一筆資料一行
            store += str( self._records[i].date)
            store += ' '
            store += str( self._records[i].category )
            store += ' '
            store += str( self._records[i].description )
            store += ' '
            store += str( self._records[i].amount )
            store += '\n'

        with open('records.txt','w') as fw:
            fw.write(str( self._initial_money ))
            fw.write('\n')
            fw.writelines(store)

    def change_initial(self, money):
        self._initial_money = money