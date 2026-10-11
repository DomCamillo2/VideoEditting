#!/usr/bin/env python3
"""Create a complete, original synthetic media project and its editable film manifest."""
import argparse
import json
import math
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import wave
from editing import write_new

ROOT=Path(__file__).resolve().parents[1]


def create(output):
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
    output=Path(output).resolve()
    if output.exists():raise FileExistsError('Choose a new project version')
    if not shutil.which('ffmpeg'):raise ValueError('FFmpeg is required for the synthetic motion fixture')
    output.mkdir(parents=True); media=output/'media';media.mkdir()
    def scenery(width=960,height=540,night=False):
        im=Image.new('RGB',(width,height),'#edc598' if night else '#bfd8dc');d=ImageDraw.Draw(im)
        d.ellipse((width*.7,height*.12,width*.84,height*.37),fill='#e6a877')
        d.polygon([(0,height*.62),(width*.22,height*.24),(width*.5,height*.65),(width*.76,height*.31),(width,height*.68),(width,height),(0,height)],fill='#49767b')
        d.polygon([(0,height*.82),(width*.42,height*.52),(width,height*.86),(width,height),(0,height)],fill='#234f5c')
        for y in range(round(height*.82),height,28):d.line((0,y,width,y),fill='#7cb0b3',width=2)
        return im
    landscape=scenery();landscape.save(media/'01-landscape.jpg',quality=95)
    shutil.copy2(media/'01-landscape.jpg',media/'02-landscape-duplicate.jpg')
    landscape.filter(ImageFilter.GaussianBlur(4)).save(media/'03-landscape-soft.jpg',quality=95)
    ImageEnhance.Color(landscape).enhance(.85).save(media/'04-landscape-alternate.jpg',quality=94)
    portrait=scenery(540,960);d=ImageDraw.Draw(portrait)
    for x,y,color in [(140,460,'#e17c57'),(285,440,'#edbb56'),(410,490,'#8aad91')]:
        d.line((x,y+100,x-25,y+330),fill='#172f3f',width=23);d.line((x,y+100,x+25,y+330),fill='#172f3f',width=23)
        d.rounded_rectangle((x-40,y-45,x+40,y+135),20,fill=color)
        d.ellipse((x-32,y-110,x+32,y-46),fill='#edc49a')
        d.ellipse((x-13,y-87,x-7,y-81),fill='#172f3f');d.ellipse((x+7,y-87,x+13,y-81),fill='#172f3f')
        d.arc((x-14,y-86,x+14,y-58),0,180,fill='#172f3f',width=3)
    portrait.save(media/'05-friends-portrait.jpg',quality=95)
    scenery(night=True).save(media/'06-evening.jpg',quality=95)
    # Camera move over our own illustration; source is 24fps, target timeline is 30fps.
    subprocess.run(['ffmpeg','-v','error','-loop','1','-framerate','24','-i',str(media/'01-landscape.jpg'),
                    '-vf',"zoompan=z='1+0.0015*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=960x540:fps=24",
                    '-frames:v','120','-c:v','libx264','-pix_fmt','yuv420p','-y',str(media/'07-motion.mp4')],check=True)
    shutil.copy2(ROOT/'studio/public/demo/friend.svg',media/'friend.svg')
    sr=24000;duration=20;samples=[]
    for n in range(sr*duration):
        t=n/sr;beat=t%.5
        kick=.35*math.sin(2*math.pi*(55*beat+8*(1-math.exp(-beat*22))))*math.exp(-beat*28)
        chord=.04*(math.sin(2*math.pi*220*t)+math.sin(2*math.pi*330*t))*min(1,t/.05)*min(1,(duration-t)/.4)
        samples.append(int(max(-1,min(1,kick+chord))*32767))
    with wave.open(str(media/'original-rhythm.wav'),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(sr);wav.writeframes(struct.pack('<'+'h'*len(samples),*samples))
    shots=[
        dict(id='landscape',asset='media/01-landscape.jpg',kind='image',start_frame=0,duration_frames=90,fit='cover',label='Auf ins Wochenende.'),
        dict(id='friends',asset='media/05-friends-portrait.jpg',kind='image',start_frame=90,duration_frames=120,fit='contain-blur',label='Zusammen unterwegs.'),
        dict(id='motion',asset='media/07-motion.mp4',kind='video',start_frame=210,duration_frames=90,fit='cover',label='Einfach los.',source=dict(fps=24,in_frame=24,out_frame=96,total_frames=120)),
        dict(id='evening',asset='media/06-evening.jpg',kind='image',start_frame=300,duration_frames=120,fit='cover',zoom=1.03,label='Noch einen Moment bleiben.'),
        dict(id='finale',asset='media/05-friends-portrait.jpg',kind='image',start_frame=420,duration_frames=120,fit='contain-blur',label='Bis zum nächsten Mal.',role='recap'),
    ]
    for i,shot in enumerate(shots):shot['captured_utc']=f'2024-08-01T10:{i*5:02d}:00Z'
    manifest=dict(schema_version=1,width=1920,height=1080,fps=30,duration_frames=540,style='funny',shots=shots,
                  audio=[dict(asset='media/original-rhythm.wav',start_frame=0,duration_frames=540,source_in_seconds=.5,volume=.75,fade_in_frames=10,fade_out_frames=30)],
                  effects=[dict(type='sticker',asset='media/friend.svg',gag='spin',start_frame=240,duration_frames=60),
                           dict(type='whip',start_frame=295,duration_frames=10)])
    write_new(output/'timeline.json',manifest)
    write_new(output/'selected-beats.json',dict(fps=30,beats_seconds=[0,3,7,10,14],cuts_frames=[0,90,210,300,420]))
    write_new(output/'selection.json',dict(decisions=[dict(asset=p.name,decision='exclude' if p.name[:2] in ('02','03','04') else 'keep',reason='Deliberate synthetic duplicate/soft/alternate fixture' if p.name[:2] in ('02','03','04') else 'Distinct demo scene') for p in sorted(media.glob('*.jpg'))],
                                               note='Authored synthetic example, not an automatic human-photo quality verdict. Dates are fixture data.'))
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output');args=parser.parse_args()
    try:print(create(args.output));return 0
    except (ImportError,OSError,ValueError,subprocess.SubprocessError) as exc:print(str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
