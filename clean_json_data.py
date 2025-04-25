import json
import os
import glob
from tqdm import tqdm

def clean_json_files():
    """
    Hàm xóa các dòng không cần thiết trong trường content của tất cả file JSON
    trong thư mục petmart_data
    """
    # Danh sách các từ khóa của dòng cần loại bỏ
    unwanted_text = [
        "Chưa có sản phẩm trong giỏ hàng",
        "Quay trở lại cửa hàng",
        "Email của bạn sẽ không được hiển thị",
        "Bình luận*",
        "Tên*",
        "Email*",
        "Nội dung và hình ảnh các bài viết trên",
        "đã được đăng ký bản quyền",
        "DMCA",
        "CC BY-ND",
        "PET MART VIỆT NAM",
        "Giấy phép số",
        "Tên tài khoản hoặc địa chỉ email",
        "Mật khẩu*",
        "Ghi nhớ mật khẩu",
        "Đăng nhập",
        "Quên mật khẩu",
        "Các trường bắt buộc được đánh dấu",
        "0106683363"
    ]
    
    # Lấy danh sách tất cả file JSON trong thư mục petmart_data
    json_files = glob.glob("petmart_data/*.json")
    print(f"Tìm thấy {len(json_files)} file JSON để xử lý")
    
    # Thống kê
    total_lines_removed = 0
    total_files_processed = 0
    
    # Xử lý từng file JSON
    for json_file in tqdm(json_files, desc="Đang xử lý file"):
        try:
            # Đọc file JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Lấy nội dung
            content = data.get("content", [])
            original_length = len(content)
            
            # Lọc nội dung, loại bỏ các dòng không mong muốn
            filtered_content = []
            for line in content:
                # Kiểm tra xem dòng có chứa bất kỳ từ khóa không mong muốn nào không
                should_keep = True
                for unwanted in unwanted_text:
                    if unwanted in line:
                        should_keep = False
                        break
                
                # Nếu dòng không chứa từ khóa không mong muốn, giữ lại
                if should_keep:
                    filtered_content.append(line)
            
            # Cập nhật nội dung đã lọc
            data["content"] = filtered_content
            
            # Ghi lại file JSON đã được làm sạch
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Cập nhật thống kê
            lines_removed = original_length - len(filtered_content)
            total_lines_removed += lines_removed
            total_files_processed += 1
            
            print(f"File {os.path.basename(json_file)}: Đã xóa {lines_removed} dòng")
            
        except Exception as e:
            print(f"Lỗi khi xử lý file {json_file}: {str(e)}")
    
    # Hiển thị thống kê tổng hợp
    print(f"\nĐã xử lý {total_files_processed} file JSON")
    print(f"Tổng số dòng đã xóa: {total_lines_removed}")
    print("Quá trình làm sạch dữ liệu hoàn tất!")

if __name__ == "__main__":
    clean_json_files() 