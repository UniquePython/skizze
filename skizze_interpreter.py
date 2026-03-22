import skizze_ast as sast
from skizze_env import SkizzeEnvironment
from skizze_errors import SkizzeRuntimeError


class SkizzeInterpreter:
    def __init__(self):
        self.global_env = SkizzeEnvironment()

    def run(self, ast):
        return self.evaluate(ast, self.global_env)

    def evaluate(self, node, env: SkizzeEnvironment):
        if (
            isinstance(node, sast.SkizzeNumberNode)
            or isinstance(node, sast.SkizzeStringNode)
            or isinstance(node, sast.SkizzeBoolNode)
        ):
            return node.value
        elif isinstance(node, sast.SkizzeIdentNode):
            return env.get(node.name)
        elif isinstance(node, sast.SkizzeLetNode):
            val = self.evaluate(node.value, env)
            env.set(node.name, val)
            return val
        elif isinstance(node, sast.SkizzeAssignNode):
            val = self.evaluate(node.value, env)
            env.assign(node.name, val)
            return val
        elif isinstance(node, sast.SkizzeBinOpNode):
            left = self.evaluate(node.left, env)
            right = self.evaluate(node.right, env)
            if node.op == "+":
                return left + right
            elif node.op == "-":
                return left - right
            elif node.op == "*":
                return left * right
            elif node.op == "/":
                return left / right
            elif node.op == "==":
                return left == right
            elif node.op == "!=":
                return left != right
            elif node.op == "<":
                return left < right
            elif node.op == ">":
                return left > right
            elif node.op == "<=":
                return left <= right
            elif node.op == ">=":
                return left >= right
            else:
                raise SkizzeRuntimeError(f"Unknown operator: {node.op}")
        elif isinstance(node, sast.SkizzeUnaryOpNode):
            return -self.evaluate(node.operand, env)
        elif isinstance(node, sast.SkizzePrintNode):
            val = self.evaluate(node.value, env)
            print(val)
            return val
        elif isinstance(node, sast.SkizzeBlockNode):
            result = None
            for stmt in node.statements:
                result = self.evaluate(stmt, env)
            return result
        elif isinstance(node, sast.SkizzeIfNode):
            cond = self.evaluate(node.condition, env)
            if cond:
                self.evaluate(node.then_block, SkizzeEnvironment(parent=env))
            elif node.else_block:
                self.evaluate(node.else_block, SkizzeEnvironment(parent=env))
        elif isinstance(node, sast.SkizzeWhileNode):
            while self.evaluate(node.condition, env):
                self.evaluate(node.body, SkizzeEnvironment(parent=env))
        elif isinstance(node, sast.SkizzeFnNode):
            node.closure_env = env
            env.set(node.name, node)
        elif isinstance(node, sast.SkizzeCallNode):
            fn = env.get(node.name)
            if not isinstance(fn, sast.SkizzeFnNode):
                raise SkizzeRuntimeError(f"{node.name} is not a function")
            if len(node.args) != len(fn.params):
                raise SkizzeRuntimeError(
                    f"{node.name} expects {len(fn.params)} args, got {len(node.args)}"
                )
            new_env = SkizzeEnvironment(parent=fn.closure_env)
            for param, arg in zip(fn.params, node.args):
                new_env.set(param, self.evaluate(arg, env))
            return self.evaluate(fn.body, new_env)
        else:
            raise SkizzeRuntimeError(f"Unknown node type: {type(node).__name__}")
