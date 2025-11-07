# === THÊM PHẦN TRAIN VÀO ĐÂY ===

# ============================================================================
# 1. Train DDL (Cấu trúc bảng)
# ============================================================================

# Bảng Knowledge Category
agent.train(
    ddl="""
    CREATE TABLE knowledge_category (
        category_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT
    );
    """
)

# Bảng Customer Potential
agent.train(
    ddl="""
    CREATE TABLE customer_potential (
        customer_full_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        customer_profile_description TEXT,
        customer_birth_date TIMESTAMP,
        customer_gender VARCHAR(10),
        month INT NOT NULL CHECK (month BETWEEN 1 AND 12),
        year INT NOT NULL,
        potential_point INT NOT NULL,
        potential_tier VARCHAR(20) NOT NULL,
        ranking INT NOT NULL,
        total_booking_requests INT NOT NULL DEFAULT 0,
        total_spending NUMERIC(15, 2) NOT NULL DEFAULT 0,
        cancelled_by_customer INT NOT NULL DEFAULT 0,
        PRIMARY KEY (customer_email, month, year)
    );
    """
)

# Bảng Seer Performance
agent.train(
    ddl="""
    CREATE TABLE seer_performance (
        seer_full_name VARCHAR(255) NOT NULL,
        seer_email VARCHAR(255) NOT NULL,
        seer_profile_description TEXT,
        seer_birth_date TIMESTAMP,
        seer_gender VARCHAR(10),
        seer_speciality TEXT[],
        month INT NOT NULL CHECK (month BETWEEN 1 AND 12),
        year INT NOT NULL,
        performance_tier VARCHAR(20) NOT NULL,
        performance_point INT NOT NULL,
        ranking INT NOT NULL,
        total_packages INT NOT NULL DEFAULT 0,
        total_rates INT NOT NULL DEFAULT 0,
        avg_rating NUMERIC(3, 2) NOT NULL DEFAULT 0,
        total_bookings INT NOT NULL DEFAULT 0,
        completed_bookings INT NOT NULL DEFAULT 0,
        cancelled_by_seer INT NOT NULL DEFAULT 0,
        total_revenue NUMERIC(15, 2) NOT NULL DEFAULT 0,
        bonus NUMERIC(15, 2) NOT NULL DEFAULT 0,
        PRIMARY KEY (seer_email, month, year)
    );
    """
)

# ============================================================================
# 2. Train Documentation (Giải thích nghiệp vụ)
# ============================================================================

# Tổng quan hệ thống
agent.train(
    documentation="""
    Hệ thống quản lý nền tảng xem bói - nơi khách hàng (customer) đặt lịch với các thầy bói (seer).
    Có 3 nhóm dữ liệu chính:
    1. knowledge_category: Các danh mục dịch vụ xem bói (Tarot, Cung Hoàng Đạo, Nhân Tướng Học, v.v.)
    2. customer_potential: Thống kê tiềm năng khách hàng theo tháng với hệ thống phân hạng
    3. seer_performance: Thống kê hiệu suất thầy bói theo tháng với hệ thống phân hạng
    """
)

# Knowledge Category
agent.train(
    documentation="""
    Bảng knowledge_category lưu các loại hình dịch vụ xem bói trên nền tảng.
    Ví dụ: Tarot (Bài Tarot), Cung Hoàng Đạo (Astrology), Nhân Tướng Học (Face Reading), 
    Ngũ Hành (Five Elements), Chỉ Tay (Palm Reading).
    Mỗi category có ID duy nhất, tên và mô tả.
    """
)

# Customer Potential
agent.train(
    documentation="""
    Bảng customer_potential theo dõi chỉ số tương tác của khách hàng theo tháng.
    Mỗi bản ghi là thống kê của 1 khách hàng trong 1 tháng cụ thể.
    
    Các trường quan trọng:
    - customer_full_name, customer_email: Thông tin khách hàng
    - month, year: Tháng và năm được đo
    - potential_point: Điểm tiềm năng (thang 0-100)
    - potential_tier: Hạng khách hàng (CASUAL, STANDARD, PREMIUM, VIP)
    - ranking: Xếp hạng trong tháng (1 = cao nhất)
    - total_booking_requests: Số lượng booking đã tạo
    - total_spending: Tổng chi tiêu
    - cancelled_by_customer: Số booking bị hủy bởi khách
    
    Hệ thống phân hạng khách hàng:
    - CASUAL: 0-49 điểm (tương tác thấp)
    - STANDARD: 50-69 điểm (tương tác trung bình)
    - PREMIUM: 70-84 điểm (tương tác cao)
    - VIP: 85-100 điểm (tương tác rất cao)
    
    Công thức tính potential_point:
    - 40% Loyalty (tần suất đặt lịch)
    - 35% Value (số tiền chi tiêu)
    - 25% Reliability (tỷ lệ hủy lịch thấp)
    """
)

# Seer Performance
agent.train(
    documentation="""
    Bảng seer_performance theo dõi hiệu suất của thầy bói theo tháng.
    Mỗi bản ghi là thống kê của 1 thầy bói trong 1 tháng cụ thể.
    
    Các trường quan trọng:
    - seer_full_name, seer_email: Thông tin thầy bói
    - seer_speciality: Mảng các chuyên môn (ví dụ: ['Tarot', 'Astrology'])
    - month, year: Tháng và năm được đo
    - performance_point: Điểm hiệu suất (thang 0-100)
    - performance_tier: Hạng thầy bói (APPRENTICE, PROFESSIONAL, EXPERT, MASTER)
    - ranking: Xếp hạng trong tháng (1 = cao nhất)
    - total_packages: Số gói dịch vụ đã tạo
    - total_rates: Số đánh giá nhận được
    - avg_rating: Điểm đánh giá trung bình (0.00-5.00)
    - total_bookings: Tổng booking nhận được
    - completed_bookings: Booking hoàn thành thành công
    - cancelled_by_seer: Booking bị hủy bởi thầy bói
    - total_revenue: Tổng doanh thu
    - bonus: Tiền thưởng
    
    Hệ thống phân hạng thầy bói:
    - APPRENTICE: 0-49 điểm (mới vào nghề)
    - PROFESSIONAL: 50-69 điểm (chuyên nghiệp)
    - EXPERT: 70-84 điểm (chuyên gia)
    - MASTER: 85-100 điểm (bậc thầy)
    
    Công thức tính performance_point:
    - 30% Engagement (gói dịch vụ và booking)
    - 25% Rating (mức độ hài lòng)
    - 20% Completion rate (độ tin cậy)
    - 15% Low cancellation (tính chuyên nghiệp)
    - 10% Earning (tạo doanh thu)
    """
)

# ============================================================================
# 3. Train Question-SQL pairs (Câu hỏi mẫu)
# ============================================================================

# === Queries cơ bản ===
agent.train(
    question="Có bao nhiêu khách hàng trong database?",
    sql="SELECT COUNT(DISTINCT customer_email) FROM customer_potential;"
)

agent.train(
    question="Có bao nhiêu thầy bói trong database?",
    sql="SELECT COUNT(DISTINCT seer_email) FROM seer_performance;"
)

agent.train(
    question="Danh sách tất cả các loại hình xem bói?",
    sql="SELECT name, description FROM knowledge_category ORDER BY name;"
)

# === Queries về Customer Tier ===
agent.train(
    question="Có bao nhiêu khách hàng VIP trong tháng 11/2025?",
    sql="SELECT COUNT(*) FROM customer_potential WHERE potential_tier = 'VIP' AND month = 11 AND year = 2025;"
)

agent.train(
    question="Hiển thị tất cả khách hàng VIP trong tháng 11/2025",
    sql="SELECT customer_full_name, customer_email, potential_point, total_spending, ranking FROM customer_potential WHERE potential_tier = 'VIP' AND month = 11 AND year = 2025 ORDER BY ranking;"
)

agent.train(
    question="Phân bố các hạng khách hàng trong tháng 11/2025?",
    sql="SELECT potential_tier, COUNT(*) as so_luong FROM customer_potential WHERE month = 11 AND year = 2025 GROUP BY potential_tier ORDER BY potential_tier;"
)

agent.train(
    question="Top 10 khách hàng chi tiêu nhiều nhất tháng 11/2025?",
    sql="SELECT customer_full_name, customer_email, total_spending, potential_tier, ranking FROM customer_potential WHERE month = 11 AND year = 2025 ORDER BY total_spending DESC LIMIT 10;"
)

agent.train(
    question="Khách hàng nào có điểm tiềm năng cao nhất tháng 11/2025?",
    sql="SELECT customer_full_name, customer_email, potential_point, potential_tier, ranking FROM customer_potential WHERE month = 11 AND year = 2025 ORDER BY potential_point DESC LIMIT 10;"
)

# === Queries về Seer Performance ===
agent.train(
    question="Có bao nhiêu thầy bói hạng MASTER trong tháng 11/2025?",
    sql="SELECT COUNT(*) FROM seer_performance WHERE performance_tier = 'MASTER' AND month = 11 AND year = 2025;"
)

agent.train(
    question="Hiển thị tất cả thầy bói hạng MASTER trong tháng 11/2025",
    sql="SELECT seer_full_name, seer_email, performance_point, total_revenue, avg_rating, ranking FROM seer_performance WHERE performance_tier = 'MASTER' AND month = 11 AND year = 2025 ORDER BY ranking;"
)

agent.train(
    question="Phân bố các hạng thầy bói trong tháng 11/2025?",
    sql="SELECT performance_tier, COUNT(*) as so_luong FROM seer_performance WHERE month = 11 AND year = 2025 GROUP BY performance_tier ORDER BY performance_tier;"
)

agent.train(
    question="Top 10 thầy bói có doanh thu cao nhất tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, total_revenue, performance_tier, ranking FROM seer_performance WHERE month = 11 AND year = 2025 ORDER BY total_revenue DESC LIMIT 10;"
)

agent.train(
    question="Thầy bói nào có rating cao nhất tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, avg_rating, total_rates, performance_tier FROM seer_performance WHERE month = 11 AND year = 2025 AND total_rates > 0 ORDER BY avg_rating DESC LIMIT 10;"
)

# === Queries về Speciality ===
agent.train(
    question="Thầy bói nào chuyên về Tarot trong tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, seer_speciality, avg_rating, total_revenue FROM seer_performance WHERE month = 11 AND year = 2025 AND 'Tarot' = ANY(seer_speciality) ORDER BY avg_rating DESC;"
)

agent.train(
    question="Có bao nhiêu thầy bói có nhiều hơn 1 chuyên môn trong tháng 11/2025?",
    sql="SELECT COUNT(*) FROM seer_performance WHERE month = 11 AND year = 2025 AND array_length(seer_speciality, 1) > 1;"
)

agent.train(
    question="Doanh thu trung bình theo từng loại chuyên môn trong tháng 11/2025?",
    sql="SELECT unnest(seer_speciality) as chuyen_mon, AVG(total_revenue) as doanh_thu_tb, COUNT(*) as so_thay FROM seer_performance WHERE month = 11 AND year = 2025 GROUP BY chuyen_mon ORDER BY doanh_thu_tb DESC;"
)

# === Queries về xu hướng theo tháng ===
agent.train(
    question="Xu hướng tổng chi tiêu khách hàng theo tháng năm 2025",
    sql="SELECT month, year, SUM(total_spending) as tong_chi_tieu, COUNT(*) as so_khach FROM customer_potential WHERE year = 2025 GROUP BY month, year ORDER BY year, month;"
)

agent.train(
    question="Xu hướng doanh thu thầy bói theo tháng năm 2025",
    sql="SELECT month, year, SUM(total_revenue) as tong_doanh_thu, AVG(avg_rating) as rating_tb FROM seer_performance WHERE year = 2025 GROUP BY month, year ORDER BY year, month;"
)

agent.train(
    question="Số lượng khách VIP thay đổi như thế nào qua các tháng 2025?",
    sql="SELECT month, year, COUNT(*) as so_vip FROM customer_potential WHERE potential_tier = 'VIP' AND year = 2025 GROUP BY month, year ORDER BY year, month;"
)

# === Queries về Ranking ===
agent.train(
    question="Khách hàng xếp hạng #1 trong tháng 11/2025 là ai?",
    sql="SELECT customer_full_name, customer_email, ranking, potential_point, total_spending FROM customer_potential WHERE month = 11 AND year = 2025 ORDER BY ranking LIMIT 1;"
)

agent.train(
    question="Thầy bói xếp hạng #1 trong tháng 11/2025 là ai?",
    sql="SELECT seer_full_name, seer_email, ranking, performance_point, total_revenue, avg_rating FROM seer_performance WHERE month = 11 AND year = 2025 ORDER BY ranking LIMIT 1;"
)

agent.train(
    question="Hiển thị khách hàng trong top 5 tháng 11/2025",
    sql="SELECT customer_full_name, customer_email, ranking, potential_point, potential_tier FROM customer_potential WHERE month = 11 AND year = 2025 AND ranking <= 5 ORDER BY ranking;"
)

# === Queries về Booking & Cancellation ===
agent.train(
    question="Tỷ lệ hủy lịch trung bình của khách hàng tháng 11/2025?",
    sql="SELECT AVG(CASE WHEN total_booking_requests > 0 THEN (cancelled_by_customer::FLOAT / total_booking_requests) ELSE 0 END) * 100 as ty_le_huy FROM customer_potential WHERE month = 11 AND year = 2025;"
)

agent.train(
    question="Khách hàng nào đặt lịch nhiều nhưng chi tiêu ít tháng 11/2025?",
    sql="SELECT customer_full_name, customer_email, total_booking_requests, total_spending, potential_tier FROM customer_potential WHERE month = 11 AND year = 2025 AND total_booking_requests > 10 ORDER BY total_spending ASC LIMIT 10;"
)

agent.train(
    question="Tỷ lệ hoàn thành booking của thầy bói tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, total_bookings, completed_bookings, CASE WHEN total_bookings > 0 THEN (completed_bookings::FLOAT / total_bookings) * 100 ELSE 0 END as ty_le_hoan_thanh FROM seer_performance WHERE month = 11 AND year = 2025 ORDER BY ty_le_hoan_thanh DESC;"
)

# === Queries về Revenue & Bonus ===
agent.train(
    question="Tổng doanh thu toàn nền tảng tháng 11/2025?",
    sql="SELECT SUM(total_revenue) as tong_doanh_thu FROM seer_performance WHERE month = 11 AND year = 2025;"
)

agent.train(
    question="Thầy bói nào nhận bonus nhiều nhất tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, bonus, total_revenue, performance_tier FROM seer_performance WHERE month = 11 AND year = 2025 ORDER BY bonus DESC LIMIT 10;"
)

agent.train(
    question="Doanh thu trung bình mỗi booking của thầy bói tháng 11/2025?",
    sql="SELECT seer_full_name, seer_email, total_revenue, total_bookings, CASE WHEN total_bookings > 0 THEN total_revenue / total_bookings ELSE 0 END as doanh_thu_per_booking FROM seer_performance WHERE month = 11 AND year = 2025 ORDER BY doanh_thu_per_booking DESC;"
)

# === Queries về Gender ===
agent.train(
    question="Phân bố khách hàng theo giới tính tháng 11/2025?",
    sql="SELECT customer_gender, COUNT(*) as so_luong FROM customer_potential WHERE month = 11 AND year = 2025 GROUP BY customer_gender;"
)

agent.train(
    question="Chi tiêu trung bình theo giới tính khách hàng tháng 11/2025?",
    sql="SELECT customer_gender, AVG(total_spending) as chi_tieu_tb, COUNT(*) as so_khach FROM customer_potential WHERE month = 11 AND year = 2025 GROUP BY customer_gender ORDER BY chi_tieu_tb DESC;"
)

agent.train(
    question="Phân bố thầy bói theo giới tính tháng 11/2025?",
    sql="SELECT seer_gender, COUNT(*) as so_luong FROM seer_performance WHERE month = 11 AND year = 2025 GROUP BY seer_gender;"
)

# === Queries phân tích phức tạp ===
agent.train(
    question="So sánh tổng chi tiêu khách vs doanh thu thầy bói tháng 11/2025",
    sql="SELECT (SELECT SUM(total_spending) FROM customer_potential WHERE month = 11 AND year = 2025) as tong_chi_khach, (SELECT SUM(total_revenue) FROM seer_performance WHERE month = 11 AND year = 2025) as tong_doanh_thu_thay;"
)

agent.train(
    question="Mối liên hệ giữa rating và doanh thu theo tier thầy bói tháng 11/2025?",
    sql="SELECT performance_tier, AVG(avg_rating) as rating_tb, AVG(total_revenue) as doanh_thu_tb FROM seer_performance WHERE month = 11 AND year = 2025 AND total_rates > 0 GROUP BY performance_tier ORDER BY performance_tier;"
)

agent.train(
    question="Tháng nào năm 2025 có tương tác khách hàng cao nhất?",
    sql="SELECT month, SUM(total_booking_requests) as tong_booking, SUM(total_spending) as tong_chi_tieu, COUNT(*) as so_khach FROM customer_potential WHERE year = 2025 GROUP BY month ORDER BY tong_booking DESC LIMIT 1;"
)

agent.train(
    question="Tìm thầy bói có rating 5.0 hoàn hảo tháng 11/2025",
    sql="SELECT seer_full_name, seer_email, avg_rating, total_rates, total_revenue FROM seer_performance WHERE month = 11 AND year = 2025 AND avg_rating = 5.00 AND total_rates > 0 ORDER BY total_rates DESC;"
)

agent.train(
    question="Phần trăm khách hàng VIP trong tháng 11/2025?",
    sql="SELECT (COUNT(CASE WHEN potential_tier = 'VIP' THEN 1 END)::FLOAT / COUNT(*)) * 100 as phan_tram_vip FROM customer_potential WHERE month = 11 AND year = 2025;"
)

agent.train(
    question="Hiển thị tuổi khách hàng cùng chi tiêu tháng 11/2025",
    sql="SELECT customer_full_name, customer_email, EXTRACT(YEAR FROM AGE(customer_birth_date)) as tuoi, total_spending, potential_tier FROM customer_potential WHERE month = 11 AND year = 2025 ORDER BY total_spending DESC;"
)