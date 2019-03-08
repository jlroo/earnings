#!/bin/bash

# filename: earnings.sh
# author: @jlroo

START=''
END=''
PAG=''
HTTP_ERRORS=''
SINGLE=''

print_usage() {
  printf "Usage: ..."
}

while getopts 'b:e:f:g:sjt' flag; do
  case "${flag}" in
    b) START="${OPTARG}" ;;
    e) END="${OPTARG}" ;;
    f) HTTP_ERRORS="${OPTARG}" ;;
    g) PAG="${OPTARG}" ;;
    s) SINGLE=true ;;
    l) LOOP=true ;;
    t) TEST=true ;;
    *) print_usage
       exit 1 ;;
  esac
done


# ./earnings.sh -g 10 --> Scrape pag 10
if [[ "${PAG}" != "" ]]; then
  python3 seeking_alpha/proxy.py &
  sleep 3
  scrapy crawl earnings -a pag="${PAG}" -o data/$(printf %04d "${PAG}")-earnings.json &
fi

# ./earnings.sh -b 5 -e 10 --> Start at pag 5 end at 10
if [[ "${LOOP}" == true ]]; then
    if [[ "${START}" != '' && "${END}" != '' ]]; then
      python3 seeking_alpha/proxy.py &
      for i in $(eval echo {${START}..${END}}); do
        scrapy crawl earnings -a pag="${i}"
        WAIT=$(jot -r 1 2 8)
        sleep ${WAIT}
      done
    fi
fi

# ./earnings.sh -s -b 5 -e 10 --> Start at pag 5 end at 10
if [[ "${SINGLE}" == true ]]; then
  if [[ "${START}" != '' && "${END}" != '' ]]; then
      python3 seeking_alpha/proxy.py &
      sleep 3
      scrapy crawl earnings -a start="${START}" -a end="${END}" &
  fi
fi


# ./earnings.sh -t -b 5 -e 10 --> Start at pag 5 end at 10
if [[ "${TEST}" == true ]]; then
  if [[ "${START}" != '' && "${END}" != '' ]]; then
      scrapy crawl earnings -a start="${START}" -a end="${END}" &
  fi
fi

# ./earnings.sh -f data/00-http_error.txt
if [[ "${HTTP_ERRORS}" != "" ]]; then
  python3 seeking_alpha/proxy.py &
  sleep 3
  for i in $(sort ${HTTP_ERRORS} | sed 's:.*/::');
    do
      #scrapy crawl earnings -a pag="${i}" -o data/$(printf %04d ${i})-earnings.json
      scrapy crawl earnings -a pag="${i}" &
      WAIT=$(jot -r 1 2 8)
      sleep ${WAIT}
    done
fi
