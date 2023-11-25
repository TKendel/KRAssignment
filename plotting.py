# opening the file in read mode 
my_file = open("performance_1.2 copy.txt", "r") 
  
# reading the file 
data = my_file.read() 
  
# replacing end splitting the text  
# when newline ('\n') is seen.
data_into_list = data.split(",\n")
print(data_into_list) 
my_file.close() 

def graph_series(data_into_list):
    from matplotlib import pyplot


    values = {}
    for element in data_into_list:
        if element[0] not in values:
            values[element[0]] = [(element[2] - element[1])]
        else:
            values[element[0]].append(element[2] - element[1])
    for key, value in values.items():
        pyplot.plot(value, markersize=20,label=key)
    pyplot.legend()
    pyplot.show()

graph_series(data_into_list)
