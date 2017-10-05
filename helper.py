def parseArguments(argv):
    """Parses cli input -options and --flags into a dictionary."""
    params = {}
    points = []
    while argv:
        if argv[0][0] == '-' and argv[0][1] == '-':
            # Found flag
            params[argv[0]] = True
        elif argv[0][0] == '-' and argv[0][1] == 'x':
            # Found individual
            points.append(argv[1])
        elif argv[0][0] == '-':
            # Found option
            params[argv[0]] = argv[1]
        argv = argv[1:]

    params['-x'] = points
    return params