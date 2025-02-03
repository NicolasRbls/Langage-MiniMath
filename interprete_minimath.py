import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def interpret_binary(filename):
    with open(filename, 'rb') as file:
        instructions = list(file.read())

    #print(f"Instructions loaded: {instructions}")  # Ajout de débogage
    stack = []

    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        #print(f"Processing instruction: {instruction}, Stack: {stack}")  # Ajout de débogage

        if instruction == 1:  # LOAD
            value = instructions[i + 1]
            stack.append(value)
            i += 2
        elif instruction == 2:  # ADD
            #print(f"Stack before ADD: {stack}")
            if len(stack) < 2:
                print("Erreur: Pas assez de valeurs dans la pile pour l'addition.")
                return
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
            i += 1
        elif instruction == 3:  # SUB
            if len(stack) < 2:
                print("Erreur: Pas assez de valeurs dans la pile pour la soustraction.")
                return
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            i += 1
        elif instruction == 4:  # MUL
            if len(stack) < 2:
                print("Erreur: Pas assez de valeurs dans la pile pour la multiplication.")
                return
            a = stack.pop()
            b = stack.pop()
            stack.append(b * a)
            i += 1
        elif instruction == 5:  # PRINT
            top_value = stack.pop()
            if isinstance(top_value, list):  # Check if it's a list (array)
                print(top_value)
            else:
                print(top_value)
            i += 1
        elif instruction == 6:  # LOAD_STRING
            string_value = ""
            i += 1
            while instructions[i] != 0:
                string_value += chr(instructions[i])
                i += 1
            stack.append(string_value)
            i += 1  # Pour l'instruction suivante
        elif instruction == 7:  # LOAD_ARRAY
            array_length = instructions[i + 1]
            new_array = [stack.pop() for _ in range(array_length)]
            new_array = new_array[::-1]  # Reverse the array
            stack.append(new_array)
            i += 2
        else:
            i += 1

# Utilisation :
interpret_binary(os.path.join(BASE_DIR, "output.bin"))
