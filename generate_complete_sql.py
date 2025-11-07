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
    """Generate complete SQL file with schema and data"""
    
    sql_lines = []
    
    # ========================================================================
    # HEADER
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- DATA IMPORT FOR VANNA AI TRAINING")
    sql_lines.append("-- Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_lines.append("-- ============================================================================")
    sql_lines.append("")
    sql_lines.append("-- Drop existing tables if exists (cascade to remove all dependencies)")
    sql_lines.append("DROP TABLE IF EXISTS seer_performance CASCADE;")
    sql_lines.append("DROP TABLE IF EXISTS customer_potential CASCADE;")
    sql_lines.append("DROP TABLE IF EXISTS seer_speciality CASCADE;")
    sql_lines.append("DROP TABLE IF EXISTS \"user\" CASCADE;")
    sql_lines.append("DROP TABLE IF EXISTS knowledge_category CASCADE;")
    sql_lines.append("")
    
    # ========================================================================
    # CREATE TABLES
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- CREATE TABLES")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("")
    
    # Knowledge Category Table
    sql_lines.append("-- Knowledge Category Table")
    sql_lines.append("CREATE TABLE knowledge_category (")
    sql_lines.append("    category_id VARCHAR(36) PRIMARY KEY,")
    sql_lines.append("    name VARCHAR(255) NOT NULL,")
    sql_lines.append("    description TEXT,")
    sql_lines.append("    created_at TIMESTAMP,")
    sql_lines.append("    updated_at TIMESTAMP")
    sql_lines.append(");")
    sql_lines.append("")
    
    # User Table
    sql_lines.append("-- User Table (Customers and Seers)")
    sql_lines.append("CREATE TABLE \"user\" (")
    sql_lines.append("    user_id VARCHAR(36) PRIMARY KEY,")
    sql_lines.append("    role VARCHAR(20) NOT NULL CHECK (role IN ('SEER', 'CUSTOMER')),")
    sql_lines.append("    email VARCHAR(255) NOT NULL UNIQUE,")
    sql_lines.append("    gender VARCHAR(10),")
    sql_lines.append("    full_name VARCHAR(255) NOT NULL,")
    sql_lines.append("    profile_description TEXT,")
    sql_lines.append("    birth_date TIMESTAMP,")
    sql_lines.append("    created_at TIMESTAMP,")
    sql_lines.append("    updated_at TIMESTAMP")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Seer Speciality Table
    sql_lines.append("-- Seer Speciality Table (Seer-Category relationship)")
    sql_lines.append("CREATE TABLE seer_speciality (")
    sql_lines.append("    id VARCHAR(36) PRIMARY KEY,")
    sql_lines.append("    seer_id VARCHAR(36) NOT NULL,")
    sql_lines.append("    category_id VARCHAR(36) NOT NULL,")
    sql_lines.append("    created_at TIMESTAMP,")
    sql_lines.append("    updated_at TIMESTAMP,")
    sql_lines.append("    FOREIGN KEY (seer_id) REFERENCES \"user\"(user_id) ON DELETE CASCADE,")
    sql_lines.append("    FOREIGN KEY (category_id) REFERENCES knowledge_category(category_id) ON DELETE CASCADE")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Customer Potential Table
    sql_lines.append("-- Customer Potential Table")
    sql_lines.append("CREATE TABLE customer_potential (")
    sql_lines.append("    id VARCHAR(36) PRIMARY KEY,")
    sql_lines.append("    customer_id VARCHAR(36) NOT NULL,")
    sql_lines.append("    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),")
    sql_lines.append("    year INT NOT NULL,")
    sql_lines.append("    potential_point INT NOT NULL,")
    sql_lines.append("    potential_tier INT NOT NULL CHECK (potential_tier BETWEEN 0 AND 3), -- 0: CASUAL, 1: STANDARD, 2: PREMIUM, 3: VIP")
    sql_lines.append("    ranking INT NOT NULL,")
    sql_lines.append("    total_booking_requests INT NOT NULL DEFAULT 0,")
    sql_lines.append("    total_spending NUMERIC(15, 2) NOT NULL DEFAULT 0,")
    sql_lines.append("    cancelled_by_customer INT NOT NULL DEFAULT 0,")
    sql_lines.append("    created_at TIMESTAMP,")
    sql_lines.append("    updated_at TIMESTAMP,")
    sql_lines.append("    FOREIGN KEY (customer_id) REFERENCES \"user\"(user_id) ON DELETE CASCADE,")
    sql_lines.append("    UNIQUE (customer_id, month, year)")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Seer Performance Table
    sql_lines.append("-- Seer Performance Table")
    sql_lines.append("CREATE TABLE seer_performance (")
    sql_lines.append("    id VARCHAR(36) PRIMARY KEY,")
    sql_lines.append("    seer_id VARCHAR(36) NOT NULL,")
    sql_lines.append("    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),")
    sql_lines.append("    year INT NOT NULL,")
    sql_lines.append("    performance_tier INT NOT NULL CHECK (performance_tier BETWEEN 0 AND 3), -- 0: APPRENTICE, 1: PROFESSIONAL, 2: EXPERT, 3: MASTER")
    sql_lines.append("    performance_point INT NOT NULL,")
    sql_lines.append("    ranking INT NOT NULL,")
    sql_lines.append("    total_packages INT NOT NULL DEFAULT 0,")
    sql_lines.append("    total_rates INT NOT NULL DEFAULT 0,")
    sql_lines.append("    avg_rating NUMERIC(3, 2) NOT NULL DEFAULT 0,")
    sql_lines.append("    total_bookings INT NOT NULL DEFAULT 0,")
    sql_lines.append("    completed_bookings INT NOT NULL DEFAULT 0,")
    sql_lines.append("    cancelled_by_seer INT NOT NULL DEFAULT 0,")
    sql_lines.append("    total_revenue NUMERIC(15, 2) NOT NULL DEFAULT 0,")
    sql_lines.append("    bonus NUMERIC(15, 2) NOT NULL DEFAULT 0,")
    sql_lines.append("    created_at TIMESTAMP,")
    sql_lines.append("    updated_at TIMESTAMP,")
    sql_lines.append("    FOREIGN KEY (seer_id) REFERENCES \"user\"(user_id) ON DELETE CASCADE,")
    sql_lines.append("    UNIQUE (seer_id, month, year)")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Indexes
    sql_lines.append("-- Create indexes for better query performance")
    sql_lines.append("CREATE INDEX idx_user_role ON \"user\"(role);")
    sql_lines.append("CREATE INDEX idx_user_email ON \"user\"(email);")
    sql_lines.append("CREATE INDEX idx_seer_speciality_seer ON seer_speciality(seer_id);")
    sql_lines.append("CREATE INDEX idx_seer_speciality_category ON seer_speciality(category_id);")
    sql_lines.append("CREATE INDEX idx_customer_potential_customer ON customer_potential(customer_id);")
    sql_lines.append("CREATE INDEX idx_customer_potential_month_year ON customer_potential(month, year);")
    sql_lines.append("CREATE INDEX idx_seer_performance_seer ON seer_performance(seer_id);")
    sql_lines.append("CREATE INDEX idx_seer_performance_month_year ON seer_performance(month, year);")
    sql_lines.append("")
    
    sql_lines.append("-- Disable triggers and constraints for faster import")
    sql_lines.append("SET session_replication_role = 'replica';")
    sql_lines.append("")
    
    # ========================================================================
    # INSERT DATA
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- INSERT DATA")
    sql_lines.append("-- ============================================================================")
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
    # USERS
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
    
    # Add customers (role = 'CUSTOMER')
    for user in customer_data['user']:
        val = f"({format_sql_value(user['user_id'])}, 'CUSTOMER', {format_sql_value(user['email'])}, {format_sql_value(user['gender'])}, {format_sql_value(user['full_name'])}, {format_sql_value(user['profile_description'])}, {format_sql_value(user['birth_date'])}, {format_sql_value(user['created_at'])}, {format_sql_value(user['updated_at'])})"
        all_users.append(val)
    
    # Add seers (role = 'SEER')
    for user in seer_data['user']:
        val = f"({format_sql_value(user['user_id'])}, 'SEER', {format_sql_value(user['email'])}, {format_sql_value(user['gender'])}, {format_sql_value(user['full_name'])}, {format_sql_value(user['profile_description'])}, {format_sql_value(user['birth_date'])}, {format_sql_value(user['created_at'])}, {format_sql_value(user['updated_at'])})"
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
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- Re-enable triggers and constraints")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("SET session_replication_role = 'origin';")
    sql_lines.append("")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- VERIFY DATA")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("SELECT 'Knowledge Categories' as table_name, COUNT(*) as record_count FROM knowledge_category")
    sql_lines.append("UNION ALL")
    sql_lines.append("SELECT 'Users', COUNT(*) FROM \"user\"")
    sql_lines.append("UNION ALL")
    sql_lines.append("SELECT 'Seer Specialities', COUNT(*) FROM seer_speciality")
    sql_lines.append("UNION ALL")
    sql_lines.append("SELECT 'Customer Potential', COUNT(*) FROM customer_potential")
    sql_lines.append("UNION ALL")
    sql_lines.append("SELECT 'Seer Performance', COUNT(*) FROM seer_performance;")
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
    print("📝 GENERATING COMPLETE SQL FILE WITH SCHEMA + DATA")
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
    
    print("\n📋 File bao gồm:")
    print("   ✅ DROP TABLE statements (xóa bảng cũ nếu có)")
    print("   ✅ CREATE TABLE statements với:")
    print("       - Primary Keys")
    print("       - Foreign Keys")
    print("       - Check Constraints")
    print("       - Unique Constraints")
    print("       - Indexes")
    print("   ✅ INSERT data cho:")
    print("       - Knowledge Categories (6 records)")
    print("       - Users - Customers & Seers (81 records)")
    print("       - Seer Specialities (25 records)")
    print("       - Customer Potential (504 records)")
    print("       - Seer Performance (109 records)")
    print("   ✅ Verification query để check số lượng records")

if __name__ == "__main__":
    main()
