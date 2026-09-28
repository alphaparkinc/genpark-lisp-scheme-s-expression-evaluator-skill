"""Minimalist Lisp / Scheme S-Expression Evaluator
100% Python Standard Library (math).
"""

import math

class LispEvaluator:
    """S-expression reader and tree-walking evaluator."""
    def __init__(self):
        self.global_env = {
            "+": lambda args: sum(args),
            "-": lambda args: args[0] - sum(args[1:]) if len(args) > 1 else -args[0],
            "*": lambda args: math.prod(args) if hasattr(math, "prod") else eval("*".join(map(str, args))),
            ">": lambda args: args[0] > args[1],
            "=": lambda args: args[0] == args[1]
        }

    def tokenize(self, chars):
        return chars.replace("(", " ( ").replace(")", " ) ").split()

    def parse(self, tokens):
        if len(tokens) == 0:
            return None
        token = tokens.pop(0)
        if token == "(":
            L = []
            while tokens[0] != ")":
                L.append(self.parse(tokens))
            tokens.pop(0)
            return L
        elif token == ")":
            raise SyntaxError("Unexpected )")
        else:
            try:
                return int(token)
            except ValueError:
                try:
                    return float(token)
                except ValueError:
                    return str(token)

    def eval(self, x, env=None):
        if env is None:
            env = dict(self.global_env)
        if isinstance(x, str):
            return env[x]
        elif not isinstance(x, list):
            return x
        op, *args = x
        if op == "if":
            (test, conseq, alt) = args
            exp = (conseq if self.eval(test, env) else alt)
            return self.eval(exp, env)
        elif op == "define":
            (var, exp) = args
            env[var] = self.eval(exp, env)
            return env[var]
        else:
            proc = self.eval(op, env)
            vals = [self.eval(arg, env) for arg in args]
            return proc(vals)
