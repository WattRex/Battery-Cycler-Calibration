#!/bin/bash
# ------------------------------------------------------------------
# [Author] Title
#          Description
# ------------------------------------------------------------------

# --- Options processing -------------------------------------------

# --- Locks -------------------------------------------------------

# --- Body --------------------------------------------------------
latest_tag=$(curl -s https://api.github.com/repos/WattRex/Regenerative-Battery-Cycler/releases/latest | sed -Ene '/^ *"tag_name": *"(v.+)",$/s//\1/p')
echo "Using version $latest_tag"
bin_file=$(curl -JLO https://github.com/WattRex/Regenerative-Battery-Cycler/archive/$latest_tag.tar.gz | cut -d\' -f2)
file_name=$(basename "$bin_file" .tar.gz)
if [ $? -ne 0 ]; then
    echo "Error downloading binary file"
    exit 1
else
    tar -xvf $bin_file > /dev/null && rm $bin_file
    rm -r ../fw_code/firmware/ && mv $file_name/firmware/ ../fw_code/ && rm -r $file_name
    cp -r ../fw_code/firmware/project_config/EPC_CONF/ ../fw_code/firmware/Sources/
    echo "Done"


fi
# -----------------------------------------------------------------
