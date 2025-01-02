# app.py
from flask import Flask, render_template, request, make_response, session
from search_rs import search_rs_process
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个密钥用于会话加密
#DB_FILE="/data/users/liteng/my_project/optimal_wgs_genotype_search/dbsnp_155_5cols_format_sorted.txt.gz"
SEARCH_RS_DB_FILE=os.environ.get("SEARCH_RS_DB_FILE")

@app.route('/', methods=['GET', 'POST'])
def index():
    snp_info_list = session.get('snp_info_list', [])
    error_message = None

    if request.method == 'POST':
        rsids = request.form.get('rsids')
        file = request.files.get('file')

        if not rsids and not file:
            error_message = "请填写RSIDs或上传文件。"
        elif rsids:
            rsids = rsids.splitlines()
        elif file:
            rsids = file.read().decode('utf-8').splitlines()
        snp_info_list = search_rs_process(SEARCH_RS_DB_FILE, rsids, tabix_path="tabix")
        session['snp_info_list'] = snp_info_list

    if request.args.get('download'):
        if snp_info_list:
            response = make_response('\n'.join([f"{snp_info['rsid']}\t{snp_info['chrom']}\t{snp_info['position']}\t{snp_info['ref']}\t{snp_info['alt']}" for snp_info in snp_info_list]))
            response.headers["Content-Disposition"] = "attachment; filename=snp_info.txt"
            return response
        else:
            error_message = "没有SNP信息可供下载。"

    return render_template('index.html', snp_info_list=snp_info_list, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)