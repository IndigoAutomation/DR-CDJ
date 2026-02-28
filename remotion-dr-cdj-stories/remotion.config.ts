import { Config } from "@remotion/cli/config";

// Instagram Stories: 1080x1920, 30fps
Config.setVideoImageFormat('jpeg');
Config.setConcurrency(4);
Config.setChromiumOpenGlRenderer('angle');
