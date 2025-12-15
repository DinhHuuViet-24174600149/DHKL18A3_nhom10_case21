import pandas as pd

# ==============================
# 1. ĐỌC DỮ LIỆU CSV
# ==============================
students = pd.read_csv("student_class.csv", engine="python", skip_blank_lines=True)
classes = pd.read_csv("class_schedule.csv", engine="python", skip_blank_lines=True)
attendance = pd.read_csv("attendance_log.csv", engine="python", skip_blank_lines=True)

# ==============================
# 2. CHUẨN HÓA DỮ LIỆU
# ==============================
for df in [students, classes, attendance]:
    df.columns = df.columns.str.strip().str.lower()
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

# Chuẩn hóa student_id và class_cohort
students["student_id"] = students["student_id"].str.lower()
students["full_name"] = students["full_name"].str.title()
students["class_cohort"] = students["class_cohort"].str.replace(r"[-_\s]", "", regex=True).str.lower()

# Chuẩn hóa class_id, course_name, weekday, slot
classes["class_id"] = classes["class_id"].str.replace(r"[-_\s]", "", regex=True).str.lower()
classes["course_name"] = classes["course_name"].str.title()
classes["weekday"] = classes["weekday"].str.lower()
classes["slot"] = classes["slot"].str.lower()

# Chuẩn hóa class_id trong attendance
attendance["class_id"] = attendance["class_id"].str.replace(r"[-_\s]", "", regex=True).str.lower()
attendance["student_id"] = attendance["student_id"].str.lower()
attendance["date"] = pd.to_datetime(attendance["date"], dayfirst=True, errors="coerce")

# Chuẩn hóa status
status_mapping = {
    "co mat": "Present",
    "vang": "Absent",
    "di muon": "Late",
    "nghi phep": "Excused"
}
attendance["status"] = attendance["status"].str.lower().map(status_mapping)
attendance["status"] = attendance["status"].fillna("Unknown")

# Chuẩn hóa note
attendance["note"] = attendance["note"].str.strip().str.title()

# ==============================
# 3. DỊCH NOTE SANG TIẾNG ANH
# ==============================
note_translation = {
    "On Time": "Đúng giờ",
    "Khong Ly Do": "No Reason",
    "Traffic Jam": "Tắc đường"
}
attendance["note_en"] = attendance["note"].map(note_translation).fillna(attendance["note"])

# ==============================
# 4. THỐNG KÊ & TRUY VẤN
# ==============================
print("\n--- Số lượng sinh viên theo lớp/khoá ---")
sv_theo_khoa = students.groupby("class_cohort")["student_id"].count()
print(sv_theo_khoa)

print("\n--- Số lượng lớp học phần theo môn học ---")
lop_theo_mon = classes.groupby("course_name")["class_id"].count()
print(lop_theo_mon)

print("\n--- Số buổi học theo class_id ---")
buoi_hoc = attendance.groupby("class_id").size()
print(buoi_hoc)

print("\n--- Số lượt điểm danh theo trạng thái ---")
trang_thai = attendance["status"].value_counts()
print(trang_thai)

print("\n--- Các bản ghi attendance bị lỗi ---")
loi = attendance[
    (~attendance["student_id"].isin(students["student_id"])) |
    (~attendance["class_id"].isin(classes["class_id"]))
]
if loi.empty:
    print("Không có bản ghi lỗi.")
else:
    print(loi)

# ==============================
# 5. HIỂN THỊ NOTE CẢ TIẾNG VIỆT & ANH
# ==============================
print("\n--- Chi tiết note của từng lượt điểm danh ---")
print(attendance[["date","class_id","student_id","status","note","note_en"]])
