import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def tokenize(source_code):
    formatted_code = source_code.replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ")
    tokens = formatted_code.split()

    i = 0
    while i < len(tokens):
        if tokens[i].startswith('"'):
            j = i
            while not tokens[j].endswith('"'):
                j += 1
            tokens[i:j + 1] = [''.join(tokens[i:j + 1])]
        elif tokens[i] == "[":
            j = i
            while tokens[j] != "]" and j < len(tokens):
                j += 1
            if j == len(tokens):
                raise SyntaxError("Bracket not closed")
            tokens[i:j + 1] = [''.join(tokens[i:j + 1])]

        i += 1
    print("Tokens:", tokens)
    return tokens



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def get_current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def eat_token(self):
        self.current_token_index += 1

    def program(self):
        asts = []
        while self.current_token_index < len(self.tokens):
            if self.get_current_token() == ";":  # Skip over semicolons
                self.eat_token()
                continue
            asts.append(self.expression())
        print("ASTs:", asts)
        return asts

    def parse_array(self):
        current_token = self.get_current_token()
        if not current_token.startswith("[") or not current_token.endswith("]"):
            raise SyntaxError("Invalid array format")

        elements = current_token[1:-1].split(",")
        return elements

    def expression(self):
        # Cas pour la fonction 'ecrire'
        if self.get_current_token() == "ecrire":
            self.eat_token()  # Consomme le mot "ecrire"
            if self.get_current_token() != "(":
                raise SyntaxError(f"Expected '(', got: {self.get_current_token()}")
            self.eat_token()  # Consomme le "("

            # Vérifie si le token actuel est un tableau
            if self.get_current_token().startswith("[") and self.get_current_token().endswith("]"):
                array_expr = self.parse_array()  # Parse le tableau
                expr = ["ARRAY", array_expr]  # Crée un noeud AST pour le tableau
                self.eat_token()  # Consomme le token de tableau
            else:
                expr = self.expression()  # Récupère la variable, la valeur ou l'expression à imprimer

            if self.get_current_token() != ")":
                raise SyntaxError(f"Expected ')', got: {self.get_current_token()}")
            self.eat_token()  # Consomme le ")"
            return ["Ecrire", expr]

        # Cas pour les assignations
        if self.look_ahead_token() == "=":
            var_name = self.get_current_token()
            self.eat_token()  # Consomme le nom de la variable
            self.eat_token()  # Consomme le '='
            expr = self.expression()  # Récupère la valeur ou l'expression à assigner
            return ["ASSIGN", var_name, expr]

        # Gestion des expressions arithmétiques
        left = self.term()  # Récupère le premier terme
        while self.get_current_token() in ["+", "-"]:
            op = self.get_current_token()
            self.eat_token()  # Consomme l'opérateur
            right = self.term()  # Récupère le terme suivant
            left = [op, left, right]  # Combine l'opérateur avec les deux termes
        return left

    def term(self):
        left = self.factor()  # récupère le premier facteur
        while self.get_current_token() in ["*", "/"]:
            op = self.get_current_token()
            self.eat_token()  # Consomme l'opérateur
            right = self.factor()  # récupère le facteur suivant
            left = [op, left, right]  # Combines l'opérateur avec les deux facteurs
        return left

    def factor(self):
        token = self.get_current_token()
        if token.isdigit():  # Si le token est un chiffre
            self.eat_token()  # Consomme le chiffre
            return ["NUM", int(token)]
        elif token.isalpha():  # Si le token est une variable
            self.eat_token()  # Consomme le nom de la variable
            return ["VAR", token]
        elif token.startswith("[") and token.endswith("]"):  # Si le token est un tableau
            self.eat_token()  # Consomme le tableau
            return ["ARRAY", self.parse_array(token)]
        elif token.startswith('"') and token.endswith('"'):  # Si le token est une chaîne de caractères
            self.eat_token()  # Consomme la chaîne
            # Enlève les guillemets pour obtenir la chaîne pure
            return ["STRING", token[1:-1]]
        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_array(self, array_token):
        # Supprime les crochets et divise les éléments du tableau
        elements = array_token[1:-1].split(",")
        return [elem.strip() for elem in elements]

    def look_ahead_token(self):
        if self.current_token_index + 1 < len(self.tokens):
            return self.tokens[self.current_token_index + 1]
        return None

def infix_to_postfix(tokens):
    output = []
    ops = []
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token in ['+', '-', '*', '/']:
            while ops and ops[-1] in ['+', '-', '*', '/'] and precedence[ops[-1]] >= precedence[token]:
                output.append(ops.pop())
            ops.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            ops.pop()  # pop '('
        elif token.startswith('"') and token.endswith('"'):  # Ajout de cette condition pour les chaînes
            output.append(token)

    while ops:
        output.append(ops.pop())

    print("output postfix : ", output)
    return output


def generate_code(ast):
    machine_code = []

    if ast[0] == "ASSIGN":
        var_name = ast[1]
        value_expr = ast[2]
        value_code = generate_code(value_expr)
        machine_code.extend(value_code)
        machine_code.append(f"STORE_VAR {var_name}")

    elif ast[0] == "Ecrire":
        expr_code = generate_code(ast[1])
        machine_code.extend(expr_code)
        machine_code.append("PRINT")

    elif ast[0] == "ARRAY":
        array_elements = ast[1]
        for element in array_elements:
            if element.isdigit():
                machine_code.append(f"LOAD {element}")
            else:
                # Ajouter la logique pour gérer d'autres types d'éléments si nécessaire
                pass
        machine_code.append(f"LOAD_ARRAY {len(array_elements)}")

    elif ast[0] in ['+', '-', '*', '/']:
        left_code = generate_code(ast[1])
        right_code = generate_code(ast[2])
        machine_code.extend(left_code)
        machine_code.extend(right_code)
        machine_code.append({
            '+': "ADD",
            '-': "SUB",
            '*': "MUL",
            '/': "DIV"
        }[ast[0]])

    elif ast[0] == "NUM":
        machine_code.append(f"LOAD {ast[1]}")

    elif ast[0] == "VAR":
        machine_code.append(f"LOAD_VAR {ast[1]}")

    elif ast[0] == "STRING":
        # Gérer les chaînes de caractères
        string_value = ast[1]
        machine_code.append(f'LOAD_STRING "{string_value}"')

    else:
        raise ValueError(f"Unexpected AST node: {ast}")

    return machine_code

def emit_binary(instructions, filename):
    binary_representation = bytearray()
    full_path = os.path.join(BASE_DIR, filename)

    for instruction in instructions:
        if instruction.startswith("STORE_VAR "):
            binary_representation.append(8)  # Opcode pour STORE_VAR
            var_name = instruction.split()[1]
            for char in var_name:
                binary_representation.append(ord(char))  # Convertit chaque caractère en son code ASCII
            binary_representation.append(0)  # Terminez le nom de la variable avec un byte nul (0)

        elif instruction.startswith("LOAD_VAR "):
            binary_representation.append(9)  # Opcode pour LOAD_VAR
            var_name = instruction.split()[1]
            for char in var_name:
                binary_representation.append(ord(char))
            binary_representation.append(0)

        elif instruction.startswith("LOAD "):
            binary_representation.append(1)  # LOAD
            binary_representation.append(int(instruction.split()[1]))

        elif instruction.startswith("LOAD_STRING"):
            binary_representation.append(6)  # LOAD_STRING
            string_value = instruction.split()[1]
            for char in string_value:
                binary_representation.append(ord(char))
            binary_representation.append(0)  # Fin de la chaîne avec un byte nul

        elif instruction == "ADD":
            binary_representation.append(2)

        elif instruction == "SUB":
            binary_representation.append(3)

        elif instruction == "MUL":
            binary_representation.append(4)

        elif instruction == "PRINT":
            binary_representation.append(5)

        elif instruction.startswith("LOAD_ARRAY"):
            binary_representation.append(7)
            array_length = int(instruction.split()[1])
            binary_representation.append(array_length)

    with open(full_path, 'wb') as file:
        file.write(binary_representation)

    print(os.path.exists(full_path))


def compile(source_code):
    tokens = tokenize(source_code)
    parser = Parser(tokens)
    asts = parser.program()

    machine_codes = []
    for ast in asts:
        machine_codes.extend(generate_code(ast))

    emit_binary(machine_codes, "output.bin")
    print("Machine Codes:", machine_codes)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python minimath_compiler.py [source_file]")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        source_code = f.read()

    print("Source code read from file:", source_code)
    compile(source_code)
    print("Compilation terminée. Vérifiez output.bin.")

