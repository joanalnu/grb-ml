import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'My Python Package Docs',
      customCss: [],
      sidebar: [
        {
          label: 'Home',
          link: '/',
        },
        {
          label: 'API Reference',
          // Automatically generates sidebar links for all files in docs/src/content/docs/reference
          items: [{ autogenerate: { "directory": "reference" } }]
        },
      ],
    }),
  ],
});
