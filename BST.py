class NumberNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'{self.tok}'


class bOps:
    def __init__(self, left_node, tokenOp, right_node):
        self.left_node = left_node
        self.tokenOp = tokenOp
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.tokenOp}, {self.right_node})'


class uOps:
    def __init__(self, tokenOp, node):
        self.tokenOp = tokenOp
        self.node = node

        self.pos_start = self.tokenOp.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.tokenOp}, {self.node})'
