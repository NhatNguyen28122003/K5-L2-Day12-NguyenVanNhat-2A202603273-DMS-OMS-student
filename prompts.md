# Khai báo dùng AI — Nguyễn Văn Nhất

Nhắc lại: không đưa ảnh cabin hay ảnh tài xế (kể cả ảnh chụp màn hình) cho bất kỳ công cụ AI nào. Trong cả buổi, AI **không** được xem ảnh: AI chỉ đọc tài liệu trong repo, file export (`annotations.xml`, chỉ có tọa độ và thuộc tính) và kết quả `cabin_check`.

| # | Công cụ | Bạn hỏi gì (tóm tắt) | Bạn dùng kết quả thế nào | Bạn có kiểm lại không? Bằng gì? |
|---|---|---|---|---|
| 1 | Claude Code (Claude Opus 5.5) | Sắp xong bài thì làm gì tiếp, cần nộp những gì | Lập danh sách việc còn lại theo SUBMISSION, CHECKPOINTS và RUBRIC | Có, đối chiếu với SUBMISSION.md |
| 2 | Claude Code | Mình gán thành 2 task (OMS và DMS) thì làm sao có 1 file `export_final.zip` 22 ảnh | AI viết `scripts/merge_exports.py` (chỉ dùng thư viện chuẩn) để gộp `oms.zip` + `dms.zip` và tách S09–S10 ra `export_extra.zip` | Có: chạy `cabin_check --expect 22` và `--expect 4`; `python -m zipfile -l` cho thấy chỉ có `annotations.xml` |
| 3 | Claude Code | Chạy `cabin_check` cho Checkpoint A, B, lần cuối và phần mở rộng; giải thích các lỗi và cảnh báo | Sửa trên CVAT: ghế S02_rgb, S04_rgb, cờ mắt D01 | Có, chạy lại `cabin_check` sau mỗi lần export |
| 4 | Claude Code | Các lệnh để mình tự chạy (gộp, check, diff, v2) | Tự chạy các lệnh trong PowerShell | Có, đọc file `check_*.txt` |
| 5 | Claude Code | Review chéo thay bạn ghép cặp (**coach cho phép**). AI đọc XML export, đối chiếu với Guideline Cabin v1.0, so box giữa ảnh rgb và ir của cùng cảnh | AI soạn `disagreement_log.csv` (16 dòng). Mình xét từng dòng trên CVAT rồi đổi verdict: giữ `hand` S01/S07_ir, giữ `object` D##, giữ điểm mắt D05, không vẽ `face` ở S01/S07 vì không thấy mặt | Có, mở từng ảnh trên CVAT. AI không xem ảnh nên mọi kết luận về thứ nhìn thấy là của mình |
Ghi chú: các chỗ khác với GUIDE bản repo (`occupied = yes`, `object` trên D##, `hand` trên S##) là do mình làm theo hướng dẫn trong buổi, không phải do AI đề xuất. Chi tiết ở `self_review.md` mục 4.
