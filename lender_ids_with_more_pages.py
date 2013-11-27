import json
import os

def find(path, extension):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1].lower()[1:] == extension.lower():
                paths.append(os.path.join(root, file))
    return paths

if __name__ == "__main__":
    json_files = find('./data', 'json')

    for json_file in json_files:
        with open(json_file, 'rb') as f:
            contents = f.read()
            if len(contents) > 0:
                data = json.loads(contents)
                if data['paging']['pages'] > 1:
                    print(json_file)
