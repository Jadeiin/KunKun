#!/bin/bash

# Define the server IP and port
SERVER_IP="127.0.0.1"
SERVER_PORT=7979

# Establish a socket connection with the server
exec 3<>/dev/tcp/$SERVER_IP/$SERVER_PORT

# Variable to store the logged-in user ID
user_id=""

# Function to display a message box
show_message() {
    dialog --backtitle "TUI Client" --msgbox "$1" 10 40
}

# Function to display a form and get user input
get_input() {
    dialog --backtitle "$1" --inputbox "$2" 10 40 2>&1 >/dev/tty
}

# Function to send a request to the server and receive the response
send_request() {
    request="$1"
    echo "$request" >&3
    response=$(timeout 1.0 cat <&3)
    echo "$response"
}

# Function to calculate the SHA1 hash of a string
sha1_hash() {
    echo -n "$1" | sha1sum | awk '{print $1}'
}

# Function to parse the response from the server and perform actions accordingly
parse_response() {
    response="$1"
    type=$(echo "$response" | jq -r '.type')
    result=$(echo "$response" | jq -r '.result')

    case "$type" in
        "acceptregister")
            if [[ "$result" == "true" ]]; then
                user_id=$(echo "$response" | jq -r '.userid')
                show_message "Registration successful!\nUser ID: $user_id"
            else
                show_message "Registration failed!"
            fi
            ;;
        "acceptlogin")
            if [[ "$result" == "true" ]]; then
                user_id=$(echo "$response" | jq -r '.userid')
                show_message "Login successful!\nUser ID: $user_id"
            else
                show_message "Login failed!"
            fi
            ;;
        "acceptroom")
            if [[ "$result" == "true" ]]; then
                roomid=$(echo "$response" | jq -r '.roomid')
                roomname=$(echo "$response" | jq -r '.roomname')
                show_message "Room created successfully!\nRoom ID: $roomid\nRoom Name: $roomname"
            else
                show_message "Room creation failed!"
            fi
            ;;
        "acceptmsg")
            if [[ "$result" == "true" ]]; then
                msgid=$(echo "$response" | jq -r '.msgid')
                senderid=$(echo "$response" | jq -r '.userid')
                roomid=$(echo "$response" | jq -r '.roomid')
                content=$(echo "$response" | jq -r '.content')
                time=$(echo "$response" | jq -r '.time')
                show_message "Message sent successfully!\nSender ID: $senderid\nRoom ID: $roomid\nContent: $content\nTime: $time"
            else
                show_message "Message send failed!"
            fi
            ;;
        *)
            show_message "Unknown response type: $type\nOriginal response: $response"
            ;;
    esac
}

# Main loop
while true; do
    # Display menu options
    choice=$(dialog --title "TUI Client" --menu "Choose an option:" 12 40 5 \
        1 "Register" \
        2 "Login" \
        3 "Create Room" \
        4 "Send Message" \
        0 "Exit" 2>&1 >/dev/tty)

    case "$choice" in
        1)
            username=$(get_input "Register" "Enter username:")
            password=$(get_input "Register" "Enter password:")
            password_hash=$(sha1_hash "$password")
            request="{ \"type\": \"register\", \"username\": \"$username\", \"userpwdhash\": \"$password_hash\" }"
            response=$(send_request "$request")
            parse_response "$response"
            ;;
        2)
            username=$(get_input "Login" "Enter username:")
            password=$(get_input "Login" "Enter password:")
            password_hash=$(sha1_hash "$password")
            request="{ \"type\": \"login\", \"username\": \"$username\", \"userpwdhash\": \"$password_hash\" }"
            response=$(send_request "$request")
            parse_response "$response"
            ;;
        3)
            member_id=$(get_input "Create Room" "Enter room member id:")
            roomname=$(get_input "Create Room" "Enter room name:")
            request="{ \"type\": \"createroom\", \"adminid\": [$user_id], \"memberid\": [$member_id], \"roomname\": \"$roomname\" }"
            response=$(send_request "$request")
            parse_response "$response"
            ;;
        4)
            userid=$(get_input "Send Message" "Enter user ID:")
            roomid=$(get_input "Send Message" "Enter room ID:")
            content=$(get_input "Send Message" "Enter message content:")
            request="{ \"type\": \"sendmsg\", \"userid\": \"$userid\", \"roomid\": \"$roomid\", \"content\": \"$content\" }"
            response=$(send_request "$request")
            parse_response "$response"
            ;;
        0)
            # Close the socket connection
            exec 3<&-
            exec 3>&-
            break
            ;;
        *)
            show_message "Invalid option!"
            ;;
    esac
done