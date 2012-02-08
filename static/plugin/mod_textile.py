import textile

def preview(s):
  return textile.textile(s)

if __name__ == '__main__':
  print preview('''
... _This_ is a *test.*
... 
... * One
... * Two
... * Three
... 
... Link to "Slashdot":http://slashdot.org/
... """
''')
