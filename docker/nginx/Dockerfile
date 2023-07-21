FROM nginx:1.15.12 AS base

RUN rm /etc/nginx/conf.d/default.conf


FROM base AS prod

COPY nginx.template /etc/nginx/nginx.template

EXPOSE 80

EXPOSE 8888

EXPOSE 443


FROM base AS local

COPY nginx.local.template /etc/nginx/nginx.template

EXPOSE 80

EXPOSE 8888