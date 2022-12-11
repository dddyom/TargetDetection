"""Found label cls"""
import re
import json
from pathlib import Path
import shutil


class Labels:

    def __init__(self, exp_path: Path, save_path: Path, fname: str = 'summary') -> None:
        self.fname = fname
        self.path = exp_path
        self.save_path = save_path
        self.summary_json, self.summary_txt = {}, []

        for label in sorted(list((exp_path / 'labels').iterdir())):
            with open(label, 'r') as f:
                single_coord_list = f.read().splitlines()

            json_line, txt_line = [], []

            single_log_path = self.save_path / (label.stem + '_r.txt')
            save_for_single = False if single_log_path.exists() else True

            for coord in single_coord_list:
                dict_coord = json.loads(coord)

                json_line.append(dict_coord)
                txt_line.append({
                    label.stem: {
                        'azimuth': dict_coord['a'],
                        'distance': dict_coord['d'],
                    }
                })

                if save_for_single:
                    with open(single_log_path, 'a') as f:
                        f.write(
                            f"Az = {dict_coord['a']:.2f}, D = {dict_coord['d']*1000:.2f},  N\n")

            self.summary_txt.append(txt_line)
            self.summary_json[label.stem] = json_line

    def remove_exp(self):
        shutil.rmtree(self.path)  # remove dir and all contains

    def save_txt(self) -> None:
        with open(self.save_path / (self.fname + '.txt'), 'a') as f:
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
