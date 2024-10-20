import pandas as pd
import rasterio
import glob

# Đường dẫn đến file CSV và thư mục chứa file TIFF
csv_file_path = 'D:/AI-Class/data/ImageData/dataFormat2.csv'
tiff_folder_path = 'D:/AI-Class/data/ImageData/Image/*.tif'  # Sử dụng glob để tìm tất cả các file TIFF

# Đọc dữ liệu từ file CSV
df = pd.read_csv(csv_file_path)

# Khởi tạo cột cho band values
df['B04'] = None
df['B05'] = None
df['B06'] = None

# Lặp qua tất cả các file TIFF trong thư mục
for tiff_file_path in glob.glob(tiff_folder_path):
    with rasterio.open(tiff_file_path) as src:
        # Lấy thông tin về band
        band_b04 = src.read(1)  # Đọc band đầu tiên
        band_b05 = src.read(2)  # Đọc band thứ hai
        band_b06 = src.read(3)  # Đọc band thứ ba

        # Lặp qua từng điểm trong DataFrame
        for index, row in df.iterrows():
            lon = row['LONG']
            lat = row['LAT']

            # Chuyển đổi tọa độ địa lý sang tọa độ pixel
            try:
                row_idx, col_idx = src.index(lon, lat)

                # Lấy giá trị từ các band, kiểm tra xem giá trị có tồn tại không
                if 0 <= row_idx < band_b04.shape[0] and 0 <= col_idx < band_b04.shape[1]:
                    df.at[index, 'B04'] = band_b04[row_idx, col_idx]
                    df.at[index, 'B05'] = band_b05[row_idx, col_idx]
                    df.at[index, 'B06'] = band_b06[row_idx, col_idx]

            except rasterio.errors.RasterioError:
                # Nếu không thể lấy giá trị, bỏ qua
                continue

# Lưu kết quả vào file CSV mới
df.to_csv('output_with_bands.csv', index=False)

print("Hoàn thành! File đã được lưu tại: output_with_bands.csv")
