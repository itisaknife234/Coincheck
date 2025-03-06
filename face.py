import streamlit as st
import numpy as np
import cv2
from PIL import Image

# 얼굴 인식용 Cascade Classifier 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Streamlit로 이미지 업로드 받기
st.title("얼굴 모자이크 처리기")
uploaded_file = st.file_uploader("이미지 파일을 업로드하세요", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    # 업로드된 이미지를 OpenCV에서 사용할 수 있도록 변환
    img = Image.open(uploaded_file)
    img = np.array(img)
    
    # BGR로 변환 (Streamlit은 RGB 형식으로 이미지를 표시하지만, OpenCV는 BGR 형식으로 처리)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # 이미지를 흑백으로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 얼굴마다 모자이크 처리
    for (x, y, w, h) in faces:
        face_img = img[y:y+h, x:x+w]
        small_face = cv2.resize(face_img, (w//20, h//20), interpolation=cv2.INTER_LINEAR)
        mosaic_face = cv2.resize(small_face, (w, h), interpolation=cv2.INTER_NEAREST)
        img[y:y+h, x:x+w] = mosaic_face

    # 모자이크 처리된 이미지를 Streamlit에서 표시
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 이미지를 RGB로 변환 (Streamlit에서 출력하기 위함)
    st.image(img, channels="RGB", use_column_width=True)
else:
    st.write("이미지를 업로드해주세요.")
