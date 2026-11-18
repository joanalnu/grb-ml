import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  integrations: [
    starlight({
      title: 'GRB-ML',
      customCss: [
        './src/styles/api.css',
        // Add the KaTeX stylesheet here
        'katex/dist/katex.min.css',
      ],
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
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
});
