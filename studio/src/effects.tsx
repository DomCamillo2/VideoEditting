import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export type Gag =
  | "spin"
  | "download"
  | "walkoff"
  | "float"
  | "launch"
  | "boing";

/** A single intentionally reusable template. Input is a reviewed, transparent cutout. */
export const Sticker: React.FC<{
  src: string;
  effect: Gag;
  seconds?: number;
}> = ({ src, effect, seconds = 3 }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const p = interpolate(
    frame,
    [0.3 * fps, (seconds - 0.35) * fps],
    [0, 1],
    clamp,
  );
  const lift = Math.sin(p * Math.PI);
  const progress = interpolate(p, [0, 0.2, 0.72, 1], [0, 0, 1, 1], clamp);
  let x = 0,
    y = 0,
    rotation = 0,
    scale = 1,
    sy = 1;
  if (effect === "spin") {
    rotation = 360 * progress;
    scale = 1 - 0.26 * lift;
    y = -height * 0.05 * lift;
  }
  if (effect === "download") {
    rotation = (1 - progress) * -360;
    scale = 0.35 + 0.65 * progress;
    y = -height * 0.14 * (1 - progress);
  }
  if (effect === "walkoff") {
    x = interpolate(p, [0, 0.2, 1], [0, 0, width * 0.85], clamp);
    y = -Math.abs(Math.sin(p * Math.PI * 8)) * height * 0.035;
    rotation = Math.sin(p * Math.PI * 8) * 8;
  }
  if (effect === "float") {
    y = -height * 0.17 * lift;
    rotation = Math.sin(p * Math.PI * 2) * 11;
  }
  if (effect === "launch") {
    x = interpolate(p, [0, 0.22, 0.8, 1], [0, -25, width * 0.85, width], clamp);
    y = interpolate(
      p,
      [0, 0.22, 0.8, 1],
      [0, 25, -height * 0.65, -height],
      clamp,
    );
    rotation = 25 * p;
  }
  if (effect === "boing") {
    const jump = Math.sin(p * Math.PI * 2);
    y = -Math.max(0, jump) * height * 0.14;
    sy = 1 + Math.min(0, jump) * 0.13;
  }
  const h = height * 0.64,
    w = (h * 400) / 720;
  return (
    <>
      <div
        style={{
          position: "absolute",
          left: width / 2 - w / 2,
          top: height * 0.2,
          width: w,
          height: h,
          transformOrigin: "50% 65%",
          translate: `${x}px ${y}px`,
          rotate: `${rotation}deg`,
          scale: `${scale} ${scale * sy}`,
          filter: "drop-shadow(0 16px 14px #102c3d55)",
        }}
      >
        <Img
          src={src}
          style={{ width: "100%", height: "100%", objectFit: "contain" }}
        />
      </div>
      {effect === "download" ? (
        <div
          style={{
            position: "absolute",
            left: width * 0.36,
            top: height * 0.88,
            width: width * 0.28,
            color: "#16323e",
            fontSize: 28,
            textAlign: "center",
          }}
        >
          <div
            style={{
              height: 9,
              borderRadius: 10,
              background: "#23404f33",
              marginBottom: 14,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${Math.round(progress * 100)}%`,
                background: "#ee7956",
              }}
            />
          </div>
          {progress < 1
            ? `Mensch wird geladen … ${Math.floor(progress * 100)} %`
            : "Bereit für Urlaub."}
        </div>
      ) : null}
    </>
  );
};

export type Anchor = readonly [number, number];
/** Both inputs occupy the same viewport. Anchors refer to the displayed, already-framed images. */
export const FaceMatch: React.FC<{
  before: React.ReactNode;
  after: React.ReactNode;
  beforeAnchor: Anchor;
  afterAnchor: Anchor;
  cutFrame: number;
  transitionFrames: number;
  maxScale?: number;
}> = ({
  before,
  after,
  beforeAnchor,
  afterAnchor,
  cutFrame,
  transitionFrames,
  maxScale = 4,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  if (maxScale <= 1 || transitionFrames <= 0)
    throw new Error("FaceMatch requires maxScale > 1 and positive duration");
  const half = transitionFrames / 2;
  const incoming = frame >= cutFrame;
  const scale = interpolate(
    frame,
    [cutFrame - half, cutFrame, cutFrame + half],
    [1, maxScale, 1],
    clamp,
  );
  const amount = (scale - 1) / (maxScale - 1);
  const [ax, ay] = incoming ? afterAnchor : beforeAnchor;
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <AbsoluteFill
        style={{
          transformOrigin: `${ax * 100}% ${ay * 100}%`,
          translate: `${(0.5 - ax) * width * amount}px ${(0.5 - ay) * height * amount}px`,
          scale,
        }}
      >
        {incoming ? after : before}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export type TrackPoint = {
  frame: number;
  x: number;
  y: number;
  scale?: number;
};
/** x/y are normalized composition coordinates AFTER source rotation and crop. */
export const TrackedFlame: React.FC<{ track: TrackPoint[] }> = ({ track }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  if (track.length < 2)
    throw new Error("TrackedFlame needs at least two keyframes");
  if (track.some((p, i) => i > 0 && p.frame <= track[i - 1].frame))
    throw new Error("Tracking frames must increase");
  const frames = track.map((p) => p.frame);
  const x = interpolate(
    f,
    frames,
    track.map((p) => p.x * width),
    clamp,
  );
  const y = interpolate(
    f,
    frames,
    track.map((p) => p.y * height),
    clamp,
  );
  const scale = interpolate(
    f,
    frames,
    track.map((p) => p.scale ?? 1),
    clamp,
  );
  const start = frames[0],
    end = frames[frames.length - 1];
  const fade = Math.min(
    1,
    Math.max(0, (f - start) / 4),
    Math.max(0, (end - f) / 4),
  );
  return (
    <svg
      width={240}
      height={140}
      viewBox="0 0 240 140"
      style={{
        position: "absolute",
        left: x - 220,
        top: y - 70,
        transformOrigin: "220px 70px",
        scale: scale * (1 + 0.07 * Math.sin(f * 1.5)),
        opacity: fade,
      }}
    >
      <path
        d="M225 70 Q115 15 10 12 L58 57 L5 83 Q110 78 110 129 Q165 100 225 70"
        fill="#ee6240"
      />
      <path
        d="M222 70 Q145 43 64 44 L111 70 L78 93 Q160 99 222 70"
        fill="#ffbd55"
      />
      <path d="M222 70 Q180 54 129 69 Q179 91 222 70" fill="#fff0b0" />
    </svg>
  );
};

/** Full subject preserved by default. Scaling requires a per-shot review. */
export const PortraitFrame: React.FC<{ src: string; zoom?: number }> = ({
  src,
  zoom = 1,
}) => {
  const f = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#193c48" }}>
      <Img
        src={src}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          filter: "blur(40px) brightness(.62)",
          scale: 1.12,
        }}
      />
      <AbsoluteFill>
        <Img
          src={src}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            scale: interpolate(
              f,
              [0, Math.max(1, durationInFrames - 1)],
              [1, zoom],
              clamp,
            ),
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** A foreground accent: timeline duration and the underlying cut remain unchanged. */
export const WhipAccent: React.FC<{ cutFrame: number; frames: number }> = ({
  cutFrame,
  frames,
}) => {
  const f = useCurrentFrame();
  const { width } = useVideoConfig();
  const p = interpolate(
    f,
    [cutFrame - frames / 2, cutFrame + frames / 2],
    [0, 1],
    clamp,
  );
  const visible = f >= cutFrame - frames / 2 && f < cutFrame + frames / 2;
  return visible ? (
    <AbsoluteFill
      style={{
        translate: `${interpolate(p, [0, 1], [-width, width])}px 0px`,
        background:
          "linear-gradient(90deg,transparent,#eaf0dfe6 35%,#eaf0dfff 65%,transparent)",
        filter: "blur(18px)",
      }}
    />
  ) : null;
};

export const PopLabel: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 180 },
    durationInFrames: Math.round(0.6 * fps),
  });
  return (
    <div
      style={{
        position: "absolute",
        right: 90,
        bottom: 100,
        background: "#f8e6b7",
        color: "#173340",
        borderRadius: 20,
        padding: "18px 32px",
        fontSize: 36,
        fontWeight: 700,
        scale: s,
      }}
    >
      {text}
    </div>
  );
};
