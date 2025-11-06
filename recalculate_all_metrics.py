import json
import math
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP

# ============================================================================
# TIER SYSTEM CONSTANTS
# ============================================================================
class TierSystem:
    """Tier system áp dụng cho cả Seer và Customer"""
    TIERS = {
        3: {"name": "VIP/MASTER", "min_point": 85},
        2: {"name": "PREMIUM/EXPERT", "min_point": 70},
        1: {"name": "STANDARD/PROFESSIONAL", "min_point": 50},
        0: {"name": "CASUAL/APPRENTICE", "min_point": 0}
    }
    
    @staticmethod
    def get_min_point(tier):
        """Lấy minPoint theo tier"""
        return TierSystem.TIERS.get(tier, {}).get("min_point", 0)
    
    @staticmethod
    def get_tier_from_point(point):
        """Tính tier dựa trên point"""
        if point >= 85:
            return 3
        elif point >= 70:
            return 2
        elif point >= 50:
            return 1
        else:
            return 0

# ============================================================================
# SEER PERFORMANCE CALCULATION
# ============================================================================
def calculate_seer_point(seer, last_tier):
    """
    Tính điểm cho Seer theo công thức từ code Java
    """
    # Reset về minPoint của tier tháng trước
    current_point = TierSystem.get_min_point(last_tier)
    
    # 1. Engagement Score (30%): Each package approved got 20 points
    engagement_score = seer['total_packages'] * 20
    
    # 2. Rating Score (25%)
    rating_score = int(seer['avg_rating']) * 20  # intValue() trong Java
    confident_boost = min(seer['total_rates'] * 2, 20)
    final_rating_score = rating_score + confident_boost
    
    # 3. Completion Score (20%)
    if seer['total_bookings'] > 0:
        completion_rate = seer['completed_bookings'] / seer['total_bookings']
        completion_score = int(completion_rate * 100)
    else:
        completion_score = 0
    
    # 4. Reliability Score (15%)
    if seer['total_bookings'] > 0:
        cancellation_rate = seer['cancelled_by_seer'] / seer['total_bookings']
        reliability_score = int((1 - cancellation_rate) * 100)
    else:
        reliability_score = 100
    
    # 5. Earning Score (10%)
    # totalRevenue * 10 / 500000
    earning_score = int((seer['total_revenue'] * 10) / 500000)
    
    # Weighted formula
    calculated_point = int(
        0.3 * engagement_score +
        0.25 * final_rating_score +
        0.2 * completion_score +
        0.15 * reliability_score +
        0.1 * earning_score
    )
    
    current_point += calculated_point
    
    return current_point

def get_seer_last_tier(seer_id, month, year, seer_data_by_id):
    """
    Lấy tier của tháng trước
    """
    # Calculate previous month
    last_month = month - 1
    last_year = year
    if last_month == 0:
        last_month = 12
        last_year -= 1
    
    # Tìm record tháng trước
    if seer_id in seer_data_by_id:
        for record in seer_data_by_id[seer_id]:
            if record['month'] == last_month and record['year'] == last_year:
                return record['performance_tier']
    
    # Nếu không tìm thấy -> tier mặc định là 0 (APPRENTICE)
    return 0

def recalculate_seer_performance():
    """
    Tính lại point, tier cho tất cả Seer Performance
    """
    print("\n🔧 ĐANG TÍNH LẠI SEER PERFORMANCE...")
    
    input_file = '3_statistic/seer_performance.json'
    
    # Đọc file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_records = len(data)
    print(f"📊 Tìm thấy {total_records} records")
    
    # Group by seer_id để dễ tìm tháng trước
    seer_data_by_id = defaultdict(list)
    for record in data:
        seer_data_by_id[record['seer_id']].append(record)
    
    # Sort by year, month để tính theo thứ tự thời gian
    data.sort(key=lambda x: (x['year'], x['month']))
    
    # Tính lại point và tier cho từng record
    for record in data:
        # Lấy tier tháng trước
        last_tier = get_seer_last_tier(
            record['seer_id'], 
            record['month'], 
            record['year'], 
            seer_data_by_id
        )
        
        # Tính point mới
        new_point = calculate_seer_point(record, last_tier)
        record['performance_point'] = new_point
        
        # Update tier dựa trên point mới
        new_tier = TierSystem.get_tier_from_point(new_point)
        record['performance_tier'] = new_tier
    
    # Ghi lại file
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật {total_records} records")
    
    # Sample output
    print(f"\n📋 Sample (first 5 records):")
    for i, record in enumerate(data[:5]):
        tier_name = TierSystem.TIERS[record['performance_tier']]['name']
        print(f"   {i+1}. Seer {record['seer_id'][-4:]} - {record['month']}/{record['year']}: "
              f"{record['performance_point']} điểm → Tier {record['performance_tier']} ({tier_name})")
    
    return data

# ============================================================================
# CUSTOMER POTENTIAL CALCULATION
# ============================================================================
def calculate_customer_point(customer, last_tier):
    """
    Tính điểm cho Customer theo công thức từ code Java
    """
    # Reset về minPoint của tier tháng trước
    current_point = TierSystem.get_min_point(last_tier)
    
    # 1. Loyalty Score (40%): Each booking request got 10 points
    loyalty_score = customer['total_booking_requests'] * 10
    
    # 2. Value Score (35%): Average spending per booking
    if customer['total_booking_requests'] > 0:
        avg_spending = customer['total_spending'] / customer['total_booking_requests']
        # Each 100k average spending -> 10 points
        value_score = int((avg_spending * 10) / 100000)
    else:
        avg_spending = 0
        value_score = 0
    
    # 3. Reliability Score (25%)
    if customer['total_booking_requests'] > 0:
        cancellation_rate = customer['cancelled_by_customer'] / customer['total_booking_requests']
        reliability_score = int((1 - cancellation_rate) * 100)
    else:
        reliability_score = 100
    
    # Weighted formula
    calculated_point = int(
        0.4 * loyalty_score +
        0.35 * value_score +
        0.25 * reliability_score
    )
    
    current_point += calculated_point
    
    return current_point

def get_customer_last_tier(customer_id, month, year, customer_data_by_id):
    """
    Lấy tier của tháng trước
    """
    # Calculate previous month
    last_month = month - 1
    last_year = year
    if last_month == 0:
        last_month = 12
        last_year -= 1
    
    # Tìm record tháng trước
    if customer_id in customer_data_by_id:
        for record in customer_data_by_id[customer_id]:
            if record['month'] == last_month and record['year'] == last_year:
                return record['potential_tier']
    
    # Nếu không tìm thấy -> tier mặc định là 0 (CASUAL)
    return 0

def recalculate_customer_potential():
    """
    Tính lại point, tier cho tất cả Customer Potential
    """
    print("\n🔧 ĐANG TÍNH LẠI CUSTOMER POTENTIAL...")
    
    input_file = '3_statistic/customer_potential.json'
    
    # Đọc file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_records = len(data)
    print(f"📊 Tìm thấy {total_records} records")
    
    # Group by customer_id để dễ tìm tháng trước
    customer_data_by_id = defaultdict(list)
    for record in data:
        customer_data_by_id[record['customer_id']].append(record)
    
    # Sort by year, month để tính theo thứ tự thời gian
    data.sort(key=lambda x: (x['year'], x['month']))
    
    # Tính lại point và tier cho từng record
    for record in data:
        # Lấy tier tháng trước
        last_tier = get_customer_last_tier(
            record['customer_id'], 
            record['month'], 
            record['year'], 
            customer_data_by_id
        )
        
        # Tính point mới
        new_point = calculate_customer_point(record, last_tier)
        record['potential_point'] = new_point
        
        # Update tier dựa trên point mới
        new_tier = TierSystem.get_tier_from_point(new_point)
        record['potential_tier'] = new_tier
    
    # Ghi lại file
    with open(input_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật {total_records} records")
    
    # Sample output
    print(f"\n📋 Sample (first 5 records):")
    for i, record in enumerate(data[:5]):
        tier_name = TierSystem.TIERS[record['potential_tier']]['name']
        print(f"   {i+1}. Customer {record['customer_id'][-4:]} - {record['month']}/{record['year']}: "
              f"{record['potential_point']} điểm → Tier {record['potential_tier']} ({tier_name})")
    
    return data

# ============================================================================
# RANKING CALCULATION
# ============================================================================
def calculate_ranking_with_ties(records, point_field):
    """
    Tính ranking xử lý đúng trường hợp ties (đã fix)
    """
    # Group by month-year
    monthly_groups = defaultdict(list)
    for record in records:
        key = (record['month'], record['year'])
        monthly_groups[key].append(record)
    
    # Calculate ranking for each month
    for (month, year), group in monthly_groups.items():
        # Sort by point descending
        sorted_group = sorted(group, key=lambda x: x[point_field], reverse=True)
        
        # Assign ranking with tie handling
        for i, record in enumerate(sorted_group):
            if i > 0 and sorted_group[i][point_field] == sorted_group[i-1][point_field]:
                # Cùng điểm -> cùng hạng
                record['ranking'] = sorted_group[i-1]['ranking']
            else:
                # Điểm khác -> hạng mới = i + 1
                record['ranking'] = i + 1

def recalculate_rankings():
    """
    Tính lại ranking cho cả Seer và Customer
    """
    print("\n🏆 ĐANG TÍNH LẠI RANKINGS...")
    
    # Seer Performance
    print("\n📊 Seer Performance:")
    seer_file = '3_statistic/seer_performance.json'
    with open(seer_file, 'r', encoding='utf-8') as f:
        seer_data = json.load(f)
    
    calculate_ranking_with_ties(seer_data, 'performance_point')
    
    with open(seer_file, 'w', encoding='utf-8') as f:
        json.dump(seer_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật ranking cho {len(seer_data)} seer records")
    
    # Customer Potential
    print("\n📊 Customer Potential:")
    customer_file = '3_statistic/customer_potential.json'
    with open(customer_file, 'r', encoding='utf-8') as f:
        customer_data = json.load(f)
    
    calculate_ranking_with_ties(customer_data, 'potential_point')
    
    with open(customer_file, 'w', encoding='utf-8') as f:
        json.dump(customer_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã cập nhật ranking cho {len(customer_data)} customer records")

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 80)
    print("🔄 TÍNH LẠI POINT, TIER, RANKING CHO SEER VÀ CUSTOMER")
    print("=" * 80)
    print("\n📌 Tier System:")
    for tier, info in sorted(TierSystem.TIERS.items(), reverse=True):
        print(f"   Tier {tier}: {info['name']:30s} (minPoint = {info['min_point']})")
    
    print("\n📌 Quy tắc:")
    print("   - Điểm reset về minPoint của tier tháng trước mỗi tháng")
    print("   - Tier được cập nhật dựa trên điểm mới")
    print("   - Ranking xử lý đúng trường hợp người cùng điểm (ties)")
    
    # Step 1: Recalculate Seer Performance
    recalculate_seer_performance()
    
    # Step 2: Recalculate Customer Potential
    recalculate_customer_potential()
    
    # Step 3: Recalculate Rankings
    recalculate_rankings()
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH! Đã tính lại tất cả point, tier và ranking")
    print("=" * 80)
    
    # Show statistics
    print("\n📈 THỐNG KÊ TIER DISTRIBUTION:")
    
    # Customer stats
    print("\n👥 Customer Potential:")
    with open('3_statistic/customer_potential.json', 'r', encoding='utf-8') as f:
        customer_data = json.load(f)
    tier_count = defaultdict(int)
    for record in customer_data:
        tier_count[record['potential_tier']] += 1
    for tier in sorted(tier_count.keys(), reverse=True):
        tier_name = TierSystem.TIERS[tier]['name'].split('/')[0]
        print(f"   Tier {tier} ({tier_name:10s}): {tier_count[tier]:3d} records")
    
    # Seer stats
    print("\n🔮 Seer Performance:")
    with open('3_statistic/seer_performance.json', 'r', encoding='utf-8') as f:
        seer_data = json.load(f)
    tier_count = defaultdict(int)
    for record in seer_data:
        tier_count[record['performance_tier']] += 1
    for tier in sorted(tier_count.keys(), reverse=True):
        tier_name = TierSystem.TIERS[tier]['name'].split('/')[1]
        print(f"   Tier {tier} ({tier_name:12s}): {tier_count[tier]:3d} records")

if __name__ == "__main__":
    main()
