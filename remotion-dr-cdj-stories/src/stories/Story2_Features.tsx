import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  Sequence,
} from 'remotion';

const COLORS = {
  coral: '#d94f4f',
  peach: '#c96418',
  turquoise: '#33a89f',
  mint: '#3db88a',
  sunshine: '#c9a820',
  lavender: '#8b50d4',
  bg: '#090909',
  text: '#f0f0f0',
  textDim: '#8a8a94',
  cardBg: '#18181f',
};

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  color: string;
  delay: number;
}

const FeatureCard: React.FC<FeatureCardProps> = ({
  icon,
  title,
  description,
  color,
  delay,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({
    frame: frame - delay,
    fps,
    config: { stiffness: 100, damping: 15 },
    from: 0.8,
    to: 1,
  });

  const opacity = interpolate(frame, [delay, delay + 15], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const translateY = spring({
    frame: frame - delay,
    fps,
    config: { stiffness: 100, damping: 15 },
    from: 40,
    to: 0,
  });

  return (
    <div
      style={{
        background: COLORS.cardBg,
        borderRadius: 24,
        padding: 28,
        marginBottom: 16,
        border: '1px solid rgba(255,255,255,0.08)',
        transform: `scale(${scale}) translateY(${translateY}px)`,
        opacity,
        display: 'flex',
        alignItems: 'center',
        gap: 20,
      }}
    >
      <div
        style={{
          width: 64,
          height: 64,
          borderRadius: 18,
          background: `${color}20`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 32,
          flexShrink: 0,
        }}
      >
        {icon}
      </div>
      <div style={{ flex: 1 }}>
        <h3
          style={{
            color: COLORS.text,
            fontSize: 28,
            fontWeight: 700,
            margin: '0 0 6px 0',
          }}
        >
          {title}
        </h3>
        <p
          style={{
            color: COLORS.textDim,
            fontSize: 20,
            margin: 0,
            lineHeight: 1.4,
          }}
        >
          {description}
        </p>
      </div>
    </div>
  );
};

export const Story2_Features: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const features = [
    {
      icon: '📁',
      title: 'Drag & Drop',
      description: 'Drop files or folders. Instant analysis.',
      color: COLORS.turquoise,
      delay: 30,
    },
    {
      icon: '🎛️',
      title: 'Multi-Player Support',
      description: 'CDJ-2000, CDJ-3000, XDJ series.',
      color: COLORS.sunshine,
      delay: 60,
    },
    {
      icon: '⚡',
      title: 'Batch Processing',
      description: 'Convert hundreds of files at once.',
      color: COLORS.mint,
      delay: 90,
    },
    {
      icon: '🎵',
      title: 'Studio Quality',
      description: 'Up to 24-bit / 96kHz output.',
      color: COLORS.lavender,
      delay: 120,
    },
  ];

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${COLORS.bg} 0%, #0d0d12 100%)`,
        display: 'flex',
        flexDirection: 'column',
        padding: '60px 40px',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Header */}
      <div style={{ marginBottom: 40, opacity: titleOpacity }}>
        <span
          style={{
            color: COLORS.turquoise,
            fontSize: 20,
            fontWeight: 600,
            letterSpacing: 2,
            textTransform: 'uppercase',
          }}
        >
          Features
        </span>
        <h2
          style={{
            color: COLORS.text,
            fontSize: 52,
            fontWeight: 800,
            margin: '12px 0 0 0',
            letterSpacing: -1,
          }}
        >
          Everything you need
        </h2>
      </div>

      {/* Feature cards */}
      <div style={{ flex: 1 }}>
        {features.map((feature, index) => (
          <FeatureCard key={index} {...feature} />
        ))}
      </div>

      {/* Brand badge at bottom */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 12,
          marginTop: 20,
          opacity: interpolate(frame, [150, 180], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        }}
      >
        <div
          style={{
            width: 12,
            height: 12,
            borderRadius: 4,
            background: `linear-gradient(135deg, ${COLORS.coral}, ${COLORS.peach})`,
          }}
        />
        <span style={{ color: COLORS.textDim, fontSize: 18, fontWeight: 600 }}>
          Dr. CDJ
        </span>
      </div>
    </AbsoluteFill>
  );
};
