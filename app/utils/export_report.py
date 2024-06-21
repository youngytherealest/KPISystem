from mailmerge import MailMerge
import os

def export(username, mssv, sv_hoten, sv_lop, tt_donvi, tt_nguoihuongdan, dg_ythuckyluat_text, dg_tuanthuthoigian_text, dg_kienthuc_text, dg_kynangnghe_text, dg_khanangdoclap_text, dg_khanangnhom_text, dg_khananggiaiquyetcongviec_text, dg_ythuckyluat_number, dg_tuanthuthoigian_number, dg_kienthuc_number, dg_kynangnghe_number, dg_khanangdoclap_number, dg_khanangnhom_number, dg_khananggiaiquyetcongviec_number, dg_danhgiachung_number) -> bool:
    '''
    NHẬN THAM SỐ ĐẦU VÀO RỒI XUẤT FILE DOCX
    ----------------
    - sv_hoten: Họ tên sinh viên
    - sv_lop: Lớp 
    - tt_donvi: Cơ sở thực tập
    - tt_nguoihuongdan: Họ tên người hướng dẫn
    - dg_ythuckyluat_text: Ý thức kỷ luật, tuân thủ nội quy (text)
    - dg_tuanthuthoigian_text: Tuân thủ thời gian (text)
    - dg_kienthuc_text: Kiến thức (text)
    - dg_kynangnghe_text: Kỹ năng nghề (text)
    - dg_khanangdoclap_text: Khả năng làm việc độc lập (text)
    - dg_khanangnhom_text: Khả năng làm việc nhóm (text)
    - dg_khananggiaiquyetcongviec_text: Khả năng giải quyết công việc (text)
    - dg_ythuckyluat_number: Ý thức kỷ luật, tuân thủ nội quy (number)
    - dg_tuanthuthoigian_number: Tuân thủ thời gian (number)
    - dg_kienthuc_number: Kiến thức (number)
    - dg_kynangnghe_number: Kỹ năng nghề (number)
    - dg_khanangdoclap_number: Khả năng làm việc độc lập (number)
    - dg_khanangnhom_number: Khả năng làm việc nhóm (number)
    - dg_khananggiaiquyetcongviec_number: Khả năng giải quyết công việc (number)
    - dg_danhgiachung: Đánh giá chung (number)
    '''
    try:
        # Đường dẫn tới file docx mẫu chứa các trường mail merge
        docx_template = "phieudanhgia_vlute.docx"

        # Dữ liệu cho các trường mail merge (được cung cấp dưới dạng từ điển)
        data = {
            "student_fullname": str(sv_hoten),
            "student_class": str(sv_lop),
            "unit": str(tt_donvi),
            "instructor_fullname": str(tt_nguoihuongdan),
            "M_1_text": str(dg_ythuckyluat_text),
            "M_2_text": str(dg_tuanthuthoigian_text),
            "M_3_text": str(dg_kienthuc_text),
            "M_4_text": str(dg_kynangnghe_text),
            "M_5_text": str(dg_khanangdoclap_text),
            "M_6_text": str(dg_khanangnhom_text),
            "M_7_text": str(dg_khananggiaiquyetcongviec_text),
            "M_1_point": str(dg_ythuckyluat_number),
            "M_2_point": str(dg_tuanthuthoigian_number),
            "M_3_point": str(dg_kienthuc_number),
            "M_4_point": str(dg_kynangnghe_number),
            "M_5_point": str(dg_khanangdoclap_number),
            "M_6_point": str(dg_khanangnhom_number),
            "M_7_point": str(dg_khananggiaiquyetcongviec_number),
            "Title": str(dg_danhgiachung_number)
        }
        # Tạo đối tượng MailMerge và mở file template
        document = MailMerge(docx_template)

        # Thực hiện mail merge với dữ liệu đã cung cấp
        document.merge(**data)

        output_path = os.path.join('DOCX', username)
        os.makedirs(output_path, exist_ok=True)
        # Lưu file docx đã được mail merge (không bắt buộc, chỉ cần nếu bạn muốn lưu phiên bản đã merge)
        output_docx = os.path.join(output_path, f"{mssv}.docx")
        document.write(output_docx)

        # Chuyển đổi file docx đã merge thành file pdf
        # output_pdf = os.path.join(output_path, f"{mssv}.pdf")
        # convert(output_docx, output_pdf)

        # Đóng đối tượng MailMerge
        document.close()

        return output_docx
    except Exception as e:
        print(e)
        return False
