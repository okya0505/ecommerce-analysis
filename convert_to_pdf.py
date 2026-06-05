from markdown_pdf import MarkdownPdf, Section

# 1. 读取你的 markdown 文件内容
with open('report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 2. 创建一个 PDF 转换器实例
pdf = MarkdownPdf()

# 3. 将读取到的全部内容作为一个"章节"添加到 PDF 中
#    toc=False 表示不为这个单独的章节生成目录，避免不必要的麻烦
pdf.add_section(Section(md_content, toc=False))

# 4. 保存为 PDF 文件
pdf.save('电商数据分析报告.pdf')