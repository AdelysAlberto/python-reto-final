FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y \
    docker.io \
    docker-compose \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN usermod -aG docker jenkins

USER jenkins

RUN jenkins-plugin-cli --plugins \
    git \
    workflow-aggregator \
    docker-workflow \
    pipeline-stage-view \
    github \
    github-branch-source
