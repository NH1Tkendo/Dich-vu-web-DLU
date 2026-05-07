# Stage 1: Build React app
FROM node:20-alpine AS build-stage

WORKDIR /app

# Khai báo build argument cho API URL
ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Sao chép package.json và cài đặt dependencies
COPY package*.json ./
RUN npm install

# Sao chép mã nguồn và build dự án
COPY . .
RUN npm run build

# Stage 2: Serve với Nginx
FROM nginx:stable-alpine

# Sao chép file build từ stage 1 vào thư mục mặc định của Nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Sao chép file cấu hình Nginx tùy chỉnh (nếu có)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
