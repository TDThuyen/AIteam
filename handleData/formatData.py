input_file_path = 'D:/AI-Class/data/ImageData/dataPoint2.txt'
# Đường dẫn để lưu file CSV đã sửa
output_file_path = 'D:/AI-Class/data/ImageData/dataFormat2.txt'

# Đọc file gốc
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Xử lý từng dòng để bỏ dấu phẩy đầu
processed_lines = []
for index, line in enumerate(lines):
    # Thêm số thứ tự bắt đầu từ 1 cho các dòng từ dòng 2 trở đi và bỏ 2 ký tự cuối
    if index >= 1:  # Bắt đầu từ dòng 2 (index 1)
        line = f"{index} {line[:-3]}\n"  # Bỏ 2 ký tự trước ký tự xuống dòng (newline)

    processed_lines.append(line)

# Ghi vào file mới
with open(output_file_path, 'w') as file:
    file.writelines(processed_lines)

print("Đã hoàn thành! File đã được lưu tại:", output_file_path)