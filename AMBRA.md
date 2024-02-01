ws="https://critical-work.com"

!curl -sL "{ws}/wp-json/wp/v2/pages" | jq '.[]'
!curl -sL "{ws}/wp-json/wp/v2/pages" | jq '.[] | {{id, link}}'

!curl -sL $WS/wp-json/wp/v2/pages/110 | jq '. | keys'

!curl -sL $WS/wp-json/wp/v2/pages/110 | jq '.content | keys'
