#!/usr/bin/env bash
pb_path=../privacybadger
repo=origin
branch=master

mkdir -p results

pushd $pb_path
git fetch $repo
git diff-index $repo/$branch --quiet
res=$?
popd
if [[ $? -ne 0 ]]; then
    pushd $pb_path
    # there was a change upstream. So we update the repo and run the crawler
    git rebase $repo/$branch --quiet
    make zip
    make crx
    export EXTENSION_PATH=$(ls -t *.crx | head -1 | xargs readlink -f)
    commit=$(git rev-parse HEAD)
    now=$(date +"%Y_%m_%d_%I_%M_%p")
    file_suffix=$now-$commit.json
    export OUT_FILE=results/data-$file_suffix
    popd
    source env/bin/activate
    ./crawler.py
    ./analysis.py $OUT_FILE
    ./update_index.py $file_suffix
    deactivate
fi
