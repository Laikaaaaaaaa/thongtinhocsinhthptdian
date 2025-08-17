# TIN NHẮN CHO DEV TEAM

## 🔥 **BUG URGENT: Bệnh về mắt không hiển thị**

**Hiện tượng:**
- Done.html: ✅ Hiển thị "viễn thị, loạn thị" 
- Admin detail: ❌ "Chưa có thông tin"
- Export XLSX: ❌ Cột trống

**Root cause:** Done đọc localStorage, Admin+Export đọc DB → hai nguồn khác nhau

---

## 🚀 **DEBUG NGAY (5 phút):**

**Bước 1:** ✅ **DONE** - DB có dữ liệu (`has_eye_diseases: true`, 5 samples)

**Bước 2:** Admin detail → F12 Console → tìm log `"Eye diseases data: {...}"`

**Bước 3:** Done.html → F12 Console → gõ:
```js
console.log('LocalStorage:', JSON.parse(localStorage.getItem('healthFormData') || '{}').eyeDiseases)
```

**Bước 4:** Test submit form → check Network payload có field `eyeDiseases`/`eye_diseases` không

---

## 📋 **LIKELY FIXES:**

1. **Frontend không gửi đúng key** khi submit (60% khả năng)
2. **Backend ghi đè rỗng** trong save_student (30% khả năng)  
3. **Admin parse format sai** JSON vs comma-separated (10% khả năng)

---

## ⚡ **TEMP FIX:** Admin đọc localStorage như Done (để khẩn cấp)
## 🎯 **PROPER FIX:** Sync localStorage ↔ DB khi submit thành công

**Assign:** Frontend dev check payload, Backend dev check save logic
**ETA:** 1-2 ngày

**CC:** @frontend-team @backend-team
