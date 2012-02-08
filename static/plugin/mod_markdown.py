import markdown

def preview(s):
  return markdown.markdown(s)

if __name__ == '__main__':
  print preview('''
hello
=====

world
-----
''')
