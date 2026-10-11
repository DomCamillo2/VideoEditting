#!/usr/bin/env python3
"""Propose local rhythmic onsets and tempo hypotheses; never certify musical beats."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from editing import frame_at, rational, sha256, write_new


def detect(samples, sample_rate=8000, min_interval=.18):
    try:
        import numpy as np
    except ImportError:
        raise ValueError('Install optional dependencies from requirements-analysis.txt') from None
    if not .05 <= min_interval <= 2: raise ValueError('min_interval must be 0.05..2 seconds')
    samples=np.asarray(samples,dtype=np.float64)
    if samples.ndim!=1 or not np.isfinite(samples).all(): raise ValueError('Finite mono samples required')
    hop, window = max(1,round(sample_rate*.01)), max(8,round(sample_rate*.032))
    taper=np.hanning(window); previous=np.zeros(window//2+1); strength=[]
    # O(window) temporary storage per hop; no full-duration spectrogram allocation.
    for offset in range(0,len(samples)-window+1,hop):
        magnitude=np.abs(np.fft.rfft(samples[offset:offset+window]*taper))
        strength.append(float(np.maximum(0,magnitude-previous).sum()))
        previous=magnitude
    strength=np.asarray(strength)
    if not len(strength) or strength.max()<1e-6:
        return [], [], 'silence-or-no-detectable-onsets'
    strength/=strength.max()
    floor=max(.035,float(np.quantile(strength,.9))*.3)
    peaks=[]
    for i in range(1,len(strength)-1):
        neighborhood=strength[max(0,i-20):min(len(strength),i+21)]
        if strength[i]>=strength[i-1] and strength[i]>strength[i+1] and strength[i]>max(floor,float(np.median(neighborhood))*2):
            peaks.append(i)
    selected=[]
    for i in sorted(peaks,key=lambda i:float(strength[i]),reverse=True):
        if all(abs(i-j)*hop/sample_rate>=min_interval for j in selected): selected.append(i)
    selected.sort()
    onsets=[dict(source_seconds=round((i*hop+window/2)/sample_rate,5),strength=round(float(strength[i]),4),kind='unverified-onset') for i in selected]
    centered=strength-strength.mean(); norm=float(np.dot(centered,centered))
    hypotheses=[]
    if len(onsets)>=4 and norm>0:
        scored=[]
        for lag in range(round(60/200*sample_rate/hop),round(60/60*sample_rate/hop)+1):
            if lag>=len(centered):continue
            score=float(np.dot(centered[:-lag],centered[lag:])/norm)
            scored.append((score,60*sample_rate/(hop*lag)))
        for score,bpm in sorted(scored,reverse=True):
            if score<=.05:break
            if all(abs(bpm-x['bpm'])>4 for x in hypotheses):
                hypotheses.append(dict(bpm=round(bpm,2),periodicity=round(score,4)))
            if len(hypotheses)==3:break
    return onsets,hypotheses,'review-required'


def analyze(path,output,fps='30',source_in=0,timeline_start=0,playback_rate=1,max_seconds=600,min_interval=.18):
    import numpy as np
    path=Path(path).resolve()
    if not path.is_file():raise ValueError('Audio input missing')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):raise ValueError('FFmpeg and ffprobe are required')
    fps=rational(fps,positive=True); source_in=rational(source_in); timeline_start=rational(timeline_start); speed=rational(playback_rate,positive=True)
    if not 1<=max_seconds<=3600:raise ValueError('max_seconds must be 1..3600')
    if Path(output).exists():raise FileExistsError('Choose a new output filename')
    probe=subprocess.run(['ffprobe','-v','error','-show_format','-of','json',str(path)],capture_output=True,text=True,check=True)
    duration=float(json.loads(probe.stdout)['format']['duration'])
    if duration-float(source_in)>max_seconds:raise ValueError('Audio exceeds analysis limit; choose a shorter local excerpt or increase --max-seconds')
    if float(source_in)>=duration:raise ValueError('source_in must precede audio end')
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(float(source_in)),'-i',str(path),'-map','0:a:0','-vn','-ac','1','-ar','8000','-t',str(max_seconds),'-f','f32le','-'],capture_output=True,check=True)
    samples=np.frombuffer(raw.stdout,dtype='<f4')
    onsets,tempo,status=detect(samples,min_interval=min_interval)
    for onset in onsets:
        source_time=source_in+rational(onset['source_seconds'])
        timeline_time=timeline_start+(source_time-source_in)/speed
        onset.update(source_seconds=float(source_time),timeline_seconds=float(timeline_time),candidate_frame=frame_at(timeline_time,fps))
    report=dict(schema_version=1,file=path.name,sha256=sha256(path),checked_at=datetime.now(timezone.utc).isoformat(),fps=str(fps),
                mapping=dict(source_in_seconds=float(source_in),timeline_start_seconds=float(timeline_start),playback_rate=float(speed)),
                analyzed_seconds=len(samples)/8000,onsets=onsets,tempo_hypotheses=tempo,status=status,listening_review='pending',
                method='positive spectral flux, local peak threshold and spacing; 8kHz mono / 10ms hop',
                note='Onsets are candidates, not verified beats or downbeats. Tempo can be half/double. Listen and select markers before beat-report; no automatic cuts.')
    write_new(output,report);return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('audio');parser.add_argument('output')
    parser.add_argument('--fps',default='30');parser.add_argument('--source-in',type=float,default=0);parser.add_argument('--timeline-start',type=float,default=0)
    parser.add_argument('--playback-rate',type=float,default=1);parser.add_argument('--max-seconds',type=int,default=600);parser.add_argument('--min-interval',type=float,default=.18)
    args=parser.parse_args()
    try:
        report=analyze(args.audio,args.output,args.fps,args.source_in,args.timeline_start,args.playback_rate,args.max_seconds,args.min_interval)
        print(json.dumps(dict(candidates=len(report['onsets']),tempo_hypotheses=report['tempo_hypotheses'],listening_review='pending')));return 0
    except (ImportError,ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:
        print(str(exc),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
