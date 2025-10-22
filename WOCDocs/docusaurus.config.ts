import type { Config } from '@docusaurus/types';

const config: Config = {
  title: 'wOpenChat Lite Docs',
  tagline: 'wOpenChat Lite Documentation for Developers and maintainers',
  favicon: 'img/favicon.png',

  url: 'https://3000--main--wopenchat-lite--arnayk.wyra.net',
  baseUrl: '/wOpenChat-Lite/',

  organizationName: 'w-y-r-a',
  projectName: 'wOpenChat-Lite',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],
};

export default config;
