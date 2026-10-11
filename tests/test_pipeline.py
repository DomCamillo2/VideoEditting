import copy
import importlib.util
import json
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import analyze_media
import beat_candidates
import film

HAVE_ANALYSIS=importlib.util.find_spec('PIL') is not None and importlib.util.find_spec('numpy') is not None

@unittest.skipUnless(HAVE_ANALYSIS,'Optional Pillow/NumPy analysis dependencies')
class AnalysisTests(unittest.TestCase):
    def pattern(self):
        from PIL import Image,ImageDraw
        image=Image.new('RGB',(200,120),'white');draw=ImageDraw.Draw(image)
        for x in range(10,190,15):draw.rectangle((x,10,x+6,105),fill='black')
        return image
    def test_sharp_and_soft_comparable_subject_regions(self):
        from PIL import ImageFilter
        sharp=self.pattern();soft=sharp.filter(ImageFilter.GaussianBlur(3))
        self.assertGreater(analyze_media.image_metrics(sharp)['focus_variance'],analyze_media.image_metrics(soft)['focus_variance'])
    def test_roi_rejects_invalid_and_empty_bounds(self):
        for roi in [[.5,.5,.4,.8],[-1,0,1,1],[0,0,1], [0,0,.001,.001]]:
            with self.subTest(roi=roi),self.assertRaises(ValueError):analyze_media.image_metrics(self.pattern(),roi)
    def test_orientation_applied(self):
        image=self.pattern();exif=image.getexif();exif[274]=6;image.info['exif']=exif.tobytes()
        metrics=analyze_media.image_metrics(image)
        self.assertEqual(metrics['metric_size'],[120,200])
    def test_contact_sheets_duplicate_and_unreadable(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'media';root.mkdir();self.pattern().save(root/'a.png')
            (root/'b.png').write_bytes((root/'a.png').read_bytes());(root/'broken.jpg').write_bytes(b'broken')
            out=Path(td)/'review';report=analyze_media.analyze(root,out)
            self.assertEqual(report['media'][1]['exact_duplicate_of'],report['media'][0]['asset_id'])
            self.assertIn('error',report['media'][2]);self.assertTrue((out/'contact-001.jpg').exists())
            self.assertTrue(all(row['decision']=='review' for row in report['media']))
            with self.assertRaises(FileExistsError):analyze_media.analyze(root,out)
    def test_asset_ids_survive_new_files(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'media';root.mkdir();self.pattern().save(root/'b.png')
            before=analyze_media.analyze(root,Path(td)/'one')['media'][0]['asset_id']
            self.pattern().save(root/'a.png')
            after=analyze_media.analyze(root,Path(td)/'two')['media'][1]['asset_id']
            self.assertEqual(before,after)
    def test_analysis_output_cannot_reenter_input(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):analyze_media.analyze(td,Path(td)/'review')
    def test_misspelled_roi_is_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'media';root.mkdir();self.pattern().save(root/'a.png')
            output=Path(td)/'review'
            with self.assertRaisesRegex(ValueError,'missing/unsupported'):analyze_media.analyze(root,output,{'wrong.png':[0,0,1,1]})
            self.assertFalse(output.exists())
    def test_complete_link_avoids_similarity_chaining(self):
        rows=[dict(asset_id=str(i),sha256=str(i),kind='image',aspect=1,mean_rgb=[100]*3,dhash=h) for i,h in enumerate(['0000','0001','0003'])]
        self.assertEqual([len(g) for g in analyze_media.cluster_rows(rows,1)],[2,1])
    def test_silence_has_no_beat_candidates(self):
        import numpy as np
        onsets,tempo,status=beat_candidates.detect(np.zeros(8000))
        self.assertEqual(onsets,[]);self.assertEqual(tempo,[]);self.assertIn('silence',status)
    def test_regular_pulses_have_localized_candidates(self):
        import numpy as np
        signal=np.zeros(8000*8)
        times=np.arange(.5,7.6,.5)
        for t in times:
            start=int(t*8000);signal[start:start+160]=np.sin(np.arange(160)*.5)*np.exp(-np.arange(160)/40)
        onsets,tempo,_=beat_candidates.detect(signal)
        for t in times:self.assertLess(min(abs(t-o['source_seconds']) for o in onsets),.04)
        self.assertTrue(any(abs(t['bpm']-120)<2 for t in tempo))
    def test_invalid_detection_samples_rejected(self):
        import numpy as np
        for data in [np.array([float('nan')]),np.ones((2,2))]:
            with self.assertRaises(ValueError):beat_candidates.detect(data)


class FilmTests(unittest.TestCase):
    def fixture(self,root):
        (root/'image.png').write_bytes(b'fixture');(root/'sound.wav').write_bytes(b'fixture')
        return dict(schema_version=1,fps=30,width=1920,height=1080,duration_frames=90,style='serious',
                    shots=[dict(id='a',kind='image',asset='image.png',start_frame=0,duration_frames=90,role='graphic')],audio=[])
    def test_manifest_preparation_copies_only_references(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);(root/'private.jpg').write_bytes(b'private')
            original=copy.deepcopy(data);output=root/'props.json'
            props=film.prepare(data,root,output,studio=root/'studio',probe=False)
            self.assertEqual(data,original);self.assertTrue(props['manifest']['shots'][0]['asset'].startswith('local/film-'))
            self.assertEqual(len(list((root/'studio/public/local').rglob('*.png'))),1)
            self.assertFalse(list((root/'studio').rglob('private.jpg')))
    def test_existing_sidecar_refused_before_writes(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);(root/'props.assets.json').write_text('{}')
            with self.assertRaises(FileExistsError):film.prepare(data,root,root/'props.json',studio=root/'studio',probe=False)
            self.assertFalse((root/'studio').exists());self.assertFalse((root/'props.json').exists())
    def test_serious_style_rejects_sticker_gag(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);data['effects']=[dict(type='sticker',asset='image.png',start_frame=0,duration_frames=60)]
            self.assertTrue(film.render_errors(data,root)[0]);data['style']='funny'
            self.assertFalse(film.render_errors(data,root)[0])
    def test_video_requires_source_range(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);data['shots'][0]['kind']='video'
            self.assertTrue(film.render_errors(data,root)[0])
    def test_unknown_effect_fails_instead_of_silent_drop(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);data['effects']=[dict(type='magic',start_frame=0,duration_frames=30)]
            self.assertTrue(film.render_errors(data,root)[0])
    def test_invalid_audio_and_dimensions(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);base=self.fixture(root)
            for change in [dict(width=101),dict(audio='bad'),dict(audio=[False]),dict(audio=[dict(asset='sound.wav',start_frame=0,duration_frames=91,volume=1)]),dict(audio=[dict(asset='sound.wav',start_frame=0,duration_frames=90,volume=None,duck=[dict(start_frame=0,end_frame=20,volume=.1)])])]:
                with self.subTest(change=change):self.assertTrue(film.render_errors(dict(base,**change),root)[0])
    def test_doctor_is_read_only(self):
        with patch.object(film.subprocess,'run',side_effect=AssertionError('Must not run processes')):
            self.assertIn('tools',film.doctor())
    def test_missing_actual_source_stream_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);data['audio']=[dict(asset='sound.wav',start_frame=0,duration_frames=90,volume=1)]
            class Result:stdout='{"streams":[],"format":{"duration":"3"}}'
            with patch.object(film.shutil,'which',return_value='ffprobe'),patch.object(film.subprocess,'run',return_value=Result()):
                with self.assertRaises(ValueError):film.check_sources(data,root)
    def test_actual_video_range_and_frame_rate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root)
            data['shots'][0].update(kind='video',source=dict(fps=24,in_frame=24,out_frame=96))
            for frames,average,nominal,passes in [('120','24/1','24/1',True),('80','24/1','24/1',False),('120','25/1','25/1',False),('120','24/1','30/1',False)]:
                result=subprocess.CompletedProcess([],0,stdout=json.dumps({'streams':[{'codec_type':'video','avg_frame_rate':average,'r_frame_rate':nominal,'nb_read_frames':frames}]}))
                with self.subTest(frames=frames,average=average,nominal=nominal),patch.object(film.shutil,'which',return_value='ffprobe'),patch.object(film.subprocess,'run',return_value=result):
                    if passes:film.check_sources(data,root)
                    else:
                        with self.assertRaises(ValueError):film.check_sources(data,root)
    def test_audio_offset_must_fit_actual_duration(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);data['audio']=[dict(asset='sound.wav',start_frame=0,duration_frames=90,volume=1,source_in_seconds=.5)]
            result=subprocess.CompletedProcess([],0,stdout='{"streams":[{"codec_type":"audio","duration":"3"}]}')
            with patch.object(film.shutil,'which',return_value='ffprobe'),patch.object(film.subprocess,'run',return_value=result):
                with self.assertRaisesRegex(ValueError,'shorter'):film.check_sources(data,root)
    def test_failed_browser_can_retry_without_overwriting_attempt(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);data=self.fixture(root);manifest=root/'timeline.json';manifest.write_text(json.dumps(data))
            studio=root/'studio';cli=studio/'node_modules/.bin/remotion';cli.parent.mkdir(parents=True);cli.touch()
            output=root/'preview.mp4'
            with patch.object(film,'STUDIO',studio),patch.object(film,'check_sources'),patch.object(film,'qa',return_value=True),patch.object(film.subprocess,'run') as run:
                # prepare's default studio is bound at definition time; explicitly direct staging into the fixture.
                real_prepare=film.prepare
                with patch.object(film,'prepare',side_effect=lambda d,r,p:real_prepare(d,r,p,studio=studio)):
                    run.side_effect=subprocess.CalledProcessError(1,['browser'])
                    with self.assertRaises(subprocess.CalledProcessError):film.render(manifest,root,output)
                    first=(root/'preview.props.json').read_bytes()
                    run.side_effect=None
                    film.render(manifest,root,output,browser='/existing/chrome')
                    self.assertEqual((root/'preview.props.json').read_bytes(),first)
                    self.assertTrue((root/'preview.attempt-002.props.json').exists())
                    self.assertIn('--browser-executable=/existing/chrome',run.call_args.args[0])
    def test_existing_qa_blocks_render_before_staging(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'preview.qa.json').write_text('{}')
            with patch.object(film,'prepare',side_effect=AssertionError('Must not stage')):
                with self.assertRaisesRegex(FileExistsError,'QA report'):film.render(root/'missing.json',root,root/'preview.mp4')
if __name__=='__main__':unittest.main()
