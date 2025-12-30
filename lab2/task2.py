import hashlib

def generate_file_hashes(*file_paths):
    hashes = {}
    for path in file_paths:
        try:
            with open(path, "rb") as file:
                file_content = file.read()
                file_hash = hashlib.sha256(file_content).hexdigest()
                hashes[path] = file_hash
        except FileNotFoundError:
            print(f"File {path} not found")
        except IOError:
            print(f"Error reading {path}")
            
    return hashes

if __name__ == "__main__":
    files = ["apache_logs.txt", "task2.py"]
    result = generate_file_hashes(*files)
    print(result)
