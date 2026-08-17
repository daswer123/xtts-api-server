#!/bin/bash
clear
cat << EOF
CHIM XTTS

This will install CHIM XTTS. This is a high quality TTS service that works with Skyrim voices. 
You can also generate your own voices.
However it will require around 4GB of VRAM! 

Options:
* deepseed = Uses more VRAM but it is faster. Needs cuda13 for 50xx series GPUs.
* lowvram = Uses less VRAM but it is slower. 
* regular = Middle ground of both options above. RECOMMENDED!

If you are not sure use lowvram.

EOF

if [ ! -d /home/dwemer/python-tts ]; then
        exit "XTTSv2 not installed"
fi

mapfile -t files < <(find /home/dwemer/xtts-api-server/ -name "start-*.sh")
# Check if any files were found

if [ ${#files[@]} -eq 0 ]; then
    echo "No files found matching the pattern."
    exit 1
fi

# Display the files in a numbered list
echo -e "Select a an option from the list:\n\n"
for i in "${!files[@]}"; do
    echo "$((i+1)). ${files[$i]}"
done

echo "0. Disable service";
echo

# Prompt the user to make a selection
read -p "Select an option by picking the matching number: " selection

# Validate the input

if [ "$selection" -eq "0" ]; then
    echo "Disabling service. Run this again to enable"
    rm /home/dwemer/xtts-api-server/start.sh &>/dev/null
    exit 0
fi

if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -lt 1 ] || [ "$selection" -gt ${#files[@]} ]; then
    echo "Invalid selection."
    exit 1
fi

# Get the selected file
selected_file="${files[$((selection-1))]}"

echo "You selected: $selected_file"

ln -sf $selected_file /home/dwemer/xtts-api-server/start.sh


# Ensure all start scripts are executable
chmod +x /home/dwemer/xtts-api-server/start-*.sh 2>/dev/null || true


