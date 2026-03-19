import markdown
import os
import glob
import sys

def get_style():
    return """
    <style>
        body {
            font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            background-color: #f9f9f9;
        }
        .container {
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1 { color: #2c3e50; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { color: #2c3e50; margin-top: 30px; border-left: 5px solid #2c3e50; padding-left: 15px; }
        h3 { color: #34495e; margin-top: 25px; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #fafafa; }
        .so-what {
            background-color: #e8f4fd;
            border-left: 5px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            font-weight: bold;
        }
        .footer { margin-top: 50px; font-size: 0.9em; color: #7f8c8d; text-align: center; }
        a { color: #3498db; text-decoration: none; }
        a:hover { text-decoration: underline; }
        @media print {
            body { background-color: #fff; padding: 0; }
            .container { box-shadow: none; padding: 0; }
            .no-print { display: none; }
        }
    </style>
    """

def convert_md_to_html(md_file_path):
    html_file_path = md_file_path.replace('.md', '.html')
    title = os.path.basename(md_file_path).replace('.md', '').replace('_', ' ')

    with open(md_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Markdown変換
    html_content = markdown.markdown(text, extensions=['extra', 'tables', 'toc'])
    
    # So What? の強調
    html_content = html_content.replace('<strong>So What?:', '<div class="so-what"><strong>So What?:')
    html_content = html_content.replace('</strong></p>', '</strong></div>')

    full_html = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        {get_style()}
    </head>
    <body>
        <div class="container">
            {html_content}
            <div class="footer">
                &copy; 2026 NAMINORI Data Science Team. Generated from {os.path.basename(md_file_path)}.
            </div>
        </div>
    </body>
    </html>
    """

    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"Converted: {md_file_path} -> {html_file_path}")

def run_conversion(root_dir):
    search_patterns = [
        os.path.join(root_dir, 'analysis/**/REPORT_*.md'),
        os.path.join(root_dir, 'analysis/**/FINAL_REPORT_*.md'),
        os.path.join(root_dir, 'analysis/INDEX.md'),
        os.path.join(root_dir, 'analysis/PROJECT_SPECIFIC_RULES.md'),
        os.path.join(root_dir, 'analysis/REVIEW_LOG.md'),
        os.path.join(root_dir, 'analysis/analysis_plan.md')
    ]
    
    found_files = []
    for pattern in search_patterns:
        found_files.extend(glob.glob(pattern, recursive=True))
    
    if not found_files:
        print(f"No markdown reports found in {root_dir}")
    else:
        for md_file in found_files:
            convert_md_to_html(md_file)
        print(f"Total {len(found_files)} files processed.")

if __name__ == "__main__":
    # utils/report_generator.py から見て親ディレクトリ（プロジェクトルート）を取得
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    run_conversion(root_dir)
