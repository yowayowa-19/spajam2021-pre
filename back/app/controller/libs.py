from pathlib import Path


def get_back_path() -> Path:
    path = Path().cwd().resolve()
    if "back" not in path.resolve().__str__():
        print(path.resolve().__str__())
        path = list(path.glob("back/"))[0]
    else:
        while not path.__str__().endswith("back"):
            path = path.parent
    return path