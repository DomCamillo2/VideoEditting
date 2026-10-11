import React from "react";
import { Audio, Video } from "@remotion/media";
import {
  AbsoluteFill,
  Composition,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Sticker, WhipAccent, type Gag } from "./effects";

export type FilmManifest = {
  schema_version: number;
  fps: number | string;
  width: number;
  height: number;
  duration_frames: number;
  style: "serious" | "emotional" | "funny";
  title?: string;
  shots: Array<{
    id: string;
    asset: string;
    kind: "image" | "video";
    start_frame: number;
    duration_frames: number;
    fit?: "contain-blur" | "cover";
    zoom?: number;
    label?: string;
    volume?: number;
    source?: {
      fps: number | string;
      in_frame: number;
      out_frame: number;
      playback_rate?: number;
    };
  }>;
  audio?: Array<{
    asset: string;
    start_frame: number;
    duration_frames: number;
    source_in_seconds?: number;
    volume: number;
    fade_in_frames?: number;
    fade_out_frames?: number;
    duck?: Array<{ start_frame: number; end_frame: number; volume: number }>;
  }>;
  effects?: Array<{
    type: "sticker" | "whip";
    start_frame: number;
    duration_frames: number;
    asset?: string;
    gag?: Gag;
  }>;
};
export type FilmProps = { manifest: FilmManifest };
export const rate = (value: number | string): number => {
  const [a, b = "1"] = String(value).split("/");
  return Number(a) / Number(b);
};
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

const FilmShot: React.FC<{ shot: FilmManifest["shots"][number] }> = ({
  shot,
}) => {
  const frame = useCurrentFrame();
  const { fps, height } = useVideoConfig();
  const src = staticFile(shot.asset);
  const isVideo = shot.kind === "video";
  // Remotion trims use composition frames; the manifest stores actual source frames.
  const trim = shot.source
    ? (shot.source.in_frame / rate(shot.source.fps)) * fps
    : 0;
  const speed = shot.source?.playback_rate ?? 1;
  const background = shot.fit !== "cover";
  const common = { width: "100%", height: "100%" } as const;
  return (
    <AbsoluteFill style={{ background: "#17343e", overflow: "hidden" }}>
      {background ? (
        isVideo ? (
          <Video
            src={src}
            trimBefore={trim}
            playbackRate={speed}
            muted
            premountFor={fps}
            objectFit="cover"
            style={{
              ...common,
              filter: "blur(36px) brightness(.65)",
              scale: 1.15,
            }}
          />
        ) : (
          <Img
            src={src}
            premountFor={fps}
            style={{
              ...common,
              objectFit: "cover",
              filter: "blur(36px) brightness(.65)",
              scale: 1.15,
            }}
          />
        )
      ) : null}
      <AbsoluteFill
        style={{
          scale: interpolate(
            frame,
            [0, Math.max(1, shot.duration_frames - 1)],
            [1, shot.zoom ?? 1],
            clamp,
          ),
        }}
      >
        {isVideo ? (
          <Video
            src={src}
            trimBefore={trim}
            playbackRate={speed}
            volume={shot.volume ?? 0}
            muted={(shot.volume ?? 0) === 0}
            premountFor={fps}
            objectFit={background ? "contain" : "cover"}
            style={common}
          />
        ) : (
          <Img
            src={src}
            premountFor={fps}
            style={{ ...common, objectFit: background ? "contain" : "cover" }}
          />
        )}
      </AbsoluteFill>
      {shot.label ? (
        <div
          style={{
            position: "absolute",
            left: "5%",
            top: "6%",
            maxWidth: "85%",
            color: "white",
            fontFamily: "Arial, sans-serif",
            fontSize: height * 0.042,
            fontWeight: 700,
            padding: "12px 20px",
            background: "#102c3dbb",
            borderRadius: 10,
            opacity: interpolate(
              frame,
              [
                0,
                shot.duration_frames / 6,
                (shot.duration_frames * 5) / 6,
                shot.duration_frames,
              ],
              [0, 1, 1, 0],
              clamp,
            ),
          }}
        >
          {shot.label}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const mixVolume = (
  track: NonNullable<FilmManifest["audio"]>[number],
  frame: number,
): number => {
  const fadeIn = Math.min(1, frame / Math.max(1, track.fade_in_frames ?? 1));
  const fadeOut = Math.min(
    1,
    (track.duration_frames - 1 - frame) /
      Math.max(1, track.fade_out_frames ?? 1),
  );
  let gain = track.volume;
  for (const duck of track.duck ?? []) {
    const absolute = frame + track.start_frame;
    const amount = Math.max(
      0,
      Math.min(
        1,
        (absolute - duck.start_frame + 6) / 6,
        (duck.end_frame + 6 - absolute) / 6,
      ),
    );
    gain = Math.min(gain, track.volume + (duck.volume - track.volume) * amount);
  }
  return Math.max(0, gain * fadeIn * fadeOut);
};

export const ManifestFilm: React.FC<FilmProps> = ({ manifest }) => {
  const { fps } = useVideoConfig();
  // Intentionally controlled by JSON; individual source-node drag editing is not supported.
  return (
    <AbsoluteFill style={{ background: "#17343e" }}>
      {manifest.shots.map((shot) => (
        <Sequence
          key={shot.id}
          name={shot.id}
          from={shot.start_frame}
          durationInFrames={shot.duration_frames}
          premountFor={fps}
        >
          <FilmShot shot={shot} />
        </Sequence>
      ))}
      {(manifest.audio ?? []).map((track, i) => (
        <Sequence
          key={`audio-${i}`}
          from={track.start_frame}
          durationInFrames={track.duration_frames}
          premountFor={fps}
        >
          <Audio
            src={staticFile(track.asset)}
            trimBefore={(track.source_in_seconds ?? 0) * fps}
            volume={(f) => mixVolume(track, f)}
            premountFor={fps}
          />
        </Sequence>
      ))}
      {(manifest.effects ?? []).map((effect, i) => (
        <Sequence
          key={`effect-${i}`}
          from={effect.start_frame}
          durationInFrames={effect.duration_frames}
          premountFor={fps}
        >
          {effect.type === "whip" ? (
            <WhipAccent
              cutFrame={effect.duration_frames / 2}
              frames={effect.duration_frames}
            />
          ) : manifest.style === "funny" && effect.asset ? (
            <Sticker
              src={staticFile(effect.asset)}
              effect={effect.gag ?? "spin"}
              seconds={effect.duration_frames / fps}
            />
          ) : null}
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const ManifestComposition = () => (
  <Composition
    id="ManifestFilm"
    component={ManifestFilm}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={360}
    defaultProps={{
      manifest: {
        schema_version: 1,
        fps: 30,
        width: 1920,
        height: 1080,
        duration_frames: 360,
        style: "serious",
        shots: [
          {
            id: "start",
            kind: "image",
            asset: "demo/landscape.svg",
            start_frame: 0,
            duration_frames: 120,
            fit: "cover",
            label: "Auf ins Wochenende.",
          },
          {
            id: "together",
            kind: "image",
            asset: "demo/portrait.svg",
            start_frame: 120,
            duration_frames: 120,
            fit: "contain-blur",
            label: "Zusammen unterwegs.",
          },
          {
            id: "end",
            kind: "image",
            asset: "demo/landscape.svg",
            start_frame: 240,
            duration_frames: 120,
            fit: "cover",
            label: "Eine Reise, die bleibt.",
          },
        ],
        audio: [
          {
            asset: "demo/beat.wav",
            start_frame: 0,
            duration_frames: 360,
            volume: 0.6,
            fade_in_frames: 10,
            fade_out_frames: 30,
          },
        ],
      },
    }}
    calculateMetadata={({ props }) => ({
      durationInFrames: props.manifest.duration_frames,
      width: props.manifest.width,
      height: props.manifest.height,
      fps: rate(props.manifest.fps),
    })}
  />
);
