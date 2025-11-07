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
    elif isinstance(value, list):
        # Convert list to PostgreSQL array format
        items = [format_sql_value(item) for item in value]
        return f"ARRAY[{', '.join(items)}]"
    else:
        return f"'{str(value)}'"

def generate_data2_sql():
    """Generate data2_import.sql with training AI data"""
    
    sql_lines = []
    
    # ========================================================================
    # HEADER
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- DATA2 IMPORT FOR VANNA AI TRAINING (Training AI Version)")
    sql_lines.append("-- Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    sql_lines.append("-- ============================================================================")
    sql_lines.append("")
    sql_lines.append("-- Drop existing tables if exists")
    sql_lines.append("DROP TABLE IF EXISTS seer_performance CASCADE;")
    sql_lines.append("DROP TABLE IF EXISTS customer_potential CASCADE;")
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
    
    # Customer Potential Table (Training AI version)
    sql_lines.append("-- Customer Potential Table (Training AI Version)")
    sql_lines.append("CREATE TABLE customer_potential (")
    sql_lines.append("    customer_full_name VARCHAR(255) NOT NULL,")
    sql_lines.append("    customer_email VARCHAR(255) NOT NULL,")
    sql_lines.append("    customer_profile_description TEXT,")
    sql_lines.append("    customer_birth_date TIMESTAMP,")
    sql_lines.append("    customer_gender VARCHAR(10),")
    sql_lines.append("    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),")
    sql_lines.append("    year INT NOT NULL,")
    sql_lines.append("    potential_point INT NOT NULL,")
    sql_lines.append("    potential_tier VARCHAR(20) NOT NULL, -- CASUAL, STANDARD, PREMIUM, VIP")
    sql_lines.append("    ranking INT NOT NULL,")
    sql_lines.append("    total_booking_requests INT NOT NULL DEFAULT 0,")
    sql_lines.append("    total_spending NUMERIC(15, 2) NOT NULL DEFAULT 0,")
    sql_lines.append("    cancelled_by_customer INT NOT NULL DEFAULT 0,")
    sql_lines.append("    PRIMARY KEY (customer_email, month, year)")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Seer Performance Table (Training AI version)
    sql_lines.append("-- Seer Performance Table (Training AI Version)")
    sql_lines.append("CREATE TABLE seer_performance (")
    sql_lines.append("    seer_full_name VARCHAR(255) NOT NULL,")
    sql_lines.append("    seer_email VARCHAR(255) NOT NULL,")
    sql_lines.append("    seer_profile_description TEXT,")
    sql_lines.append("    seer_birth_date TIMESTAMP,")
    sql_lines.append("    seer_gender VARCHAR(10),")
    sql_lines.append("    seer_speciality TEXT[], -- Array of speciality names")
    sql_lines.append("    month INT NOT NULL CHECK (month BETWEEN 1 AND 12),")
    sql_lines.append("    year INT NOT NULL,")
    sql_lines.append("    performance_tier VARCHAR(20) NOT NULL, -- APPRENTICE, PROFESSIONAL, EXPERT, MASTER")
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
    sql_lines.append("    PRIMARY KEY (seer_email, month, year)")
    sql_lines.append(");")
    sql_lines.append("")
    
    # Indexes
    sql_lines.append("-- Create indexes for better query performance")
    sql_lines.append("CREATE INDEX idx_customer_potential_email ON customer_potential(customer_email);")
    sql_lines.append("CREATE INDEX idx_customer_potential_month_year ON customer_potential(month, year);")
    sql_lines.append("CREATE INDEX idx_customer_potential_tier ON customer_potential(potential_tier);")
    sql_lines.append("CREATE INDEX idx_seer_performance_email ON seer_performance(seer_email);")
    sql_lines.append("CREATE INDEX idx_seer_performance_month_year ON seer_performance(month, year);")
    sql_lines.append("CREATE INDEX idx_seer_performance_tier ON seer_performance(performance_tier);")
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
    sql_lines.append("-- KNOWLEDGE CATEGORIES")
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
    # CUSTOMER POTENTIAL (Training AI)
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- CUSTOMER POTENTIAL (Training AI Version)")
    sql_lines.append("-- ============================================================================")
    
    with open('3_statistic_training_ai/customer_potential.json', 'r', encoding='utf-8') as f:
        cp_data = json.load(f)
    
    sql_lines.append("INSERT INTO customer_potential (customer_full_name, customer_email, customer_profile_description, customer_birth_date, customer_gender, month, year, potential_point, potential_tier, ranking, total_booking_requests, total_spending, cancelled_by_customer) VALUES")
    
    cp_values = []
    for record in cp_data:
        val = f"({format_sql_value(record['customer_full_name'])}, {format_sql_value(record['customer_email'])}, {format_sql_value(record['customer_profile_description'])}, {format_sql_value(record['customer_birth_date'])}, {format_sql_value(record['customer_gender'])}, {record['month']}, {record['year']}, {record['potential_point']}, {format_sql_value(record['potential_tier'])}, {record['ranking']}, {record['total_booking_requests']}, {record['total_spending']}, {record['cancelled_by_customer']})"
        cp_values.append(val)
    
    sql_lines.append(",\n".join(cp_values) + ";")
    sql_lines.append("")
    sql_lines.append(f"-- Total: {len(cp_data)} customer potential records")
    sql_lines.append("")
    
    # ========================================================================
    # SEER PERFORMANCE (Training AI)
    # ========================================================================
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- SEER PERFORMANCE (Training AI Version)")
    sql_lines.append("-- ============================================================================")
    
    with open('3_statistic_training_ai/seer_performance.json', 'r', encoding='utf-8') as f:
        sp_data = json.load(f)
    
    sql_lines.append("INSERT INTO seer_performance (seer_full_name, seer_email, seer_profile_description, seer_birth_date, seer_gender, seer_speciality, month, year, performance_tier, performance_point, ranking, total_packages, total_rates, avg_rating, total_bookings, completed_bookings, cancelled_by_seer, total_revenue, bonus) VALUES")
    
    sp_values = []
    for record in sp_data:
        val = f"({format_sql_value(record['seer_full_name'])}, {format_sql_value(record['seer_email'])}, {format_sql_value(record['seer_profile_description'])}, {format_sql_value(record['seer_birth_date'])}, {format_sql_value(record['seer_gender'])}, {format_sql_value(record['seer_speciality'])}, {record['month']}, {record['year']}, {format_sql_value(record['performance_tier'])}, {record['performance_point']}, {record['ranking']}, {record['total_packages']}, {record['total_rates']}, {record['avg_rating']}, {record['total_bookings']}, {record['completed_bookings']}, {record['cancelled_by_seer']}, {record['total_revenue']}, {record['bonus']})"
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
    sql_lines.append("SELECT 'Customer Potential', COUNT(*) FROM customer_potential")
    sql_lines.append("UNION ALL")
    sql_lines.append("SELECT 'Seer Performance', COUNT(*) FROM seer_performance;")
    sql_lines.append("")
    sql_lines.append("-- ============================================================================")
    sql_lines.append("-- IMPORT SUMMARY")
    sql_lines.append("-- ============================================================================")
    sql_lines.append(f"-- Knowledge Categories: {len(cat_data['knowledge_category'])} records")
    sql_lines.append(f"-- Customer Potential: {len(cp_data)} records (Training AI format)")
    sql_lines.append(f"-- Seer Performance: {len(sp_data)} records (Training AI format)")
    sql_lines.append(f"-- TOTAL: {len(cat_data['knowledge_category']) + len(cp_data) + len(sp_data)} records")
    sql_lines.append("-- ============================================================================")
    
    return "\n".join(sql_lines)

def main():
    print("=" * 80)
    print("📝 GENERATING DATA2_IMPORT.SQL (Training AI Version)")
    print("=" * 80)
    
    print("\n📖 Reading JSON files from 3_statistic_training_ai...")
    sql_content = generate_data2_sql()
    
    output_file = '4_sqldata_vanna/data2_import.sql'
    
    print(f"\n💾 Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(sql_content)
    
    print(f"\n✅ File created: {output_file}")
    print(f"📊 File size: {len(sql_content):,} characters")
    
    print("\n" + "=" * 80)
    print("🎉 HOÀN THÀNH!")
    print("=" * 80)
    
    print("\n📋 File bao gồm 3 bảng:")
    print("   ✅ knowledge_category - Các danh mục kiến thức")
    print("   ✅ customer_potential - Dữ liệu customer từ 3_statistic_training_ai")
    print("       • Có thông tin chi tiết: full_name, email, profile, birth_date, gender")
    print("       • potential_tier là TEXT (CASUAL, STANDARD, PREMIUM, VIP)")
    print("       • KHÔNG có customer_id (thay bằng thông tin chi tiết)")
    print("   ✅ seer_performance - Dữ liệu seer từ 3_statistic_training_ai")
    print("       • Có thông tin chi tiết: full_name, email, profile, birth_date, gender")
    print("       • seer_speciality là TEXT[] array")
    print("       • performance_tier là TEXT (APPRENTICE, PROFESSIONAL, EXPERT, MASTER)")
    print("       • KHÔNG có seer_id (thay bằng thông tin chi tiết)")

if __name__ == "__main__":
    main()
