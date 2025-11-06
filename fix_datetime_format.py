import json
from datetime import datetime
import random

def convert_datetime_to_iso(date_str):
    """
    Chuyển đổi từ '2025-03-01 00:00:00.000' sang '2025-03-01T06:10:20.070+00:00'
    Thêm random giờ, phút, giây, millisecond để data realistic hơn
    """
    # Parse datetime từ format cũ
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    
    # Thêm random time trong ngày (6-22 giờ để realistic)
    hour = random.randint(6, 22)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    millisecond = random.randint(0, 999)
    
    # Tạo ISO 8601 format với timezone +00:00
    iso_datetime = f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}T{hour:02d}:{minute:02d}:{second:02d}.{millisecond:03d}+00:00"
    
    return iso_datetime

def fix_file_datetime(input_file, output_file):
    """
    Đọc file JSON, chuyển đổi created_at và updated_at sang ISO format
    """
    print(f"\n🔧 Đang xử lý file: {input_file}")
    
    # Đọc file JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Tìm thấy {len(data)} records")
    
    # Chuyển đổi datetime cho từng record
    for record in data:
        if 'created_at' in record:
            record['created_at'] = convert_datetime_to_iso(record['created_at'])
        if 'updated_at' in record:
            record['updated_at'] = convert_datetime_to_iso(record['updated_at'])
    
    # Ghi file mới
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã lưu file: {output_file}")
    
    # Hiển thị sample
    if len(data) > 0:
        print(f"\n📋 Sample record đầu tiên:")
        print(f"   created_at: {data[0].get('created_at')}")
        print(f"   updated_at: {data[0].get('updated_at')}")

def main():
    print("=" * 60)
    print("🔄 CHUYỂN ĐỔI DATETIME FORMAT SANG ISO 8601")
    print("=" * 60)
    
    # Fix customer_potential.json
    fix_file_datetime(
        '3_statistic/customer_potential.json',
        '3_statistic/customer_potential.json'
    )
    
    # Fix seer_performance.json
    fix_file_datetime(
        '3_statistic/seer_performance.json',
        '3_statistic/seer_performance.json'
    )
    
    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH! Tất cả datetime đã được chuyển sang ISO 8601 format")
    print("=" * 60)

if __name__ == "__main__":
    main()
