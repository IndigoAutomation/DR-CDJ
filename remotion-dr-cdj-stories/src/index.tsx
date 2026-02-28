import { Composition, registerRoot } from 'remotion';
import { Story1_Intro } from './stories/Story1_Intro';
import { Story2_Features } from './stories/Story2_Features';
import { Story3_CTA } from './stories/Story3_CTA';

// Instagram Stories dimensions: 1080x1920, 30fps
// Each story: 7 seconds (210 frames at 30fps)

const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* Story 1: Intro - Brand reveal */}
      <Composition
        id="Story1-Intro"
        component={Story1_Intro}
        durationInFrames={210}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          productName: "Dr. CDJ",
          tagline: "Audio Compatibility Checker",
        }}
      />

      {/* Story 2: Features showcase */}
      <Composition
        id="Story2-Features"
        component={Story2_Features}
        durationInFrames={210}
        fps={30}
        width={1080}
        height={1920}
      />

      {/* Story 3: Call to Action */}
      <Composition
        id="Story3-CTA"
        component={Story3_CTA}
        durationInFrames={210}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          downloadUrl: "https://indigoautomation.github.io/DR-CDJ/",
        }}
      />
    </>
  );
};

registerRoot(RemotionRoot);
