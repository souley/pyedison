#!/bin/bash
#Environment setup


alias tfidfclean="rm -rf ../results/tfidf"
alias transjobs="python translate_save.py"
alias tfidf="tfidfclean && transjobs && python tfidfsim.py"

alias jaccclean="rm -rf ../results/jaccard"
alias rankprep="python sgrankprep.py"
alias jacc="jaccclean && transjobs && rankprep && python jaccsim.py"

alias ldaclean="rm -rf ../results/lda"
alias lda="ldaclean && transjobs && python ldasim.py"

alias allclean="tfidfclean && jaccclean && ldaclean"
alias allsim="tfidf && jacc && lda"

