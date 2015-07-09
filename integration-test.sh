#!/usr/bin/env sh
USER_BASE="http://127.0.0.1:5000/users"
GROUP_BASE="http://127.0.0.1:5000/groups"
JSON_HEADER="-H \"Content-type: application/json\""

USER1="Brian"
USER2="John"
GROUP1="group1"
GROUP2="group2"

USER1_GET="GET $USER_BASE/$USER1"
GROUP1_GET="GET $GROUP_BASE/$GROUP1"
USER2_GET="GET $USER_BASE/$USER2"
GROUP2_GET="GET $GROUP_BASE/$GROUP2"

START_TEST="\n-----"
END_TEST="-----\n"
LINE_MARKER="\n+++++++++++++++++++"

echo "$START_TEST TEST USER CREATION"
USER_POST="POST $USER_BASE/ -d '{\"userid\":\"$USER1\", \"first_name\":\"Brian\"}' $JSON_HEADER"
echo $USER_POST
eval "curl -X $USER_POST"

echo "$USER1_GET"
eval "curl -X $USER1_GET"
echo $END_TEST

echo "$START_TEST TEST DUPLICATE USER"
echo $USER_POST
echo "curl -X $USER_POST"
echo $END_TEST

echo "$START_TEST TEST USER UPDATE$LINE_MARKER"
USER_PUT="PUT $USER_BASE/Brian -d '{\"userid\":\"$USER1\", \"first_name\":\"Brian\", \"last_name\":\"Hansen\",\"groups\":[\"$GROUP1\"]}' $JSON_HEADER"
echo "+ Update $USER1 with last_name and groups:['$GROUP1']"
echo "$USER_PUT"
eval "curl -X $USER_PUT"

echo "\n+ $USER1 should have a last_name and groups now$LINE_MARKER"
echo $USER1_GET
eval "curl -X $USER1_GET"

echo "\n+ $GROUP1 should have been automatically created when $USER1 had groups added$LINE_MARKER"
echo $GROUP1_GET
eval "curl -X $GROUP1_GET"
echo $END_TEST

echo "$START_TEST TEST GROUP UPDATE$LINE_MARKER"
echo "+ Update $GROUP1 to have no users"
GROUP_PUT="PUT $GROUP_BASE/$GROUP1 -d '[]' $JSON_HEADER"
echo $GROUP_PUT
eval "curl -X $GROUP_PUT"

echo "\n+ $GROUP1 user list should be empty$LINE_MARKER"
echo $GROUP1_GET
eval "curl -X $GROUP1_GET"

echo "\n+ $USER1 should no longer be a member of $GROUP1 $LINE_MARKER"
echo $USER1_GET
eval "curl -X $USER1_GET"
echo $END_TEST

echo "$START_TEST TEST GROUP CREATION + MISSING USER EDGE CASE"
GROUP_POST="POST $GROUP_BASE/ -d '{\"name\":\"$GROUP2\"}' $JSON_HEADER"
echo "+ Make a new group: $GROUP2"
echo $GROUP_POST
eval "curl -X $GROUP_POST"

echo "\n+ Update $GROUP2 with 1 real user and 1 fake user$LINE_MARKER"
GROUP_PUT="PUT $GROUP_BASE/$GROUP2 -d '[\"$USER1\", \"$USER2\"]' $JSON_HEADER"
echo $GROUP_PUT
eval "curl -X $GROUP_PUT"

echo "\n+ $GROUP2 should only have 1 user, the existing $USER1, on the list$LINE_MARKER"
echo $GROUP2_GET
eval "curl -X $GROUP2_GET"

echo "\n+ Create $USER2 and try again$LINE_MARKER"
USER_POST="POST $USER_BASE/ -d '{\"userid\":\"$USER2\", \"first_name\":\"John\", \"last_name\":\"Doe\"}' $JSON_HEADER"
echo $USER_POST
eval "curl -X $USER_POST"
echo $GROUP_PUT
eval "curl -X $GROUP_PUT"

echo "\n+ Both users should be in $GROUP2$LINE_MARKER"
echo $USER1_GET
eval "curl -X $USER1_GET"
echo $USER2_GET
eval "curl -X $USER2_GET"
echo $END_TEST

echo "$START_TEST TEST USER DELETION"
USER_DELETE="DELETE $USER_BASE/$USER2"
echo $USER_DELETE
eval "curl -X $USER_DELETE"
echo $USER2_GET
eval "curl -X $USER2_GET"

echo "\n+ $GROUP2 user list should no longer contain deleted $USER2 $LINE_MARKER"
echo $GROUP2_GET
eval "curl -X $GROUP2_GET"
echo "$END_TEST"

echo "$START_TEST TEST GROUP DELETION"
GROUP_DELETE="DELETE $GROUP_BASE/$GROUP2"
echo $GROUP_DELETE
eval "curl -X $GROUP_DELETE"
echo $GROUP2_GET
eval "curl -X $GROUP2_GET"

echo "\n+ $USER1 should no longer be in $GROUP2 $LINE_MARKER"
echo $USER1_GET
eval "curl -X $USER1_GET"
echo $END_TEST

