from DagVisitor import Visited, AbstractDag, Visitor

#Passes will be run on this
class DagNode(Visited):
    def __init__(self, *children):
        self._children = children

    def children(self):
        return self._children

class A(DagNode):
    def __init__(self, c1, c2):
        super().__init__(c1, c2)

class B(DagNode):
    def __init__(self, c):
        super().__init__(c)

class C(DagNode):
    def __init__(self):
        super().__init__()


class Dag(AbstractDag):
    def __init__(self, roots, leafs):
        self.leafs = leafs
        super().__init__(*roots)


class AddID(Visitor):
    def __init__(self):
        self.curid = 0

    def generic_visit(self, node):
        node._id_ = self.curid
        self.curid +=1
        Visitor.generic_visit(self, node)

class Printer(Visitor):
    def __init__(self):
        self.res = "\n"

    def get(self, dag: AbstractDag):
        roots = ", ".join(str(n._id_) for n in dag.roots())
        self.res += f"roots = [{roots}]\n"
        self.run(dag)
        return self.res

    def generic_visit(self, node):
        child_ids = ", ".join([str(child._id_) for child in node.children()])
        self.res += f"{node.kind()[0]}{node._id_}({child_ids})\n"
        Visitor.generic_visit(self, node)

    def visit_A(self, node):
        c0, c1 = node.children()
        self.res += f"A{node._id_}({c0._id_}, {c1._id_})\n"
        Visitor.generic_visit(self, node)

    def visit_C(self, node):
        self.res += f"C{node._id_}\n"
        Visitor.generic_visit(self, node)


def test_visitor():

    c0 = C()
    c1 = C()
    c2 = C()
    a0 = A(c0, c1)
    a1 = A(c0, c2)
    b0 = B(a0)
    b1 = B(a1)
    dag = Dag(roots=[b0, b1, c2], leafs=[c0, c1, c2])
    AddID().run(dag)
    res = Printer().get(dag)
    print(res)
    assert res == '''
roots = [0, 4, 6]
B0(1)
A1(2, 3)
C2
C3
B4(5)
A5(2, 6)
C6
'''
