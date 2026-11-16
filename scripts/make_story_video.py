"""Build the optional captioned teaching video. Requires Pillow and imageio-ffmpeg."""
from pathlib import Path
import os, subprocess
from PIL import Image, ImageDraw, ImageFont
from imageio_ffmpeg import get_ffmpeg_exe
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from study_v3 import STEPS

ROOT=Path(__file__).resolve().parents[1]
FONT=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/msyh.ttc'
def font(size): return ImageFont.truetype(str(FONT),size)

def frame(i,t):
 year,city,title,history,memory,_=STEPS[i]
 im=Image.new('RGB',(960,540),'#102b30'); d=ImageDraw.Draw(im)
 for j in range(4):
  x=750+j*80+t*12
  d.ellipse((x-190,10-j*20,x+170,268+j*25),fill=['#15363b','#193f43','#1d484b','#215256'][j])
 d.text((63,46),'GTstudy  /  认信的五幕',font=font(22),fill='#abddd4')
 d.text((63,104),year+'  ·  '+city,font=font(28),fill='#ffe1a4')
 d.text((63,167),title,font=font(47),fill='#fffcf5')
 lines=['']
 for c in history:
  if d.textlength(lines[-1]+c,font=font(26))>820:lines.append(c)
  else:lines[-1]+=c
 for j,line in enumerate(lines): d.text((65,256+j*41),line,font=font(26),fill='#d3e6e2')
 d.rounded_rectangle((63,408,896,477),radius=16,fill='#25494a')
 d.text((83,423),memory,font=font(27),fill='#ffe1a4')
 for j in range(5):
  x=64+j*169; d.rounded_rectangle((x,503,x+153,507),radius=2,fill='#3a5b5c')
  n=153 if j<i else (min(153,round(t*153/6)) if j==i else 0)
  if n:d.rectangle((x,503,x+n,507),fill='#8fe2cf')
 return im

def main():
 frame(0,0).save(ROOT/'dist/story-poster.webp',quality=88)
 cmd=[get_ffmpeg_exe(),'-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','960x540','-r','12','-i','-','-c:v','libx264','-preset','fast','-crf','25','-vf','format=yuv420p','-movflags','+faststart',str(ROOT/'dist/confession-story.mp4')]
 with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
  for i in range(len(STEPS)):
   for f in range(72):proc.stdin.write(frame(i,f/12).tobytes())
  proc.stdin.close()
  if proc.wait():raise RuntimeError('Video encoding failed')

if __name__=='__main__':main()
