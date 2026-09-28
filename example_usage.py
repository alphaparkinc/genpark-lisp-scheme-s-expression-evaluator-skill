from client import LispEvaluator

def main():
    lisp = LispEvaluator()
    tokens = lisp.tokenize("(if (> 5 2) (+ 10 20) (* 2 3))")
    ast = lisp.parse(tokens)
    res = lisp.eval(ast)
    print("Lisp S-Expression Evaluator Verification:")
    print(f"Parsed Form: {ast}")
    print(f"Evaluation Result: {res} (Expected: 30)")

if __name__ == "__main__":
    main()
