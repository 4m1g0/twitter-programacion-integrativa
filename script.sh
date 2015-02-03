#! /usr/bin/sh


if [ $(curl --write-out %{http_code} --silent --output /dev/null localhost:8000/tweet/newTweet.html) == 200 ]; then echo "Ha llegado un tweet nuevo sobre el tema que estabas buscando."| mail -s "Notificacion twitter" twitterficpi@gmail.com; fi

#if [ $(curl --write-out %{http_code} --silent --output /dev/null localhost:8000/tweet/newTweet.html) == 200 ]; then echo testtttt > pepepepepe.txt; fi

