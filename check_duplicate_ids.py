import json
from collections import Counter

# Đọc file customer.json
with open('2_user/customer.json', 'r', encoding='utf-8') as f:
    customer_data = json.load(f)

# Đọc file seer.json
with open('2_user/seer.json', 'r', encoding='utf-8') as f:
    seer_data = json.load(f)

# Lấy tất cả user_id từ customer
customer_ids = [user['user_id'] for user in customer_data['user']]

# Lấy tất cả user_id từ seer
seer_ids = [user['user_id'] for user in seer_data['user']]

# Kiểm tra trùng lặp trong customer
customer_duplicates = [id for id, count in Counter(customer_ids).items() if count > 1]

# Kiểm tra trùng lặp trong seer
seer_duplicates = [id for id, count in Counter(seer_ids).items() if count > 1]

# Kiểm tra ID trùng giữa customer và seer
ids_in_both = set(customer_ids) & set(seer_ids)

print("="*80)
print("KẾT QUẢ KIỂM TRA ID TRÙNG LẶP")
print("="*80)

print(f"\nTổng số customer: {len(customer_ids)}")
print(f"Tổng số seer: {len(seer_ids)}")

print("\n" + "="*80)
print("1. ID TRÙNG LẶP TRONG CUSTOMER.JSON:")
print("="*80)
if customer_duplicates:
    print(f"Tìm thấy {len(customer_duplicates)} ID bị trùng:")
    for dup_id in customer_duplicates:
        count = customer_ids.count(dup_id)
        print(f"\n  ID: {dup_id}")
        print(f"  Xuất hiện: {count} lần")
        
        # Tìm và hiển thị thông tin các user trùng
        users_with_id = [user for user in customer_data['user'] if user['user_id'] == dup_id]
        for idx, user in enumerate(users_with_id, 1):
            print(f"    [{idx}] {user['full_name']} - {user['email']}")
else:
    print("✓ Không có ID trùng lặp")

print("\n" + "="*80)
print("2. ID TRÙNG LẶP TRONG SEER.JSON:")
print("="*80)
if seer_duplicates:
    print(f"Tìm thấy {len(seer_duplicates)} ID bị trùng:")
    for dup_id in seer_duplicates:
        count = seer_ids.count(dup_id)
        print(f"\n  ID: {dup_id}")
        print(f"  Xuất hiện: {count} lần")
        
        # Tìm và hiển thị thông tin các user trùng
        users_with_id = [user for user in seer_data['user'] if user['user_id'] == dup_id]
        for idx, user in enumerate(users_with_id, 1):
            print(f"    [{idx}] {user['full_name']} - {user['email']}")
else:
    print("✓ Không có ID trùng lặp")

print("\n" + "="*80)
print("3. ID TRÙNG GIỮA CUSTOMER VÀ SEER:")
print("="*80)
if ids_in_both:
    print(f"⚠ CẢNH BÁO: Tìm thấy {len(ids_in_both)} ID xuất hiện ở CẢ 2 FILE!")
    print("(Một user không thể vừa là customer vừa là seer với cùng ID)\n")
    for shared_id in ids_in_both:
        customer_user = next(user for user in customer_data['user'] if user['user_id'] == shared_id)
        seer_user = next(user for user in seer_data['user'] if user['user_id'] == shared_id)
        
        print(f"  ID: {shared_id}")
        print(f"    - Customer: {customer_user['full_name']} ({customer_user['email']})")
        print(f"    - Seer: {seer_user['full_name']} ({seer_user['email']})")
        print()
else:
    print("✓ Không có ID nào trùng giữa 2 file")

print("="*80)

# Kiểm tra thêm các ID khác có thể trùng (customer_id, seer_id)
print("\n" + "="*80)
print("4. KIỂM TRA THÊM - PROFILE IDs:")
print("="*80)

# Kiểm tra customer_profile IDs
customer_profile_ids = [user['customer_profile']['customer_id'] 
                       for user in customer_data['user'] 
                       if user['customer_profile'] is not None]
customer_profile_duplicates = [id for id, count in Counter(customer_profile_ids).items() if count > 1]

print(f"\nCustomer Profile IDs trùng: ", end="")
if customer_profile_duplicates:
    print(f"{len(customer_profile_duplicates)} ID")
    for dup_id in customer_profile_duplicates:
        print(f"  - {dup_id}")
else:
    print("✓ Không có")

# Kiểm tra seer_profile IDs
seer_profile_ids = [user['seer_profile']['seer_id'] 
                   for user in seer_data['user'] 
                   if user['seer_profile'] is not None]
seer_profile_duplicates = [id for id, count in Counter(seer_profile_ids).items() if count > 1]

print(f"\nSeer Profile IDs trùng: ", end="")
if seer_profile_duplicates:
    print(f"{len(seer_profile_duplicates)} ID")
    for dup_id in seer_profile_duplicates:
        print(f"  - {dup_id}")
else:
    print("✓ Không có")

print("\n" + "="*80)
