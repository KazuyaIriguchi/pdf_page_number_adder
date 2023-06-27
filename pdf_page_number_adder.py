import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os
import argparse


def create_page_number_overlay(page_number, total_pages, position, page_width, page_height):
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    margin = 50  # Margin from the edge
    x, y = 0, 0
    page_width = float(page_width)
    page_height = float(page_height)
    if position == 'br':
        x, y = page_width - margin, margin
    elif position == 'tr':
        x, y = page_width - margin, page_height - margin
    elif position == 'bl':
        x, y = margin, margin
    elif position == 'tl':
        x, y = margin, page_height - margin
    c.drawString(x, y, f"{page_number}/{total_pages}")
    c.save()
    packet.seek(0)
    return PyPDF2.PdfReader(packet)


def add_page_numbers(input_pdf, position='br', offset=0):
    input_reader = PyPDF2.PdfReader(input_pdf)
    pdf_writer = PyPDF2.PdfWriter()

    for i in range(len(input_reader.pages)):
        page = input_reader.pages[i]
        page_number = i + 1 + offset
        total_pages = len(input_reader.pages) + offset
        page_width = page.mediabox.width
        page_height = page.mediabox.height
        overlay = create_page_number_overlay(page_number, total_pages, position, page_width, page_height)
        page.merge_page(overlay.pages[0])
        pdf_writer.add_page(page)
    output = io.BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    print("Page numbers added successfully.")
    return output


def export_pdf(output_pdf, pdf_data):
    """PDFに出力

    Args:
        output_pdf (str): 出力ファイル名
        pdf_data (BytesIO): PDFページオブジェクト
    """
    # 出力PDFファイルに保存
    with open(output_pdf, 'wb') as f:
        f.write(pdf_data.getvalue())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add page numbers to a PDF file.')

    # 入力PDFファイル名
    parser.add_argument('input_pdf', type=str, help='Input PDF file name')
    # 出力PDFファイル名 (オプション)
    parser.add_argument('-o', '--output_pdf', type=str, default=None, help='Output PDF file name (optional)')
    # テキストの位置 (オプション)
    parser.add_argument('-p', '--position', type=str, choices=['br', 'tr', 'bl', 'tl'], default='tr', help='Position of the page numbers (bottom-right, top-right, bottom-left, top-left).')
    # ページ番号のオフセット (オプション)
    parser.add_argument('--offset', type=int, default=0, help='Offset for the page numbers (optional)')

    # 引数を解析
    args = parser.parse_args()

    # 関数を呼び出してPDFにページ番号を追加
    output = add_page_numbers(input_pdf=args.input_pdf, position=args.position, offset=args.offset)
    output_pdf = args.output_pdf
    if output_pdf is None:
        # 出力PDFファイル名を設定
        base_name, _ = os.path.splitext(args.input_pdf)
        output_pdf = f"{base_name}_edited.pdf"
    # エクスポート
    export_pdf(output_pdf, output)
