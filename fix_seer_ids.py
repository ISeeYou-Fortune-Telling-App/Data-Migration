import json

# Mapping từ ID cũ sang ID mới
# Từ 0021-0031 -> 0071-0081
old_to_new_mapping = {
    "550e8400-e29b-41d4-a716-446655440021": "550e8400-e29b-41d4-a716-446655440071",
    "550e8400-e29b-41d4-a716-446655440022": "550e8400-e29b-41d4-a716-446655440072",
    "550e8400-e29b-41d4-a716-446655440023": "550e8400-e29b-41d4-a716-446655440073",
    "550e8400-e29b-41d4-a716-446655440024": "550e8400-e29b-41d4-a716-446655440074",
    "550e8400-e29b-41d4-a716-446655440025": "550e8400-e29b-41d4-a716-446655440075",
    "550e8400-e29b-41d4-a716-446655440026": "550e8400-e29b-41d4-a716-446655440076",
    "550e8400-e29b-41d4-a716-446655440027": "550e8400-e29b-41d4-a716-446655440077",
    "550e8400-e29b-41d4-a716-446655440028": "550e8400-e29b-41d4-a716-446655440078",
    "550e8400-e29b-41d4-a716-446655440029": "550e8400-e29b-41d4-a716-446655440079",
    "550e8400-e29b-41d4-a716-446655440030": "550e8400-e29b-41d4-a716-446655440080",
    "550e8400-e29b-41d4-a716-446655440031": "550e8400-e29b-41d4-a716-446655440081",
}

print("="*80)
print("BẮT ĐẦU CÂP NHẬT SEER IDs")
print("="*80)

# 1. Cập nhật seer.json
print("\n1. Đang cập nhật file seer.json...")
with open('2_user/seer.json', 'r', encoding='utf-8') as f:
    seer_data = json.load(f)

seer_updated_count = 0
for user in seer_data['user']:
    old_id = user['user_id']
    if old_id in old_to_new_mapping:
        new_id = old_to_new_mapping[old_id]
        user['user_id'] = new_id
        
        # Cập nhật seer_profile.seer_id
        if user['seer_profile']:
            user['seer_profile']['seer_id'] = new_id
        
        # Cập nhật seer_speciality
        if user['seer_speciality']:
            for speciality in user['seer_speciality']:
                speciality['seer_id'] = new_id
        
        # Cập nhật certificate
        if user.get('certificate'):
            for cert in user['certificate']:
                cert['seer_id'] = new_id
        
        # Cập nhật service_package
        if user['service_package']:
            for package in user['service_package']:
                package['seer_id'] = new_id
        
        seer_updated_count += 1
        print(f"   ✓ {old_id} -> {new_id} ({user['full_name']})")

# Lưu file seer.json
with open('2_user/seer.json', 'w', encoding='utf-8') as f:
    json.dump(seer_data, f, ensure_ascii=False, indent=4)

print(f"\n   Đã cập nhật {seer_updated_count} seers trong seer.json")

# 2. Cập nhật seer_performance.json
print("\n2. Đang cập nhật file seer_performance.json...")
with open('3_statistic/seer_performance.json', 'r', encoding='utf-8') as f:
    performance_data = json.load(f)

performance_updated_count = 0
for record in performance_data:
    old_id = record['seer_id']
    if old_id in old_to_new_mapping:
        new_id = old_to_new_mapping[old_id]
        record['seer_id'] = new_id
        performance_updated_count += 1

# Lưu file seer_performance.json
with open('3_statistic/seer_performance.json', 'w', encoding='utf-8') as f:
    json.dump(performance_data, f, ensure_ascii=False, indent=4)

print(f"   Đã cập nhật {performance_updated_count} records trong seer_performance.json")

# 3. Kiểm tra file training AI
print("\n3. Đang kiểm tra file seer_performance trong training_ai...")
try:
    with open('3_statistic_training_ai/seer_performance.json', 'r', encoding='utf-8') as f:
        ai_performance_data = json.load(f)
    
    ai_updated_count = 0
    for record in ai_performance_data:
        old_id = record['seer_id']
        if old_id in old_to_new_mapping:
            new_id = old_to_new_mapping[old_id]
            record['seer_id'] = new_id
            ai_updated_count += 1
    
    # Lưu file
    with open('3_statistic_training_ai/seer_performance.json', 'w', encoding='utf-8') as f:
        json.dump(ai_performance_data, f, ensure_ascii=False, indent=4)
    
    print(f"   Đã cập nhật {ai_updated_count} records trong seer_performance (training_ai)")
except Exception as e:
    print(f"   ⚠ Không tìm thấy hoặc lỗi khi cập nhật file training_ai: {e}")

print("\n" + "="*80)
print("KẾT QUẢ")
print("="*80)
print(f"✓ Đã cập nhật {seer_updated_count} seers")
print(f"✓ Đã cập nhật {performance_updated_count} performance records")
print("\nMapping ID đã thực hiện:")
print("-"*80)
for old_id, new_id in old_to_new_mapping.items():
    old_suffix = old_id[-4:]
    new_suffix = new_id[-4:]
    print(f"  ...{old_suffix} -> ...{new_suffix}")
print("="*80)

# Xác minh không còn ID trùng
print("\n4. XÁC MINH KHÔNG CÒN ID TRÙNG...")
with open('2_user/customer.json', 'r', encoding='utf-8') as f:
    customer_data = json.load(f)

customer_ids = set(user['user_id'] for user in customer_data['user'])
seer_ids = set(user['user_id'] for user in seer_data['user'])

ids_in_both = customer_ids & seer_ids

if ids_in_both:
    print(f"   ⚠ VẪN CÒN {len(ids_in_both)} ID TRÙNG!")
    for id in ids_in_both:
        print(f"      - {id}")
else:
    print("   ✓ KHÔNG CÒN ID TRÙNG! Hoàn thành!")

print("\n" + "="*80)
