import json
from datetime import datetime
import random

# Đọc customer data để lấy created_at
with open('2_user/customer.json', 'r', encoding='utf-8') as f:
    customer_data = json.load(f)

# Map customer_id -> created_at month
customer_start_months = {}
for user in customer_data['user']:
    if user['role'] == 4:  # CUSTOMER
        user_id = user['user_id']
        created_at = user['created_at']
        dt = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')
        customer_start_months[user_id] = dt.month

print(f"Found {len(customer_start_months)} customers")

# Generate customer_potential data
result = {
    "enum": {
        "potential_tier": {
            "BRONZE": 0,
            "SILVER": 1,
            "GOLD": 2,
            "PLATINUM": 3
        }
    },
    "customer_potential": []
}

# ID counter
id_counter = 1

# Sort customers by ID for consistent output
sorted_customers = sorted(customer_start_months.items(), key=lambda x: x[0])

for customer_id, start_month in sorted_customers:
    customer_num = int(customer_id.split('440')[-1])
    
    # Determine customer tier trajectory (random but realistic)
    trajectory_type = random.choice(['high_performer', 'steady_growth', 'average', 'low_activity', 'new_user'])
    
    if trajectory_type == 'high_performer':
        base_point = random.randint(65, 75)
        growth_rate = random.uniform(2, 4)
        max_point = random.randint(90, 98)
    elif trajectory_type == 'steady_growth':
        base_point = random.randint(50, 60)
        growth_rate = random.uniform(1.5, 2.5)
        max_point = random.randint(75, 88)
    elif trajectory_type == 'average':
        base_point = random.randint(40, 55)
        growth_rate = random.uniform(1, 2)
        max_point = random.randint(60, 75)
    elif trajectory_type == 'low_activity':
        base_point = random.randint(25, 45)
        growth_rate = random.uniform(0.5, 1.5)
        max_point = random.randint(45, 60)
    else:  # new_user
        base_point = random.randint(20, 40)
        growth_rate = random.uniform(2, 3)
        max_point = random.randint(55, 70)
    
    current_point = base_point
    
    # Generate monthly records from start_month to November (11)
    for month in range(start_month, 12):  # 12 = through November
        # Calculate potential_point with some variation
        if current_point < max_point:
            current_point += growth_rate + random.uniform(-0.5, 1.5)
            current_point = min(current_point, max_point)
        else:
            current_point += random.uniform(-2, 1)  # slight fluctuation at max
        
        current_point = max(20, min(100, current_point))  # clamp between 20-100
        potential_point = int(current_point)
        
        # Determine tier based on potential_point
        if potential_point < 50:
            potential_tier = 0  # BRONZE
        elif potential_point < 70:
            potential_tier = 1  # SILVER
        elif potential_point < 85:
            potential_tier = 2  # GOLD
        else:
            potential_tier = 3  # PLATINUM
        
        # Generate realistic metrics
        booking_multiplier = potential_point / 20
        total_booking_requests = int(booking_multiplier + random.randint(1, 5))
        total_spending = total_booking_requests * random.randint(150000, 300000)
        cancelled_by_customer = random.randint(0, max(1, total_booking_requests // 4))
        
        # Ranking (will be adjusted later based on all customers)
        ranking = random.randint(1, 70)
        
        # Create record
        record = {
            "id": f"cp0e8400-e29b-41d4-a716-446655440{id_counter:03d}",
            "customer_id": customer_id,
            "month": month,
            "year": 2025,
            "potential_point": potential_point,
            "potential_tier": potential_tier,
            "ranking": ranking,
            "total_booking_requests": total_booking_requests,
            "total_spending": float(total_spending),
            "cancelled_by_customer": cancelled_by_customer,
            "created_at": f"2025-{month+1:02d}-01 00:00:00.000",
            "updated_at": f"2025-{month+1:02d}-01 00:00:00.000"
        }
        
        result['customer_potential'].append(record)
        id_counter += 1

# Adjust rankings per month based on actual potential_points
for month in range(1, 12):
    month_records = [r for r in result['customer_potential'] if r['month'] == month]
    # Sort by potential_point descending
    month_records.sort(key=lambda x: x['potential_point'], reverse=True)
    
    # Assign rankings
    for rank, record in enumerate(month_records, 1):
        record['ranking'] = rank

print(f"Generated {len(result['customer_potential'])} records for {len(customer_start_months)} customers")

# Write to file
with open('3_statistic/customer_potential.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print("✅ File customer_potential.json has been created successfully!")
print(f"📊 Total records: {len(result['customer_potential'])}")

# Statistics
tier_counts = {0: 0, 1: 0, 2: 0, 3: 0}
for record in result['customer_potential']:
    tier_counts[record['potential_tier']] += 1

print("\n📈 Tier distribution:")
print(f"   BRONZE (0): {tier_counts[0]} records")
print(f"   SILVER (1): {tier_counts[1]} records")
print(f"   GOLD (2): {tier_counts[2]} records")
print(f"   PLATINUM (3): {tier_counts[3]} records")
