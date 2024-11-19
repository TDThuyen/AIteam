import pandas as pd
import rasterio
import glob

# Đường dẫn đến file CSV và thư mục chứa file TIFF
csv_file_path = 'D:/tài liệu môn học/trí tuệ nhân tạo/project/data/data thu thập màu sau khi fix NaN/newBarrenLand.csv'
tiff_folder_path = 'D:/tài liệu môn học/trí tuệ nhân tạo/project/tiffimagelan2may1/thanhoattotnhat/*.tif'

# Đọc dữ liệu từ file CSV
df = pd.read_csv(csv_file_path)

# Khởi tạo cột cho các giá trị band
bands = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6',
         'B7', 'B8', 'B8A', 'B9', 'B10', 'B11', 'B12']
for band in bands:
    df[band] = None

# Lặp qua tất cả các file TIFF trong thư mục
for tiff_file_path in glob.glob(tiff_folder_path):
    with rasterio.open(tiff_file_path) as src:
        # Lấy thông tin về các band tương ứng
        band_data = {}
        for i, band in enumerate(bands, start=1):
            band_data[band] = src.read(i)

        # Lặp qua từng điểm trong DataFrame
        for index, row in df.iterrows():
            lon = row['Long']
            lat = row['Lat']

            # Chuyển đổi tọa độ địa lý sang tọa độ pixel
            try:
                row_idx, col_idx = src.index(lon, lat)

                # Kiểm tra xem tọa độ pixel có nằm trong phạm vi ảnh không
                if (0 <= row_idx < src.height) and (0 <= col_idx < src.width):
                    for band in bands:
                        df.at[index, band] = band_data[band][row_idx, col_idx]
            except rasterio.errors.RasterioError:
                # Nếu điểm không nằm trong phạm vi ảnh, bỏ qua
                continue

# Loại bỏ các điểm không có giá trị (nếu có)
df = df.dropna(subset=bands)

# Lưu kết quả vào file CSV mới
df.to_csv('output_with_bands_Thuyen_new.csv', index=False)
