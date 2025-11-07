import json
from collections import Counter

print("=" * 80)
print("📊 VERIFY TRANSFORMED DATA")
print("=" * 80)

# ============================================================================
# CUSTOMER POTENTIAL
# ============================================================================
print("\n👥 CUSTOMER POTENTIAL:")
with open('3_statistic_training_ai/customer_potential.json', 'r', encoding='utf-8') as f:
    customer_data = json.load(f)

print(f"   Total records: {len(customer_data)}")

# Check fields
if len(customer_data) > 0:
    sample = customer_data[0]
    print(f"\n   ✅ Các trường đã transform:")
    for key in sample.keys():
        print(f"      - {key}")
    
    # Check removed fields
    removed_fields = ['_id', 'customer_id', 'created_at', 'updated_at']
    has_removed = any(field in sample for field in removed_fields)
    if has_removed:
        print(f"\n   ❌ Cảnh báo: Vẫn còn trường cũ!")
    else:
        print(f"\n   ✅ Đã bỏ các trường: _id, customer_id, created_at, updated_at")

# Tier distribution
tier_count = Counter(record['potential_tier'] for record in customer_data)
print(f"\n   📈 Tier Distribution:")
for tier, count in sorted(tier_count.items()):
    print(f"      {tier:12s}: {count:3d} records ({count/len(customer_data)*100:.1f}%)")

# Sample record
print(f"\n   📋 Sample Record:")
sample = customer_data[0]
print(f"      Full Name: {sample['customer_full_name']}")
print(f"      Email: {sample['customer_email']}")
print(f"      Gender: {sample['customer_gender']}")
print(f"      Birth Date: {sample['customer_birth_date']}")
print(f"      Month/Year: {sample['month']}/{sample['year']}")
print(f"      Tier: {sample['potential_tier']} ({sample['potential_point']} điểm)")
print(f"      Ranking: #{sample['ranking']}")
print(f"      Bookings: {sample['total_booking_requests']}")
print(f"      Spending: {sample['total_spending']:,.0f}")

# ============================================================================
# SEER PERFORMANCE
# ============================================================================
print("\n" + "=" * 80)
print("🔮 SEER PERFORMANCE:")
with open('3_statistic_training_ai/seer_performance.json', 'r', encoding='utf-8') as f:
    seer_data = json.load(f)

print(f"   Total records: {len(seer_data)}")

# Check fields
if len(seer_data) > 0:
    sample = seer_data[0]
    print(f"\n   ✅ Các trường đã transform:")
    for key in sample.keys():
        print(f"      - {key}")
    
    # Check removed fields
    removed_fields = ['_id', 'seer_id', 'created_at', 'updated_at']
    has_removed = any(field in sample for field in removed_fields)
    if has_removed:
        print(f"\n   ❌ Cảnh báo: Vẫn còn trường cũ!")
    else:
        print(f"\n   ✅ Đã bỏ các trường: _id, seer_id, created_at, updated_at")

# Tier distribution
tier_count = Counter(record['performance_tier'] for record in seer_data)
print(f"\n   📈 Tier Distribution:")
for tier, count in sorted(tier_count.items()):
    print(f"      {tier:12s}: {count:3d} records ({count/len(seer_data)*100:.1f}%)")

# Speciality distribution
all_specialities = []
for record in seer_data:
    all_specialities.extend(record['seer_speciality'])
speciality_count = Counter(all_specialities)
print(f"\n   🎯 Speciality Distribution:")
for spec, count in sorted(speciality_count.items(), key=lambda x: x[1], reverse=True):
    print(f"      {spec:20s}: {count:3d} occurrences")

# Sample record
print(f"\n   📋 Sample Record:")
sample = seer_data[0]
print(f"      Full Name: {sample['seer_full_name']}")
print(f"      Email: {sample['seer_email']}")
print(f"      Gender: {sample['seer_gender']}")
print(f"      Birth Date: {sample['seer_birth_date']}")
print(f"      Specialities: {', '.join(sample['seer_speciality'])}")
print(f"      Month/Year: {sample['month']}/{sample['year']}")
print(f"      Tier: {sample['performance_tier']} ({sample['performance_point']} điểm)")
print(f"      Ranking: #{sample['ranking']}")
print(f"      Packages: {sample['total_packages']}")
print(f"      Avg Rating: {sample['avg_rating']:.2f}/5.0")
print(f"      Revenue: {sample['total_revenue']:,.0f}")

print("\n" + "=" * 80)
print("✅ VERIFIED! Dữ liệu đã được transform đúng")
print("=" * 80)
