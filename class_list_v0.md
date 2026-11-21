# Danh sách lớp v0 — Nguyễn Văn Nhật · G02

Viết tiếp từ slide 54 bài giảng. Mỗi lớp trả lời: **model cần nhận ra cái này để làm gì?**

## DMS (8 lớp)

| # | Lớp / thuộc tính | Giá trị | Để làm gì (chức năng DMS) | Nhìn thấy được trên IR? |
|---|---|---|---|---|
| 1 | `eye_state` (mỗi mắt) | open / closed / unknown | Phát hiện buồn ngủ: đo tỉ lệ thời gian mắt nhắm (PERCLOS), mắt nhắm lâu thì cảnh báo | Có, trừ khi kính phản xạ đèn LED (D04, D06: `unknown`) |
| 2 | `gaze_zone` | road / mirror_l / mirror_r / mirror_c / cluster / center / lap / other | Phát hiện mất tập trung: nhìn ngoài `road` quá ngưỡng (ví dụ > 2 s) thì cảnh báo; xe tự lái dùng để biết tài xế có sẵn sàng nhận lại lái không | Có, dựa vào hướng đầu và mắt; kém khi mắt `unknown` |
| 3 | `face` + `face13` (13 điểm) | box + 13 điểm, cờ occluded/outside | Đầu vào cho ước lượng hướng đầu (yaw/pitch), độ mở mắt và miệng; theo dõi tài xế qua các khung | Có, NIR cho ảnh mặt ổn định cả ngày lẫn đêm |
| 4 | `glasses` | none / clear / sun / unknown | Biết khi nào trạng thái mắt không đáng tin (kính phản xạ, kính râm) để hạ độ tin cậy cảnh báo buồn ngủ thay vì báo sai | Một phần: thấy gọng, nhưng kính râm có thể trông trong suốt trên NIR |
| 5 | `hand` + `on_wheel` | left / right theo người · yes / no / unknown | Phát hiện rời tay khỏi vô lăng; khi xe tự lái trả quyền điều khiển thì kiểm tay đã đặt lại vô lăng chưa | Có (hình dạng); khó khi tay khuất sau vô lăng |
| 6 | `phone` + `state` | held / mounted / lap | Phát hiện dùng điện thoại khi lái (cầm áp tai, nhắn tin trên đùi) để cảnh báo | Một phần: máy tối khó tách khỏi tay và tóc; chỉ gán khi thấy cạnh máy (D02) |
| 7 | `person.seatbelt` (tài xế) | worn_correct / worn_incorrect / not_worn / unknown | Nhắc thắt dây an toàn; phát hiện thắt sai (dưới nách, sau lưng) làm túi khí và dây kém hiệu quả | Có nếu dải đai tương phản với áo; áo tối thì thường `unknown` |
| 8 | `frame_meta.camera_blocked` | yes / no | Biết camera bị che (tay, khăn, vật) để báo lỗi hệ thống thay vì kết luận sai rằng tài xế ổn | Có |

## OMS (8 lớp)

| # | Lớp / thuộc tính | Giá trị | Để làm gì (chức năng OMS) | Nhìn thấy được trên IR? |
|---|---|---|---|---|
| 1 | `person` + `seat` | driver / front_passenger / rear_left / rear_middle / rear_right | Đếm người theo ghế: nhắc thắt dây cho ghế có người, chỉnh điều hòa và âm thanh theo vùng | Có (hình dạng người) |
| 2 | `infant_seat` + `facing` | rear / front, theo ghế | Nhắc quên trẻ trong xe; ghế em bé quay về sau ở ghế trước thì **phải tắt túi khí** ghế đó | Có (hình dạng nôi) |
| 3 | `child_seat` + `occupied` | no / unknown / yes (theo schema cập nhật) | Nhắc quên trẻ; chỉnh túi khí và lực căng dây theo loại ghế | Có (hình dạng); khó biết bên trong có gì vì mất màu (S04) |
| 4 | `object` + `type` | bag / box / cup / other, theo ghế | Nhắc quên đồ khi rời xe; phân biệt vật với người để không báo "chưa thắt dây" cho một chiếc túi | Có (hình dạng); không phân biệt được bằng màu |
| 5 | `person.seatbelt` (từng ghế) | worn_correct / worn_incorrect / not_worn / unknown | Nhắc thắt dây cho hành khách ghế sau, nơi cảm biến khóa đai thường không có | Có nếu đai tương phản; dễ chìm trong bóng tối |
| 6 | `face` (box, hành khách) | box | Biết hành khách quay mặt về đâu; xác định người lớn hay trẻ em theo kích thước để chỉnh túi khí | Có khi mặt hướng về camera; không vẽ khi không thấy mặt (S01, S07) |
| 7 | Ghế trống (đếm theo ghế) | số ghế trống mỗi khung | Phân biệt "không có ai" với "model bỏ sót"; đếm ghế còn trống | Có |
| 8 | Tư thế ngồi lệch (đề xuất cho v1.x) | in_position / out_of_position | Người ngồi sát túi khí hoặc gác chân lên táp-lô thì túi khí bung có thể gây thương tích, cần giảm lực hoặc tắt | Có (hình dạng cơ thể) |

## 2 câu hỏi leo thang

Câu hỏi bạn muốn hỏi người viết guideline (hoặc khách hàng) vì guideline v1.0 chưa trả lời. Mỗi câu kèm **tên khung** làm ví dụ.

1. Câu hỏi: Khi `child_seat` có thứ gì đó bên trong, gán `occupied = yes` (như schema vừa cập nhật) hay vẽ thêm box riêng cho thứ bên trong (như GUIDE 4.8)? Nếu vẽ box riêng thì đó là `object` hay `person`, khi GUIDE §3 ghi bộ SVIRO không có trẻ em ngồi? GUIDE/RUBRIC và `cabin_schema.py` đang nói khác nhau.
   Khung ví dụ: G02 S03_rgb / S03_ir (ghế `rear_middle`), cùng loại với S05, S06, S08.
   Bạn tạm gán thế nào và vì sao: tạm gán `occupied = yes`, không thêm box bên trong, vì người ra đề đã cho phép `yes` trong schema. Đã ghi chú trong `check_final.txt` và `self_review.md`.

2. Câu hỏi: Trên ảnh OMS, khi tay hành khách thấy rõ, có gán `hand` không? Bảng 4.1 ghi `hand` dùng cho DMS, còn 4.3 ghi "chỉ gán label bảng 4.1 ghi cho phần đó". Tương tự, trên ảnh DMS có gán `object` cho đồ để ở ghế phụ không, khi 4.2 ghi DMS không vẽ `object` nhưng trong buổi được phổ biến là phải gán?
   Khung ví dụ: G02 S07_ir (2 tay người ngồi `rear_middle`, bản rgb không gán tay); G02 D02 (túi và một vật ở `front_passenger`).
   Bạn tạm gán thế nào và vì sao: giữ `hand` trên S01 và S07_ir vì tay thấy rõ; giữ `object` trên D02–D06 theo hướng dẫn trong buổi. Cả hai đã ghi trong `self_review.md` để coach xác nhận và cập nhật guideline v1.x.
