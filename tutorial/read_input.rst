Take user input.
----------------

Create an object of type ``CommandLineInterface`` from ``prompt_toolkit`` and start accepting input.

.. code:: python

    from prompt_toolkit import CommandLineInterface

    def main():
        cli = CommandLineInterface()
        code_obj = cli.read_input()
        print 'You entered:', code_obj.text

    if __name__ == '__main__':
        main()



