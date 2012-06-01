from distutils.core import setup

setup(name='pyle',
      version='0.1',
      description='Use Python for shell one-liners.',
      author='Alexander Ljungberg',
      author_email='aljungberg@slevenbits.com',
      url='https://github.com/aljungberg/pyle',
      py_modules=['pyle', 'pyle_test'],
      scripts=['pyle']
      )
