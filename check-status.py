with open('error.txt') as f:
    data = f.read()
    if 'Opening Teensy Loader' in data:
        print("Pass")
    else:
        raise NameError(data)
