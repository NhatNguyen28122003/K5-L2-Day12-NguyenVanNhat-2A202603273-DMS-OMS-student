# TEAM — Ngày 12

Mã bộ ảnh: **G02** · Hình thức: cá nhân

| Họ tên | MSSV | Đã gán đủ 22 ảnh? | Review chéo với (peer diff) | Số dòng disagreement đã xử lý |
|---|---|---|---|---|
| Nguyễn Văn Nhất | 2A202603273 | có (cộng thêm S09–S10 ở phần mở rộng) | AI (Claude), được coach cho phép. AI đọc file XML export và đối chiếu với Guideline Cabin v1.0, không xem ảnh | 16 dòng: 8 `mine`, 2 `peer`, 6 `ambiguous` |

Các ca vẫn chưa thống nhất, cần hỏi coach (ghi tên ảnh + đối tượng):

- G02 S03, S05, S06, S08 · `child_seat`: gán `occupied = yes` theo schema cập nhật, hay vẽ box riêng cho thứ bên trong (GUIDE 4.8)?
- G02 S04_rgb / S04_ir · `child_seat.occupied`: ảnh rgb ghi `unknown`, ảnh ir ghi `yes`.
- G02 S01_ir, S07_ir · `hand`: có gán tay hành khách trên ảnh OMS không (bảng 4.1 ghi `hand` dùng cho DMS)?
- G02 D02–D06 · `object`: được phổ biến là phải gán, nhưng GUIDE 4.2 ghi DMS không vẽ `object`.
- G02 S07 `object`, S01 `infant_seat`: box trên rgb và ir lệch nhau; cần căn lại theo ảnh.
- G02 D03 `eye_right`, D01 `gaze_zone`: cần xem lại trên ảnh.

## Cá nhân

### NguyenVanNhat-2A202603273
- Phần mình làm (ngoài 22 ảnh của mình): tự gán thêm S09–S10 (`export_extra.zip`). Gán thành 2 task CVAT (OMS và DMS) rồi gộp export bằng `scripts/merge_exports.py`. Xét từng dòng review của AI dựa trên ảnh trên CVAT, giữ hoặc sửa nhãn theo những gì nhìn thấy.
- Điều mình học được hôm nay: ghế OMS gọi theo xe (trái ảnh là `rear_right`); hai ảnh rgb và ir của cùng cảnh phải được đối chiếu lại; trên ảnh NIR thật, kính phản xạ đèn LED làm mắt thành `unknown`, không phải `closed`.
