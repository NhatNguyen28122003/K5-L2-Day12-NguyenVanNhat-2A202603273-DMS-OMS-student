# Tự đánh giá — Nguyễn Văn Nhất · G02

## 1. Tự rà soát 4 cảnh

Nghỉ tay 1 phút, mở lại bài của mình, chọn 4 ảnh (2 S##, 2 D##), đọc như người lạ.

Loại lỗi: `seat_flip`, `wrong_class`, `guess`, `box`, `missing`, `extra`, `lr_flip` (trái/phải mặt), `flag` (thiếu cờ điểm), `ok`.

| Ảnh | Đối tượng | Loại lỗi | Ghi chú | Đã sửa? |
|---|---|---|---|---|
| S02_rgb | `child_seat` | `seat_flip` | Bản đầu ghi `rear_right`, trùng ghế với `infant_seat`. S02_ir cùng cảnh ghi `rear_left`. Ghế trẻ em nằm bên phải ảnh nên là `rear_left` (camera nhìn về sau, trái ảnh = phải xe) | Có, sửa thành `rear_left` |
| S04_rgb | `child_seat` | `seat_flip` | Bản đầu ghi `seat = driver`. SVIRO chỉ nhìn hàng ghế sau, ghế nằm giữa ảnh nên là `rear_middle` | Có, sửa thành `rear_middle` |
| D01 | `face` + `face13` | `flag` | Bản đầu ghi cả 2 mắt `unknown` nhưng không điểm `*_eye_*` nào có cờ. Xem lại: mắt trái thấy khe mắt nên `open`; mắt phải bị che nên `unknown` và bật `occluded` cho 4 điểm `right_eye_*` | Có |
| D05 | `person` | `box` | Box `person` tràn khỏi ảnh (y2 = 1143, ảnh cao 1024) và không bao hết box `face`. D06 cũng bị tương tự | Đang sửa (export_final_v2) |

## 2. Lỗi mình lặp lại nhiều nhất hôm nay

Lỗi: ảnh `_rgb` và `_ir` của cùng một cảnh bị gán **không nhất quán** (ghế khác nhau ở S02 và S04, `occupied` khác nhau ở S04, box cùng một vật lệch nhau ở S07 và S01).

Vì sao mình mắc: mình gán từng ảnh riêng lẻ theo thứ tự trong task, ảnh rgb và ảnh ir của cùng cảnh không nằm cạnh nhau, nên không đối chiếu lại. Ở ảnh rgb mình dễ đọc ghế theo ảnh thay vì theo xe.

Lần sau tránh bằng cách:
- Gán xong một cặp `S##_rgb` / `S##_ir` thì mở cả hai, so từng box: cùng label, cùng `seat`, vị trí gần giống nhau.
- Trước khi gán mỗi ảnh OMS, nói to "trái ảnh là `rear_right`" (Guideline 4.3 bước 2, 4.4-3).
- Vẫn gán từng ảnh dựa trên những gì thấy trên chính ảnh đó (4.4-1). Đối chiếu là để bắt lỗi ghế/box, không để chép thuộc tính từ ảnh kia sang.

## 3. Ghi chú về disagreement_log

Review chéo làm với AI (Claude), được coach cho phép. AI chỉ đọc file XML export, không xem ảnh.

Một dòng bạn của mình đúng và mình sai: D05 và D06, box `person` tràn khỏi ảnh và không bao hết mặt tài xế (4.4-5). Mình học được: với ảnh D01 xoay 90°, người tài xế nằm ngang nên mình kéo box theo cảm giác và kéo quá mép ảnh. Hộp phải sát phần cơ thể thấy được, nằm trong ảnh, và phải chứa box `face` của chính người đó.

## 4. Các điểm khác với GUIDE bản repo

Những chỗ dưới đây mình làm theo hướng dẫn được phổ biến trong buổi, khác với chữ trong GUIDE/RUBRIC của repo:

- `child_seat occupied = yes`: người ra đề cho phép và đã cập nhật `scripts/cabin_schema.py` (commit `f7b6f48`). GUIDE 4.8 và RUBRIC vẫn ghi không dùng `yes`.
- `object` trên ảnh D02 (D02–D06): được phổ biến là phải gán. GUIDE 4.2 ghi DMS không vẽ `object`.
- `hand` trên ảnh S01 và S07_ir: tay thấy rõ nên mình giữ. Bảng 4.1 ghi `hand` dùng cho DMS. Mình đã hỏi lại coach.
- S01 và S07: không vẽ box `face` cho người lớn vì không thấy mặt (4.5).

## 5. Ghi chú quy trình

- Mình gán thành 2 task CVAT (OMS 20 ảnh gồm S09–S10, DMS 6 ảnh), rồi gộp export bằng `scripts/merge_exports.py`: `export_final.zip` có 22 ảnh cốt lõi, `export_extra.zip` có S09–S10.
- `check_cpA.txt` và `check_cpB.txt` chạy trên bản export cuối (lọc bằng `--only`), không phải bản tại đúng giờ checkpoint.
