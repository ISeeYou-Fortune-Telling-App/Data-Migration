import json
from datetime import datetime

def format_sql_value(value):
    """Format value for SQL"""
    if value is None:
        return 'NULL'
    elif isinstance(value, str):
        # Escape single quotes
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    elif isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        return f"'{str(value)}'"

def generate_sql_file():
    """Generate SQL import file"""
    
    sql_lines = []
    
    # Header
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- DATA IMPORT FOR VANNA AI TRAINING")
    sql_lines.append("-- Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_lines.append("-- ============================================================================")
    sql_lines.append("")
    sql_lines.append("-- Disable triggers and constraints for faster import")
    sql_lines.append("SET session_replication_role = 'replica';")
    sql_lines.append("")
    
    # ========================================================================
    # KNOWLEDGE CATEGORIES
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- KNOWLEDGE CATEGORIES (6 categories)")
    sql_lines.append("-- ============================================================================")
    
    with open('1_knowledge/knowledge_category.json', 'r', encoding='utf-8') as f:
        cat_data = json.load(f)
    
    sql_lines.append("INSERT INTO knowledge_category (category_id, name, description, created_at, updated_at) VALUES")
    
    values = []
    for cat in cat_data['knowledge_category']:
        val = f"({format_sql_value(cat['category_id'])}, {format_sql_value(cat['name'])}, {format_sql_value(cat['description'])}, {format_sql_value(cat['created_at'])}, {format_sql_value(cat['updated_at'])})"
        values.append(val)
    
    sql_lines.append(",\n".join(values) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(cat_data['knowledge_category'])} categories")
    sql_lines.append("")
    
    # ========================================================================
    # USERS (CUSTOMERS + SEERS) - Only essential fields
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- USERS (Customers and Seers - Essential fields only)")
    sql_lines.append("-- ============================================================================")
    
    # Load customers
    with open('2_user/customer.json', 'r', encoding='utf-8') as f:
        customer_data = json.load(f)
    
    # Load seers
    with open('2_user/seer.json', 'r', encoding='utf-8') as f:
        seer_data = json.load(f)
    
    sql_lines.append("INSERT INTO \"user\" (user_id, role, email, gender, full_name, profile_description, birth_date, created_at, updated_at) VALUES")
    
    all_users = []
    
    # Add customers (role = 4)
    for user in customer_data['user']:
        val = f"({format_sql_value(user['user_id'])}, 4, {format_sql_value(user['email'])}, {format_sql_value(user['gender'])}, {format_sql_value(user['full_name'])}, {format_sql_value(user['profile_description'])}, {format_sql_value(user['birth_date'])}, {format_sql_value(user['created_at'])}, {format_sql_value(user['updated_at'])})"
        all_users.append(val)
    
    # Add seers (role = 1)
    for user in seer_data['user']:
        val = f"({format_sql_value(user['user_id'])}, 1, {format_sql_value(user['email'])}, {format_sql_value(user['gender'])}, {format_sql_value(user['full_name'])}, {format_sql_value(user['profile_description'])}, {format_sql_value(user['birth_date'])}, {format_sql_value(user['created_at'])}, {format_sql_value(user['updated_at'])})"
        all_users.append(val)
    
    sql_lines.append(",\n".join(all_users) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(customer_data['user'])} customers + {len(seer_data['user'])} seers = {len(all_users)} users")
    sql_lines.append("")
    
    # ========================================================================
    # SEER SPECIALITIES
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- SEER SPECIALITIES (Seer-Category relationships)")
    sql_lines.append("-- ============================================================================")
    
    sql_lines.append("INSERT INTO seer_speciality (id, seer_id, category_id, created_at, updated_at) VALUES")
    
    specialities = []
    for user in seer_data['user']:
        if user['seer_speciality']:
            for spec in user['seer_speciality']:
                val = f"({format_sql_value(spec['id'])}, {format_sql_value(spec['seer_id'])}, {format_sql_value(spec['category_id'])}, {format_sql_value(spec['created_at'])}, {format_sql_value(spec['updated_at'])})"
                specialities.append(val)
    
    sql_lines.append(",\n".join(specialities) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(specialities)} seer-speciality relationships")
    sql_lines.append("")
    
    # ========================================================================
    # CUSTOMER POTENTIAL
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- CUSTOMER POTENTIAL (Monthly performance tracking)")
    sql_lines.append("-- ============================================================================")
    
    with open('3_statistic/customer_potential.json', 'r', encoding='utf-8') as f:
        cp_data = json.load(f)
    
    sql_lines.append("INSERT INTO customer_potential (id, customer_id, month, year, potential_point, potential_tier, ranking, total_booking_requests, total_spending, cancelled_by_customer, created_at, updated_at) VALUES")
    
    cp_values = []
    for record in cp_data:
        val = f"({format_sql_value(record['_id'])}, {format_sql_value(record['customer_id'])}, {record['month']}, {record['year']}, {record['potential_point']}, {record['potential_tier']}, {record['ranking']}, {record['total_booking_requests']}, {record['total_spending']}, {record['cancelled_by_customer']}, {format_sql_value(record['created_at'])}, {format_sql_value(record['updated_at'])})"
        cp_values.append(val)
    
    sql_lines.append(",\n".join(cp_values) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(cp_data)} customer potential records")
    sql_lines.append("")
    
    # ========================================================================
    # SEER PERFORMANCE
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- SEER PERFORMANCE (Monthly performance tracking)")
    sql_lines.append("-- ============================================================================")
    
    with open('3_statistic/seer_performance.json', 'r', encoding='utf-8') as f:
        sp_data = json.load(f)
    
    sql_lines.append("INSERT INTO seer_performance (id, seer_id, month, year, performance_tier, performance_point, ranking, total_packages, total_rates, avg_rating, total_bookings, completed_bookings, cancelled_by_seer, total_revenue, bonus, created_at, updated_at) VALUES")
    
    sp_values = []
    for record in sp_data:
        val = f"({format_sql_value(record['_id'])}, {format_sql_value(record['seer_id'])}, {record['month']}, {record['year']}, {record['performance_tier']}, {record['performance_point']}, {record['ranking']}, {record['total_packages']}, {record['total_rates']}, {record['avg_rating']}, {record['total_bookings']}, {record['completed_bookings']}, {record['cancelled_by_seer']}, {record['total_revenue']}, {record['bonus']}, {format_sql_value(record['created_at'])}, {format_sql_value(record['updated_at'])})"
        sp_values.append(val)
    
    sql_lines.append(",\n".join(sp_values) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(sp_data)} seer performance records")
    sql_lines.append("")
    
    # Footer
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- Re-enable triggers and constraints")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("SET session_replication_role = 'origin';")
    sql_lines.append("")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- IMPORT SUMMARY")
    sql_lines.append("-- ============================================================================")
    sql_lines.append(f"-- Knowledge Categories: {len(cat_data['knowledge_category'])} records")
    sql_lines.append(f"-- Users: {len(all_users)} records ({len(customer_data['user'])} customers + {len(seer_data['user'])} seers)")
    sql_lines.append(f"-- Seer Specialities: {len(specialities)} records")
    sql_lines.append(f"-- Customer Potential: {len(cp_data)} records")
    sql_lines.append(f"-- Seer Performance: {len(sp_data)} records")
    sql_lines.append(f"-- TOTAL: {len(cat_data['knowledge_category']) + len(all_users) + len(specialities) + len(cp_data) + len(sp_data)} records")
    sql_lines.append("-- ============================================================================")
    
    return "\n".join(sql_lines)

def main():
    print("=" * 80)
    print("📝 GENERATING SQL IMPORT FILE")
    print("=" * 80)
    
    print("\n📖 Reading JSON files...")
    sql_content = generate_sql_file()
    
    output_file = '4_sqldata_vanna/data_import.sql'
    
    print(f"\n💾 Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"\n✅ File created: {output_file}")
    print(f"📊 File size: {len(sql_content):,} characters")
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH!")
    print("=" * 80)
    
    print("\n📋 Dữ liệu đã import:")
    print("   ✅ Knowledge Categories")
    print("   ✅ Users (Customers + Seers - chỉ các trường cần thiết)")
    print("   ✅ Seer Specialities")
    print("   ✅ Customer Potential")
    print("   ✅ Seer Performance")

if __name__ == "__main__":
    main()
