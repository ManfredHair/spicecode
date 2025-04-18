import os

# gustavo testando alguma coisa 
from spice.analyzers.identation import detect_indentation
from spice.utils.get_langague import detect_language


# this is the analyze function
def analyze_file(file_path: str, selected_stats=None):
    """
    Analyze a file and return only the requested stats.
    
    Args:
        file_path (str): Path to the file to analyze
        selected_stats (list, optional): List of stats to compute. If None, compute all stats.
    
    Returns:
        dict: Dictionary containing the requested stats
    """
    # default to all stats if none specified
    if selected_stats is None:
        selected_stats = ["line_count", "function_count", "comment_line_count", "identation_level"]

    # initialize results with the file name (dont change this please)
    results = {
        "file_name": os.path.basename(file_path)
    }
    
    LANG = detect_language(file_path)
    
    # read the code file only once and load it into memory
    with open(file_path, "r", encoding="utf-8") as file:
        code = file.read()
    
    # line count if requested
    if "line_count" in selected_stats:
        from spice.analyzers.count_lines import count_lines
        results["line_count"] = count_lines(code)

    # comment line count if requested
    if "comment_line_count" in selected_stats:
        from spice.analyzers.count_comment_lines import count_comment_lines
        results["comment_line_count"] = count_comment_lines(code, LANG)

    # @gtins botei sua funcao aqui pq ela usa o codigo raw e nao o tokenizado, ai so tirei ela ali de baixo pra nao ficar chamando o parser sem precisar
    # edit: ok i see whats going on, instead of appending the results to the resuls, this will itself print the results to the terminal
    # TODO: make analyze_code_structure return the results, then append those results to the results array
    if "identation_level" in selected_stats:
            analyze_code_structure(code)
    
    # only put the code through the lexer and proceed with tokenization if we need function count (UPDATE THIS WHEN  NEEDED PLEASE !!!!!!!!)
    if "function_count" in selected_stats:

        # get the lexer for the code's language
        from spice.utils.get_lexer import get_lexer_for_file
        LexerClass = get_lexer_for_file(file_path)
        
        # tokenize the code via lexer
        lexer = LexerClass(code)
        tokens = lexer.tokenize()
        
        # only put the code through the parser and proceed with parsing if we need function count (UPDATE THIS WHEN  NEEDED PLEASE !!!!!!!!)
        if "function_count" in selected_stats:

            # import parser here to avoid error i still dont know why but it works
            from parser.parser import Parser
            
            # prase tokens into AST
            parser = Parser(tokens)
            ast = parser.parse()
            
            # count functions
            from spice.analyzers.count_functions import count_functions
            results["function_count"] = count_functions(ast)
    
    return results





# im not sure what to do with this part 😂
# this is the identation analyzer
# but it's not included in the menu?
# im not going to change this since gtins knows better than me how this works
# but this needs to be refactores and included directly into the analyze_file function and the analyze menu
def analyze_code_structure(code):
    indentation_info = detect_indentation(code)

    print(f"Detected Indentation Type: {indentation_info['indent_type']}")
    print(f"Detected Indentation Size: {indentation_info['indent_size']}")
    for line, level in indentation_info["levels"]:
        # print(f"Indentation Level {level}: {line}")
        print(f"Detected Indentation Type: {indentation_info['indent_type']}")
        print(f"Detected Indentation Size: {indentation_info['indent_size']}")

# ----------------------------------------------------------------------------------------------------