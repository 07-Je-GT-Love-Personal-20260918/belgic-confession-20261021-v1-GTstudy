"""One-time upgrade of the small v1 controller; safe to rerun."""
from pathlib import Path
base=Path(__file__).resolve().parent.parent
p=base/'dist/app.js';s=p.read_text(encoding='utf8')
if 'const originalData=' in s:s=s[:s.index('const originalData=')]+'})();\n'
if 'const queueSave=' not in s:
 needle='function applyPrefs()'
 s=s.replace(needle,"let saveTimer;const queueSave=()=>{clearTimeout(saveTimer);saveTimer=setTimeout(save,250)};window.addEventListener('pagehide',()=>{clearTimeout(saveTimer);save()});\nconst readSavedMarks=()=>{try{const m=JSON.parse(localStorage.getItem('gtstudy-belgic-marks-v2')||'[]');return Array.isArray(m)?m:[]}catch{return []}};\n"+needle)
 s=s.replace("state.notes[t.dataset.note]=t.value;save()","state.notes[t.dataset.note]=t.value;queueSave()")
 s=s.replace("date:new Date().toISOString(),state}","date:new Date().toISOString(),state,marks:readSavedMarks()}")
 s=s.replace("save();progress();$$('[data-note]')","if(Array.isArray(d.marks))window.dispatchEvent(new CustomEvent('gtstudy:merge-marks',{detail:d.marks}));save();progress();$$('[data-note]')")
p.write_text(s,encoding='utf8',newline='\n')
