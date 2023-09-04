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
curl -JLO https://github.com/WattRex/Regenerative-Battery-Cycler/archive/$latest_tag.tar.gz

# -----------------------------------------------------------------
