from csv import reader

file = open("example.csv", "r")

new_file = []

for line in file:
    data = line.split(",")
    xi_val = int(data[0])
    yi_val = int(data[1])
    closeness_val = int(data[2])
    for line2 in file:
        
        #if index != index2:
        xi2_val = int(data[0])
        yi2_val = int(data[1])
        if( (((xi2_val - xi_val)**2 + (yi2_val - yi_val)**2 )**0.5) < close ) : 
            new_closeness_val = closeness_val + 1 
            new_line = "$s, %s, %s" % (data[0], data[1], new_closeness_val)
            new_file.append(new_line)

        else: new_file.append(line)

file.close()

file = open("example.csv", "w")

for line in new_file:
    file.write(line)

file.close()

