name: Build APK

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Get Date
      id: get-date
      run: |
        echo "::set-output name=date::$(/bin/date -u "+%Y%m%d")"
      shell: bash

    - name: Cache Buildozer global directory
      uses: actions/cache@v4
      with:
        path: ~/.buildozer_global
        key: buildozer-global-${{ hashFiles('buildozer.spec') }}

    - name: Cache Buildozer directory
      uses: actions/cache@v4
      with:
        path: ~/.buildozer
        key: ${{ runner.os }}-${{ steps.get-date.outputs.date }}-${{ hashFiles('buildozer.spec') }}

    - name: Buildozer dependencies
      run: |
        sudo apt update
        sudo apt install -y git zip unzip python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
        sudo apt install -y libgl1-mesa-dev libgles2-mesa-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
        sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev libmtdev-dev xclip xsel

    - name: Install Python dependencies
      run: |
        pip install --upgrade pip setuptools wheel
        pip install cython==0.29.36
        pip install buildozer

    - name: Set JAVA_HOME
      run: |
        export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64

    - name: Build APK
      run: |
        export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64
        buildozer android debug --verbose

    - name: Upload APK
      uses: actions/upload-artifact@v4
      with:
        name: my-apk
        path: bin/*.apk
