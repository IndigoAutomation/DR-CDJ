import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from 'remotion';
import { z } from 'zod';

const COLORS = {
  coral: '#d94f4f',
  peach: '#c96418',
  turquoise: '#33a89f',
  mint: '#3db88a',
  bg: '#090909',
  text: '#f0f0f0',
  textDim: '#8a8a94',
  cardBg: '#18181f',
};

const Story3Schema = z.object({
  downloadUrl: z.string(),
});

type Story3Props = z.infer<typeof Story3Schema>;

export const Story3_CTA: React.FC<Story3Props> = ({ downloadUrl }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Logo animation
  const logoScale = spring({
    frame,
    fps,
    config: { stiffness: 100, damping: 15 },
    from: 0,
    to: 1,
  });

  // Title animation
  const titleY = spring({
    frame: frame - 30,
    fps,
    config: { stiffness: 80, damping: 12 },
    from: 40,
    to: 0,
  });

  const titleOpacity = interpolate(frame, [30, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Subtitle animation
  const subtitleOpacity = interpolate(frame, [50, 70], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Button animation
  const buttonScale = spring({
    frame: frame - 90,
    fps,
    config: { stiffness: 100, damping: 12 },
    from: 0.8,
    to: 1,
  });

  const buttonOpacity = interpolate(frame, [90, 110], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // URL animation
  const urlOpacity = interpolate(frame, [120, 140], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Floating particles
  const particles = [
    { x: 10, y: 20, delay: 0, size: 8 },
    { x: 85, y: 30, delay: 20, size: 6 },
    { x: 15, y: 70, delay: 40, size: 10 },
    { x: 80, y: 65, delay: 60, size: 7 },
    { x: 5, y: 50, delay: 80, size: 5 },
    { x: 90, y: 45, delay: 100, size: 9 },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${COLORS.bg} 0%, #101015 50%, ${COLORS.bg} 100%)`,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        position: 'relative',
      }}
    >
      {/* Background gradient blob */}
      <div
        style={{
          position: 'absolute',
          width: 500,
          height: 500,
          borderRadius: '50%',
          background: `radial-gradient(circle, ${COLORS.mint}30 0%, transparent 70%)`,
          filter: 'blur(80px)',
          top: '20%',
          opacity: 0.6,
        }}
      />

      {/* Floating particles */}
      {particles.map((p, i) => (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            background: i % 2 === 0 ? COLORS.turquoise : COLORS.mint,
            opacity: interpolate(frame, [p.delay, p.delay + 30], [0, 0.6], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          }}
        />
      ))}

      {/* Logo */}
      <div
        style={{
          width: 120,
          height: 120,
          borderRadius: 28,
          background: `linear-gradient(135deg, ${COLORS.coral}, ${COLORS.peach})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 60,
          transform: `scale(${logoScale})`,
          boxShadow: `0 20px 60px ${COLORS.coral}40`,
          marginBottom: 48,
        }}
      >
        🎧
      </div>

      {/* Title */}
      <h1
        style={{
          fontSize: 64,
          fontWeight: 800,
          color: COLORS.text,
          margin: '0 0 16px 0',
          letterSpacing: -1,
          textAlign: 'center',
          transform: `translateY(${titleY}px)`,
          opacity: titleOpacity,
        }}
      >
        Ready to check
        <br />
        your audio?
      </h1>

      {/* Subtitle */}
      <p
        style={{
          fontSize: 28,
          color: COLORS.textDim,
          margin: '0 0 48px 0',
          textAlign: 'center',
          opacity: subtitleOpacity,
        }}
      >
        Free • Open Source • For macOS
      </p>

      {/* CTA Button */}
      <div
        style={{
          background: `linear-gradient(135deg, ${COLORS.mint}, ${COLORS.turquoise})`,
          borderRadius: 20,
          padding: '24px 56px',
          transform: `scale(${buttonScale})`,
          opacity: buttonOpacity,
          boxShadow: `0 16px 48px ${COLORS.mint}50`,
          marginBottom: 32,
        }}
      >
        <span
          style={{
            color: '#0a0a0d',
            fontSize: 32,
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            gap: 12,
          }}
        >
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="7 10 12 15 17 10" />
            <line x1="12" y1="15" x2="12" y2="3" />
          </svg>
          Get it free
        </span>
      </div>

      {/* URL */}
      <div
        style={{
          background: COLORS.cardBg,
          borderRadius: 12,
          padding: '16px 28px',
          border: '1px solid rgba(255,255,255,0.08)',
          opacity: urlOpacity,
        }}
      >
        <span
          style={{
            color: COLORS.textDim,
            fontSize: 20,
            fontFamily: 'monospace',
          }}
        >
          {downloadUrl.replace('https://', '')}
        </span>
      </div>

      {/* Bottom badge */}
      <div
        style={{
          position: 'absolute',
          bottom: 60,
          display: 'flex',
          alignItems: 'center',
          gap: 12,
          opacity: interpolate(frame, [150, 180], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: COLORS.mint,
            animation: 'pulse 2s infinite',
          }}
        />
        <span style={{ color: COLORS.textDim, fontSize: 18 }}>
          Link in bio
        </span>
      </div>
    </AbsoluteFill>
  );
};
