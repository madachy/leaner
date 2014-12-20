
url="https://github.com/ai-se/leaner/blob/master"

py=$(shell cd src; ls *.py)
md=$(subst src/,,$(subst .py,.md,$(py)))

all: publish commit

typo:
	- git status
	- git commit -am "stuff"
	- git push origin master

commit:
	- git status
	- git commit -a
	- git push origin master

update:
	- git pull origin master

status:
	- git status

./%.md : src/%.py
	@bash etc/py2md $< $(url) > $@
	git add $@

README.md : etc/readme.md etc/license.md $(md) etc/toc1.awk
	@cat $< > $@
	@printf "\n\n## Contents\n\n" >> $@
	@$(foreach f,$(py),\
		gawk -f etc/toc1.awk src/$f >> $@;)
	@cat etc/license.md  >> $@
	git add $@

publish: $(md) README.md 
