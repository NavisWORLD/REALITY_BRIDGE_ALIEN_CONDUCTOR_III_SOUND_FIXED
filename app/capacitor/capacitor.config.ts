import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'world.navis.cosmicconductor',
  appName: 'Cosmic Conductor',
  webDir: 'www',
  server: {
    androidScheme: 'https',
    hostname: 'localhost'
  }
};

export default config;
