/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: [
    '@mui/x-data-grid',
    '@mui/x-data-grid-pro',
    '@mui/x-data-grid-premium',
  ],
  // Optional: Enable React Strict Mode (recommended for development)
  reactStrictMode: true,
  // Optional: Configure webpack if needed
  webpack: (config) => {
    // Add any webpack configurations here if needed
    return config;
  },
};

export default nextConfig;
