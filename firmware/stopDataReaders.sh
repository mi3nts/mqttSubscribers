# LoRa Nodes
kill $(pgrep -f 'python3 loraNodesDataRead.py')
sleep 1
#python3 loraNodesDataRead.py &

# Central Nodes
kill $(pgrep -f 'python3 centralNodesDataRead.py')
sleep 1
#python3 centralNodesDataRead.py &

# UTD Nodes 
kill $(pgrep -f 'python3 utdNodesDataRead.py')
sleep 1
#python3 utdNodesDataRead.py &


