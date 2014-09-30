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
