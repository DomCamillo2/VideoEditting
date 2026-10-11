#!/usr/bin/env python3
"""Validate, stage and render the JSON ManifestFilm locally without changing originals."""
import argparse
import copy
import importlib.util
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
from editing import validate, relative_asset, rational, sha256, write_new, qa

ROOT=Path(__file__).resolve().parents[1]
STUDIO=ROOT/'studio'
GAGS={'spin','download','walkoff','float','launch','boing'}


def bounded_number(value,low,high):
    return type(value) in (int,float) and math.isfinite(value) and low<=value<=high


def render_errors(data,root):
    errors,warnings=validate(data,root)
    if errors:return errors,warnings
    for dimension in ('width','height'):
        value=data.get(dimension)
        if type(value) is not int or value<16 or value>8192 or value%2:errors.append(dimension+' must be an even integer from 16 to 8192')
    if data.get('style') not in ('serious','emotional','funny'):errors.append('Choose style: serious, emotional or funny')
    duration=data['duration_frames']
    for shot in data['shots']:
        if shot.get('kind') not in ('image','video'):errors.append(shot['id']+': kind must be image or video')
        if shot.get('kind')=='video' and not shot.get('source'):errors.append(shot['id']+': video requires an explicit source range')
        if shot.get('fit','contain-blur') not in ('contain-blur','cover'):errors.append(shot['id']+': unsupported fit')
        if not bounded_number(shot.get('zoom',1),1,1.15):errors.append(shot['id']+': zoom must be 1..1.15; inspect faces individually')
        if not bounded_number(shot.get('volume',0),0,1):errors.append(shot['id']+': volume must be 0..1')
        if 'label' in shot and (not isinstance(shot['label'],str) or len(shot['label'])>100):errors.append(shot['id']+': label must be at most 100 characters')
    audio=data.get('audio',[])
    if not isinstance(audio,list):return errors+['audio must be a list'],warnings
    for track in audio:
        if not isinstance(track,dict):errors.append('audio entries must be objects');continue
        for key in ('start_frame','duration_frames'):
            if type(track.get(key)) is not int:errors.append('Audio timing must be integer frames')
        start,length=track.get('start_frame'),track.get('duration_frames')
        if type(start) is int and type(length) is int and (start<0 or length<=0 or start+length>duration):errors.append('Audio outside timeline')
        if not bounded_number(track.get('volume'),0,1):errors.append('Audio volume must be 0..1')
        try:rational(track.get('source_in_seconds',0))
        except ValueError:errors.append('Audio source_in_seconds must be nonnegative')
        for key in ('fade_in_frames','fade_out_frames'):
            if key in track and (type(track[key]) is not int or track[key]<0):errors.append('Audio fades must be nonnegative integer frames')
        ducks=track.get('duck',[])
        if not isinstance(ducks,list):errors.append('duck must be a list');continue
        for duck in ducks:
            if not isinstance(duck,dict) or type(duck.get('start_frame')) is not int or type(duck.get('end_frame')) is not int:
                errors.append('Duck timing must be integer frames');continue
            if not 0<=duck['start_frame']<duck['end_frame']<=duration or not bounded_number(duck.get('volume'),0,track['volume'] if bounded_number(track.get('volume'),0,1) else 0):
                errors.append('Invalid duck interval/volume')
    for effect in data.get('effects',[]):
        if effect.get('type') not in ('sticker','whip'):errors.append('Unsupported effect; supported: sticker, whip')
        if effect.get('type')=='sticker':
            if data.get('style')!='funny':errors.append('Sticker gags require explicit funny style')
            if effect.get('gag','spin') not in GAGS:errors.append('Unknown sticker gag')
            if effect['duration_frames']/rational(data['fps'])<=.65:errors.append('Sticker needs more than 0.65 seconds')
    if errors:return errors,warnings
    for entry in media_entries(data):
        path=entry.get('asset')
        if not relative_asset(path):errors.append('Every audio/effect asset must have a portable relative path');continue
        source=(Path(root)/path).resolve()
        if Path(root).resolve() not in source.parents or not source.is_file():errors.append('Missing or escaping media: '+path)
    return errors,warnings


def media_entries(data):
    return data.get('shots',[])+data.get('audio',[])+[effect for effect in data.get('effects',[]) if effect.get('type')=='sticker']


def check_sources(data,root):
    """Probe actual selected streams before expensive rendering; explicit ranges are not evidence."""
    if not shutil.which('ffprobe'):raise ValueError('ffprobe is required')
    for entry in data['shots']+data.get('audio',[]):
        if entry.get('kind')=='image':continue
        source=(root/entry['asset']).resolve()
        result=subprocess.run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(source)],capture_output=True,text=True,check=True)
        metadata=json.loads(result.stdout)
        is_video=entry.get('kind')=='video'
        streams=[s for s in metadata.get('streams',[]) if s.get('codec_type')==('video' if is_video else 'audio')]
        if not streams:raise ValueError('Expected media stream missing: '+entry['asset'])
        stream=streams[0]
        duration=float(stream.get('duration') or metadata.get('format',{}).get('duration') or 0)
        if is_video:
            source_range=entry['source']; declared=rational(source_range['fps'],positive=True)
            measured=rational(stream.get('avg_frame_rate','0/1'),positive=True)
            nominal=rational(stream.get('r_frame_rate','0/1'),positive=True)
            if abs(float(declared-measured))>.001 or abs(float(measured-nominal))>.001:
                raise ValueError('Source fps differs or possible VFR; prepare a verified CFR proxy: '+entry['asset'])
            frames=int(stream.get('nb_read_frames') or 0)
            if frames<=0 or source_range['out_frame']>frames:raise ValueError('Selected range exceeds actual source: '+entry['asset'])
        else:
            needed=float(rational(entry.get('source_in_seconds',0)))+entry['duration_frames']/float(rational(data['fps']))
            if needed>duration+.02:raise ValueError('Audio is shorter than selected range: '+entry['asset'])


def prepare(data,root,props_output,studio=STUDIO,probe=True):
    root=Path(root).resolve(); props_output=Path(props_output)
    if props_output.exists() or props_output.with_suffix('.assets.json').exists():raise FileExistsError('Choose a new props filename')
    errors,warnings=render_errors(data,root)
    if errors:raise ValueError('; '.join(errors))
    if probe:check_sources(data,root)
    manifest=copy.deepcopy(data)
    # The interchange schema accepts rational strings; Remotion expects numeric props here.
    for shot in manifest['shots']:
        if shot.get('source'):
            shot['source']['playback_rate']=float(rational(shot['source'].get('playback_rate',1),positive=True))
    for track in manifest.get('audio',[]):
        track['source_in_seconds']=float(rational(track.get('source_in_seconds',0)))
    stage=Path(studio)/'public/local'/('film-'+uuid.uuid4().hex)
    if Path(studio).resolve() not in stage.resolve().parents:raise ValueError('Staging path escapes studio')
    stage.mkdir(parents=True,exist_ok=False)
    mapping,inventory={},[]
    for entry in media_entries(manifest):
        original=entry['asset']
        if original not in mapping:
            source=(root/original).resolve();digest=sha256(source)
            target=stage/(digest+source.suffix.lower())
            if not target.exists():shutil.copy2(source,target)
            mapping[original]=target.relative_to(Path(studio)/'public').as_posix()
            inventory.append(dict(asset=original,sha256=digest,staged_asset=mapping[original]))
        entry['asset']=mapping[original]
    props=dict(manifest=manifest)
    write_new(props_output,props)
    write_new(props_output.with_suffix('.assets.json'),dict(media=inventory,warnings=warnings,visual_review='pending',listening_review='pending'))
    return props


def render(manifest_path,root,output,scale=.5,browser=None,gl=None):
    output=Path(output).resolve()
    if output.exists():raise FileExistsError('Export already exists (possibly incomplete); choose a new version filename')
    qa_output=output.parent/(output.stem+'.qa.json')
    if qa_output.exists():raise FileExistsError('QA report already exists; choose a new export version filename')
    if not bounded_number(scale,.1,1):raise ValueError('scale must be 0.1..1')
    cli=STUDIO/'node_modules/.bin'/('remotion.cmd' if sys.platform=='win32' else 'remotion')
    if not cli.exists():raise ValueError('Run npm ci inside studio first')
    data=json.loads(Path(manifest_path).read_text())
    props=output.parent/(output.stem+'.props.json')
    attempt=1
    while props.exists() or props.with_suffix('.assets.json').exists():
        attempt+=1
        props=output.parent/(output.stem+f'.attempt-{attempt:03d}.props.json')
    if attempt>1:print('Preserving earlier attempt files; fresh props: '+props.name,file=sys.stderr)
    prepare(data,root,props)
    command=[str(cli),'render','src/index.ts','ManifestFilm',str(output),'--props='+str(props),'--codec=h264',
             '--scale='+str(scale),'--concurrency=2','--crf=18']
    if browser:command+=['--browser-executable='+str(Path(browser).resolve())]
    if gl:command+=['--gl='+gl]
    subprocess.run(command,cwd=STUDIO,check=True)
    if not qa(output,qa_output,data['duration_frames']):raise ValueError('Export QA failed; see '+qa_output.name)
    return output


def doctor():
    tools={name:bool(shutil.which(name)) for name in ('python3','node','npm','ffmpeg','ffprobe','exiftool')}
    modules={name:importlib.util.find_spec(name) is not None for name in ('PIL','numpy')}
    return dict(tools=tools,analysis_modules=modules,studio_dependencies=(STUDIO/'node_modules/.bin/remotion').exists(),
                note='Read-only presence check. Does not install software or test browser/MCP connections.')


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor')
    for name in ('prepare','render'):
        p=sub.add_parser(name);p.add_argument('manifest');p.add_argument('output');p.add_argument('--media-root',required=True)
        if name=='render':p.add_argument('--scale',type=float,default=.5);p.add_argument('--browser-executable');p.add_argument('--gl',choices=['angle','egl','swiftshader','swangle'])
    args=parser.parse_args()
    try:
        if args.command=='doctor':print(json.dumps(doctor(),indent=2))
        elif args.command=='prepare':prepare(json.loads(Path(args.manifest).read_text()),args.media_root,args.output);print('Prepared props: '+args.output)
        else:print('Export: '+str(render(args.manifest,args.media_root,args.output,args.scale,args.browser_executable,args.gl)))
        return 0
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:print(str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
