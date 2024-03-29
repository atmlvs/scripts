# Flutter (https://flutter.dev) Development Environment for Linux
# ===============================================================
#
# This environment passes all Linux Flutter Doctor checks and is sufficient
# for building Android applications and running Flutter tests.
#
# To build iOS applications, a Mac development environment is necessary.
#
# This includes applications and sdks that are needed only by the CI system
# for performing pushes to production, and so this image is quite a bit larger
# than strictly needed for just building Flutter apps.

# Last manual update 2020-10-05 (changing this comment will re-build image)

# Note: updating past stretch (Debian 9) will bump Java past version 8,
# which will break the Android SDK.
FROM debian:stretch
MAINTAINER Flutter Developers <flutter-dev@googlegroups.com>

RUN apt-get update -y
RUN apt-get upgrade -y

# Install basics
RUN apt-get install -y --no-install-recommends \
    git \
    wget \
    curl \
    zip \
    unzip \
    apt-transport-https \
    ca-certificates \
    gnupg

# Add repo for chrome stable
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list

# Add repo for gcloud sdk and install it
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

RUN apt-get update && apt-get install -y google-cloud-sdk && \
    gcloud config set core/disable_usage_reporting true && \
    gcloud config set component_manager/disable_update_check true

# Add nodejs repository to apt sources and install it.
ENV NODEJS_INSTALL="/opt/nodejs_install"
RUN mkdir -p "${NODEJS_INSTALL}"
RUN wget -q https://deb.nodesource.com/setup_10.x -O "${NODEJS_INSTALL}/nodejs_install.sh"
RUN bash "${NODEJS_INSTALL}/nodejs_install.sh"

# Install the rest of the dependencies.
RUN apt-get install -y --no-install-recommends \
    locales \
    gcc \
    ruby \
    ruby-dev \
    nodejs \
    lib32stdc++6 \
    libstdc++6 \
    libglu1-mesa \
    build-essential \
    default-jdk-headless \
    google-chrome-stable

# Install the Android SDK Dependency.
ENV ANDROID_SDK_URL="https://dl.google.com/android/repository/sdk-tools-linux-4333796.zip"
ENV ANDROID_TOOLS_ROOT="/opt/android_sdk"
RUN mkdir -p "${ANDROID_TOOLS_ROOT}"
RUN mkdir -p ~/.android
# Silence warning.
RUN touch ~/.android/repositories.cfg
ENV ANDROID_SDK_ARCHIVE="${ANDROID_TOOLS_ROOT}/archive"
RUN wget --progress=dot:giga "${ANDROID_SDK_URL}" -O "${ANDROID_SDK_ARCHIVE}"
RUN unzip -q -d "${ANDROID_TOOLS_ROOT}" "${ANDROID_SDK_ARCHIVE}"
# Suppressing output of sdkmanager to keep log size down
# (it prints install progress WAY too often).
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "tools" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "build-tools;28.0.3" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "platforms;android-30" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "platform-tools" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "extras;android;m2repository" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "extras;google;m2repository" > /dev/null
RUN yes "y" | "${ANDROID_TOOLS_ROOT}/tools/bin/sdkmanager" "patcher;v4" > /dev/null
RUN rm "${ANDROID_SDK_ARCHIVE}"
ENV PATH="${ANDROID_TOOLS_ROOT}/tools:${PATH}"
ENV PATH="${ANDROID_TOOLS_ROOT}/tools/bin:${PATH}"
# Silence warnings when accepting android licenses.
RUN mkdir -p ~/.android
RUN touch ~/.android/repositories.cfg

# Add npm to path.
ENV PATH="/usr/bin:${PATH}"
RUN dpkg-query -L nodejs
# Install Firebase
# This is why we need nodejs installed.
RUN /usr/bin/npm --verbose install -g firebase-tools

# Install golang more recent than in repo (necessary for dashing to build)
RUN curl 'https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz' | tar xvz
ENV GOBINARY=/go/bin/go

# Install dashing
RUN mkdir -p /opt/gopath/bin
ENV GOPATH=/opt/gopath
ENV PATH="${GOPATH}/bin:${PATH}"
RUN $GOBINARY get -u github.com/technosophos/dashing

# Set locale to en_US
RUN locale-gen en_US "en_US.UTF-8" && dpkg-reconfigure locales
ENV LANG en_US.UTF-8

# Install fastlane via pinned Gemfile & Gemfile.lock
# Skip all the documentation (-N) since it's just on CI.
RUN gem install bundler -N

# Gemfile last edited 1/6/2019 (update to trigger a rebuild of Docker image)
COPY ci/docker_linux/Gemfile /Gemfile
COPY ci/docker_linux/Gemfile.lock /Gemfile.lock

RUN bundle config set system 'true' && \
    bundle install --system
