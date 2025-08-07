ulimit -c unlimited
ulimit -n 4096 
bash scripts/7_gstacks_create_script.sh  > scripts/7_gstacks_command.sh

bash scripts/7_gstacks_command.sh