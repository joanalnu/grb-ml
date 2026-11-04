import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  integrations: [
    starlight({
      title: 'GRB-ML',
      customCss: [],
      sidebar: [
        {
          label: 'Home',
          link: '/',
        },
        {
          label: 'Manual',
          items: [{ autogenerate: { "directory": "manual" } }]
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
