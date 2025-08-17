# CHECKLIST DEBUG - BỆNH VỀ MẮT

## Bước 1: Kiểm tra Debug Endpoint
```
Mở trình duyệt → F12 → Console → gõ:
fetch('/api/debug/schema').then(r=>r.json()).then(d=>console.log('SCHEMA:', d))

Mong đợi: 
- Has eye_diseases column: true
- Sample data có giá trị eye_diseases

Nếu false/null → DB bị lỗi schema
```

## Bước 2: Kiểm tra Admin Console Log
```
Vào admin.html → Mở Chi tiết học sinh có bệnh về mắt → F12 Console

Tìm log: "Eye diseases data: {eyeDiseases: ..., eye_diseases: ..., selected: ...}"

Nếu tất cả đều '' hoặc null → DB đã bị ghi rỗng
Nếu có dữ liệu → vấn đề ở parseArrayField
```

## Bước 3: So sánh Done.html vs Admin
```
Vào done.html → F12 Console → gõ:
console.log('LocalStorage:', JSON.parse(localStorage.getItem('healthFormData') || '{}'))

So sánh eyeDiseases ở localStorage vs Admin detail:
- Done có, Admin không → DB bị ghi rỗng
- Cả hai đều không → form chưa từng submit
- Admin có, Done không → localStorage cũ
```

## Bước 4: Test Flow Submit
```
1. Vào form học sinh → Chọn bệnh về mắt → Submit
2. Ngay sau submit, check:
   - Done.html hiển thị đúng không
   - Admin detail hiển thị đúng không  
   - F12 Console gõ: fetch('/api/debug/simple').then(r=>r.json()).then(d=>console.log(d))

Nếu Done có, Admin không → logic save_student ghi rỗng
```

## Bước 5: Kiểm tra Export Log
```
Admin → Export XLSX → Check server log hoặc F12 Network tab

Tìm request /api/export-xlsx → Response headers
Nếu file rỗng nhưng request thành công → DB không có dữ liệu
```

## Bước 6: Check Raw Database (nếu cần)
```
F12 Console → gõ:
fetch('/api/student/201').then(r=>r.json()).then(s=>console.log('RAW STUDENT:', s.eye_diseases, s.eyeDiseases))

(Thay 201 = ID học sinh có bệnh về mắt)
```

---

# KẾT QUẢ DỰ KIẾN

## Trường hợp 1: DB bị ghi rỗng
```
- Bước 1: Has eye_diseases = true, sample = null/''
- Bước 2: Admin log = '', '', ''  
- Bước 3: localStorage có, admin không
→ Nguyên nhân: save_student ghi đè rỗng
```

## Trường hợp 2: Frontend không gửi đúng key
```
- Bước 1: Has eye_diseases = true, sample có dữ liệu
- Bước 2: Admin log có dữ liệu
- Bước 4: Submit → Admin detail vẫn rỗng
→ Nguyên nhân: mismatch key eyeDiseases vs eye_diseases
```

## Trường hợp 3: parseArrayField lỗi
```
- Bước 1: OK
- Bước 2: selected có dữ liệu, nhưng parseArrayField return 'Chưa có thông tin'
→ Nguyên nhân: format JSON vs comma-separated
```

---

# ACTION PLAN (ƯU TIÊN)

1. **Nếu Trường hợp 1**: Sửa save_student - không ghi rỗng khi payload empty
2. **Nếu Trường hợp 2**: Đồng nhất key frontend/backend  
3. **Nếu Trường hợp 3**: Fix parseArrayField handle JSON format

**Copy đoạn debug này → paste vào Console → báo kết quả → tôi sẽ sửa đúng chỗ!**
