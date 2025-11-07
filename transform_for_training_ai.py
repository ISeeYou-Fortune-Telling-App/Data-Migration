import json
from collections import defaultdict

# ============================================================================
# TIER MAPPING
# ============================================================================
CUSTOMER_TIER_NAMES = {
    0: "CASUAL",
    1: "STANDARD",
    2: "PREMIUM",
    3: "VIP"
}

SEER_TIER_NAMES = {
    0: "APPRENTICE",
    1: "PROFESSIONAL",
    2: "EXPERT",
    3: "MASTER"
}

# ============================================================================
# LOAD SOURCE DATA
# ============================================================================
def load_customers():
    """Load customer data from customer.json"""
    print("📖 Đang đọc customer.json...")
    with open('2_user/customer.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    customer_map = {}
    for user in data['user']:
        customer_map[user['user_id']] = {
            'full_name': user['full_name'],
            'email': user['email'],
            'profile_description': user['profile_description'],
            'birth_date': user['birth_date'],
            'gender': user['gender']
        }
    
    print(f"✅ Đã load {len(customer_map)} customers")
    return customer_map

def load_seers():
    """Load seer data from seer.json"""
    print("📖 Đang đọc seer.json...")
    with open('2_user/seer.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    seer_map = {}
    for user in data['user']:
        # Get speciality category IDs
        speciality_ids = []
        if user['seer_speciality']:
            speciality_ids = [s['category_id'] for s in user['seer_speciality']]
        
        seer_map[user['user_id']] = {
            'full_name': user['full_name'],
            'email': user['email'],
            'profile_description': user['profile_description'],
            'birth_date': user['birth_date'],
            'gender': user['gender'],
            'speciality_ids': speciality_ids
        }
    
    print(f"✅ Đã load {len(seer_map)} seers")
    return seer_map

def load_categories():
    """Load knowledge categories"""
    print("📖 Đang đọc knowledge_category.json...")
    with open('1_knowledge/knowledge_category.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    category_map = {}
    for cat in data['knowledge_category']:
        category_map[cat['category_id']] = cat['name']
    
    print(f"✅ Đã load {len(category_map)} categories")
    return category_map

# ============================================================================
# TRANSFORM CUSTOMER POTENTIAL
# ============================================================================
def transform_customer_potential(customer_map):
    """Transform customer_potential.json"""
    print("\n🔧 ĐANG TRANSFORM CUSTOMER POTENTIAL...")
    
    input_file = '3_statistic_training_ai/customer_potential.json'
    output_file = '3_statistic_training_ai/customer_potential.json'
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_records = len(data)
    print(f"📊 Tìm thấy {total_records} records")
    
    transformed_data = []
    not_found_count = 0
    
    for record in data:
        customer_id = record['customer_id']
        
        # Get customer info
        if customer_id in customer_map:
            customer_info = customer_map[customer_id]
            
            # Create new record without _id, created_at, updated_at
            new_record = {
                'customer_full_name': customer_info['full_name'],
                'customer_email': customer_info['email'],
                'customer_profile_description': customer_info['profile_description'],
                'customer_birth_date': customer_info['birth_date'],
                'customer_gender': customer_info['gender'],
                'month': record['month'],
                'year': record['year'],
                'potential_point': record['potential_point'],
                'potential_tier': CUSTOMER_TIER_NAMES.get(record['potential_tier'], 'UNKNOWN'),
                'ranking': record['ranking'],
                'total_booking_requests': record['total_booking_requests'],
                'total_spending': record['total_spending'],
                'cancelled_by_customer': record['cancelled_by_customer']
            }
            
            transformed_data.append(new_record)
        else:
            not_found_count += 1
            print(f"⚠️  Customer not found: {customer_id}")
    
    # Save transformed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã transform {len(transformed_data)} records")
    if not_found_count > 0:
        print(f"⚠️  {not_found_count} customers không tìm thấy")
    
    # Sample output
    if len(transformed_data) > 0:
        print(f"\n📋 Sample record:")
        sample = transformed_data[0]
        print(f"   Name: {sample['customer_full_name']}")
        print(f"   Email: {sample['customer_email']}")
        print(f"   Month/Year: {sample['month']}/{sample['year']}")
        print(f"   Point: {sample['potential_point']}")
        print(f"   Tier: {sample['potential_tier']}")
        print(f"   Ranking: {sample['ranking']}")

# ============================================================================
# TRANSFORM SEER PERFORMANCE
# ============================================================================
def transform_seer_performance(seer_map, category_map):
    """Transform seer_performance.json"""
    print("\n🔧 ĐANG TRANSFORM SEER PERFORMANCE...")
    
    input_file = '3_statistic_training_ai/seer_performance.json'
    output_file = '3_statistic_training_ai/seer_performance.json'
    
    # Read file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_records = len(data)
    print(f"📊 Tìm thấy {total_records} records")
    
    transformed_data = []
    not_found_count = 0
    
    for record in data:
        seer_id = record['seer_id']
        
        # Get seer info
        if seer_id in seer_map:
            seer_info = seer_map[seer_id]
            
            # Convert speciality IDs to names
            speciality_names = []
            for spec_id in seer_info['speciality_ids']:
                if spec_id in category_map:
                    speciality_names.append(category_map[spec_id])
                else:
                    speciality_names.append(f"Unknown ({spec_id})")
            
            # Create new record without _id, created_at, updated_at
            new_record = {
                'seer_full_name': seer_info['full_name'],
                'seer_email': seer_info['email'],
                'seer_profile_description': seer_info['profile_description'],
                'seer_birth_date': seer_info['birth_date'],
                'seer_gender': seer_info['gender'],
                'seer_speciality': speciality_names,
                'month': record['month'],
                'year': record['year'],
                'performance_tier': SEER_TIER_NAMES.get(record['performance_tier'], 'UNKNOWN'),
                'performance_point': record['performance_point'],
                'ranking': record['ranking'],
                'total_packages': record['total_packages'],
                'total_rates': record['total_rates'],
                'avg_rating': record['avg_rating'],
                'total_bookings': record['total_bookings'],
                'completed_bookings': record['completed_bookings'],
                'cancelled_by_seer': record['cancelled_by_seer'],
                'total_revenue': record['total_revenue'],
                'bonus': record['bonus']
            }
            
            transformed_data.append(new_record)
        else:
            not_found_count += 1
            print(f"⚠️  Seer not found: {seer_id}")
    
    # Save transformed data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Đã transform {len(transformed_data)} records")
    if not_found_count > 0:
        print(f"⚠️  {not_found_count} seers không tìm thấy")
    
    # Sample output
    if len(transformed_data) > 0:
        print(f"\n📋 Sample record:")
        sample = transformed_data[0]
        print(f"   Name: {sample['seer_full_name']}")
        print(f"   Email: {sample['seer_email']}")
        print(f"   Speciality: {', '.join(sample['seer_speciality'])}")
        print(f"   Month/Year: {sample['month']}/{sample['year']}")
        print(f"   Point: {sample['performance_point']}")
        print(f"   Tier: {sample['performance_tier']}")
        print(f"   Ranking: {sample['ranking']}")

# ============================================================================
# MAIN
# ============================================================================
def main():
    print("=" * 80)
    print("🔄 TRANSFORM DATA FOR TRAINING AI")
    print("=" * 80)
    print("\n📌 Thay đổi:")
    print("   1. Bỏ trường: _id, created_at, updated_at")
    print("   2. Customer: Thay customer_id → customer_full_name, email, profile, birth_date, gender")
    print("   3. Customer: Thay potential_tier number → tier name (CASUAL, STANDARD, PREMIUM, VIP)")
    print("   4. Seer: Thay seer_id → seer_full_name, email, profile, birth_date, gender, speciality")
    print("   5. Seer: Thay performance_tier number → tier name (APPRENTICE, PROFESSIONAL, EXPERT, MASTER)")
    print("   6. Seer: Chuyển speciality_id → speciality_name (Tarot, Cung Hoàng Đạo, ...)")
    
    # Load source data
    print("\n" + "=" * 80)
    print("📂 ĐANG LOAD DỮ LIỆU NGUỒN")
    print("=" * 80)
    
    customer_map = load_customers()
    seer_map = load_seers()
    category_map = load_categories()
    
    # Transform customer potential
    print("\n" + "=" * 80)
    print("🔄 TRANSFORM CUSTOMER POTENTIAL")
    print("=" * 80)
    transform_customer_potential(customer_map)
    
    # Transform seer performance
    print("\n" + "=" * 80)
    print("🔄 TRANSFORM SEER PERFORMANCE")
    print("=" * 80)
    transform_seer_performance(seer_map, category_map)
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH! Dữ liệu đã được transform xong")
    print("=" * 80)
    print("\n📁 Files đã được cập nhật:")
    print("   - 3_statistic_training_ai/customer_potential.json")
    print("   - 3_statistic_training_ai/seer_performance.json")

if __name__ == "__main__":
    main()
