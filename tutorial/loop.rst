Loop
----

The ``read_input`` method takes a keyword arg called ``on_exit`` that
dictates what do when ``^D`` is pressed. The ``AbortAction`` is a class that
provides various opitons and we've chosen to throw an exception called
``Exit``. This exception is caught in the except clause and we quit the
program.

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

