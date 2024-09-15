import os

mapping = {31: 0, 21: 1, 19: 2, 20: 3, 25: 4, 29: 5, 18: 6, 13: 7, 34: 8, 37: 9, 33: 10, 
    36: 11, 35: 12, 39: 13, 38: 14, 17: 15, 9: 16, 10: 17, 15: 18, 16: 19, 27: 20,
    11: 21, 12: 22, 32: 23, 6: 24, 24: 25, 40: 26, 28: 27, 23: 28, 7: 29, 0: 30,
    1: 31, 2: 32, 3: 33, 4: 34, 5: 35, 14: 36, 26: 37, 22: 38
}

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            with open(input_file, 'r') as f:
                lines = f.readlines()
            new_lines = []

            for line in lines:
                values = line.strip().split()
                x = int(values[0])
                if x in mapping:
                    mapped_x = mapping[x]
                    new_line = f"{mapped_x} " + " ".join(values[1:])
                    new_lines.append(new_line)

            with open(output_file, 'w') as f:
                f.write("\n".join(new_lines))

# Esempio di utilizzo:
input_folder = "your/input/folder"
output_folder = "your/output/folder"
process_files(input_folder, output_folder)
