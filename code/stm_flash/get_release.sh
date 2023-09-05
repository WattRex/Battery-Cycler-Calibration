#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------
WS_PATH=$(cd .. && pwd)
FW_WS="${WS_PATH}/fw_code"
cd $FW_WS
# --- Options processing -------------------------------------------

# --- Locks -------------------------------------------------------

# --- Body --------------------------------------------------------
latest_tag=$(curl -s https://api.github.com/repos/WattRex/Regenerative-Battery-Cycler/releases/latest | sed -Ene '/^ *"tag_name": *"(v.+)",$/s//\1/p')
echo "Using version $latest_tag"
repo_url="https://github.com/WattRex/Regenerative-Battery-Cycler/archive/$latest_tag.tar.gz"
curl_output=$(curl -JLO ${repo_url} 2> /dev/null)
err_code=$?
if [ ${err_code} -eq 23 ] || [ ${err_code} -eq 0 ]; then
    if [ ${err_code} -eq 23 ]; then
        echo "Binary file already downloaded"
        # Remove first char from string latest_tag
        bin_file=$(ls ./*${latest_tag:1}.tar.gz)
    else
        bin_file=$(echo ${curl_output} | cut -d\' -f2)
    fi
    
    echo "Lastest release downloaded: $bin_file"
    release_path=$(basename "$bin_file" .tar.gz)
    tar -xvf $bin_file > /dev/null && rm $bin_file
    FW_CODE="${FW_WS}/firmware"
    if [ -d "${FW_CODE}" ]; then
        echo "Removing old firmware content: ${FW_CODE}"
        rm -r "${FW_CODE}/"
    fi
    mkdir -p "${FW_CODE}"

    mv $release_path/firmware/* ${FW_CODE}/ && rm -r $release_path
    cd ${FW_CODE} && cp -r project_config/EPC_CONF/ Sources/
    echo "Done"

else
    echo "Error downloading binary file. Error: ${err_code}"
    exit 1
fi
# -----------------------------------------------------------------
