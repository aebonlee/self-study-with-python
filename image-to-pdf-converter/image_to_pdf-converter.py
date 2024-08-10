import os
from PIL import Image
from tqdm import tqdm
from datetime import datetime
from PyPDF2 import PdfMerger
from tkinter import Tk, simpledialog
from tkinter.filedialog import askdirectory

def images_to_pdf(folder_path, quality):
    # 폴더 내의 이미지 파일 리스트 가져오기
    image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg'))]
    
    # 이미지 파일 리스트를 오름차순으로 정렬
    image_files.sort()
    
    # 현재 시간 가져오기
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 폴더 이름 가져오기
    folder_name = os.path.basename(os.path.normpath(folder_path))
    
    # 상위 폴더 경로 가져오기
    parent_folder = os.path.dirname(folder_path)
    
    # PDF 파일 이름 생성
    output_pdf = os.path.join(parent_folder, f"{folder_name}_{current_time}.pdf")
    
    # PDF 병합 객체 생성
    merger = PdfMerger()
    
    # 이미지 객체 리스트 생성 및 PDF로 변환
    pdf_files = []
    for image_file in tqdm(image_files, desc="Processing images"):
        image = Image.open(image_file)
        pdf_path = image_file.replace(image_file.split('.')[-1], 'pdf')
        image.save(pdf_path, "PDF", quality=quality)
        merger.append(pdf_path)
        pdf_files.append(pdf_path)
    
    # 병합된 PDF 저장
    with tqdm(total=len(image_files), desc="Saving PDF") as pbar:
        merger.write(output_pdf)
        pbar.update(len(image_files))
    
    merger.close()
    print(f'PDF 파일이 {output_pdf}에 저장되었습니다.')
    
    # 개별 PDF 파일 삭제
    for pdf_file in pdf_files:
        os.remove(pdf_file)
    print('개별 PDF 파일이 삭제되었습니다.')

# 폴더 경로 선택 및 이미지 품질 입력
def select_folder_and_quality():
    root = Tk()
    root.withdraw()  # Tkinter 창 숨기기
    folder_path = askdirectory(title="폴더를 선택하세요")
    if folder_path:
        quality = simpledialog.askinteger("이미지 품질 입력", "이미지 품질을 입력하세요 (1-100):", initialvalue=100, minvalue=1, maxvalue=100)
        return folder_path, quality
    return None, None

folder_path, quality = select_folder_and_quality()  # 파일 탐색기를 통해 폴더 경로 선택 및 이미지 품질 입력
if folder_path and quality:
    images_to_pdf(folder_path, quality)
else:
    print("폴더를 선택하지 않았거나 이미지 품질을 입력하지 않았습니다.")
