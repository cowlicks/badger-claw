#!/usr/bin/env bash
set -e
source config.py
pb_path=../privacybadger
repo=origin
branch=master

do_crawl=0  # zero is yes

mkdir -p results


if [[ $ONLY_ON_UPDATE -eq 1 ]]; then
    pushd $pb_path
    git fetch $repo
    git diff-index $repo/$branch --quiet
    do_crawl=$?
    popd
fi


if [[ $do_crawl -eq 0 ]]; then
    pushd $pb_path
    # there was a change upstream. So we update the repo and run the crawler
    git rebase $repo/$branch --quiet
    make zip
    make crx
    export EXTENSION_PATH=$(ls -t *.crx | head -1 | xargs readlink -f)
    popd
    source env/bin/activate
    ./main.py
    if [[ $PUSH_TO_S3 -eq 1 ]]; then
        aws s3 sync --region us-east-2 results/ s3://badgers.cowlicks.website/results/
    fi
    deactivate
fi
