from configparser import ConfigParser
from pathlib import Path
import json
import codecs
import sys

def summary_save(data_list: list, path: Path, fname: str) -> None:

    with open(path / fname, 'w') as f:

        if fname.split('.')[-1] == 'json': 
            json.dump(data_list, f)
        else:
            for line in data_list:
                f.write(f"{line}\n")

def main() -> None:

    config = ConfigParser()
    config.read_file(codecs.open("config.ini", "r", "utf8"))

    if len(sys.argv) > 1:
        exp_path = Path(sys.argv[-1]).parent
    else:
        exp_path = Path(config['DEFAULT']['project']) / Path(config['DEFAULT']['name'])


    summary_json, summary_txt = {}, []

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


        summary_txt.append(txt_line)
        summary_json[label.stem] = json_line

    summary_save(data_list=summary_json, path=exp_path, fname='summary.json')
    summary_save(data_list=summary_txt, path=exp_path, fname='summary.txt')
            


if __name__ == '__main__':
    main()

