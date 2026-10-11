import React from "react";
import {
  AbsoluteFill,
  Composition,
  Img,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";
import {
  FaceMatch,
  PopLabel,
  PortraitFrame,
  Sticker,
  TrackedFlame,
  WhipAccent,
  type Gag,
} from "./effects";

const Palette: React.FC<{
  title: string;
  number: string;
  children: React.ReactNode;
}> = ({ title, number, children }) => (
  <AbsoluteFill
    style={{
      background: "#e6eddf",
      fontFamily: "Arial, Helvetica, sans-serif",
      color: "#16343e",
      overflow: "hidden",
    }}
  >
    <div
      style={{
        position: "absolute",
        left: 90,
        top: 66,
        fontSize: 24,
        letterSpacing: 5,
      }}
    >
      VIDEO EDITTING / EFFECT LAB
    </div>
    <div
      style={{
        position: "absolute",
        left: 86,
        top: 115,
        fontSize: 64,
        fontWeight: 700,
        letterSpacing: -2,
      }}
    >
      {title}
    </div>
    <div style={{ position: "absolute", right: 90, top: 65, fontSize: 28 }}>
      {number}
    </div>
    <div
      style={{
        position: "absolute",
        left: 80,
        right: 80,
        bottom: 60,
        height: 1,
        background: "#16343e44",
      }}
    />
    {children}
  </AbsoluteFill>
);

const GagScene: React.FC<{
  effect: Gag;
  title: string;
  number: string;
  sound: string;
}> = ({ effect, title, number, sound }) => {
  const { fps } = useVideoConfig();
  return (
    <Palette title={title} number={number}>
      <div
        style={{
          position: "absolute",
          width: 520,
          height: 70,
          borderRadius: "50%",
          background: "#16343e20",
          left: 700,
          top: 880,
          filter: "blur(12px)",
        }}
      />
      <Sticker src={staticFile("demo/friend.svg")} effect={effect} />
      <Audio
        src={staticFile(`demo/${sound}.wav`)}
        from={Math.round(0.55 * fps)}
        volume={0.35}
        premountFor={fps}
      />
    </Palette>
  );
};

const FaceScene = () => {
  const { fps } = useVideoConfig();
  const Picture = ({ second = false }: { second?: boolean }) => (
    <AbsoluteFill style={{ background: second ? "#b5cbbc" : "#f2d8aa" }}>
      <Img
        src={staticFile("demo/friend.svg")}
        style={{
          position: "absolute",
          height: 850,
          width: 472,
          left: second ? 1060 : 370,
          top: 170,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: 100,
          left: 120,
          fontSize: 50,
          fontFamily: "Arial",
          color: "#19343f",
        }}
      >
        {second ? "… und wieder raus." : "Ins Gesicht …"}
      </div>
    </AbsoluteFill>
  );
  return (
    <FaceMatch
      before={<Picture />}
      after={<Picture second />}
      beforeAnchor={[0.316, 0.268]}
      afterAnchor={[0.675, 0.268]}
      cutFrame={Math.round(1.5 * fps)}
      transitionFrames={Math.round(0.6 * fps)}
    />
  );
};

const ScooterScene = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const x = 320 + (f / 90) * 1100;
  return (
    <Palette title="Urlaubsmodus: Turbo." number="08">
      <svg width="1920" height="1080" style={{ position: "absolute" }}>
        <path d="M100 830 H1820" stroke="#173340" strokeWidth="3" />
        <g
          transform={`translate(${x} 790)`}
          stroke="#173340"
          strokeWidth="12"
          strokeLinecap="round"
          fill="none"
        >
          <circle cx="0" cy="0" r="38" />
          <circle cx="220" cy="0" r="38" />
          <path d="M0 -15 H165 L205 -260 H155 M165 -15 L220 0" />
          <path
            d="M30 -24 L45 -176 L120 -178 L180 -246 M45 -176 L26 -280"
            stroke="#ee7956"
            strokeWidth="34"
          />
          <circle cx="25" cy="-325" r="37" fill="#dda576" strokeWidth="7" />
        </g>
      </svg>
      <TrackedFlame
        track={[
          { frame: 8, x: 0.21, y: 0.72 },
          { frame: 40, x: 0.414, y: 0.72 },
          { frame: 82, x: 0.681, y: 0.72 },
        ]}
      />
      <PopLabel text="+ 10 Urlaubs-PS" />
      <Audio
        src={staticFile("demo/zap.wav")}
        from={Math.round(0.6 * fps)}
        volume={0.3}
        premountFor={fps}
      />
    </Palette>
  );
};

const WhipScene = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: "#183e4c", overflow: "hidden" }}>
      {f < 1.5 * fps ? (
        <Img
          src={staticFile("demo/landscape.svg")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      ) : (
        <PortraitFrame src={staticFile("demo/portrait.svg")} />
      )}
      <WhipAccent
        cutFrame={Math.round(1.5 * fps)}
        frames={Math.round(0.45 * fps)}
      />
      <Audio
        src={staticFile("demo/swish.wav")}
        from={Math.round(1.3 * fps)}
        volume={0.4}
        premountFor={fps}
      />
    </AbsoluteFill>
  );
};

export const EffectsLab = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="spin"
          title="Einmal um die eigene Achse."
          number="01"
          sound="swish"
        />
      </Sequence>
      <Sequence from={3 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="download"
          title="Urlaub wird geladen."
          number="02"
          sound="blip"
        />
      </Sequence>
      <Sequence from={6 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="walkoff"
          title="Okay, ich bin dann weg."
          number="03"
          sound="swish"
        />
      </Sequence>
      <Sequence from={9 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="float"
          title="Ganz leicht im Kopf."
          number="04"
          sound="chime"
        />
      </Sequence>
      <Sequence from={12 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="launch"
          title="Abflug nach Norden."
          number="05"
          sound="zap"
        />
      </Sequence>
      <Sequence from={15 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <GagScene
          effect="boing"
          title="Noch Energie übrig."
          number="06"
          sound="boing"
        />
      </Sequence>
      <Sequence from={18 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <FaceScene />
      </Sequence>
      <Sequence from={21 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <ScooterScene />
      </Sequence>
      <Sequence from={24 * fps} durationInFrames={3 * fps} premountFor={fps}>
        <WhipScene />
      </Sequence>
      <Audio
        src={staticFile("demo/beat.wav")}
        volume={(f) => Math.min(0.45, ((27 * fps - f) / (fps * 0.35)) * 0.45)}
        premountFor={fps}
      />
    </AbsoluteFill>
  );
};

const PortraitDemo = () => (
  <PortraitFrame src={staticFile("demo/portrait.svg")} />
);
export const DemoCompositions = () => (
  <>
    <Composition
      id="EffectsLab"
      component={EffectsLab}
      durationInFrames={810}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="PortraitFraming"
      component={PortraitDemo}
      durationInFrames={90}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
