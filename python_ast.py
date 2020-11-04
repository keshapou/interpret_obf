import ast
from rope.base.project import Project as RopeProject
from rope.refactor.rename import Rename as RopeRename
import rope
import pathlib

class Ast:

    NEED_NODES = (
        ast.FunctionDef,
        ast.Assign
    )

    def __init__(self, filename):
        self.filename = pathlib.Path(filename).absolute()
        self.proj  = None
        self.mod   = None
        self.code  = None
        self.tu    = None
        self.lines = None
        self._refresh()

    def _refresh(self):
        self.proj     = RopeProject(self.filename.parent)
        self.mod      = self.proj.get_module(self.filename.stem)
        self.code     = self.mod.resource.read()
        self.tu       = self.mod.ast_node
        self.lines    = self.code.splitlines()

    def get_top_level_pos(self, kind_filter=None):
        res = []
        for child in self.tu.body:
            if type(child) in Ast.NEED_NODES:
                begin = self._get_pos(child.lineno, child.col_offset)
                end   = self._get_pos(child.end_lineno, child.end_col_offset)
                res.append((begin, end))
        return res

    def _get_pos(self, line, col):
        offset = sum(map(len, self.lines[:line-1]))
        return offset + col + line - 1

    def rename_at(self, pos, new_name):
        pos = self._fix_offset(pos)
        renamer = RopeRename(self.proj, self.mod.resource, pos)
        changes = renamer.get_changes(new_name)
        self.proj.do(changes)
        self._refresh()

    def _fix_offset(self, pos):
        after_code = self.code[pos:]
        if after_code.startswith('def '):
            pos += len('def ')
            while after_code[pos] == ' ':
                pos += 1
        return pos

if __name__ == "__main__":
    filename = "test.py"
    a = Ast(filename)
    top_1 = a.get_top_level_pos()
    print("before rename: ", top_1)

    a.rename_at(top_1[3][1], "python_bbb")

    top_2 = a.get_top_level_pos()
    print("after rename: ", top_2)

    for pos in top_2:
        b, e = pos
        print("\n=====", pos, "=====")
        print(a.code[b:e])
