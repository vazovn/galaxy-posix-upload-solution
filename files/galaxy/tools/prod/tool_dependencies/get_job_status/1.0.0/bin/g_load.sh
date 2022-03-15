#!/bin/bash

export PATH=/cluster/bin:$PATH
export PERL5LIB=/node/lib/perl5:/cluster/lib/perl5

echo '<html<title>FOX load</title><body>  src="https://metadoc.metacenter.no/status_graph/?machine=fox&period=week&type=cpu&size=large&dynamic=true&start=0&end=0&format=png" alt="https://metadoc.metacenter.no/status_graph/?machine=fox&period=week&type=cpu&size=large&dynamic=true&start=0&end=0&format=png"></body></html>' > out.html
freepe
#echo '</body></html>'i


