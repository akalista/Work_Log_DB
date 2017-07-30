import unittest
import Log
import Database
import Errors

log = Log
db = Database
error = Errors


class LogTests(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()

# ['Employee: Anton', 'Task Name: W', 'Time Spent: 2', 'Additional Notes: A', 'Date of Entry: 07/26/2017']
# ['Anton', 'W', '2', 'A', '07/26/2017'])