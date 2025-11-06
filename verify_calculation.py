import json

# Check Seer Performance
print("=" * 80)
print("🔍 VERIFY SEER PERFORMANCE CALCULATION")
print("=" * 80)

with open('3_statistic/seer_performance.json', 'r', encoding='utf-8') as f:
    seer_data = json.load(f)

# Lấy 3 records tháng 1/2025
jan_data = [d for d in seer_data if d['month'] == 1 and d['year'] == 2025][:3]

for i, d in enumerate(jan_data, 1):
    print(f"\n📊 Seer #{i} - {d['seer_id'][-8:]} (Tháng {d['month']}/{d['year']}):")
    print(f"   📦 Packages: {d['total_packages']}")
    print(f"   ⭐ Avg Rating: {d['avg_rating']:.2f} / 5.0")
    print(f"   💬 Total Rates: {d['total_rates']}")
    print(f"   ✅ Completed: {d['completed_bookings']}/{d['total_bookings']}")
    print(f"   ❌ Cancelled by Seer: {d['cancelled_by_seer']}")
    print(f"   💰 Revenue: {d['total_revenue']:,.0f}")
    print(f"   🎯 Point: {d['performance_point']}")
    print(f"   🏆 Tier: {d['performance_tier']}")
    print(f"   📍 Ranking: {d['ranking']}")
    
    # Manual calculation
    print(f"\n   🧮 Manual Verification:")
    engagement = d['total_packages'] * 20
    print(f"      Engagement (30%): {d['total_packages']} × 20 = {engagement}")
    
    rating_base = int(d['avg_rating']) * 20
    rating_boost = min(d['total_rates'] * 2, 20)
    rating_final = rating_base + rating_boost
    print(f"      Rating (25%): {int(d['avg_rating'])} × 20 + min({d['total_rates']} × 2, 20) = {rating_base} + {rating_boost} = {rating_final}")
    
    completion_rate = d['completed_bookings'] / d['total_bookings'] if d['total_bookings'] > 0 else 0
    completion = int(completion_rate * 100)
    print(f"      Completion (20%): ({d['completed_bookings']}/{d['total_bookings']}) × 100 = {completion}")
    
    cancel_rate = d['cancelled_by_seer'] / d['total_bookings'] if d['total_bookings'] > 0 else 0
    reliability = int((1 - cancel_rate) * 100)
    print(f"      Reliability (15%): (1 - {d['cancelled_by_seer']}/{d['total_bookings']}) × 100 = {reliability}")
    
    earning = int((d['total_revenue'] * 10) / 500000)
    print(f"      Earning (10%): ({d['total_revenue']:,.0f} × 10) / 500,000 = {earning}")
    
    weighted = int(0.3 * engagement + 0.25 * rating_final + 0.2 * completion + 0.15 * reliability + 0.1 * earning)
    print(f"      Weighted Sum: {weighted}")
    print(f"      Starting from minPoint: 0 (first month)")
    print(f"      Final Point: 0 + {weighted} = {weighted}")

print("\n" + "=" * 80)
print("🔍 VERIFY CUSTOMER POTENTIAL CALCULATION")
print("=" * 80)

with open('3_statistic/customer_potential.json', 'r', encoding='utf-8') as f:
    customer_data = json.load(f)

# Lấy 3 records tháng 1/2025
jan_cust = [d for d in customer_data if d['month'] == 1 and d['year'] == 2025][:3]

for i, d in enumerate(jan_cust, 1):
    print(f"\n📊 Customer #{i} - {d['customer_id'][-8:]} (Tháng {d['month']}/{d['year']}):")
    print(f"   📋 Booking Requests: {d['total_booking_requests']}")
    print(f"   💰 Total Spending: {d['total_spending']:,.0f}")
    print(f"   ❌ Cancelled: {d['cancelled_by_customer']}")
    print(f"   🎯 Point: {d['potential_point']}")
    print(f"   🏆 Tier: {d['potential_tier']}")
    print(f"   📍 Ranking: {d['ranking']}")
    
    # Manual calculation
    print(f"\n   🧮 Manual Verification:")
    loyalty = d['total_booking_requests'] * 10
    print(f"      Loyalty (40%): {d['total_booking_requests']} × 10 = {loyalty}")
    
    avg_spend = d['total_spending'] / d['total_booking_requests'] if d['total_booking_requests'] > 0 else 0
    value = int((avg_spend * 10) / 100000)
    print(f"      Value (35%): ({d['total_spending']:,.0f} / {d['total_booking_requests']}) × 10 / 100,000 = {avg_spend:,.0f} → {value}")
    
    cancel_rate = d['cancelled_by_customer'] / d['total_booking_requests'] if d['total_booking_requests'] > 0 else 0
    reliability = int((1 - cancel_rate) * 100)
    print(f"      Reliability (25%): (1 - {d['cancelled_by_customer']}/{d['total_booking_requests']}) × 100 = {reliability}")
    
    weighted = int(0.4 * loyalty + 0.35 * value + 0.25 * reliability)
    print(f"      Weighted Sum: {weighted}")
    print(f"      Starting from minPoint: 0 (first month)")
    print(f"      Final Point: 0 + {weighted} = {weighted}")

print("\n" + "=" * 80)
