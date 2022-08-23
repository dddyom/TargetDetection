"""Found label cls"""
import re
import json
from pathlib import Path


class Labels:

    def __init__(self, exp_path: Path, fname: str = 'summary') -> None:
        self.fname = fname
        self.path = exp_path
        self.summary_json, self.summary_txt = {}, []

        for label in sorted(list((exp_path / 'labels').iterdir())):

            with open(label, 'r') as f:
                single_coord_list = f.read().splitlines()

            json_line, txt_line = [], []

            for coord in single_coord_list:
                dict_coord = json.loads(coord)

                json_line.append(dict_coord)
                txt_line.append({
                    'azimuth': dict_coord['a'],
                    'distance': dict_coord['d'],
                })

            self.summary_txt.append(txt_line)
            self.summary_json[label.stem] = json_line

    def save_txt(self) -> None:
        with open(self.path / (self.fname + '.txt'), 'w') as f:
            for line in self.summary_txt:
                f.write(f"{line}\n")

    def save_json(self) -> None:
        with open(self.path / (self.fname + '.json'), 'w') as f:
            json.dump(self.summary_json, f)

    @staticmethod
    def get_creating_exp_path(project_path: Path, exp_name: Path) -> Path:
        correct: list[Path] = []
        for exp in project_path.iterdir():
            if re.search(f"^{exp_name}", exp.name):
                correct.append(exp)
        return sorted(correct)[-1]
        # return sorted(list(project_path.iterdir()))[-1]
