# BUG REPORT: Bệnh về mắt không hiển thị trong Admin Detail và Export XLSX

## 🔴 **PRIORITY: HIGH** 
**Ảnh hưởng:** Dữ liệu quan trọng không hiển thị cho admin và báo cáo

---

## 📋 **SUMMARY**
- **Done.html**: Hiển thị đúng "viễn thị, loạn thị" 
- **Admin detail**: Hiển thị "Chưa có thông tin"
- **Export XLSX**: Cột "Bệnh về mắt" trống

## 🔍 **ROOT CAUSE ANALYSIS**
Done.html đọc từ **localStorage/cache**, Admin+Export đọc từ **database** → Hai nguồn dữ liệu khác nhau.

---

## 📝 **STEPS TO REPRODUCE**
1. Học sinh submit form với bệnh về mắt: "Viễn thị, Loạn thị"
2. Vào `done.html` → ✅ Hiển thị đúng
3. Admin → Chi tiết học sinh → ❌ "Chưa có thông tin"  
4. Export XLSX → ❌ Cột trống

---

## 🎯 **EXPECTED vs ACTUAL**

| Trang | Expected | Actual | Status |
|-------|----------|---------|---------|
| Done.html | "Viễn thị, Loạn thị" | "Viễn thị, Loạn thị" | ✅ OK |
| Admin Detail | "Viễn thị, Loạn thị" | "Chưa có thông tin" | ❌ FAIL |
| Export XLSX | "Viễn thị, Loạn thị" | (trống) | ❌ FAIL |

---

## 🔧 **DEBUG CHECKLIST (FOR DEV)**

### Step 1: Check API Response
```javascript
// F12 Console → gõ:
fetch('/api/student/[ID]').then(r=>r.json()).then(d=>console.log('API Response:', d.eye_diseases, d.eyeDiseases))
```
**Expected:** Có giá trị bệnh về mắt  
**If empty:** Database bị ghi rỗng

### Step 2: Check Form Submit Payload  
```
Network Tab → Submit form → Check POST payload
Tìm field: eyeDiseases / eye_diseases
```
**Expected:** Payload chứa bệnh về mắt  
**If missing:** Frontend không gửi đúng key

### Step 3: Check LocalStorage
```javascript
// F12 Console → gõ:
console.log('LocalStorage:', JSON.parse(localStorage.getItem('healthFormData') || '{}').eyeDiseases)
```
**Expected:** localStorage có giá trị  
**Meaning:** Done.html đọc từ localStorage, không phải DB

### Step 4: Check Database Schema
```javascript
// F12 Console → gõ:
fetch('/api/debug/schema').then(r=>r.json()).then(d=>console.log('DB Schema:', d))
```
**Expected:** `has_eye_diseases_column: true` + sample data  
**If false:** Schema thiếu cột

### Step 5: Check Admin Parsing
```
Admin detail → F12 Console → tìm log:
"Eye diseases data: {eyeDiseases: ..., eye_diseases: ..., selected: ...}"
```
**Expected:** Có dữ liệu nhưng parse sai  
**If all empty:** DB thực sự rỗng

---

## 🚨 **LIKELY CAUSES & FIXES**

### Cause 1: Frontend không gửi đúng key (Probability: 60%)
**Symptom:** Payload thiếu hoặc sai tên field  
**Fix:** Đảm bảo form gửi `eyeDiseases` hoặc `eye_diseases` đúng với backend expect

### Cause 2: Backend ghi đè rỗng khi update (Probability: 30%)
**Symptom:** Payload có nhưng DB vẫn rỗng  
**Fix:** Sửa logic `save_student` - không ghi đè field nếu payload empty

### Cause 3: Data format mismatch (Probability: 10%)
**Symptom:** DB có dữ liệu nhưng admin không parse được  
**Fix:** Đồng nhất format JSON array vs comma-separated string

---

## 📸 **SCREENSHOTS**
- [ ] Done.html hiển thị đúng
- [ ] Admin detail hiển thị sai  
- [ ] Export XLSX trống
- [ ] F12 Console logs
- [ ] Network payload

---

## ⚡ **QUICK TEMP FIX** 
Nếu cần fix gấp: Sửa admin detail đọc từ localStorage như done.html (tạm thời)

## 🎯 **LONG TERM FIX**
1. DB làm single source of truth
2. LocalStorage chỉ cache UI
3. Đồng nhất format lưu trữ
4. Admin + Export + Done đều đọc từ DB

---

## 👥 **ASSIGNMENT**
- **Frontend Dev:** Check form submit payload & localStorage sync
- **Backend Dev:** Check save_student logic & data format  
- **QA:** Verify fix across all 3 interfaces

**ETA:** 1-2 days
