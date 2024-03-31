
import os

def convert_custom_csv(file_path, delimiter):
    
    current_path = os.path.dirname(os.path.realpath(__file__))

    output_path = current_path + (file_path.split('.')[0] + '.csv')
    
    output_file = open(output_path, 'w')

    with open(current_path + file_path) as file:
        for line in file:
            delims = line.strip().split(delimiter)
            
            if(len(delims) > 1):
                for i in range(0,len(delims)):
                    if(delims[i] != ''):
                        if (i < len(delims) -1): output_file.write(delims[i].strip() + ',')
                        else: output_file.write(delims[i] + '\n')
                    elif(i == len(delims) -1): output_file.write('\n')

convert_custom_csv('/data/SNasiagosn.txt', '|')

