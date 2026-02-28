import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Easing,
} from 'remotion';
import { z } from 'zod';
import { zColor } from '@remotion/zod-types';

// Brand colors from Dr. CDJ
const COLORS = {
  coral: '#d94f4f',
  peach: '#c96418',
  turquoise: '#33a89f',
  bg: '#090909',
  text: '#f0f0f0',
  textDim: '#8a8a94',
};

const Story1Schema = z.object({
  productName: z.string(),
  tagline: z.string(),
});

type Story1Props = z.infer<typeof Story1Schema>;

export const Story1_Intro: React.FC<Story1Props> = ({ productName, tagline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo animation (0-60 frames)
  const logoScale = spring({
    frame,
    fps,
    config: { stiffness: 100, damping: 15 },
    from: 0,
    to: 1,
  });

  const logoOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Product name animation (30-90 frames)
  const titleY = spring({
    frame: frame - 30,
    fps,
    config: { stiffness: 80, damping: 12 },
    from: 50,
    to: 0,
  });

  const titleOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Tagline animation (60-120 frames)
  const taglineY = spring({
    frame: frame - 60,
    fps,
    config: { stiffness: 80, damping: 12 },
    from: 30,
    to: 0,
  });

  const taglineOpacity = interpolate(frame, [60, 80], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Background gradient animation
  const bgOpacity = interpolate(frame, [0, 30], [0.3, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${COLORS.bg} 0%, #101015 100%)`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Animated background blob */}
      <div
        style={{
          position: 'absolute',
          width: 600,
          height: 600,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${COLORS.coral}40 0%, transparent 70%)`,
          filter: 'blur(80px)',
          top: '10%',
          opacity: bgOpacity * 0.5,
          animation: 'pulse 4s ease-in-out infinite',
        }}
      />

      {/* Logo icon */}
      <div
        style={{
          width: 140,
          height: 140,
          borderRadius: 32,
          background: `linear-gradient(135deg, ${COLORS.coral}, ${COLORS.peach})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 72,
          transform: `scale(${logoScale})`,
          opacity: logoOpacity,
          boxShadow: `0 20px 60px ${COLORS.coral}50`,
          marginBottom: 40,
        }}
      >
        🎧
      </div>

      {/* Product name */}
      <h1
        style={{
          fontSize: 80,
          fontWeight: 800,
          color: COLORS.text,
          margin: 0,
          letterSpacing: -2,
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
          textAlign: 'center',
        }}
      >
        {productName}
      </h1>

      {/* Tagline */}
      <p
        style={{
          fontSize: 36,
          fontWeight: 500,
          color: COLORS.textDim,
          marginTop: 16,
          letterSpacing: 0.5,
          transform: `translateY(${taglineY}px)`,
          opacity: taglineOpacity,
          textAlign: 'center',
        }}
      >
        {tagline}
      </p>

      {/* Subtle hint at bottom */}
      <div
        style={{
          position: 'absolute',
          bottom: 80,
          opacity: interpolate(frame, [120, 150], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            width: 4,
            height: 40,
            background: `linear-gradient(180deg, ${COLORS.turquoise}, transparent)`,
            borderRadius: 2,
          }}
        />
        <span
          style={{
            color: COLORS.turquoise,
            fontSize: 20,
            marginTop: 12,
            fontWeight: 600,
          }}
        >
          Swipe up →
        </span>
      </div>
    </AbsoluteFill>
  );
};
