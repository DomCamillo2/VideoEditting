#!/usr/bin/env python3
"""Generate original deterministic audio fixtures. Refuses existing files."""
import math
import random
import struct
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'studio/public/demo'
SR=48000

def save(name, samples):
    path=ROOT/(name+'.wav')
    if path.exists():
        raise FileExistsError(str(path)+' exists; move it before deliberately regenerating')
    pcm=b''.join(struct.pack('<hh',int(max(-1,min(1,x))*32767),int(max(-1,min(1,x))*32767)) for x in samples)
    with wave.open(str(path),'wb') as w:
        w.setnchannels(2);w.setsampwidth(2);w.setframerate(SR);w.writeframes(pcm)


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for name in ['boing','zap','blip','chime','swish']:
        rng=random.Random(20261011)
        samples=[];phase=0
        for n in range(int(.6*SR)):
            t=n/SR
            frequency={'boing':170+100*math.exp(-t*8)*math.sin(t*28),'zap':800*math.exp(-t*6)+90,'blip':680,'chime':880,'swish':1}[name]
            phase+=2*math.pi*frequency/SR
            envelope=min(1,t/.005)*math.exp(-t*8)*min(1,(.6-t)/.03)
            source=rng.uniform(-1,1)*math.sin(math.pi*t/.6) if name=='swish' else math.sin(phase)
            samples.append(.26*source*envelope)
        save(name,samples)
    samples=[];rng=random.Random(7)
    for n in range(30*SR):
        t=n/SR;b=t%.5
        kick=math.sin(2*math.pi*(55*b+9*(1-math.exp(-b*25))))*math.exp(-b*24)
        hat=rng.uniform(-1,1)*math.exp(-(t%.25)*100)
        samples.append((.23*kick+.025*hat)*min(1,(30-t)/.25))
    save('beat',samples)

if __name__=='__main__':main()
