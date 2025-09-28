# Node.js LTS 버전 사용
FROM node:18-alpine AS base

# 1. 의존성 설치 단계
FROM base AS deps
WORKDIR /app
# package.json 파일만 복사하여 의존성 레이어 캐싱
COPY package.json package-lock.json ./
RUN npm install

# 2. 빌드 단계
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
# 소스 코드 복사
COPY . .
# Next.js 앱 빌드 (프론트엔드 최적화)
RUN npm run build

# 3. 최종 실행 단계 (최적화된 런타임 이미지)
FROM node:18-alpine AS runner
WORKDIR /app
# 환경 변수 설정
ENV NODE_ENV production

# 빌드 결과만 복사
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# 서버 실행 명령어 (Next.js 시작)
EXPOSE 3000
CMD ["npm", "start"]