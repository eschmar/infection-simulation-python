def parseArguments(argv):
    """Parses cli input -options and --flags into a dictionary."""
    params = {}
    while argv:
        if argv[0][0] == '-' and argv[0][1] == '-':
            # Found flag
            params[argv[0]] = True
        elif argv[0][0] == '-':
            # Found option
            params[argv[0]] = argv[1]
        argv = argv[1:]
    
    return params
