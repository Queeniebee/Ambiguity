'''

Full documentation: http://pegjs.majda.cz/documentation#grammar-syntax-and-semantics-parsing-expression-types

'x'   : match the literal character 'x'
[xyz] : match one of the literal character 'x', 'y', or 'z'
x+    : match x 1 or more times
x*    : match x 0 or more times
x?    : match x 0 or 1 times
!x    : match anything but the match x
x/y   : match x or y, trying in that order
v:x   : assign the result of the match x to the variable v

-->
'''

'''
BASIC RPLY API

from rply import ParserGenerator, LexerGenerator
from rply.token import BaseBox

lg = LexerGenerator()
# Add takes a rule name, and a regular expression that defines the rule.
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("NUMBER", r"\d+")

lg.ignore(r"\s+")

# This is a list of the token names. precedence is an optional list of
# tuples which specifies order of operation for avoiding ambiguity.
# precedence must be one of "left", "right", "nonassoc".
# cache_id is an optional string which specifies an ID to use for
# caching. It should *always* be safe to use caching,
# RPly will automatically detect when your grammar is
# changed and refresh the cache for you.
pg = ParserGenerator(["NUMBER", "PLUS", "MINUS"],
        precedence=[("left", ['PLUS', 'MINUS'])], cache_id="myparser")

@pg.production("main : expr")
def main(p):
    # p is a list, of each of the pieces on the right hand side of the
    # grammar rule
    return p[0]

@pg.production("expr : expr PLUS expr")
@pg.production("expr : expr MINUS expr")
def expr_op(p):
    lhs = p[0].getint()
    rhs = p[2].getint()
    if p[1].gettokentype() == "PLUS":
        return BoxInt(lhs + rhs)
    elif p[1].gettokentype() == "MINUS":
        return BoxInt(lhs - rhs)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : NUMBER")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))

lexer = lg.build()
parser = pg.build()

class BoxInt(BaseBox):
    def __init__(self, value):
        self.value = value

    def getint(self):
        return self.value

'''

from rply import ParserGenerator, LexerGenerator

# from rply.token import BaseBox 
# removed BaseBox because language deals with strings
# and not using RPython

lexgen = LexerGenerator()

lexgen.add('AND', r"(and)")
lexgen.add('WITHOUT', r"(without)")
lexgen.add('MULTIPLY', r"(multiply)")
lexgen.add('DIVIDE', r"(divide)")
lexgen.add("NOT", r"(not)")
lexgen.add("IF", r"(if)")
lexgen.add("ELSE", r"(else)")
lexgen.add("CHOOSE", r"(choose)")
lexgen.add("WHO", r"[^ ]")
lexgen.add("WHO", r"[^ ]")

# lexgen.add("COMMENT", r"(?#[a-zA-Z_][a-zA-Z0-9_]*)")
# lexgen.add("WHO", r"[a-zA-Z_][a-zA-Z0-9_]*")


'''
lexgen.add("WHO", r"[a-zA-Z_][a-zA-Z0-9_]*")
lexgen.add("WHAT", r"[a-zA-Z_][a-zA-Z0-9_]*")
lexgen.add("WHY", r"[a-zA-Z_][a-zA-Z0-9_]*")
lexgen.add("HOW", r"[a-zA-Z_][a-zA-Z0-9_]*")
lexgen.add("DEF", )
'''


pg = ParserGenerator(["WHO", "AND", "WITHOUT", "MULTIPLY", "DIVIDE"],
    precedence = [
		("left", ['AND', 'WITHOUT']),
		("left", ["MULTIPLY","DIVIDE"]),
		
	], cache_id="myparser")


@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')

def expression_person(p):
    # p is a list of the pieces matched by the right hand side of the
    # rule
    return Person(value_array[random.randrange(0, 10)])


@pg.production("main : expression")
def main(p):
    return p[0]

@pg.production("expr : expr AND expr")
@pg.production("expr : expr WITHOUT expr")
def expr_op(p):
    leftside = p[0]
    rightside = p[2]
    if p[1].gettokentype() == "AND":
        return BoxInt(leftside + rightside)
    elif p[1].gettokentype() == "WITHOUT":
        return BoxInt(leftside - rightside)
	elif p[1].gettokentype() == "MULTIPLY":
		return Mul(leftside, rightside)
    else:
        raise AssertionError("This is impossible, abort the time machine!")

@pg.production("expr : WHO")
def expr_num(p):
    return BoxInt(int(p[0].getstr()))


lexer = lexgen.build()
parser = pg.build()

# class BoxInt(BaseBox):
#     def __init__(self, value):
#         self.value = value
# 
#     def getint(self):
#         return self.value

'''
keywords = {
        "return": Keyword("RETURN", "RETURN", EXPR_MID),
        "if": Keyword("IF", "IF_MOD", EXPR_BEG),
        "unless": Keyword("UNLESS", "UNLESS_MOD", EXPR_BEG),
        "then": Keyword("THEN", "THEN", EXPR_BEG),
        "elsif": Keyword("ELSIF", "ELSIF", EXPR_BEG),
        "else": Keyword("ELSE", "ELSE", EXPR_BEG),
        "while": Keyword("WHILE", "WHILE_MOD", EXPR_BEG),
        "until": Keyword("UNTIL", "UNTIL_MOD", EXPR_BEG),
        "for": Keyword("FOR", "FOR", EXPR_BEG),
        "in": Keyword("IN", "IN", EXPR_BEG),
        "do": Keyword("DO", "DO", EXPR_BEG),
        "begin": Keyword("BEGIN", "BEGIN", EXPR_BEG),
        "rescue": Keyword("RESCUE", "RESCUE_MOD", EXPR_MID),
        "ensure": Keyword("ENSURE", "ENSURE", EXPR_BEG),
        "def": Keyword("DEF", "DEF", EXPR_FNAME),
        "class": Keyword("CLASS", "CLASS", EXPR_CLASS),
        "module": Keyword("MODULE", "MODULE", EXPR_BEG),
        "case": Keyword("CASE", "CASE", EXPR_BEG),
        "when": Keyword("WHEN", "WHEN", EXPR_BEG),
        "end": Keyword("END", "END", EXPR_END),
        "and": Keyword("AND", "AND", EXPR_BEG),
        "or": Keyword("OR", "OR", EXPR_BEG),
        "not": Keyword("NOT", "NOT", EXPR_BEG),
        "alias": Keyword("ALIAS", "ALIAS", EXPR_FNAME),
        "self": Keyword("SELF", "SELF", EXPR_END),
        "nil": Keyword("NIL", "NIL", EXPR_END),
        "__FILE__": Keyword("__FILE__", "__FILE__", EXPR_END),
        "__LINE__": Keyword("__LINE__", "__LINE__", EXPR_END),
        "true": Keyword("TRUE", "TRUE", EXPR_END),
        "false": Keyword("FALSE", "FALSE", EXPR_END),
        "defined?": Keyword("DEFINED", "DEFINED", EXPR_ARG),
        "super": Keyword("SUPER", "SUPER", EXPR_ARG),
        "undef": Keyword("UNDEF", "UNDEF", EXPR_FNAME),
        "next": Keyword("NEXT", "NEXT", EXPR_MID),
        "break": Keyword("BREAK", "BREAK", EXPR_MID),
    }
'''

