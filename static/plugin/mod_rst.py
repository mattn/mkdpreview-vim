from docutils.core import publish_parts

def preview(s):
  return publish_parts(s, writer_name='html')['body']

if __name__ == '__main__':
  print preview('''
*anurag*
''')
