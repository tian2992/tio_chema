import unittest
import bot_chema

class ChemaBotCheck(unittest.TestCase):
  def __init__(self):
    self.c = ChemaBot(self.config['nickname'])
    self.c.factory = self
    self.c.say = show

    ## TODO: enable testing of _execute_command
    self.c._execute_command = show

  def show(self, *args, **kwargs):
    print str(args) + str(kwargs)




if __name__ == "__main__":
    unittest.main()