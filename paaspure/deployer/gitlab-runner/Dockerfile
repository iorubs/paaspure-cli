FROM gitlab/gitlab-runner:latest

LABEL maintainer "ruben.vasconcelos3@mail.dcu.ie"

# Install and setup docker.
RUN curl -sSL https://get.docker.com/ | sh

# Setup docker-compose.
ENV COMPOSE_URL https://github.com/docker/compose/releases/download/1.20.1/docker-compose-Linux-x86_64
RUN curl -L $COMPOSE_URL -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

ENTRYPOINT ["gitlab-runner"]
CMD ["run", "--working-directory=/home/gitlab-runner"]
