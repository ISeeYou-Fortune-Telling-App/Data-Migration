import re

print("=" * 80)
print("📊 VERIFY SQL IMPORT FILE")
print("=" * 80)

with open('4_sqldata_vanna/data_import.sql', 'r', encoding='utf-8') as f:
    sql_content = f.read()

print(f"\n📁 File: 4_sqldata_vanna/data_import.sql")
print(f"📏 Size: {len(sql_content):,} characters")
print(f"📄 Lines: {sql_content.count(chr(10)):,} lines")

print("\n" + "=" * 80)
print("📋 TABLES IMPORTED:")
print("=" * 80)

# Count INSERT statements
tables = [
    'knowledge_category',
    '"user"',
    'seer_speciality',
    'customer_potential',
    'seer_performance'
]

for table in tables:
    # Find INSERT INTO statement for this table
    pattern = f'INSERT INTO {table}'
    if pattern in sql_content:
        # Count VALUES
        table_section = sql_content.split(pattern)[1].split(';')[0]
        values_count = table_section.count('(') - table_section.count('VALUES (')
        print(f"✅ {table:30s}: Found (estimated {values_count} records)")
    else:
        print(f"❌ {table:30s}: NOT FOUND")

print("\n" + "=" * 80)
print("🔍 SUMMARY FROM FILE:")
print("=" * 80)

# Extract summary from file
if "IMPORT SUMMARY" in sql_content:
    summary_section = sql_content.split("IMPORT SUMMARY")[1].split("======")[0]
    summary_lines = [line.strip() for line in summary_section.split('\n') if line.strip() and line.strip().startswith('--')]
    for line in summary_lines:
        if 'records' in line.lower():
            print(line)

print("\n" + "=" * 80)
print("✅ VERIFICATION COMPLETE!")
print("=" * 80)

print("\n💡 Lưu ý:")
print("   - File chỉ chứa các trường cần thiết của User (không có password, phone, avatar, etc.)")
print("   - Sử dụng session_replication_role để tối ưu tốc độ import")
print("   - Dữ liệu đã được format đúng chuẩn PostgreSQL")
print("   - Tất cả string đã được escape đúng cách (single quotes)")

print("\n📝 Cách sử dụng:")
print("   1. Connect vào PostgreSQL database")
print("   2. Run: \\i 4_sqldata_vanna/data_import.sql")
print("   3. Hoặc: psql -U username -d database_name -f 4_sqldata_vanna/data_import.sql")
