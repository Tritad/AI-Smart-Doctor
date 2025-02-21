from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import pandas as pd
import faiss
import numpy as np

app = Flask(__name__)

# โหลดโมเดล SBERT ที่รองรับหลายภาษา (รวมถึงไทย)
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# โหลด CSV
csv_file = "Data_set.csv"

try:
    df = pd.read_csv(csv_file, encoding="ISO-8859-1")  # หรือ "latin-1"
    print(f"✅ CSV โหลดสำเร็จ! มี {len(df)} แถว")
except Exception as e:
    print(f"❌ เกิดข้อผิดพลาดในการโหลด CSV: {e}")
    exit()

# ตรวจสอบว่ามีคอลัมน์ที่ต้องใช้หรือไม่
required_columns = {"qtype", "Question", "Answer"}
if not required_columns.issubset(df.columns):
    raise ValueError(f"CSV ต้องมีคอลัมน์ {required_columns} แต่พบ {set(df.columns)}")

# รวม qtype และ Question เพื่อให้ embedding มีข้อมูลมากขึ้น
df["combined_info"] = df["qtype"].astype(str) + " | " + df["Question"].astype(str)

# แปลงข้อความเป็นเวกเตอร์ (Embedding)
question_embeddings = np.array([model.encode(q) for q in df["combined_info"]])

# สร้าง FAISS index
index = faiss.IndexFlatL2(question_embeddings.shape[1])
index.add(question_embeddings)

# ฟังก์ชันค้นหาคำตอบจาก CSV (ไม่มี threshold)
def retrieve_context(query, top_k=3):
    query_embedding = model.encode(query).reshape(1, -1)  # ทำให้เป็น 2D array
    distances, indices = index.search(query_embedding, top_k)  # ค้นหาผลลัพธ์
    
    # ดึงคำตอบที่เกี่ยวข้องที่สุด โดยไม่ใช้ threshold
    relevant_answers = df.iloc[indices[0]]["Answer"].tolist()

    return relevant_answers if relevant_answers else ["⚠️ No relevant answer found"]

# Route สำหรับหน้าเว็บ
@app.route("/")
def home():
    return render_template("index.html")

# API Endpoint สำหรับรับคำถาม
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    answer = retrieve_context(user_question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
