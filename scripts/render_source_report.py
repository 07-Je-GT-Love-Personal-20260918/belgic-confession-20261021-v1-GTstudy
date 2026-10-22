from pathlib import Path
import json, html, shutil
base=Path(__file__).resolve().parent.parent
data=json.loads((base/'qa/source-baseline.json').read_text(encoding='utf8'))
attempt=json.loads((base/'qa/source-recheck.json').read_text(encoding='utf8'))
e=lambda s:html.escape(str(s),quote=True)
summary=data['summary']
out='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>原文核验报告 · GTstudy</title><link rel="stylesheet" href="style.css"></head><body><main class="report-main"><a class="button" href="index.html#sources">← 返回学习站</a><p class="eyebrow">SOURCE VERIFICATION · 发布2026.10.22</p><h1>原文核验报告</h1><div class="callout amber"><h3>两份记录，不能混同</h3><p>原文基线：复用本项目2026年10月21日11:22—11:23（台北时间）的成功核验记录，155个页面、232个正文单元全部相符。本站保存文本已重新计算摘要，与这份记录逐段相符。</p><p>本次批量访问：2026年10月21日晚尝试访问同一批页面，155个连接均超时；没有取得可比较正文，因此不能声称本次又实时核对成功，也不能把232个未证实单元称为232处文本改动。</p><p>本次另外通过网页检索服务抽查了三大信经、比利时第1与36条、目录及相关导言。这些抽查不代替232段全部实时复核。下面的相符数字及逐条表格属于成功基线，非本次连接失败的结果。</p></div><p>比较方法只忽略Unicode布局空白，保留用字、标点、脚注与段号。</p><div class="report-summary">'''
for name,key in [('正文单元','total_sections'),('相符单元','matched'),('差异或未证实','differences'),('唯一来源页面','unique_sources'),('HTTP成功','sources_ok')]: out+=f'<p>{name}<br><b>{summary[key]}</b></p>'
out+='</div><p>方法：基线按原站正文容器抽取段落与有序列表，逐节与保留的中文译文比对；每个来源记录HTTP状态、原始响应摘要，每个正文记录规范化文字摘要。脚注HTML另经允许标签处理。段落换行与屏幕排版不是原文字符的增删。</p><p>该报告不宣称网站永不改变、所有历史信息均无误或已穷尽全站。原文书房的HTML另由本地完整性检查对照232个保存单元。</p><p><a href="source-baseline.json">下载成功基线记录 ↗</a> · <a href="source-recheck.json">下载本次连接失败记录 ↗</a></p><div class="table-wrap" tabindex="0"><table><thead><tr><th>文献</th><th>正文单元</th><th>基线状态</th><th>原文来源</th></tr></thead><tbody>'
for row in data['sections']:out+=f'<tr><td>{e(row["document"])}</td><td>{e(row["title"])}</td><td>{"相符" if row["match"] else "需要复核"}</td><td><a href="{e(row["source"])}" target="_blank" rel="noopener noreferrer">查看原文 ↗</a></td></tr>'
out+='</tbody></table></div><p class="tiny">检查时刻 UTC：'+e(data['meta']['checked_at_utc'])+'</p></main></body></html>'
(base/'dist/source-report.html').write_text(out,encoding='utf8')
shutil.copyfile(base/'qa/source-recheck.json',base/'dist/source-recheck.json')
shutil.copyfile(base/'qa/source-baseline.json',base/'dist/source-baseline.json')
print(json.dumps(summary))
