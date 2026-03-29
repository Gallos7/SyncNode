# -----------------------------------------------------------------------------
# STAGE: Development Build Environment
# Using the lightweight 'alpine' variant of Node.js for smaller, more secure images.
# Node 20 is the current LTS (Long-Term Support) version.
# -----------------------------------------------------------------------------
FROM node:20-alpine

# Set the working directory within the container's filesystem.
WORKDIR /app

# -----------------------------------------------------------------------------
# LAYER OPTIMIZATION: Dependency Installation
# Copy dependency lists (package.json and package-lock.json*) first.
# By copying only these files, we ensure that the 'npm install' step is cached
# unless dependencies are explicitly added/changed.
# -----------------------------------------------------------------------------
COPY package.json package-lock.json* ./

# -----------------------------------------------------------------------------
# OPTIONAL BUT RECOMMENDED: Ensure Node Package Manager (NPM) is Up-to-Date.
# This eliminates "npm notice New version available" warnings from build logs
# and ensures we are using modern security protocols in the installer.
# -----------------------------------------------------------------------------
RUN npm install -g npm@latest

# Install dependencies using npm.
# For production builds, one would typically use `npm ci --only=production`.
RUN npm install

# -----------------------------------------------------------------------------
# APPLICATION SOURCE CODE COPY
# Copy the entire frontend source code directory into the container.
# This layer will be rebuilt frequently as the application is developed.
# -----------------------------------------------------------------------------
COPY . .

# Inform Docker that the container intends to listen on port 5173 at runtime.
# This documentation facilitates port mapping in docker-compose.yml.
EXPOSE 5173

# -----------------------------------------------------------------------------
# CONTAINER EXECUTION COMMAND
# Starts the frontend development server (e.g., Vite or standard Create React App).
# The --host flag is critical; it ensures the dev server broadcasts beyond localhost
# to all network interfaces within the private Docker network, allowing connectivity
# to the mapped host port (5173).
# -----------------------------------------------------------------------------
CMD ["npm", "run", "dev", "--", "--host"]