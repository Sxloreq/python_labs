def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_counts = {}
    try:
        with open(input_file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.split()
                if len(parts) > 0:
                    current_ip = parts[0]
                    if current_ip in allowed_ips:
                        if current_ip in ip_counts:
                            ip_counts[current_ip] += 1
                        else:
                            ip_counts[current_ip] = 1
                            
        with open(output_file_path, "w", encoding="utf-8") as out_file:
            for ip, count in ip_counts.items():
                out_file.write(f"{ip} - {count}\n")

    except FileNotFoundError:
        print(f"File {input_file_path} not found")
    except IOError:
        print("Error processing files")

if __name__ == "__main__":
    my_allowed_ips = [
        "192.168.1.10", 
        "46.105.14.53", 
        "8.8.8.8", 
        "127.0.0.1",
        "93.114.45.13"
    ]
    filter_ips("apache_logs.txt", "filtered_ips.txt", my_allowed_ips)
