# Workflow Summary for AI Smart Doctor Chatbot using FAISS:

## โหลดโมเดล Sentence Transformer

* ใช้โมเดล sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 ที่รองรับหลายภาษา รวมถึงภาษาไทย
* แปลงข้อความเป็นเวกเตอร์ (Embedding) เพื่อใช้ในการค้นหาคำตอบ

## โหลดและเตรียมข้อมูลจาก CSV

* โหลดไฟล์ 1-10001.csv ด้วย pandas
* ตรวจสอบว่ามีคอลัมน์ที่จำเป็น ได้แก่ "qtype", "Question", และ "Answer"
* รวมคอลัมน์ "qtype" และ "Question" เป็น "combined_info" เพื่อให้การค้นหามีข้อมูลบริบทมากขึ้น

## สร้างและจัดเก็บ Embeddings

* แปลง "combined_info" เป็นเวกเตอร์โดยใช้โมเดล SBERT
* จัดเก็บเวกเตอร์ลงใน FAISS IndexFlatL2 เพื่อให้สามารถค้นหาคำถามที่ใกล้เคียงได้อย่างมีประสิทธิภาพ

## ค้นหาคำตอบจาก FAISS

* เมื่อผู้ใช้ส่งคำถามเข้ามา ระบบจะทำการแปลงคำถามเป็นเวกเตอร์
* FAISS ค้นหาคำถามที่ใกล้เคียงที่สุด (Top 3) จากฐานข้อมูล
* คืนค่าคำตอบที่เกี่ยวข้อง โดยไม่มีการใช้ threshold ในการกรอง

## Flask Web Application

* Route "/": แสดงหน้าเว็บหลัก (index.html)
* API "/ask":
  * รับ JSON ที่มี "question"
  * ใช้ retrieve_context() เพื่อค้นหาคำตอบ
  * คืนค่าคำตอบในรูปแบบ JSON

## Deployment

* รัน Flask App บน 0.0.0.0:5000 โดยเปิด debug=True เพื่อใช้ในระหว่างพัฒนา

![image](https://github.com/user-attachments/assets/8f4451de-8252-416a-9d86-609053e25d3a)
