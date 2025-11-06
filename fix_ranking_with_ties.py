import json
from collections import defaultdict

def fix_ranking_with_ties(records, point_field, month_field='month', year_field='year'):
    """
    Sửa ranking để xử lý đúng trường hợp có người cùng hạng (ties)
    
    Ví dụ:
    - Người 1: 100 điểm → Hạng 1
    - Người 2: 100 điểm → Hạng 1 (cùng hạng)
    - Người 3: 95 điểm  → Hạng 3 (không phải hạng 2!)
    - Người 4: 90 điểm  → Hạng 4
    """
    # Group records by month-year
    monthly_groups = defaultdict(list)
    for record in records:
        key = (record[month_field], record[year_field])
        monthly_groups[key].append(record)
    
    # Fix ranking for each month
    for (month, year), group in monthly_groups.items():
        # Sort by point (descending)
        sorted_group = sorted(group, key=lambda x: x[point_field], reverse=True)
        
        # Assign ranking with proper tie handling
        current_rank = 1
        for i, record in enumerate(sorted_group):
            if i > 0 and sorted_group[i][point_field] == sorted_group[i-1][point_field]:
                # Cùng điểm với người trước → giữ nguyên hạng
                record['ranking'] = sorted_group[i-1]['ranking']
            else:
                # Điểm khác → hạng mới = vị trí hiện tại (i+1)
                record['ranking'] = i + 1
                current_rank = i + 1
    
    return records

def fix_customer_potential():
    """
    Fix ranking cho customer_potential.json
    """
    print("\n🔧 Đang sửa ranking cho customer_potential.json...")
    
    input_file = '3_statistic/customer_potential.json'
    
    # Đọc file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data)
    print(f"📊 Tìm thấy {original_count} records")
    
    # Fix ranking
    fixed_data = fix_ranking_with_ties(data, 'potential_point')
    
    # Ghi lại file
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật {original_count} records")
    
    # Hiển thị sample để verify
    print(f"\n📋 Sample ranking (tháng 2/2025):")
    month_2_data = [d for d in fixed_data if d['month'] == 2 and d['year'] == 2025]
    month_2_sorted = sorted(month_2_data, key=lambda x: x['potential_point'], reverse=True)[:15]
    
    prev_point = None
    for record in month_2_sorted:
        point = record['potential_point']
        rank = record['ranking']
        marker = " ← Cùng hạng!" if point == prev_point else ""
        print(f"   Hạng {rank:2d}: {point:3d} điểm{marker}")
        prev_point = point

def fix_seer_performance():
    """
    Fix ranking cho seer_performance.json
    """
    print("\n🔧 Đang sửa ranking cho seer_performance.json...")
    
    input_file = '3_statistic/seer_performance.json'
    
    # Đọc file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    original_count = len(data)
    print(f"📊 Tìm thấy {original_count} records")
    
    # Fix ranking
    fixed_data = fix_ranking_with_ties(data, 'performance_point')
    
    # Ghi lại file
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật {original_count} records")
    
    # Hiển thị sample để verify
    print(f"\n📋 Sample ranking (tháng 1/2025):")
    month_1_data = [d for d in fixed_data if d['month'] == 1 and d['year'] == 2025]
    month_1_sorted = sorted(month_1_data, key=lambda x: x['performance_point'], reverse=True)[:15]
    
    prev_point = None
    for record in month_1_sorted:
        point = record['performance_point']
        rank = record['ranking']
        marker = " ← Cùng hạng!" if point == prev_point else ""
        print(f"   Hạng {rank:2d}: {point:3d} điểm{marker}")
        prev_point = point

def main():
    print("=" * 70)
    print("🏆 FIX RANKING WITH TIES (XỬ LÝ NGƯỜI CÙNG HẠNG)")
    print("=" * 70)
    print("\nQuy tắc:")
    print("  - Nếu 2 người cùng 100 điểm → cùng hạng 1")
    print("  - Người tiếp theo (95 điểm) → hạng 3 (KHÔNG phải hạng 2)")
    print("  - Nếu 3 người cùng hạng 5 → người tiếp theo là hạng 8")
    
    # Fix customer_potential
    fix_customer_potential()
    
    # Fix seer_performance
    fix_seer_performance()
    
    print("\n" + "=" * 70)
    print("🎉 HOÀN THÀNH! Tất cả ranking đã được sửa đúng")
    print("=" * 70)

if __name__ == "__main__":
    main()
