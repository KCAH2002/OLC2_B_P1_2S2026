import ply.lex as lex


# palabras reservadas confirmadas en el enunciado actualizado
reserved = {
    "let": "LET",
    "mut": "MUT",
    "fn": "FN",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "loop": "LOOP",
    "match": "MATCH",
    "break": "BREAK",
    "continue": "CONTINUE",
    "return": "RETURN",
    "struct": "STRUCT",
    "true": "TRUE",
    "false": "FALSE",
    "i32": "TYPE_I32",
    "f64": "TYPE_F64",
    "bool": "TYPE_BOOL",
    "char": "TYPE_CHAR",
    "String": "TYPE_STRING",
}


# aqui coloco todos los tokens que mi lexer puede reconocer
tokens = [
    "IDENTIFIER",
    "BLOCK_COMMENT",
    "UNCLOSED_BLOCK_COMMENT",
    "LBRACE",
    "RBRACE",
] + list(reserved.values())


# almacena los errores encontrados durante el analisis
lexical_errors = []


# aqui le digo a ply que ignore espacios, tabulaciones y retornos de carro
t_ignore = " \t\r"

# con estas reglas reconozco las llaves de apertura y cierre
t_LBRACE = r"\{"
t_RBRACE = r"\}"


def find_column(source, token):
    """
    calcula la columna donde comienza un token
    """

    # busca el ultimo salto de linea antes del token
    last_newline = source.rfind("\n", 0, token.lexpos)

    # lexpos inicia en cero, pero la columna debe iniciar en uno
    return token.lexpos - last_newline


def t_BLOCK_COMMENT(token):
    r"/\*(.|\n)*?\*/"

    # actualiza la linea segun los saltos presentes en el comentario
    token.lexer.lineno += token.value.count("\n")

    # no se retorna el token porque los comentarios se descartan
    pass


def t_UNCLOSED_BLOCK_COMMENT(token):
    r"/\*(.|\n)*"

    # obtiene la posicion donde comenzo el comentario
    column = find_column(token.lexer.lexdata, token)

    lexical_errors.append(
        {
            "type": "lexical",
            "description": "El comentario de bloque no tiene cierre.",
            "line": token.lineno,
            "column": column,
            "fragment": token.value,
        }
    )

    # actualiza las lineas consumidas por el comentario incompleto
    token.lexer.lineno += token.value.count("\n")

    # el contenido se descarta despues de registrar el error
    pass


def t_LINE_COMMENT(token):
    r"//[^\n]*"

    # los comentarios de linea no generan tokens
    pass


def t_IDENTIFIER(token):
    r"[a-zA-Z_][a-zA-Z_0-9]*"

    # comprueba si el texto es una palabra reservada
    token.type = reserved.get(token.value, "IDENTIFIER")

    return token


def t_newline(token):
    r"\n+"

    # suma la cantidad de saltos encontrados
    token.lexer.lineno += len(token.value)


def t_error(token):
    """
    registra cualquier caracter que todavia no pueda reconocerse
    """

    column = find_column(token.lexer.lexdata, token)

    lexical_errors.append(
        {
            "type": "lexical",
            "description": f"El caracter '{token.value[0]}' no es reconocido.",
            "line": token.lineno,
            "column": column,
            "fragment": token.value[0],
        }
    )

    # avanza un caracter para impedir un ciclo infinito
    token.lexer.skip(1)


def build_lexer():
    """
    construye una nueva instancia del analizador lexico
    """

    return lex.lex()


def analyze_tokens(source):
    """
    analiza el codigo fuente y devuelve los tokens y errores encontrados
    """

    # elimina los errores de una ejecucion anterior
    lexical_errors.clear()

    lexer = build_lexer()
    lexer.lineno = 1
    lexer.input(source)

    generated_tokens = []

    for token in lexer:
        generated_tokens.append(
            {
                "type": token.type,
                "value": token.value,
                "line": token.lineno,
                "column": find_column(source, token),
            }
        )

    return {
        "tokens": generated_tokens,
        "errors": lexical_errors.copy(),
    }

if __name__ == "__main__":
    # aqui preparo un ejemplo valido para probar mi lexer
    test_source = """
fn main {
    // comentario de una linea
    let edad
    let mut Edad
    let activo
    if true
    while false

    /*
    comentario de varias lineas
    */
}
"""

    # aqui mando el texto al lexer
    result = analyze_tokens(test_source)

    print("TOKENS ENCONTRADOS")

    # aqui muestro cada token reconocido
    for generated_token in result["tokens"]:
        print(generated_token)

    print("\nERRORES ENCONTRADOS")

    # aqui muestro cada error encontrado
    for error in result["errors"]:
        print(error)