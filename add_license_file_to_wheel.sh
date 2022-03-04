#!/bin/bash
# Shell script to include the LICENSE text file to a wheel.
# Remove once maturin adds built-in support for this:
# https://github.com/PyO3/maturin/issues/829
set -e

dist_name=pngquant_cli
tmp_dir="wheels-temp"

mkdir -p $tmp_dir
for wheel_file in "$@"
do
    echo "Adding LICENSE to $wheel_file"
    python -m wheel unpack -d $tmp_dir "$wheel_file"
    unpacked_wheel=$(find $tmp_dir -type d -name $dist_name'*' -maxdepth 1)
    distinfo=$(find $unpacked_wheel -type d -name $dist_name'*.dist-info' -maxdepth 1)
    cp LICENSE $distinfo
    dest=$(dirname "$wheel_file")
    python -m wheel pack -d "$dest" "$unpacked_wheel"
    rm -rf "$unpacked_wheel"
    echo
done
rm -rf $tmp_dir
