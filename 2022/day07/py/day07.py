from io import StringIO
import sys
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    files: list[File] = field(default_factory=list)
    directories: list["Directory"] = field(default_factory=list)
    parent: Optional["Directory"] = None


@dataclass
class State:
    root: Directory = Directory("/")
    cwd: Directory = root

    def evaluate(self, inp):
        line = inp.pop(0)
        if line == "$ ls":
            while inp and not inp[0].startswith("$"):
                line = inp.pop(0)
                x, name = line.split()
                if x == "dir":
                    self.cwd.directories.append(
                        Directory(name, [], [], parent=self.cwd)
                    )
                else:
                    self.cwd.files.append(File(name, int(x)))
        elif line.startswith("$ cd"):
            arg = line.split()[2]
            if arg == "/":
                self.cwd = self.root
            elif arg == "..":
                assert self.cwd.parent is not None
                self.cwd = self.cwd.parent
            else:
                for d in self.cwd.directories:
                    if d.name == arg:
                        self.cwd = d
                        break
                else:
                    raise ValueError("No such directory: " + arg)
        else:
            raise ValueError("Unknown command: " + line)

    def __str__(self):
        return self.render()

    def render(self, d=None):
        if d is None:
            d = self.root
        out = StringIO()
        self._render(d, 0, out)
        return out.getvalue()

    def _render(self, d, depth, out):
        print("  " * depth, "-", d.name, file=out)
        for f in d.files:
            print("  " * (depth + 1), "-", f.name, f.size, file=out)
        for d in d.directories:
            self._render(d, depth + 1, out)

    def get_size(self, d=None):
        if d is None:
            d = self.root
        return sum(f.size for f in d.files) + sum(
            self.get_size(d) for d in d.directories
        )

    def get_directories(self, d=None):
        if d is None:
            d = self.root
        yield d
        for d in d.directories:
            yield from self.get_directories(d)


def main():
    lines = sys.stdin.read().splitlines()
    state = State()

    while lines:
        state.evaluate(lines)

    print(state)

    dirs = state.get_directories()
    greater = 0
    for d in dirs:
        size = state.get_size(d)
        if size <= 100000:
            greater += size
    print("Part 1", greater)

    total_disk = 70000000
    required = 30000000
    used_space = state.get_size()
    left = total_disk - used_space
    needed = required - left
    chosen = min(
        state.get_size(d)
        for d in state.get_directories()
        if state.get_size(d) >= needed
    )
    print("Part 2", chosen)


if __name__ == "__main__":
    main()
