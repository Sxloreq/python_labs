def analyze_log_file(log_file_path):
    stats = {}
    try:
        with open(log_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split('"')
                if len(parts) > 2:
                    status_part = parts[2].strip()
                    if status_part:
                        status_code = status_part.split()[0]
                        if status_code in stats:
                            stats[status_code] += 1
                        else:
                            stats[status_code] = 1
        return stats
    except FileNotFoundError:
        print(f"File {log_file_path} not found")
        return {}
    except IOError:
        print("Error reading file")
        return {}

if __name__ == "__main__":
    result = analyze_log_file("apache_logs.txt")
    print(result)
