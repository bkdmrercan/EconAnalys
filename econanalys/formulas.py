import ast
import re

import numpy as np

def clean_formula(f):
    if not f: return ""
    f = f.replace('^', '**')
    f = re.sub(r'(?<![a-zA-Z])[pPqQsS](?![a-zA-Z])', 'x', f)
    return re.sub(r'(\d+)([a-zA-Z])', r'\1*\2', f)


ALLOWED_FORMULA_FUNCS = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "exp": np.exp,
    "log": np.log,
    "sqrt": np.sqrt,
}


def _eval_formula_node(node, names):
    if isinstance(node, ast.Expression):
        return _eval_formula_node(node.body, names)

    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.Name) and node.id in names:
        return names[node.id]

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return +_eval_formula_node(node.operand, names)

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval_formula_node(node.operand, names)

    if isinstance(node, ast.BinOp):
        left = _eval_formula_node(node.left, names)
        right = _eval_formula_node(node.right, names)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right

    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ALLOWED_FORMULA_FUNCS:
        args = [_eval_formula_node(arg, names) for arg in node.args]
        return ALLOWED_FORMULA_FUNCS[node.func.id](*args)

    raise ValueError("Desteklenmeyen formül ifadesi.")


def safe_eval_formula(formula: str, x_values):
    expr = ast.parse(formula, mode="eval")
    return _eval_formula_node(expr, {"x": x_values, "pi": np.pi, "e": np.e})
