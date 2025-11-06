import json
import os
import re

def sanitize_filename(filename):
    """
    Loại bỏ các ký tự không hợp lệ trong tên file Windows
    """
    # Các ký tự không được phép trong tên file Windows: < > : " / \ | ? *
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Loại bỏ khoảng trắng thừa và thay thế nhiều khoảng trắng liên tiếp bằng 1 khoảng trắng
    filename = ' '.join(filename.split())
    
    # Giới hạn độ dài tên file (Windows giới hạn 255 ký tự)
    # Trừ đi phần item_id (36 chars) + underscore (1 char) + extension (4 chars) = 41 chars
    max_title_length = 200  # Để an toàn
    if len(filename) > max_title_length:
        filename = filename[:max_title_length].strip()
    
    return filename

def create_knowledge_files():
    """
    Đọc knowledge_item.json và tạo các file txt cho mỗi item
    """
    print("=" * 70)
    print("📚 TẠO FILES TXT CHO KNOWLEDGE ITEMS")
    print("=" * 70)
    
    # Đường dẫn file input
    input_file = '1_knowledge/knowledge_item.json'
    
    # Thư mục output
    output_dir = r'C:\Users\Windows\Downloads\data_migration\data'
    
    # Tạo thư mục nếu chưa tồn tại
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✅ Đã tạo thư mục: {output_dir}\n")
    else:
        print(f"📁 Thư mục đã tồn tại: {output_dir}\n")
    
    # Đọc file JSON
    print(f"📖 Đang đọc file: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    knowledge_items = data.get('knowledge_item', [])
    total_items = len(knowledge_items)
    print(f"📊 Tìm thấy {total_items} knowledge items\n")
    
    # Duyệt qua từng item và tạo file
    created_count = 0
    for idx, item in enumerate(knowledge_items, 1):
        item_id = item.get('item_id', 'unknown')
        title = item.get('title', 'Untitled')
        content = item.get('content', '')
        
        # Sanitize title để tạo tên file hợp lệ
        safe_title = sanitize_filename(title)
        
        # Tạo tên file theo format: <item_id>_<title>.txt
        filename = f"{item_id}_{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        # Ghi nội dung vào file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Ghi metadata
                f.write(f"Title: {title}\n")
                f.write(f"Item ID: {item_id}\n")
                f.write(f"Status: {item.get('status', 'N/A')}\n")
                f.write(f"View Count: {item.get('view_count', 0)}\n")
                f.write(f"Source: {item.get('source', 'N/A')}\n")
                f.write(f"Created At: {item.get('created_at', 'N/A')}\n")
                f.write(f"Updated At: {item.get('updated_at', 'N/A')}\n")
                f.write("=" * 70 + "\n\n")
                
                # Ghi content
                f.write(content)
            
            created_count += 1
            print(f"✅ [{idx}/{total_items}] Đã tạo: {filename[:80]}{'...' if len(filename) > 80 else ''}")
            
        except Exception as e:
            print(f"❌ [{idx}/{total_items}] Lỗi khi tạo file '{filename}': {str(e)}")
    
    # Tổng kết
    print("\n" + "=" * 70)
    print(f"🎉 HOÀN THÀNH!")
    print(f"📊 Đã tạo thành công: {created_count}/{total_items} files")
    print(f"📁 Thư mục: {output_dir}")
    print("=" * 70)

if __name__ == "__main__":
    create_knowledge_files()
