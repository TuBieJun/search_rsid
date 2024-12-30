# app.py
from flask import Flask, render_template, request, make_response, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个密钥用于会话加密

# 模拟的函数，用于根据rsID获取SNP信息
def get_snp_info(rsid):
    # 这里应该实现根据rsID查询数据库或API获取SNP信息的逻辑
    # 返回一个字典，包含chrom和position等信息
    return {
        "rsid": rsid,
        "chrom": "chr1",
        "position": "105678",
        "ref": "A",
        "alt": "G"
    }

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
            snp_info_list = []
            for rsid in rsids:
                snp_info = get_snp_info(rsid.strip())
                if snp_info:
                    snp_info_list.append(snp_info)
        elif file:
            rsids = file.read().decode('utf-8').splitlines()
            snp_info_list = []
            for rsid in rsids:
                snp_info = get_snp_info(rsid.strip())
                if snp_info:
                    snp_info_list.append(snp_info)

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