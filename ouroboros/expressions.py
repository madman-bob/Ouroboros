from ouroboros.operators import Operator


class Expression(Operator):
    eval = Operator.__call__
