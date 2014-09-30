Build a REPL With Python Prompt Toolkit
'''''''''''''''''''''''''''''''''''''''

The aim of this tutorial is to build an interactive command line interface for
SQLite database using prompt_toolkit_.

prompt_toolkit_ is an easy to use library for building powerful command
lines (REPLs) in Python.

.. _prompt_toolkit: https://github.com/jonathanslenders/python-prompt-toolkit

First install the library using pip.

::

    pip install prompt_toolkit


Let's get started!

#. Take user input.

   Create an object of type ``CommandLineInterface`` from ``prompt_toolkit`` and start accepting input.

   .. code:: python

       from prompt_toolkit import CommandLineInterface

       def main():
           cli = CommandLineInterface()
           code_obj = cli.read_input()
           print 'You entered:', code_obj.text

       if __name__ == '__main__':
           main()

