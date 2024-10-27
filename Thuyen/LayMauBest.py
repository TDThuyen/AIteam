import pandas as pd
import rasterio
import glob

# Đường dẫn đến file CSV và thư mục chứa file TIFF
csv_file_path = 'data/ThuyenData_updated.csv'
# Sử dụng glob để tìm tất cả các file TIFF
tiff_folder_path = 'tiff image/project img/*.tif'

# Đọc dữ liệu từ file CSV
df = pd.read_csv(csv_file_path)

# Khởi tạo cột cho các giá trị band
df['B2'] = None
df['B3'] = None
df['B4'] = None
df['B5'] = None
df['B8'] = None
df['B8A'] = None
df['B11'] = None
df['B12'] = None

# Lặp qua tất cả các file TIFF trong thư mục
for tiff_file_path in glob.glob(tiff_folder_path):
    with rasterio.open(tiff_file_path) as src:
        # Lấy thông tin về các band tương ứng
        band_b02 = src.read(2)   # Band B2
        band_b03 = src.read(3)   # Band B3
        band_b04 = src.read(4)   # Band B4
        band_b05 = src.read(5)   # Band B5
        band_b08 = src.read(8)   # Band B8
        band_b8A = src.read(9)   # Band B8A
        band_b11 = src.read(11)  # Band B11
        band_b12 = src.read(12)  # Band B12

        # Lặp qua từng điểm trong DataFrame
        for index, row in df.iterrows():
            lon = row['Long']
            lat = row['Lat']

            # Chuyển đổi tọa độ địa lý sang tọa độ pixel
            try:
                row_idx, col_idx = src.index(lon, lat)

                # Lấy giá trị từ các band, kiểm tra xem giá trị có tồn tại không
                if (0 <= row_idx < band_b02.shape[0]) and (0 <= col_idx < band_b02.shape[1]):
                    df.at[index, 'B2'] = band_b02[row_idx, col_idx]
                    df.at[index, 'B3'] = band_b03[row_idx, col_idx]
                    df.at[index, 'B4'] = band_b04[row_idx, col_idx]
                    df.at[index, 'B5'] = band_b05[row_idx, col_idx]
                    df.at[index, 'B8'] = band_b08[row_idx, col_idx]
                    df.at[index, 'B8A'] = band_b8A[row_idx, col_idx]
                    df.at[index, 'B11'] = band_b11[row_idx, col_idx]
                    df.at[index, 'B12'] = band_b12[row_idx, col_idx]

            except rasterio.errors.RasterioError:
                # Nếu không thể lấy giá trị, bỏ qua
                continue

# Lưu kết quả vào file CSV mới
df.to_csv('output_with_bands_Thuyen_new.csv', index=False)

print("Hoàn thành! File đã được lưu tại: output_with_bands.csv")
