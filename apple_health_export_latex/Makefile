PDF=apple_health_export_study.pdf

all:
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	xelatex -interaction=nonstopmode -halt-on-error main.tex
	mv main.pdf $(PDF)

clean:
	rm -f *.aux *.log *.out *.toc *.pdf *.fls *.fdb_latexmk *.synctex.gz
	rm -f chapters/*.aux
