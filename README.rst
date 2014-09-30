Build a REPL With Python Prompt Toolkit
'''''''''''''''''''''''''''''''''''''''

The aim of this tutorial is to build an interactive command line interface for
SQLite database using prompt_toolkit_.

prompt_toolkit_ is an easy to use library for building powerful command
lines (REPLs) in Python.


First install the library using pip.

::

    pip install prompt_toolkit

Let's get started!

#. Read User Input

   Create an object of type ``CommandLineInterface`` from ``prompt_toolkit`` and
   start accepting input using the ``read_input()`` method.
 
   .. code:: python
 
       from prompt_toolkit import CommandLineInterface
 
       def main():
           cli = CommandLineInterface()
           code_obj = cli.read_input()
           print 'You entered:', code_obj.text
 
       if __name__ == '__main__':
           main()


#. Loop The REPL

   The ``read_input`` method takes a kwarg called ``on_exit`` that dictates
   what happens ``^D`` is pressed. ``AbortAction`` is a class that provides
   various opitons and we've chosen to throw an exception called ``Exit``. This
   exception is caught in the except clause and we quit the program.
   
   .. code:: python
   
       from prompt_toolkit import CommandLineInterface, AbortAction, Exit
   
       def main(): 
           cli = CommandLineInterface() 
           try: 
               while True: 
                   code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION) 
                   print 'You entered:', code_obj.text 
           except Exit: 
               print 'GoodBye!'
   
       if __name__ == '__main__': 
           main()
   

#. Syntax Highlighting

   The ``prompt_toolkit.layout`` class is responsible for how the REPL is
   displayed. This allows us to customize the prompt and choose a lexer for
   We're going to use the ``SqlLexer`` from the Pygments_ library for
   highlighting.

   .. code:: python

       from prompt_toolkit import CommandLineInterface, AbortAction, Exit
       from prompt_toolkit.layout import Layout
       from prompt_toolkit.layout.prompt import DefaultPrompt
       from pygments.lexers.sql import SqlLexer
   
       def main():
           layout = Layout(before_input=DefaultPrompt('> '), lexer=SqlLexer)
           cli = CommandLineInterface(layout=layout)
           try:
               while True:
                   code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION)
                   print 'You entered:', code_obj.text
           except Exit:
               print 'GoodBye!'
   
       if __name__ == '__main__':
           main()


#. Auto-completion
   
   Create a class called ``SqlCompleter`` that is derived from
   ``prompt_toolkit.Completer``. Define a set of ``keywords`` for
   auto-completion. Override the methods ``complete_after_insert_text`` and
   ``get_completions``.  The first method ``complete_after_insert_text``
   determines whether you want auto-completion to trigger as soon as you start
   typing or only when you hit <tab>. The second method ``get_completions`` is
   used to populate the completion menu with possible candidates from the list
   of ``keywords``.

   This ``SqlCompleter`` class will be used by ``prompt_toolkit.Line`` class
   which controls the cusor position and completion of a line. 

   .. code:: python

       from prompt_toolkit import CommandLineInterface, AbortAction, Exit
       from prompt_toolkit.layout import Layout
       from prompt_toolkit.line import Line
       from prompt_toolkit.layout.prompt import DefaultPrompt
       from prompt_toolkit.layout.menus import CompletionMenu
       from prompt_toolkit.completion import Completion, Completer
       from pygments.lexers.sql import SqlLexer

       class SqlCompleter(Completer):
           keywords = ['create', 'select', 'insert', 'drop', 
                       'delete', 'from', 'where', 'table']

           def complete_after_insert_text(self, document):
               """
               Open completion menu when we type a character.
               (Except if we typed whitespace.)
               """
               return not document.char_before_cursor.isspace()

           def get_completions(self, document):
               word_before_cursor = document.get_word_before_cursor()

               for keyword in self.keywords:
                   if keyword.startswith(word_before_cursor):
                       yield Completion(keyword, -len(word_before_cursor))
   
       def main():
           layout = Layout(before_input=DefaultPrompt('> '), 
                           lexer=SqlLexer, menus=[CompletionMenu()])
           line = Line(completer=SqlCompleter())
           cli = CommandLineInterface(layout=layout, line=line)
           try:
               while True:
                   code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION)
                   print 'You entered:', code_obj.text
           except Exit:
               print 'GoodBye!'
   
       if __name__ == '__main__':
           main()


#. Hook up Sqlite

   This step is totally optional ;). So far we've been focusing on building the
   REPL. Now it's time to relay the input to SQLite. 

   Obviously I haven't done the due diligence to deal with the errors. But it
   gives you an idea of how to get started.

   .. code:: python

       import sys
       import sqlite3

       from prompt_toolkit import CommandLineInterface, AbortAction, Exit
       from prompt_toolkit.layout import Layout
       from prompt_toolkit.line import Line
       from prompt_toolkit.layout.prompt import DefaultPrompt
       from prompt_toolkit.layout.menus import CompletionMenu
       from prompt_toolkit.completion import Completion, Completer
       from pygments.lexers.sql import SqlLexer

       class SqlCompleter(Completer):
           keywords = ['create', 'select', 'insert', 'drop', 
                       'delete', 'from', 'where', 'table']

           def complete_after_insert_text(self, document):
               """
               Open completion menu when we type a character.
               (Except if we typed whitespace.)
               """
               return not document.char_before_cursor.isspace()

           def get_completions(self, document):
               word_before_cursor = document.get_word_before_cursor()

               for keyword in self.keywords:
                   if keyword.startswith(word_before_cursor):
                       yield Completion(keyword, -len(word_before_cursor))
   
       def main(database):
           connection = sqlite3.connect(database)
           layout = Layout(before_input=DefaultPrompt('> '), 
                           lexer=SqlLexer, menus=[CompletionMenu()])
           line = Line(completer=SqlCompleter())
           cli = CommandLineInterface(layout=layout, line=line)
           try:
               while True:
                   code_obj = cli.read_input(on_exit=AbortAction.RAISE_EXCEPTION)
                   with connection:
                       messages = connection.execute(code_obj.text)
                       for message in messages:
                           print message
           except Exit:
               print 'GoodBye!'
   
       if __name__ == '__main__':
           if len(sys.argv) < 2:
              db = ':memory:'
           else:
               db = sys.argv[1]

           main(db)

.. _prompt_toolkit: https://github.com/jonathanslenders/python-prompt-toolkit
.. _Pygments: http://pygments.org/
