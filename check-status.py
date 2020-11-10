with open('error.txt') as f1:
    data1 = f1.read()

with open('output.txt') as f2:
    data2 = f2.read()
    if 'Opening Teensy Loader' in data1 or 'Opening Teensy Loader' in data2:
        print("Pass")
    else:
        raise NameError(data1 + data2)
