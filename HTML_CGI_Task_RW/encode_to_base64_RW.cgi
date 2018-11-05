#!/bin/bash

function urlencode {

  local url_encoded="${1//+/ }"
  printf '%b' "${url_encoded//%/\\x}"

}

[ -z "$POST_STRING" -a "$REQUEST_METHOD" == "POST" -a ! -z "$CONTENT_LENGTH" ] && read -n $CONTENT_LENGTH POST_STRING

OIFS=$IFS
IFS='=&'

parm_get=($QUERY_STRING)
parm_post=($POST_STRING)

IFS=$OIFS

declare -A get
declare -A post


for ((i=0; i<${#parm_get[@]}; i+=2)); do
  get[${parm_get[i]}]=$(urlencode ${parm_get[i+1]})
done


for ((i=0; i<${#parm_post[@]}; i+=2)); do
  post[${parm_post[i]}]=$(urlencode ${parm_post[i+1]})
done

encoded_text=$(echo ${post[to_be_encoded_text]} | openssl base64)

echo "Content: text/html"
echo
cat <<EOT
<!DOCTYPE html>
<html>
<head></head>
<body>
<p> Dear <b>${post[title]} ${post[name]}</b>, please find your Base64 encoded string below. </p>
<hr>
<p><b>${encoded_text}</b></p>
<a href="/encode_to_base64.html">BACK</a>
</body>
</html>
EOT
